import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import StudioView from '../StudioView.vue';
import { builderService } from '../../services/builderService';

vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: 'test-id-123' }
  }),
  RouterLink: {
    template: '<a><slot /></a>'
  }
}));

const mockToastError = vi.fn();
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    error: mockToastError
  })
}));

vi.mock('../../services/builderService', () => ({
  builderService: {
    getDeployment: vi.fn(),
    saveCustomData: vi.fn()
  }
}));

// Stub RenderEngineMaster and BuilderLayout
const mountOptions = {
  global: {
    stubs: {
      BuilderLayout: {
        template: '<div><slot name="actions" /><slot /></div>'
      },
      RenderEngineMaster: {
        template: '<div class="render-engine-master-stub">RenderEngineMaster Mock</div>',
        props: ['status', 'customData', 'slug', 'deploymentId']
      },
      EnvelopeWrapper: {
        template: '<div class="envelope-wrapper-stub"><slot /></div>',
        props: ['type']
      },
      'router-link': {
        template: '<a><slot /></a>'
      }
    }
  }
};

describe('StudioView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería renderizar la portada por defecto y cargar la configuración del backend', async () => {
    builderService.getDeployment.mockResolvedValueOnce({
      data: {
        slug: 'mi-boda-test',
        status: 'DRAFT',
        allowed_features: {
          background_music: true,
          custom_audio_url: false,
          countdown_timer: true,
          timeline: false,
          custom_theme: true,
          custom_og: false
        },
        custom_data: {
          cover: {
            title: 'Ana & Juan',
            subtitle: '¡Te invitamos!',
            date: '2026-10-10'
          }
        }
      }
    });

    const wrapper = mount(StudioView, mountOptions);

    // Wait for async hooks to resolve
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(builderService.getDeployment).toHaveBeenCalledWith('test-id-123');
    
    // Check initial cover settings
    expect(wrapper.vm.localConfig.cover.title).toBe('Ana & Juan');
    expect(wrapper.vm.localConfig.cover.subtitle).toBe('¡Te invitamos!');
    expect(wrapper.vm.localConfig.cover.date).toBe('2026-10-10');
    
    // Check features state
    expect(wrapper.vm.allowedFeatures.countdown_timer).toBe(true);
    expect(wrapper.vm.allowedFeatures.timeline).toBe(false);
  });

  it('debería manejar y propagar envelope_type / envelope correctamente', async () => {
    builderService.getDeployment.mockResolvedValueOnce({
      data: {
        slug: 'mi-boda-test',
        status: 'DRAFT',
        allowed_features: {
          background_music: true,
          custom_audio_url: false,
          countdown_timer: true,
          timeline: false,
          custom_theme: true,
          custom_og: false
        },
        custom_data: {
          envelope_type: '1'
        }
      }
    });

    const wrapper = mount(StudioView, mountOptions);

    // Wait for async hooks to resolve
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(builderService.getDeployment).toHaveBeenCalledWith('test-id-123');

    // Check loaded envelope settings
    expect(wrapper.vm.localConfig.envelope_type).toBe('1');
    expect(wrapper.vm.localConfig.envelope).toBe('1');

    // Change envelope_type and check reactive sync to envelope
    wrapper.vm.localConfig.envelope_type = '2';
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.localConfig.envelope).toBe('2');

    // Set to null
    wrapper.vm.localConfig.envelope_type = null;
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.localConfig.envelope).toBeNull();
  });
});
