/**
 * Binary search to find least greater index than given date.
 *
 * @param {*} events Array of events.
 * @param {*} leftBound Left bound.
 * @param {*} rightBound Right bound.
 */
export const findLeastGreater = (
  eventDetail,
  leftBound,
  rightBound,
  boundDate,
) => {
  if (leftBound === rightBound) {
    return leftBound;
  }
  const mid = parseInt(leftBound + (rightBound - leftBound) / 2);
  const midEventDate = new Date(eventDetail[mid].node.updatedAt);
  if (midEventDate.getTime() >= boundDate.getTime()) {
    return findLeastGreater(eventDetail, mid + 1, rightBound, boundDate);
  }
  return findLeastGreater(eventDetail, leftBound, mid, boundDate);
};

/**
 * Binary search to find greatest lesser index than given date.
 *
 * @param {*} events Array of events.
 * @param {*} leftBound Left bound.
 * @param {*} rightBound Right bound.
 */
export const findGreatestLesser = (
  eventDetail,
  leftBound,
  rightBound,
  boundDate,
) => {
  if (leftBound === rightBound) {
    return leftBound;
  }
  const mid = parseInt(leftBound + (rightBound - leftBound) / 2);
  const midEventDate = new Date(eventDetail[mid].node.updatedAt);

  if (midEventDate.getTime() > boundDate.getTime()) {
    return findGreatestLesser(eventDetail, mid + 1, rightBound, boundDate);
  }
  return findGreatestLesser(eventDetail, leftBound, mid, boundDate);
};
