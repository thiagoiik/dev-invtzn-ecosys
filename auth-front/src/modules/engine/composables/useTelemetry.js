import { engineService } from '../services/engineService';

export function useTelemetry() {
  const trackVisit = async (slug) => {
    try {
      // Disparo silencioso de métrica de visita
      await engineService.submitMetric(slug, 'VISIT');
      console.log('Telemetry: Visit tracked successfully.');
    } catch (err) {
      console.warn('Telemetry: Fail tracking visit silently.', err);
    }
  };

  const trackRsvpSubmit = async (slug) => {
    try {
      // Disparo silencioso de métrica de envío de RSVP
      await engineService.submitMetric(slug, 'RSVP_SUBMIT');
      console.log('Telemetry: RSVP submission tracked.');
    } catch (err) {
      console.warn('Telemetry: Fail tracking RSVP silently.', err);
    }
  };

  return {
    trackVisit,
    trackRsvpSubmit
  };
}
