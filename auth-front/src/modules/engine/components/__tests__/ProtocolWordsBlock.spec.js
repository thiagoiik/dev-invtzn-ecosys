import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ProtocolWordsBlock from '../ProtocolWordsBlock.vue';

describe('ProtocolWordsBlock.vue', () => {
  it('debería renderizar la información básica: título y descripción', () => {
    const config = {
      title: 'Nuestros Padres',
      description: 'Con su amor y apoyo incondicional...',
      columns: []
    };

    const wrapper = mount(ProtocolWordsBlock, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Nuestros Padres');
    expect(wrapper.text()).toContain('Con su amor y apoyo incondicional...');
  });

  it('debería renderizar las columnas de roles y nombres responsivamente', () => {
    const config = {
      title: 'Palabras Protocolares',
      description: '',
      columns: [
        { role: 'Padres de la Novia', names: 'Roberto Silva & Elena Gómez' },
        { role: 'Padres del Novio', names: 'Marcos Soto & Patricia Díaz' }
      ]
    };

    const wrapper = mount(ProtocolWordsBlock, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Padres de la Novia');
    expect(wrapper.text()).toContain('Roberto Silva & Elena Gómez');
    expect(wrapper.text()).toContain('Padres del Novio');
    expect(wrapper.text()).toContain('Marcos Soto & Patricia Díaz');

    // Debe aplicar la clase de columnas adecuada para 2 columnas
    const container = wrapper.find('.grid');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('cols-2');
  });

  it('debería aplicar la clase para 3 columnas si se especifican más de 2', () => {
    const config = {
      title: 'Cortejo',
      description: '',
      columns: [
        { role: 'Padrinos de Velación', names: 'Pedro & María' },
        { role: 'Padrinos de Anillos', names: 'Juan & Laura' },
        { role: 'Padrinos de Arras', names: 'Luis & Clara' }
      ]
    };

    const wrapper = mount(ProtocolWordsBlock, {
      props: { config }
    });

    const container = wrapper.find('.grid');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('cols-3');
  });
});
