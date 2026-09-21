import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import TelemetryListView from '../views/TelemetryListView.vue';
import { createTestingPinia } from '@pinia/testing';
import axios from 'axios';

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

// Mock del componente hijo Player para evitar problemas de canvas/rrweb en JSDOM
vi.mock('../components/TelemetryPlayer.vue', () => ({
  default: {
    template: '<div>Player Mock</div>'
  }
}));

describe('TelemetryListView.vue', () => {
  let originalConfirm;

  beforeEach(() => {
    vi.clearAllMocks();
    originalConfirm = window.confirm;
    window.confirm = vi.fn(() => true); // Siempre confirmamos borrado
  });

  afterEach(() => {
    window.confirm = originalConfirm;
  });

  it('renderiza correctamente la lista de sesiones desde la API', async () => {
    // Simulamos respuesta con user_name para probar el binding mapeado
    axios.get.mockResolvedValueOnce({
      data: [
        {
          id: 99,
          user_id: 1,
          user_name: 'Juan Perez',
          role: 'ADMIN',
          window_width: 1920,
          window_height: 1080,
          created_at: new Date().toISOString()
        }
      ]
    });

    const wrapper = mount(TelemetryListView, {
      global: {
        plugins: [createTestingPinia()]
      }
    });
    
    // Esperar a que se resuelva la promesa onMounted
    await new Promise(r => setTimeout(r, 10));
    await wrapper.vm.$nextTick();

    // Verificamos que no diga "Anonimo" ni "1", sino el user_name
    expect(wrapper.text()).toContain('Juan Perez');
    expect(wrapper.text()).toContain('ADMIN');
    expect(wrapper.text()).toContain('1920x1080');
  });

  it('llama a axios.delete al confirmar la eliminacion de sesion', async () => {
    axios.get.mockResolvedValueOnce({
      data: [
        { id: 99, user_name: 'Juan', role: 'ADMIN' }
      ]
    });

    const wrapper = mount(TelemetryListView, {
      global: {
        plugins: [createTestingPinia()]
      }
    });
    
    await new Promise(r => setTimeout(r, 10));
    await wrapper.vm.$nextTick();

    const deleteBtn = wrapper.find('button.btn-error');
    expect(deleteBtn.exists()).toBe(true);

    await deleteBtn.trigger('click');

    expect(window.confirm).toHaveBeenCalled();
    expect(axios.delete).toHaveBeenCalled();
    
    // Verificamos remocion del UI
    expect(wrapper.vm.sessions.length).toBe(0);
  });
});
