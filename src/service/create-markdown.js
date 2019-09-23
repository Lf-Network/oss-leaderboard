import fs from 'fs';

/**
 * Write data content to external markdown file.
 * let fileName = users.md
 * let data = firstname | lastname
                --- | ---
              Nischal | Shakya
              Avishkar | KC
 *
 * @param {string} fileName
 * @param {object} data
*/
export function createMarkdown(fileName, data) {
  fs.writeFile(fileName, data, err => {
    if (err) {
      console.log(err);
    }
    console.log('Successfully Written to File.');
  });
}
