import invtznClient from '@/core/api/invtznClient';

export const deploymentService = {
  createSandbox(productId) {
    // Crea una invitación en estado DRAFT asociada al producto seleccionado
    return invtznClient.post('deployments/', {
      product: productId,
      status: 'DRAFT',
      custom_data: {
        message: "¡Diseña tu invitación aquí!",
        theme: "light"
      }
    });
  },
  
  fetchMyDeployments() {
    return invtznClient.get('deployments/');
  }
};
