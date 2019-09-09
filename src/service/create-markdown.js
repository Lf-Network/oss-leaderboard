import fs from 'fs';

export function createMarkdown(fileName, data) {
  fs.writeFile(fileName, data, err => {
    if (err) {
      console.log(err);
    }
    console.log('Successfully Written to File.');
  });
}
