import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import CoverBlock from '../CoverBlock.vue';

describe('CoverBlock.vue', () => {
  it('debería renderizar la información básica: título, subtítulo, etiqueta y fecha', () => {
    const config = {
      title: 'Sofía & Diego',
      subtitle: '¡Acompáñanos a celebrar nuestra boda!',
      headerLabel: 'Nuestra Ceremonia',
      date: '10 OCTUBRE 2026',
      titleColor: '',
      subtitleColor: ''
    };

    const wrapper = mount(CoverBlock, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Sofía & Diego');
    expect(wrapper.text()).toContain('¡Acompáñanos a celebrar nuestra boda!');
    expect(wrapper.text()).toContain('Nuestra Ceremonia');
    expect(wrapper.text()).toContain('10 OCTUBRE 2026');
  });

  it('debería aplicar el color y tamaño de título personalizado en línea y omitir text-white', () => {
    const config = {
      title: 'Sofía & Diego',
      titleColor: '#ff0000',
      titleSize: 5.5
    };

    const wrapper = mount(CoverBlock, {
      props: { config }
    });

    const h1 = wrapper.find('h1');
    expect(h1.exists()).toBe(true);
    expect(h1.attributes('style')).toContain('color: rgb(255, 0, 0)');
    expect(h1.attributes('style')).toContain('font-size: 5.5rem');
    expect(h1.classes()).not.toContain('text-white');
  });

  it('debería aplicar text-white en el título cuando no hay color de título personalizado', () => {
    const config = {
      title: 'Sofía & Diego',
      titleColor: ''
    };

    const wrapper = mount(CoverBlock, {
      props: { config }
    });

    const h1 = wrapper.find('h1');
    expect(h1.exists()).toBe(true);
    expect(h1.classes()).toContain('text-white');
  });

  it('debería aplicar el color de subtítulo y color de fecha heredado del subtítulo o de la etiqueta superior', () => {
    const config = {
      subtitle: '¡Te esperamos!',
      subtitleColor: '#00ff00',
      headerLabelColor: '#ffbb00'
    };

    const wrapper = mount(CoverBlock, {
      props: { config }
    });

    const p = wrapper.find('p');
    expect(p.exists()).toBe(true);
    expect(p.attributes('style')).toContain('color: rgb(0, 255, 0)');
    expect(p.classes()).not.toContain('text-slate-200/90');

    const dateP = wrapper.find('.inline-block p');
    expect(dateP.exists()).toBe(true);
    expect(dateP.attributes('style')).toContain('color: rgb(0, 255, 0)');
    expect(dateP.classes()).not.toContain('text-white');
  });

  it('debería aplicar la opacidad personalizada al overlay de fondo', () => {
    const config = {
      overlayOpacity: 45
    };

    const wrapper = mount(CoverBlock, {
      props: { config }
    });

    const overlay = wrapper.findAll('div')[2]; // El tercer div es el overlay en la jerarquía
    expect(overlay.exists()).toBe(true);
    expect(overlay.attributes('style')).toContain('opacity: 0.45');
  });
});
