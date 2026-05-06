import fs from 'fs';
import path from 'path';

const targetDirs = ['src'];
const context = {
  files: {},
  structure: {}
};

function readDir(dir) {
  const result = {};
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      if (file !== 'node_modules' && file !== '.git') {
        result[file] = readDir(fullPath);
      }
    } else {
      result[file] = 'file';
      // Leer archivos críticos si quieres incluirlos directamente
      if (file.endsWith('.js') || file.endsWith('.vue')) {
        context.files[fullPath] = fs.readFileSync(fullPath, 'utf8');
      }
    }
  });
  return result;
}

context.structure = readDir('src');
fs.writeFileSync('CONTEXTO.json', JSON.stringify(context, null, 2));
console.log('Contexto generado en CONTEXTO.json');