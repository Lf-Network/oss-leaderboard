/**
 * Filter keys from flat json
 *
 * let json = [{name : "Nischal" lastname: "Shakya"}, {"name": "Avishkar", lastnane: "KC"}]
 *
 * @param {json} json
 * @return ["name", "lastname"]
 */
export function getKeys(json) {
  return Object.keys(json[json.length - 1]);
}

/**
 * Filter values from json array
 *
 * let json = [{name : "Nischal" lastname: "Shakya"}, {"name": "Avishkar", lastnane: "KC"}]
 * let keys = ["name", "lastname"]
 *
 * @param {json} json
 * @param {string[]} keys
 * @return [["Nischal", "Shakya"], ["Avishkar", "KC"]]
 */
export async function getValues(json, keys) {
  const twoDValuesArray = [];
  let keyIndex = 0;
  json.forEach(element => {
    const singleDValuesArray = [];
    do {
      const key = keys[keyIndex];
      singleDValuesArray.push(element[key]);
      keyIndex++;
    } while (keyIndex != keys.length);
    keyIndex = 0;
    twoDValuesArray.push(singleDValuesArray);
  });
  return twoDValuesArray;
}
