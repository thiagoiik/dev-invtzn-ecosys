import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import LoginView from '../LoginView.vue';
import { useAuthStore } from '../../store/auth';

const mockPush = vi.fn();
const mockCurrentRoute = { value: { query: {} } };

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockPush,
    currentRoute: mockCurrentRoute
  }),
  RouterLink: {
    template: '<a><slot /></a>'
  }
}));

const mockToastSuccess = vi.fn();
const mockToastError = vi.fn();
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: mockToastSuccess,
    error: mockToastError
  })
}));

const mountOptions = {
  global: {
    stubs: {
      'router-link': {
        template: '<a><slot /></a>'
      }
    }
  }
};

describe('LoginView.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    mockCurrentRoute.value.query = {};
  });

  it('debería renderizar el formulario correctamente con sus campos vacíos', () => {
    const wrapper = mount(LoginView, mountOptions);
    expect(wrapper.find('h3').text()).toBe('Iniciar Sesión');
    expect(wrapper.find('input[type="text"]').element.value).toBe('');
    expect(wrapper.find('input[type="password"]').element.value).toBe('');
    expect(wrapper.find('button[type="submit"]').text()).toBe('Ingresar');
  });

  it('debería llamar a authStore.login al enviar el formulario con datos válidos', async () => {
    const store = useAuthStore();
    vi.spyOn(store, 'login').mockResolvedValue();

    const wrapper = mount(LoginView, mountOptions);
    
    // Rellenar formulario
    await wrapper.find('input[type="text"]').setValue('juanperez');
    await wrapper.find('input[type="password"]').setValue('mi-password');
    
    // Enviar formulario
    await wrapper.find('form').trigger('submit.prevent');
    
    expect(store.login).toHaveBeenCalledWith({
      username: 'juanperez',
      password: 'mi-password'
    });
    expect(mockToastSuccess).toHaveBeenCalledWith('¡Bienvenido de vuelta!');
    expect(mockPush).toHaveBeenCalledWith('/dashboard');
  });

  it('debería mostrar mensaje de error si el login falla', async () => {
    const store = useAuthStore();
    vi.spyOn(store, 'login').mockRejectedValue(new Error('Auth failed'));

    const wrapper = mount(LoginView, mountOptions);
    
    await wrapper.find('input[type="text"]').setValue('usuario-invalido');
    await wrapper.find('input[type="password"]').setValue('wrong-password');
    
    await wrapper.find('form').trigger('submit.prevent');
    
    expect(store.login).toHaveBeenCalled();
    expect(mockToastError).toHaveBeenCalledWith('Las credenciales no coinciden.');
    
    // Comprobar que el mensaje de error se renderiza
    expect(wrapper.find('p.text-error').text()).toBe('Error al iniciar sesión. Revisa tus credenciales.');
  });
});
