import { describe, it, expect, vi } from 'vitest';
import { profileService } from '../profileService';
import invtznClient from '@/core/api/invtznClient';

// Mockeamos el cliente HTTP
vi.mock('@/core/api/invtznClient', () => ({
  default: {
    get: vi.fn(),
    patch: vi.fn()
  }
}));

describe('profileService', () => {
  it('fetchMyProfile hace un GET a profiles/me/', async () => {
    invtznClient.get.mockResolvedValue({ data: { custom_role: 'VENDOR' } });
    
    const response = await profileService.fetchMyProfile();
    
    expect(invtznClient.get).toHaveBeenCalledWith('profiles/me/');
    expect(response.data.custom_role).toBe('VENDOR');
  });

  it('updateMyProfile hace un PATCH a profiles/me/ con los datos', async () => {
    const updateData = { phone_number: '123456789' };
    invtznClient.patch.mockResolvedValue({ data: updateData });
    
    const response = await profileService.updateMyProfile(updateData);
    
    expect(invtznClient.patch).toHaveBeenCalledWith('profiles/me/', updateData);
    expect(response.data.phone_number).toBe('123456789');
  });
});
