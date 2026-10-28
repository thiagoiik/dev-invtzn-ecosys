import invtznClient from '@/core/api/invtznClient';

export const engineService = {
  // Función pública, usa get() que enviará la solicitud al backend
  // Si invtznClient inyecta el token y da error de CORS, podemos limpiar los headers,
  // pero nuestro backend ya permite peticiones públicas a este endpoint específico.
  fetchDeploymentBySlug(slug) {
    return invtznClient.get(`deployments/slug/${slug}/`);
  },
  
  submitRSVP(slug, data) {
    return invtznClient.post(`deployments/slug/${slug}/rsvp/`, data);
  },

  submitMetric(slug, metricType = 'VISIT') {
    return invtznClient.post(`deployments/slug/${slug}/metric/`, { metric_type: metricType });
  }
};
