import { describe, it, expect, vi } from 'vitest';
import { eventService } from '../eventService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}));

describe('eventService', () => {
  it('fetchMyEvents hace un GET a events/', async () => {
    const mockEvents = [{ id: 1, title: 'Boda' }];
    invtznClient.get.mockResolvedValue({ data: mockEvents });
    
    const response = await eventService.fetchMyEvents();
    
    expect(invtznClient.get).toHaveBeenCalledWith('events/');
    expect(response.data).toEqual(mockEvents);
  });

  it('createEvent hace un POST a events/ con el nuevo evento', async () => {
    const newEvent = { title: 'Boda', event_type: 'BODA' };
    invtznClient.post.mockResolvedValue({ data: newEvent });
    
    const response = await eventService.createEvent(newEvent);
    
    expect(invtznClient.post).toHaveBeenCalledWith('events/', newEvent);
    expect(response.data.title).toBe('Boda');
  });
});
