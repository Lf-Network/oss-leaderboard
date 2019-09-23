/**
 * Binary search to count total events which lies after target date
 *
 * @param {*} events Array of events.
 * @param {*} l Left bound.
 * @param {*} r Right bound.
 */
export const findLeastGreater = (eventDetail, l, r, boundDate) => {
  if (l === r) {
    return l;
  }
  const mid = parseInt(l + (r - l) / 2);
  const midEventDate = new Date(eventDetail[mid].node.updatedAt);
  if (midEventDate.getTime() >= boundDate.getTime()) {
    return findLeastGreater(eventDetail, mid + 1, r, boundDate);
  }
  return findLeastGreater(eventDetail, l, mid, boundDate);
};

export const findGreatestLesser = (eventDetail, l, r, boundDate) => {
  if (l === r) {
    return l;
  }
  const mid = parseInt(l + (r - l) / 2);
  const midEventDate = new Date(eventDetail[mid].node.updatedAt);

  if (midEventDate.getTime() > boundDate.getTime()) {
    return findGreatestLesser(eventDetail, mid + 1, r, boundDate);
  }
  return findGreatestLesser(eventDetail, l, mid, boundDate);
};
