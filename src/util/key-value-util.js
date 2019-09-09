export function getKeys(json) {
  return Object.keys(json[json.length - 1]);
}

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
