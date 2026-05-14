import { describe, it, expect, vi, beforeEach } from 'vitest';
import { builderService } from '../builderService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient');

describe('builderService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch a deployment by id', async () => {
    const mockData = { id: 1, custom_data: { theme: 'dark' } };
    invtznClient.get.mockResolvedValueOnce({ data: mockData });

    const result = await builderService.getDeployment(1);
    
    expect(invtznClient.get).toHaveBeenCalledWith('deployments/1/');
    expect(result.data).toEqual(mockData);
  });

  it('should save custom data using PATCH', async () => {
    const customData = { title: 'Boda' };
    invtznClient.patch.mockResolvedValueOnce({ status: 200 });

    await builderService.saveCustomData(1, customData);
    
    expect(invtznClient.patch).toHaveBeenCalledWith('deployments/1/', {
      custom_data: customData
    });
  });
});
