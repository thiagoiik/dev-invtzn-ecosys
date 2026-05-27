import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import CatalogFormView from '../CatalogFormView.vue';
import { builderService } from '../../services/builderService';

vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: 'test-deployment-123' },
    query: {}
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn()
  }),
  RouterLink: {
    template: '<a><slot /></a>'
  }
}));

const mockToastError = vi.fn();
const mockToastSuccess = vi.fn();
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    error: mockToastError,
    success: mockToastSuccess
  })
}));

vi.mock('../../services/builderService', () => ({
  builderService: {
    getDeployment: vi.fn(),
    saveCustomData: vi.fn()
  }
}));

const mountOptions = {
  global: {
    stubs: {
      BuilderLayout: {
        template: '<div><slot name="actions" /><slot /></div>'
      },
      UpgradeModal: {
        template: '<div class="upgrade-modal-stub">UpgradeModal Mock</div>'
      },
      'router-link': {
        template: '<a><slot /></a>'
      }
    }
  }
};

describe('CatalogFormView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería cargar la configuración del backend y mostrar los campos del formulario', async () => {
    builderService.getDeployment.mockResolvedValueOnce({
      data: {
        status: 'DRAFT',
        allowed_features: {
          background_music: true,
          custom_audio_url: false,
          countdown_timer: true,
          timeline: true,
          custom_theme: true,
          custom_og: true
        },
        custom_data: {
          cover: {
            title: 'Boda Real',
            subtitle: 'Estás invitado',
            date: '2026-11-11'
          },
          is_catalog_complete: false
        }
      }
    });

    const wrapper = mount(CatalogFormView, mountOptions);

    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    expect(builderService.getDeployment).toHaveBeenCalledWith('test-deployment-123');
    expect(wrapper.vm.localConfig.cover.title).toBe('Boda Real');
    expect(wrapper.vm.localConfig.is_catalog_complete).toBe(false);
  });

  it('debería poder agregar y remover items del itinerario', async () => {
    builderService.getDeployment.mockResolvedValueOnce({
      data: {
        status: 'LIVE',
        allowed_features: { timeline: true },
        custom_data: {
          timeline: {
            title: 'Cronograma',
            schedule: [
              { time: '18:00', title: 'Entrada', description: 'Inicio', icon: '💍' }
            ]
          }
        }
      }
    });

    const wrapper = mount(CatalogFormView, mountOptions);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    // Agregar un item
    wrapper.vm.addScheduleItem();
    expect(wrapper.vm.localConfig.timeline.schedule.length).toBe(2);
    expect(wrapper.vm.saveStatus).toBe('unsaved');

    // Remover el primer item
    wrapper.vm.removeScheduleItem(0);
    expect(wrapper.vm.localConfig.timeline.schedule.length).toBe(1);
  });

  it('debería guardar la configuración modificada al enviar el formulario', async () => {
    builderService.getDeployment.mockResolvedValueOnce({
      data: {
        status: 'DRAFT',
        allowed_features: {},
        custom_data: {
          cover: { title: 'Test original' }
        }
      }
    });
    builderService.saveCustomData.mockResolvedValueOnce({ success: true });

    const wrapper = mount(CatalogFormView, mountOptions);
    await new Promise(resolve => setTimeout(resolve, 50));
    await wrapper.vm.$nextTick();

    wrapper.vm.localConfig.cover.title = 'Test Modificado';
    await wrapper.vm.saveAllData();

    expect(builderService.saveCustomData).toHaveBeenCalledWith('test-deployment-123', wrapper.vm.localConfig);
    expect(wrapper.vm.saveStatus).toBe('saved');
    expect(mockToastSuccess).toHaveBeenCalledWith('¡Cambios guardados con éxito!');
  });
});
