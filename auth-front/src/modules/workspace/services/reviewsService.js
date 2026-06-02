import invtznClient from '@/core/api/invtznClient';

export const reviewsService = {
  fetchAllReviews() {
    return invtznClient.get('reviews/');
  },
  toggleApprove(reviewId) {
    return invtznClient.post(`reviews/${reviewId}/toggle-approve/`);
  },
  deleteReview(reviewId) {
    return invtznClient.delete(`reviews/${reviewId}/`);
  }
};
