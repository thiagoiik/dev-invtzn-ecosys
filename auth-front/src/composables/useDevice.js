import { ref, onMounted, onUnmounted } from 'vue';

export function useDevice() {
  const isMobile = ref(false);
  const isTablet = ref(false);
  const isDesktop = ref(false);

  let mediaMobile = null;
  let mediaTablet = null;
  let mediaDesktop = null;

  const updateMatch = () => {
    isMobile.value = mediaMobile ? mediaMobile.matches : false;
    isTablet.value = mediaTablet ? mediaTablet.matches : false;
    isDesktop.value = mediaDesktop ? mediaDesktop.matches : false;
  };

  onMounted(() => {
    mediaMobile = window.matchMedia('(max-width: 767px)');
    mediaTablet = window.matchMedia('(min-width: 768px) and (max-width: 1024px)');
    mediaDesktop = window.matchMedia('(min-width: 1025px)');

    updateMatch();

    if (mediaMobile.addEventListener) {
      mediaMobile.addEventListener('change', updateMatch);
      mediaTablet.addEventListener('change', updateMatch);
      mediaDesktop.addEventListener('change', updateMatch);
    } else {
      mediaMobile.addListener(updateMatch);
      mediaTablet.addListener(updateMatch);
      mediaDesktop.addListener(updateMatch);
    }
  });

  onUnmounted(() => {
    if (mediaMobile) {
      if (mediaMobile.removeEventListener) {
        mediaMobile.removeEventListener('change', updateMatch);
        mediaTablet.removeEventListener('change', updateMatch);
        mediaDesktop.removeEventListener('change', updateMatch);
      } else {
        mediaMobile.removeListener(updateMatch);
        mediaTablet.removeListener(updateMatch);
        mediaDesktop.removeListener(updateMatch);
      }
    }
  });

  return {
    isMobile,
    isTablet,
    isDesktop
  };
}
