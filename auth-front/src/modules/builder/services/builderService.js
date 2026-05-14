import invtznClient from '@/core/api/invtznClient';

export const builderService = {
  getDeployment(id) {
    return invtznClient.get(`deployments/${id}/`);
  },
  
  saveCustomData(id, customData) {
    // Usamos PATCH para modificar solo el campo custom_data
    return invtznClient.patch(`deployments/${id}/`, {
      custom_data: customData
    });
  }
};
