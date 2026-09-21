import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import RrwebReporter from '../RrwebReporter.vue';
import { createTestingPinia } from '@pinia/testing';
import axios from 'axios';
import { useToast } from 'vue-toastification';

// Mock dependencias
vi.mock('axios', () => {
  const instance = {
    post: vi.fn(() => Promise.resolve({ data: {} })),
    get: vi.fn(() => Promise.resolve({ data: [] })),
    delete: vi.fn(() => Promise.resolve({})),
    interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } }
  };
  return {
    default: {
      ...instance,
      create: vi.fn(() => instance)
    }
  };
});

const mockToast = {
  success: vi.fn(),
  warning: vi.fn(),
  error: vi.fn()
};

vi.mock('vue-toastification', () => ({
  useToast: vi.fn(() => mockToast)
}));

// Mock rrweb para poder simular que graba eventos
let mockEmitFn = null;
vi.mock('rrweb', () => ({
  record: vi.fn(({ emit }) => {
    mockEmitFn = emit;
    return vi.fn(); // stopFn
  })
}));

describe('RrwebReporter.vue', () => {
  let originalEnv;

  beforeEach(() => {
    vi.clearAllMocks();
    mockEmitFn = null;
    originalEnv = import.meta.env.VITE_APP_ENV;
    import.meta.env.VITE_APP_ENV = 'sandbox'; // Simulamos entorno sandbox
  });

  afterEach(() => {
    import.meta.env.VITE_APP_ENV = originalEnv;
  });

  it('no se renderiza si el usuario no esta autenticado', () => {
    const wrapper = mount(RrwebReporter, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: { token: null }
          }
        })]
      }
    });
    expect(wrapper.find('button').exists()).toBe(false);
  });

  it('no se renderiza si el entorno no es sandbox', () => {
    import.meta.env.VITE_APP_ENV = 'production';
    const wrapper = mount(RrwebReporter, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: { token: 'faketoken' }
          }
        })]
      }
    });
    expect(wrapper.find('button').exists()).toBe(false);
  });

  it('se renderiza correctamente en sandbox autenticado', () => {
    const wrapper = mount(RrwebReporter, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: { token: 'faketoken' }
          }
        })]
      }
    });
    expect(wrapper.find('button').exists()).toBe(true);
  });

  it('envia reporte manual correctamente con toast', async () => {
    const wrapper = mount(RrwebReporter, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: { token: 'fake-token' }
          }
        })]
      }
    });
    
    // Esperar a que monte e inicie rrweb
    await new Promise(r => setTimeout(r, 10));
    
    // Disparar evento falso para llenar el array events
    if (mockEmitFn) mockEmitFn({ type: 1, timestamp: Date.now() });

    const toast = useToast();
    
    // Disparamos reporte manual invocando metodo
    await wrapper.vm.reportError(false, 'Mensaje manual');
    
    expect(axios.post).toHaveBeenCalled();
    expect(toast.success).toHaveBeenCalledWith("¡Reporte enviado exitosamente! Los ingenieros revisarán tu sesión.");
  });
  
  it('atrapa error global de ventana y hace auto-reporte', async () => {
    const wrapper = mount(RrwebReporter, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            auth: { token: 'fake-token' }
          }
        })]
      }
    });
    
    await new Promise(r => setTimeout(r, 10));
    if (mockEmitFn) mockEmitFn({ type: 1, timestamp: Date.now() });

    const toast = useToast();
    
    // Simulamos un error global
    window.dispatchEvent(new ErrorEvent('error', {
      error: new Error('Error critico simulado'),
      message: 'Uncaught Error: Error critico simulado'
    }));
    
    // Esperamos tick
    await new Promise(r => setTimeout(r, 10));
    
    expect(axios.post).toHaveBeenCalled();
    // No debe mostrar toast en modo auto
    expect(toast.success).not.toHaveBeenCalled();
    // El payload debe contener el mensaje de error
    const postCall = axios.post.mock.calls[0];
    expect(postCall[1].error_message).toBe('Uncaught Error: Error critico simulado');
  });
});
