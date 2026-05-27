import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import DevToolsView from '../DevToolsView.vue';
import invtznClient from '@/core/api/invtznClient';
import { ref } from 'vue';

const mockRole = ref('ADMIN');
const mockUser = ref({ username: 'testadmin', is_superuser: true });

vi.mock('@/modules/auth/store/auth', () => ({
  useAuthStore: () => ({
    role: mockRole.value,
    user: mockUser.value
  })
}));

const mockToastError = vi.fn();
const mockToastSuccess = vi.fn();
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    error: mockToastError,
    success: mockToastSuccess
  })
}));

vi.mock('@/core/api/invtznClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}));

describe('DevToolsView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    HTMLDialogElement.prototype.showModal = vi.fn();
    HTMLDialogElement.prototype.close = vi.fn();
    
    vi.spyOn(document, 'getElementById').mockImplementation((id) => {
      if (id === 'payload_modal' || id === 'metadata_modal') {
        return {
          showModal: HTMLDialogElement.prototype.showModal,
          close: HTMLDialogElement.prototype.close
        };
      }
      return null;
    });
  });

  it('debería cargar logs de webhooks al montar para admin', async () => {
    mockRole.value = 'ADMIN';
    invtznClient.get.mockResolvedValueOnce({
      data: [
        { id: 1, created_at: '2026-05-25T12:00:00Z', provider: 'stripe', status: 'success', message: 'Webhook OK', payload: { event: 'charge.succeeded' } }
      ]
    });

    const wrapper = mount(DevToolsView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(invtznClient.get).toHaveBeenCalledWith('webhook-logs/');
    expect(wrapper.vm.webhookLogs.length).toBe(1);
    expect(wrapper.text()).toContain('Webhook OK');
  });

  it('debería cargar logs del sistema al cambiar a la pestaña de sistema', async () => {
    mockRole.value = 'ADMIN';
    // first call for webhooks on mount
    invtznClient.get.mockResolvedValueOnce({ data: [] });
    // second call for system logs on tab switch
    invtznClient.get.mockResolvedValueOnce({
      data: [
        { id: 10, created_at: '2026-05-25T12:05:00Z', log_type: 'USER_ACTION', message: 'User login', username: 'testadmin', user_id: 1, metadata: { ip: '127.0.0.1' } }
      ]
    });

    const wrapper = mount(DevToolsView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    // Switch tab
    wrapper.vm.activeTab = 'system';
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(invtznClient.get).toHaveBeenCalledWith('system-logs/');
    expect(wrapper.vm.systemLogs.length).toBe(1);
    expect(wrapper.text()).toContain('User login');
  });

  it('debería permitir abrir el payload modal del webhook', async () => {
    mockRole.value = 'ADMIN';
    const logItem = { id: 1, created_at: '2026-05-25T12:00:00Z', provider: 'stripe', status: 'success', message: 'Webhook OK', payload: { event: 'charge.succeeded' } };
    invtznClient.get.mockResolvedValueOnce({ data: [logItem] });

    const wrapper = mount(DevToolsView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    wrapper.vm.viewPayload(logItem);
    expect(wrapper.vm.selectedPayload).toContain('charge.succeeded');
    expect(HTMLDialogElement.prototype.showModal).toHaveBeenCalled();
  });

  it('debería simular la activación forzada de una orden', async () => {
    mockRole.value = 'ADMIN';
    invtznClient.get.mockResolvedValueOnce({ data: [] });
    invtznClient.post.mockResolvedValueOnce({ data: { message: 'Orden 42 activada' } });

    const wrapper = mount(DevToolsView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    wrapper.vm.orderIdToForce = '42';
    await wrapper.vm.forceActivation();

    expect(invtznClient.post).toHaveBeenCalledWith('orders/42/force-activation/');
    expect(mockToastSuccess).toHaveBeenCalledWith('Orden 42 activada');
  });
});
