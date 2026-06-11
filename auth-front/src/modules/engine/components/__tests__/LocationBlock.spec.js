import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import LocationBlock from '../LocationBlock.vue';

// Mock vue-toastification if needed, although not imported in LocationBlock
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    error: vi.fn(),
    success: vi.fn()
  })
}));

describe('LocationBlock.vue', () => {
  it('debería renderizar la información básica de la ubicación', () => {
    const config = {
      title: 'Ceremonia Religiosa',
      venueName: 'Catedral Metropolitana',
      address: 'Plaza de la Constitución S/N, Centro Histórico',
      googleMapsUrl: 'https://maps.app.goo.gl/catedral-test',
      zoom: 16
    };

    const wrapper = mount(LocationBlock, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Ceremonia Religiosa');
    expect(wrapper.text()).toContain('Catedral Metropolitana');
    expect(wrapper.text()).toContain('Plaza de la Constitución S/N, Centro Histórico');

    const link = wrapper.find('a[target="_blank"]');
    expect(link.exists()).toBe(true);
    expect(link.attributes('href')).toBe(config.googleMapsUrl);
  });

  it('debería computar correctamente la URL del iframe con el nivel de zoom especificado', () => {
    const config = {
      venueName: 'Salón Las Nubes',
      address: 'Av. Vista Hermosa 456',
      zoom: 18
    };

    const wrapper = mount(LocationBlock, {
      props: { config }
    });

    const iframe = wrapper.find('iframe');
    expect(iframe.exists()).toBe(true);
    
    const src = iframe.attributes('src');
    expect(src).toContain('q=Sal%C3%B3n%20Las%20Nubes%20Av.%20Vista%20Hermosa%20456');
    expect(src).toContain('z=18');
    expect(src).toContain('output=embed');
  });

  it('debería usar zoom 14 por defecto si no se proporciona', () => {
    const config = {
      venueName: 'Salón Las Nubes',
      address: 'Av. Vista Hermosa 456'
    };

    const wrapper = mount(LocationBlock, {
      props: { config }
    });

    const iframe = wrapper.find('iframe');
    const src = iframe.attributes('src');
    expect(src).toContain('z=14');
  });

  it('debería extraer correctamente el src si el usuario ingresa un código iframe de Google Maps', () => {
    const config = {
      venueName: '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3762.4!2d-99.1!3d19.4" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
      address: ''
    };

    const wrapper = mount(LocationBlock, {
      props: { config }
    });

    const iframe = wrapper.find('iframe');
    const src = iframe.attributes('src');
    expect(src).toBe('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3762.4!2d-99.1!3d19.4');
  });
});
