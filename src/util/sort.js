const SORT_ASCENDING = 'asc';
const SORT_DESCENDING = 'desc';

/**
 * Sort array of object on basic of key and order.
 *
 *  @example sort {{
 *    [{firstName : "Nischal" lastName: "Shakya"}, {firstName: "Avishkar", lastName: "KC"}],
 *    "firstName",
 *    SORT_ASCENDING
 *  }} => [{firstName: "Avishkar", lastName: "KC"}, {firstName : "Nischal" lastName: "Shakya"}]
 *  @param {Event} arr
 *  @param {string} key
 *  @param {string} sortBy
 *  @returns {array}
 *
 */
export function sort(arr, key, sortBy = 'asc') {
  return arr.sort((paramOne, paramTwo) => {
    if (sortBy === SORT_ASCENDING) {
      return paramOne[key] === paramTwo[key]
        ? 0
        : paramOne[key] < paramTwo[key]
          ? -1
          : 1;
    } else if (sortBy === SORT_DESCENDING) {
      return paramOne[key] === paramTwo[key]
        ? 0
        : paramOne[key] > paramTwo[key]
          ? -1
          : 1;
    }
  });
}
