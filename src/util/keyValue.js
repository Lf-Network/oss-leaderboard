/**
 * Filter keys from flat json.
 *
 * @example
 *      {{getKeys [{firstName : "Nischal" lastName: "Shakya"}, {firstName: "Avishkar", lastName: "KC"}] }}
 *            => ["firstName", "lastName"]
 * @param {any[]} any
 * @returns {array}.
 */
export function getKeys(any) {
  let keysObj = {};

  for (const item of any) {
    const temp = {};

    Object.keys(item).forEach(key => {
      temp[key] = 1;
    });
    temp.score = 'Score';
    keysObj = Object.assign({}, keysObj, temp);
  }

  return Object.keys(keysObj);
}

/**
 * Filter values from flat json.
 *
 * @example
 *      {{getValues [{firstName : "Nischal" lastName: "Shakya"}, {firstName: "Avishkar", lastName: "KC"}], ["firstName", "lastName"] }}
 *            => [["Nischal", "Shakya"], ["Avishkar", "KC"]]
 * @param {Array} json
 * @param {string[]} keys
 * @returns {array}
 */
export function getValues(json, keys) {
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
