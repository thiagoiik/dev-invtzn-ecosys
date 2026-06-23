import { describe, it, expect } from 'vitest';
import { COLOR_PALETTES, CONTENT_TEXTURES } from '../palettes';

describe('palettes.js constants', () => {
  it('debería exportar COLOR_PALETTES y tener elementos definidos', () => {
    expect(Array.isArray(COLOR_PALETTES)).toBe(true);
    expect(COLOR_PALETTES.length).toBeGreaterThan(0);
  });

  it('cada paleta de colores debería tener las propiedades requeridas', () => {
    COLOR_PALETTES.forEach(palette => {
      expect(palette.id).toBeDefined();
      expect(palette.name).toBeDefined();
      expect(palette.category).toBeDefined();
      expect(palette.premium).toBeDefined();
      expect(palette.colors).toBeDefined();
      expect(palette.colors.primary).toBeDefined();
      expect(palette.colors.secondary).toBeDefined();
      expect(palette.colors.accent).toBeDefined();
      expect(palette.colors.blockBg).toBeDefined();
      expect(palette.colors.cardBg).toBeDefined();
      expect(palette.colors.contentBg).toBeDefined();
    });
  });

  it('debería exportar CONTENT_TEXTURES y tener elementos definidos', () => {
    expect(Array.isArray(CONTENT_TEXTURES)).toBe(true);
    expect(CONTENT_TEXTURES.length).toBeGreaterThan(0);
  });

  it('cada textura de contenido debería tener las propiedades requeridas', () => {
    CONTENT_TEXTURES.forEach(texture => {
      expect(texture.id).toBeDefined();
      expect(texture.name).toBeDefined();
      expect(texture.premium).toBeDefined();
      expect(texture.style).toBeDefined();
    });
  });
});
