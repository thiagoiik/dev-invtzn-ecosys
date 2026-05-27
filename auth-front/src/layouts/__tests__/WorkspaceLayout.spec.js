import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import WorkspaceLayout from '../WorkspaceLayout.vue';
import { ref } from 'vue';

const mockRole = ref('ADMIN');
const mockUser = ref({ username: 'testadmin', is_superuser: true });

vi.mock('@/modules/auth/store/auth', () => ({
  useAuthStore: () => ({
    role: mockRole.value,
    user: mockUser.value,
    logout: vi.fn()
  })
}));

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  }),
  RouterView: {
    template: '<div class="router-view-stub">RouterView Mock</div>'
  },
  RouterLink: {
    template: '<a :href="to"><slot /></a>',
    props: ['to']
  }
}));

vi.mock('@/composables/useDevice', () => ({
  useDevice: () => ({
    isMobile: ref(false),
    isTablet: ref(false),
    isDesktop: ref(true)
  })
}));

describe('WorkspaceLayout.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería mostrar todos los enlaces configurables para un rol ADMIN', () => {
    mockRole.value = 'ADMIN';
    mockUser.value = { username: 'testadmin', is_superuser: true };

    const wrapper = mount(WorkspaceLayout, {
      global: {
        stubs: {
          'router-link': {
            template: '<a :href="to" class="nav-link"><slot /></a>',
            props: ['to']
          },
          'router-view': true
        }
      }
    });

    const links = wrapper.findAll('.nav-link').map(w => w.attributes('href'));
    expect(links).toContain('/workspace/crm');
    expect(links).toContain('/workspace/designs');
    expect(links).toContain('/workspace/pos');
    expect(links).toContain('/workspace/finance');
    expect(links).toContain('/workspace/stores');
    expect(links).toContain('/workspace/products');
    expect(links).toContain('/workspace/coupons');
    expect(links).toContain('/workspace/tools');
  });

  it('debería ocultar opciones de configuración administrativa para el rol VENDOR', () => {
    mockRole.value = 'VENDOR';
    mockUser.value = { username: 'testvendor', is_superuser: false };

    const wrapper = mount(WorkspaceLayout, {
      global: {
        stubs: {
          'router-link': {
            template: '<a :href="to" class="nav-link"><slot /></a>',
            props: ['to']
          },
          'router-view': true
        }
      }
    });

    const links = wrapper.findAll('.nav-link').map(w => w.attributes('href'));
    expect(links).toContain('/workspace/crm');
    expect(links).toContain('/workspace/designs');
    expect(links).toContain('/workspace/pos');
    
    // VENDOR shouldn't have config routes
    expect(links).not.toContain('/workspace/finance');
    expect(links).not.toContain('/workspace/stores');
    expect(links).not.toContain('/workspace/products');
    expect(links).not.toContain('/workspace/coupons');
    expect(links).not.toContain('/workspace/tools');
  });

  it('debería mostrar únicamente Gestión de Diseños para el rol DESIGNER', () => {
    mockRole.value = 'DESIGNER';
    mockUser.value = { username: 'testdesigner', is_superuser: false };

    const wrapper = mount(WorkspaceLayout, {
      global: {
        stubs: {
          'router-link': {
            template: '<a :href="to" class="nav-link"><slot /></a>',
            props: ['to']
          },
          'router-view': true
        }
      }
    });

    const links = wrapper.findAll('.nav-link').map(w => w.attributes('href'));
    expect(links).toContain('/workspace/designs');
    expect(links).not.toContain('/workspace/crm');
    expect(links).not.toContain('/workspace/pos');
    expect(links).not.toContain('/workspace/finance');
  });
});
