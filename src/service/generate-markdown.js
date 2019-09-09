const json2md = require('json2md');

export async function generateMarkdown(jsonArray, headers) {
  return json2md([
    {
      table: { headers: headers, rows: jsonArray },
    },
  ]);
}
