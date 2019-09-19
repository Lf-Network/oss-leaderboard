/*
 * sort array of object on basics of key and order
 * */
export function sort(arr, key, sortBy = 'asc') {
  return arr.sort((paramOne, paramTwo) => {
    if (sortBy === 'asc') {
      return paramOne[key] === paramTwo[key]
        ? 0
        : paramOne[key] < paramTwo[key]
        ? -1
        : 1;
    } else if (sortBy === 'desc') {
      return paramOne[key] === paramTwo[key]
        ? 0
        : paramOne[key] > paramTwo[key]
        ? -1
        : 1;
    }
  });
}
