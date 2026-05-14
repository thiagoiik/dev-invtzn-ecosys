import { describe, it, expect, vi, beforeEach } from 'vitest';
import { crmService } from '../crmService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient');

describe('crmService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch all profiles', async () => {
    invtznClient.get.mockResolvedValueOnce({ data: [] });

    await crmService.fetchAllProfiles();
    
    expect(invtznClient.get).toHaveBeenCalledWith('profiles/');
  });

  it('should update profile role', async () => {
    invtznClient.patch.mockResolvedValueOnce({ data: {} });

    await crmService.updateProfileRole(123, 'VENDOR');
    
    expect(invtznClient.patch).toHaveBeenCalledWith('profiles/123/', { custom_role: 'VENDOR' });
  });

  it('should fetch all deployments globally', async () => {
    invtznClient.get.mockResolvedValueOnce({ data: [] });

    await crmService.fetchAllDeployments();
    
    expect(invtznClient.get).toHaveBeenCalledWith('deployments/');
  });
});
