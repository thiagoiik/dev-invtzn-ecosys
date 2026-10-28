import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import ProductsManagerView from '../ProductsManagerView.vue';
import invtznClient from '@/core/api/invtznClient';

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
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}));

describe('ProductsManagerView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(window, 'confirm').mockImplementation(() => true);
  });

  it('debería listar los productos al montar la vista', async () => {
    invtznClient.get.mockResolvedValueOnce({
      data: [
        { id: 1, name: 'Invitación Boda', sku: 'BOD-01', product_type: 'DIGITAL', tier_level: 'STANDARD', base_price: '299.00', is_active: true }
      ]
    });

    const wrapper = mount(ProductsManagerView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(invtznClient.get).toHaveBeenCalledWith('products/');
    expect(wrapper.vm.products.length).toBe(1);
    expect(wrapper.text()).toContain('Invitación Boda');
    expect(wrapper.text()).toContain('BOD-01');
  });

  it('debería abrir el drawer de creación al presionar Nuevo Producto', async () => {
    invtznClient.get.mockResolvedValueOnce({ data: [] });

    const wrapper = mount(ProductsManagerView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.drawerOpen).toBe(false);
    wrapper.vm.openCreateDrawer();
    expect(wrapper.vm.drawerOpen).toBe(true);
    expect(wrapper.vm.isEditMode).toBe(false);
    expect(wrapper.vm.form.name).toBe('');
  });

  it('debería enviar un POST al guardar un producto nuevo', async () => {
    invtznClient.get.mockResolvedValueOnce({ data: [] });
    invtznClient.post.mockResolvedValueOnce({ data: { id: 2, name: 'Nuevo Producto' } });

    const wrapper = mount(ProductsManagerView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    wrapper.vm.openCreateDrawer();
    wrapper.vm.form.name = 'Nuevo Producto';
    wrapper.vm.form.sku = 'NEW-02';
    
    await wrapper.vm.saveProduct();

    expect(invtznClient.post).toHaveBeenCalledWith('products/', expect.any(Object));
    expect(mockToastSuccess).toHaveBeenCalledWith('Producto creado con éxito.');
    expect(wrapper.vm.drawerOpen).toBe(false);
  });

  it('debería abrir el drawer de edición prellenado y enviar un PUT al guardar', async () => {
    const product = { id: 1, name: 'Invitación Boda', sku: 'BOD-01', product_type: 'DIGITAL', tier_level: 'STANDARD', base_price: '299.00', is_active: true };
    invtznClient.get.mockResolvedValueOnce({ data: [product] });
    invtznClient.put.mockResolvedValueOnce({ data: { ...product, name: 'Invitación Boda Editada' } });

    const wrapper = mount(ProductsManagerView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    wrapper.vm.openEditDrawer(product);
    expect(wrapper.vm.drawerOpen).toBe(true);
    expect(wrapper.vm.isEditMode).toBe(true);
    expect(wrapper.vm.form.name).toBe('Invitación Boda');

    wrapper.vm.form.name = 'Invitación Boda Editada';
    await wrapper.vm.saveProduct();

    expect(invtznClient.put).toHaveBeenCalledWith('products/1/', expect.any(Object));
    expect(mockToastSuccess).toHaveBeenCalledWith('Producto actualizado con éxito.');
  });

  it('debería enviar un DELETE al confirmar la eliminación de un producto', async () => {
    const product = { id: 1, name: 'Invitación Boda', sku: 'BOD-01', product_type: 'DIGITAL', tier_level: 'STANDARD', base_price: '299.00', is_active: true };
    invtznClient.get.mockResolvedValueOnce({ data: [product] });
    invtznClient.delete.mockResolvedValueOnce({ data: {} });

    const wrapper = mount(ProductsManagerView);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    await wrapper.vm.deleteProduct(1);

    expect(window.confirm).toHaveBeenCalled();
    expect(invtznClient.delete).toHaveBeenCalledWith('products/1/');
    expect(mockToastSuccess).toHaveBeenCalledWith('Producto eliminado con éxito.');
  });
});
