const json2md = require('json2md');

/**
 * @example generateMarkdown{{
 *          ["firstName", "lastName"],
 *          [["Nischal", "Shakya"], ["Avishkar", "KC"]]
 *      }} => "firstName | lastName \n
 *             --- | --- \n
 *         Nischal | Shakya \n
 *         Avishkar | KC "
 * @param {array} rows
 * @param {string[]} headers
 * @returns {string}
 */
export async function generateMarkdown(rows, headers) {
  return json2md([
    { h1: 'oss-leaderboard' },
    {
      table: { headers: Object.values(headers), rows: rows },
    },
    { blockquote: 'PR = Pull request' },
  ]);
}
