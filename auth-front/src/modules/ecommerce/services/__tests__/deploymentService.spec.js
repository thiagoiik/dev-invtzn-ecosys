import { describe, it, expect, vi, beforeEach } from 'vitest';
import { deploymentService } from '../deploymentService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient');

describe('deploymentService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create a sandbox deployment', async () => {
    invtznClient.post.mockResolvedValueOnce({ data: { id: 1 } });

    await deploymentService.createSandbox(10);
    
    expect(invtznClient.post).toHaveBeenCalledWith('deployments/', {
      product: 10,
      status: 'DRAFT',
      custom_data: {
        message: '¡Diseña tu invitación aquí!',
        theme: 'light'
      }
    });
  });

  it('should fetch my deployments', async () => {
    invtznClient.get.mockResolvedValueOnce({ data: [] });

    await deploymentService.fetchMyDeployments();
    
    expect(invtznClient.get).toHaveBeenCalledWith('deployments/');
  });
});
