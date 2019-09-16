import { keys } from '../constants';

const json2md = require('json2md');

/**
 * let headers = ["name", "lastname"]
 * let jsonArray = [["Nischal", "Shakya"], ["Avishkar", "KC"]]
 *
 * @param {array} jsonArray
 * @param {string[]} headers
 * @return firstname | lastname
 --- | ---
 Nischal | Shakya
 Avishkar | KC
 */
export async function generateMarkdown(jsonArray, headers) {
  return json2md([
    { h1: 'oss-leaderboard' },
    {
      table: { headers: Object.values(keys), rows: jsonArray },
    },
    { blockquote: 'PR = Pull request' },
  ]);
}
