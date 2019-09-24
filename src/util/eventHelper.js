/**
 * Binary search to find least greater index than given date.
 *
 * @param {Array} events Array of events.
 * @param {Number} leftBound Left bound.
 * @param {Number} rightBound Right bound.
 * @param {Date} boundDate Bound date.
 */
export const findLeastGreater = (events, leftBound, rightBound, boundDate) => {
  if (leftBound === rightBound) {
    return leftBound;
  }
  const mid = parseInt(leftBound + (rightBound - leftBound) / 2);
  const midEventDate = new Date(events[mid].node.updatedAt);

  if (midEventDate.getTime() >= boundDate.getTime()) {
    return findLeastGreater(events, mid + 1, rightBound, boundDate);
  }

  return findLeastGreater(events, leftBound, mid, boundDate);
};

/**
 * Binary search to find greatest lesser index than given date.
 *
 * @param {Array} events Array of events.
 * @param {Number} leftBound Left bound.
 * @param {Number} rightBound Right bound.
 * @param {Date} boundDate Bound date.
 */
export const findGreatestLesser = (
  events,
  leftBound,
  rightBound,
  boundDate,
) => {
  if (leftBound === rightBound) {
    return leftBound;
  }
  const mid = parseInt(leftBound + (rightBound - leftBound) / 2);
  const midEventDate = new Date(events[mid].node.updatedAt);

  if (midEventDate.getTime() > boundDate.getTime()) {
    return findGreatestLesser(events, mid + 1, rightBound, boundDate);
  }

  return findGreatestLesser(events, leftBound, mid, boundDate);
};
