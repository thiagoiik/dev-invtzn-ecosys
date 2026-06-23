export const COLOR_PALETTES = [
  // 🟢 CATEGORÍA: BÁSICOS (Plan Gratis/Básico)
  {
    id: 'classic_navy',
    name: 'Azul Imperial',
    category: 'basic',
    premium: false,
    colors: {
      primary: '#1e3a8a',      // Azul marino
      secondary: '#475569',    // Slate grisáceo
      accent: '#3b82f6',       // Azul vibrante
      blockBg: 'rgba(255, 255, 255, 0.45)', // Transparente glass
      cardBg: 'rgba(255, 255, 255, 0.75)',
      contentBg: '#f8fafc'     // Fondo liso slate
    }
  },
  {
    id: 'salvia_crema',
    name: 'Salvia & Crema',
    category: 'basic',
    premium: false,
    colors: {
      primary: '#2d4a22',      // Verde oliva oscuro
      secondary: '#64748b',    // Gris slate
      accent: '#15803d',       // Verde acento
      blockBg: 'rgba(255, 255, 255, 0.45)',
      cardBg: 'rgba(255, 255, 255, 0.75)',
      contentBg: '#fbfbf7'     // Blanco cálido
    }
  },
  {
    id: 'burgundy_classic',
    name: 'Borgoña Clásico',
    category: 'basic',
    premium: false,
    colors: {
      primary: '#881337',      // Vino tinto
      secondary: '#4b5563',    // Gris neutro
      accent: '#be123c',       // Rojo vivo
      blockBg: 'rgba(255, 255, 255, 0.45)',
      cardBg: 'rgba(255, 255, 255, 0.75)',
      contentBg: '#fffbfb'     // Blanco sutil rosado
    }
  },
  {
    id: 'monochrome_luxury',
    name: 'Monocromo Luxury',
    category: 'basic',
    premium: false,
    colors: {
      primary: '#0f172a',      // Negro slate
      secondary: '#64748b',    // Gris slate
      accent: '#1e293b',       // Gris oscuro
      blockBg: 'rgba(255, 255, 255, 0.45)',
      cardBg: 'rgba(255, 255, 255, 0.8)',
      contentBg: '#ffffff'     // Blanco absoluto
    }
  },

  // 👑 CATEGORÍA: PASTEL (Premium)
  {
    id: 'lavender_mint',
    name: 'Lavanda Silvestre 👑',
    category: 'pastel',
    premium: true,
    colors: {
      primary: '#6d28d9',      // Violeta lavanda
      secondary: '#475569',    // Gris
      accent: '#10b981',       // Menta verde
      blockBg: 'rgba(255, 255, 255, 0.5)',
      cardBg: 'rgba(255, 255, 255, 0.8)',
      contentBg: '#faf8ff'     // Blanco lila
    }
  },
  {
    id: 'rose_quartz',
    name: 'Rosa Cuarzo 👑',
    category: 'pastel',
    premium: true,
    colors: {
      primary: '#db2777',      // Rosa oscuro
      secondary: '#6b7280',    // Gris neutro
      accent: '#d97706',       // Champaña oro
      blockBg: 'rgba(255, 255, 255, 0.5)',
      cardBg: 'rgba(255, 255, 255, 0.8)',
      contentBg: '#fff5f7'     // Rosa blanquecino
    }
  },
  {
    id: 'sea_breeze',
    name: 'Brisa Marina 👑',
    category: 'pastel',
    premium: true,
    colors: {
      primary: '#0369a1',      // Azul océano
      secondary: '#4b5563',    // Gris
      accent: '#f97316',       // Coral naranja
      blockBg: 'rgba(255, 255, 255, 0.5)',
      cardBg: 'rgba(255, 255, 255, 0.8)',
      contentBg: '#f0f9ff'     // Azul blanquecino
    }
  },

  // 👑 CATEGORÍA: CANDY (Premium)
  {
    id: 'sweet_lollipop',
    name: 'Sweet Lollipop 👑',
    category: 'candy',
    premium: true,
    colors: {
      primary: '#d01c8b',      // Rosa chicle
      secondary: '#5c6bc0',    // Morado suave
      accent: '#f5b041',       // Amarillo dulce
      blockBg: 'rgba(255, 240, 245, 0.55)',
      cardBg: 'rgba(255, 255, 255, 0.85)',
      contentBg: '#fff0f5'     // Lavanda blanquecina
    }
  },
  {
    id: 'mint_melon',
    name: 'Menta & Melón 👑',
    category: 'candy',
    premium: true,
    colors: {
      primary: '#0f9d58',      // Verde menta
      secondary: '#5a6b7c',    // Gris azulado
      accent: '#f26522',       // Naranja melón
      blockBg: 'rgba(240, 253, 244, 0.55)',
      cardBg: 'rgba(255, 255, 255, 0.85)',
      contentBg: '#f5fff9'     // Menta blanquecina
    }
  },

  // 👑 CATEGORÍA: NEÓN (Premium)
  {
    id: 'cyber_neon',
    name: 'Electro Neon 👑',
    category: 'neon',
    premium: true,
    colors: {
      primary: '#00f6ff',      // Cyan eléctrico
      secondary: '#94a3b8',    // Slate gris
      accent: '#ff007f',       // Magenta neón
      blockBg: 'rgba(15, 23, 42, 0.65)', // Fondo oscuro translúcido
      cardBg: 'rgba(30, 41, 59, 0.7)',
      contentBg: '#090d16'     // Fondo ultra oscuro
    }
  },
  {
    id: 'green_acid',
    name: 'Green Acid 👑',
    category: 'neon',
    premium: true,
    colors: {
      primary: '#39ff14',      // Verde ácido neón
      secondary: '#94a3b8',    // Slate gris
      accent: '#ffffff',       // Blanco puro
      blockBg: 'rgba(24, 24, 27, 0.7)',
      cardBg: 'rgba(39, 39, 42, 0.75)',
      contentBg: '#0a0a0a'     // Negro absoluto
    }
  },

  // 👑 CATEGORÍA: METÁLICOS (Premium - con degradados especiales)
  {
    id: 'gold_luxury',
    name: 'Oro Imperial 👑',
    category: 'metallic',
    premium: true,
    colors: {
      primary: '#d4af37',      // Oro metálico
      secondary: '#94a3b8',    // Slate gris
      accent: '#aa7c11',       // Bronce
      blockBg: 'rgba(15, 23, 42, 0.7)', // Slate oscuro
      cardBg: 'rgba(30, 41, 59, 0.75)',
      contentBg: '#030712',    // Negro azulado
      primaryGradient: 'linear-gradient(135deg, #bf953f 0%, #fcf6ba 25%, #b38728 50%, #fbf5b7 75%, #aa771c 100%)'
    }
  },
  {
    id: 'silver_luxury',
    name: 'Plata Luxury 👑',
    category: 'metallic',
    premium: true,
    colors: {
      primary: '#a1a1aa',      // Plata
      secondary: '#4b5563',    // Gris medio
      accent: '#cbd5e1',       // Plata brillante
      blockBg: 'rgba(255, 255, 255, 0.4)',
      cardBg: 'rgba(255, 255, 255, 0.75)',
      contentBg: '#f1f5f9',    // Gris perla
      primaryGradient: 'linear-gradient(135deg, #e2e8f0 0%, #ffffff 50%, #cbd5e1 100%)'
    }
  },
  {
    id: 'copper_rose',
    name: 'Cobre Rosé 👑',
    category: 'metallic',
    premium: true,
    colors: {
      primary: '#b87333',      // Cobre
      secondary: '#6b7280',    // Gris
      accent: '#e59866',       // Bronce cobre
      blockBg: 'rgba(253, 244, 245, 0.5)',
      cardBg: 'rgba(255, 255, 255, 0.75)',
      contentBg: '#fdfbfb',    // Blanco rosado
      primaryGradient: 'linear-gradient(135deg, #ca7a65 0%, #f7d2c4 50%, #b85a43 100%)'
    }
  }
];

export const CONTENT_TEXTURES = [
  {
    id: 'none',
    name: 'Color Liso de la Paleta',
    premium: false,
    style: ''
  },
  {
    id: 'paper_fiber',
    name: 'Papel de Fibra / Algodón 👑',
    premium: true,
    url: '/assets/backgrounds/textured_paper.svg',
    style: 'background-image: url("/assets/backgrounds/textured_paper.svg"); background-repeat: repeat;'
  },
  {
    id: 'elegant_canvas',
    name: 'Lienzo Fino 👑',
    premium: true,
    url: '/assets/backgrounds/elegant_canvas.svg',
    style: 'background-image: url("/assets/backgrounds/elegant_canvas.svg"); background-repeat: repeat;'
  },
  {
    id: 'watercolor_soft',
    name: 'Acuarela Suave 👑',
    premium: true,
    url: '/assets/backgrounds/watercolor_soft.svg',
    style: 'background-image: url("/assets/backgrounds/watercolor_soft.svg"); background-repeat: no-repeat; background-size: cover; background-position: center;'
  },
  {
    id: 'starry_night',
    name: 'Destellos Noche 👑',
    premium: true,
    style: 'background: radial-gradient(circle, rgba(20,20,35,1) 0%, rgba(3,7,18,1) 100%); background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px), radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px); background-size: 550px 550px, 350px 350px; background-position: 0 0, 40px 60px;'
  }
];
