import { ref } from 'vue';

class SoundSynthesizer {
  constructor() {
    this.ctx = null;
  }

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    // Resume context if it was suspended (browser autoplay policy)
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playP1() {
    this.init();
    const t = this.ctx.currentTime;
    
    // 1. Clic del Lacre
    const osc1 = this.ctx.createOscillator();
    const gain1 = this.ctx.createGain();
    osc1.type = 'triangle';
    osc1.frequency.setValueAtTime(150, t);
    osc1.frequency.exponentialRampToValueAtTime(10, t + 0.1);
    gain1.gain.setValueAtTime(0.3, t);
    gain1.gain.exponentialRampToValueAtTime(0.01, t + 0.1);
    
    osc1.connect(gain1);
    gain1.connect(this.ctx.destination);
    osc1.start(t);
    osc1.stop(t + 0.1);

    // 2. Whoosh de la Tarjeta (Deslizamiento)
    const osc2 = this.ctx.createOscillator();
    const gain2 = this.ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(300, t + 0.3);
    osc2.frequency.exponentialRampToValueAtTime(600, t + 0.8);
    gain2.gain.setValueAtTime(0, t + 0.3);
    gain2.gain.linearRampToValueAtTime(0.15, t + 0.5);
    gain2.gain.exponentialRampToValueAtTime(0.001, t + 0.9);

    osc2.connect(gain2);
    gain2.connect(this.ctx.destination);
    osc2.start(t + 0.3);
    osc2.stop(t + 0.9);
  }

  playP2() {
    this.init();
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    
    osc.type = 'sine';
    osc.frequency.setValueAtTime(200, t);
    osc.frequency.exponentialRampToValueAtTime(450, t + 1.2);
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.1, t + 0.3);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 1.3);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 1.3);
  }

  playP3() {
    this.init();
    const t = this.ctx.currentTime;
    const delays = [0, 0.2, 0.4, 0.6];
    
    delays.forEach((delay, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(300 + (idx * 80), t + delay);
      osc.frequency.exponentialRampToValueAtTime(100, t + delay + 0.08);
      gain.gain.setValueAtTime(0.15, t + delay);
      gain.gain.exponentialRampToValueAtTime(0.01, t + delay + 0.08);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t + delay);
      osc.stop(t + delay + 0.08);
    });

    const oscEnd = this.ctx.createOscillator();
    const gainEnd = this.ctx.createGain();
    oscEnd.type = 'sine';
    oscEnd.frequency.setValueAtTime(440, t + 0.8);
    oscEnd.frequency.exponentialRampToValueAtTime(880, t + 1.3);
    gainEnd.gain.setValueAtTime(0, t + 0.8);
    gainEnd.gain.linearRampToValueAtTime(0.1, t + 0.9);
    gainEnd.gain.exponentialRampToValueAtTime(0.001, t + 1.3);

    oscEnd.connect(gainEnd);
    gainEnd.connect(this.ctx.destination);
    oscEnd.start(t + 0.8);
    oscEnd.stop(t + 1.3);
  }

  playP4() {
    this.init();
    const t = this.ctx.currentTime;
    
    const oscScan = this.ctx.createOscillator();
    const gainScan = this.ctx.createGain();
    oscScan.type = 'sawtooth';
    oscScan.frequency.setValueAtTime(600, t);
    oscScan.frequency.linearRampToValueAtTime(1200, t + 0.5);
    oscScan.frequency.linearRampToValueAtTime(800, t + 1.0);
    gainScan.gain.setValueAtTime(0, t);
    gainScan.gain.linearRampToValueAtTime(0.08, t + 0.2);
    gainScan.gain.linearRampToValueAtTime(0.08, t + 0.8);
    gainScan.gain.exponentialRampToValueAtTime(0.001, t + 1.1);

    oscScan.connect(gainScan);
    gainScan.connect(this.ctx.destination);
    oscScan.start(t);
    oscScan.stop(t + 1.1);

    setTimeout(() => {
      if(!this.ctx) return;
      const oscGate = this.ctx.createOscillator();
      const gainGate = this.ctx.createGain();
      oscGate.type = 'triangle';
      oscGate.frequency.setValueAtTime(90, this.ctx.currentTime);
      oscGate.frequency.exponentialRampToValueAtTime(20, this.ctx.currentTime + 0.8);
      gainGate.gain.setValueAtTime(0.2, this.ctx.currentTime);
      gainGate.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.8);

      oscGate.connect(gainGate);
      gainGate.connect(this.ctx.destination);
      oscGate.start();
      oscGate.stop(this.ctx.currentTime + 0.8);
    }, 1200);
  }

  playP5() {
    this.init();
    const t = this.ctx.currentTime;
    const notes = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99, 1046.50]; 
    
    notes.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t + (idx * 0.1));
      gain.gain.setValueAtTime(0.12, t + (idx * 0.1));
      gain.gain.exponentialRampToValueAtTime(0.001, t + (idx * 0.1) + 0.6);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t + (idx * 0.1));
      osc.stop(t + (idx * 0.1) + 0.6);
    });
  }
}

// Global instance to reuse context
const synth = new SoundSynthesizer();

export function useAudioFX() {
  const playEnvelopeAudio = (type) => {
    try {
      switch (type) {
        case 'classic':
        case 1:
        case '1':
          synth.playP1();
          break;
        case 'gatefold':
        case 2:
        case '2':
          synth.playP2();
          break;
        case 'origami':
        case 3:
        case '3':
          synth.playP3();
          break;
        case 'cyber':
        case 4:
        case '4':
          synth.playP4();
          break;
        case 'curtain':
        case 5:
        case '5':
          synth.playP5();
          break;
        default:
          synth.playP1(); // default fallback
      }
    } catch (e) {
      console.warn('Audio API failed:', e);
    }
  };

  return {
    playEnvelopeAudio
  };
}
