import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import InvitationTextBlock from '../InvitationTextBlock.vue';

describe('InvitationTextBlock.vue', () => {
  it('debería renderizar la información básica: título y texto', () => {
    const config = {
      title: 'Nuestra Historia',
      text: 'Con la bendición de nuestros seres queridos...',
      align: 'center',
      fontStyle: 'serif'
    };

    const wrapper = mount(InvitationTextBlock, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Nuestra Historia');
    expect(wrapper.text()).toContain('Con la bendición de nuestros seres queridos...');
  });

  it('debería aplicar la clase de alineación correcta', () => {
    const config = {
      title: 'Pensamiento',
      text: 'Prueba de alineación a la izquierda',
      align: 'left',
      fontStyle: 'serif'
    };

    const wrapper = mount(InvitationTextBlock, {
      props: { config }
    });

    const container = wrapper.find('.py-12');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('text-left');
    expect(container.classes()).not.toContain('text-center');
  });

  it('debería aplicar la clase de fuente serif', () => {
    const config = {
      title: 'Pensamiento',
      text: 'Prueba de fuente serif',
      align: 'center',
      fontStyle: 'serif'
    };

    const wrapper = mount(InvitationTextBlock, {
      props: { config }
    });

    const p = wrapper.find('p');
    expect(p.exists()).toBe(true);
    expect(p.classes()).toContain('font-serif');
    expect(p.classes()).not.toContain('font-sans');
  });

  it('debería aplicar la clase de fuente sans-serif si se configura', () => {
    const config = {
      title: 'Pensamiento',
      text: 'Prueba de fuente sans-serif',
      align: 'center',
      fontStyle: 'sans'
    };

    const wrapper = mount(InvitationTextBlock, {
      props: { config }
    });

    const p = wrapper.find('p');
    expect(p.exists()).toBe(true);
    expect(p.classes()).toContain('font-sans');
    expect(p.classes()).not.toContain('font-serif');
  });
});
