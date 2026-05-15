import invtznClient from '@/core/api/invtznClient';

export const crmService = {
  fetchAllProfiles() {
    return invtznClient.get('profiles/');
  },
  
  updateProfileRole(profileId, newRole) {
    return invtznClient.patch(`profiles/${profileId}/change-role/`, { custom_role: newRole });
  },
  
  fetchAllDeployments() {
    return invtznClient.get('deployments/');
  },

  searchProfile(remoteAuthId) {
    return invtznClient.get('profiles/search/', { params: { remote_auth_id: remoteAuthId } });
  }
};
