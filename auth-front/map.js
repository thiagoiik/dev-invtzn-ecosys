import fs from 'fs';
import path  from 'path';

function getFiles(dir, prefix = '') {
  fs.readdirSync(dir).forEach(file => {
    if (file === 'node_modules' || file === '.git') return;
    console.log(prefix + file);
    if (fs.statSync(path.join(dir, file)).isDirectory()) {
      getFiles(path.join(dir, file), prefix + '  ');
    }
  });
}
getFiles('./src');