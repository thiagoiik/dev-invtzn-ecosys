import invtznClient from '@/core/api/invtznClient';

export const profileService = {
  // Obtiene el perfil de negocio del usuario desde api-invtzn
  fetchMyProfile() {
    return invtznClient.get('profiles/me/');
  },
  
  // Sincroniza datos básicos desde api-auth
  syncProfile(data) {
    return invtznClient.post('profiles/me/', data); 
  },
  
  // Actualiza los datos de perfil como el número de teléfono
  updateMyProfile(data) {
    return invtznClient.patch('profiles/me/', data);
  }
};
