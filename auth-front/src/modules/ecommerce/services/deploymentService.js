import invtznClient from '@/core/api/invtznClient';

export const deploymentService = {
  createSandbox(productId, customData = null) {
    // Crea una invitación en estado DRAFT asociada al producto seleccionado
    return invtznClient.post('deployments/', {
      product: productId,
      status: 'DRAFT',
      custom_data: customData || {
        message: "¡Diseña tu invitación aquí!",
        theme: "light"
      }
    });
  },
  
  fetchMyDeployments() {
    return invtznClient.get('deployments/');
  },
  
  deleteDeployment(id) {
    return invtznClient.delete(`deployments/${id}/`);
  },
  
  fetchDeploymentGuests(id) {
    return invtznClient.get(`deployments/${id}/guests/`);
  }
};
