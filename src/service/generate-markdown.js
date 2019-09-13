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
    {
      table: { headers: headers, rows: jsonArray },
    },
  ]);
}
