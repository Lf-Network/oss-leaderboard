import fs from 'fs';

/**
 * Write data content to external markdown file.
 *
 * @example createMarkdown {{
 *     "oss-leaderboard.md", "firstName | lastName \n
                              --- | --- \n
                              Nischal | Shakya \n
                              Avishkar | KC."
 * }} => "oss-leaderboard.md"
 * @param {string} fileName
 * @param {string} data
 */
export async function createMarkdown(fileName, data) {
  fs.writeFile(fileName, data, err => {
    if (err) {
      throw err;
    }
  });
}
