/**
 *
 * Filter keys from flat json.
 *
 * Suppose: let json = [{name : "Nischal" lastname: "Shakya"}, {"name": "Avishkar", lastnane: "KC"}].
 *
 * @param {any[]} json
 * @return Keys = ["name", "lastname"].
 */
export function getKeys(json) {
  let keysObj = {};

  json.forEach(item => {
    const temp = {};

    Object.keys(item).forEach(key => {
      temp[key] = 1;
    });
    temp.score = 'Score';
    keysObj = Object.assign({}, keysObj, temp);
  });

  return Object.keys(keysObj);
}

/**
 * Filter values from json array.
 *
 * let json = [{name : "Nischal" lastname: "Shakya"}, {"name": "Avishkar", lastnane: "KC"}]
 * let keys = ["name", "lastname"].
 *
 * @param {json} json
 * @param {string[]} keys
 * @return [["Nischal", "Shakya"], ["Avishkar", "KC"]]
 */
export async function getValues(json, keys) {
  const twoDValuesArray = [];
  let keyIndex = 0;

  for (const element of json) {
    const singleDValuesArray = [];

    do {
      const key = keys[keyIndex];

      singleDValuesArray.push(element[key]);
      keyIndex++;
    } while (keyIndex !== keys.length);
    keyIndex = 0;
    twoDValuesArray.push(singleDValuesArray);
  }
  
  return twoDValuesArray;
}
