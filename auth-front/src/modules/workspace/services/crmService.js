import invtznClient from '@/core/api/invtznClient';

export const crmService = {
  fetchAllProfiles() {
    return invtznClient.get('profiles/');
  },
  
  updateProfileRole(profileId, newRole) {
    return invtznClient.patch(`profiles/${profileId}/`, { custom_role: newRole });
  }
};
