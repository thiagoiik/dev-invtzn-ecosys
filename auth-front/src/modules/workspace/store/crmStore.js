import { defineStore } from 'pinia';
import { crmService } from '@/modules/workspace/services/crmService';

export const useCrmStore = defineStore('crm', {
  state: () => ({
    profiles: [],
    selectedProfile: null,
    loading: false,
    drawerOpen: false,
  }),
  
  actions: {
    async fetchProfiles() {
      this.loading = true;
      try {
        const res = await crmService.fetchAllProfiles();
        this.profiles = res.data;
      } catch (error) {
        console.error('Error fetching profiles', error);
      } finally {
        this.loading = false;
      }
    },

    selectProfile(profile) {
      this.selectedProfile = profile;
      this.drawerOpen = true;
    },

    closeDrawer() {
      this.drawerOpen = false;
      this.selectedProfile = null;
    }
  }
});
