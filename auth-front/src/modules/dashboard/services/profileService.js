import invtznClient from '@/core/api/invtznClient';

export const profileService = {
  // Obtiene el perfil de negocio del usuario desde api-invtzn
  fetchMyProfile() {
    return invtznClient.get('profiles/me/');
  },
  
  // Actualiza los datos de perfil como el número de teléfono
  updateMyProfile(data) {
    return invtznClient.patch('profiles/me/', data);
  }
};
