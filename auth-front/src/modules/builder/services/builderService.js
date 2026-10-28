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
  },
  
  updateDeployment(id, data) {
    return invtznClient.patch(`deployments/${id}/`, data);
  },
  
  activateBasic(id, reviewData) {
    return invtznClient.post(`deployments/${id}/activate-basic/`, reviewData);
  },
  
  publishProduct(id, productData) {
    return invtznClient.post(`deployments/${id}/publish-product/`, productData);
  },
  
  requestReview(id) {
    return invtznClient.post(`deployments/${id}/request-review/`);
  },
  
  uploadMedia(id, formData) {
    return invtznClient.post(`deployments/${id}/upload-media/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  deleteMedia(id, url) {
    return invtznClient.delete(`deployments/${id}/delete-media/`, {
      data: { url }
    });
  }

};
