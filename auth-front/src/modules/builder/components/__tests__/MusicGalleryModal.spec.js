import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import MusicGalleryModal from '../MusicGalleryModal.vue';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient', () => ({
  default: {
    get: vi.fn()
  }
}));

// Mock Audio
const mockPlay = vi.fn().mockResolvedValue(undefined);
const mockPause = vi.fn();
global.Audio = vi.fn().mockImplementation(() => ({
  play: mockPlay,
  pause: mockPause,
  addEventListener: vi.fn(),
  volume: 0.5,
  src: ''
}));

describe('MusicGalleryModal.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('no debería renderizar si isOpen es false', () => {
    const wrapper = mount(MusicGalleryModal, {
      props: { isOpen: false }
    });
    expect(wrapper.find('div.fixed').exists()).toBe(false);
  });

  it('debería renderizar si isOpen es true', () => {
    const wrapper = mount(MusicGalleryModal, {
      props: { isOpen: true }
    });
    expect(wrapper.find('div.fixed').exists()).toBe(true);
    expect(wrapper.find('h2').text()).toBe('Buscar Melodías (Jamendo)');
  });

  it('debería realizar búsquedas y renderizar la lista de canciones', async () => {
    invtznClient.get.mockResolvedValueOnce({
      data: {
        results: [
          {
            id: 'track1',
            title: 'Song One',
            artist: 'Artist One',
            duration: 120,
            cover: 'http://cover.url',
            audio: 'http://audio.mp3'
          }
        ]
      }
    });

    const wrapper = mount(MusicGalleryModal, {
      props: { isOpen: true }
    });

    // Introducir texto en la búsqueda
    const input = wrapper.find('input[type="text"]');
    await input.setValue('romantic');

    // Hacer clic en buscar
    const searchBtn = wrapper.find('button.btn-primary');
    await searchBtn.trigger('click');

    expect(invtznClient.get).toHaveBeenCalledWith('deployments/jamendo-search/', {
      params: { q: 'romantic' }
    });

    // Esperar a que se actualice la reactividad
    await wrapper.vm.$nextTick();

    // Comprobar que renderiza el track
    expect(wrapper.find('h3').text()).toBe('Song One');
    expect(wrapper.find('p').text()).toBe('Artist One');
    expect(wrapper.find('.font-mono').text()).toBe('2:00');
  });

  it('debería emitir select-audio al seleccionar una pista', async () => {
    invtznClient.get.mockResolvedValueOnce({
      data: {
        results: [
          {
            id: 'track1',
            title: 'Song One',
            artist: 'Artist One',
            duration: 120,
            cover: 'http://cover.url',
            audio: 'http://audio.mp3'
          }
        ]
      }
    });

    const wrapper = mount(MusicGalleryModal, {
      props: { isOpen: true }
    });

    // Buscar y renderizar
    const input = wrapper.find('input[type="text"]');
    await input.setValue('romantic');
    await wrapper.find('button.btn-primary').trigger('click');
    await wrapper.vm.$nextTick();

    // Hacer clic en seleccionar
    const selectBtn = wrapper.find('button.btn-primary.px-4');
    await selectBtn.trigger('click');

    expect(wrapper.emitted('select-audio')).toBeTruthy();
    expect(wrapper.emitted('select-audio')[0]).toEqual(['http://audio.mp3']);
    expect(wrapper.emitted('close')).toBeTruthy();
  });
});
