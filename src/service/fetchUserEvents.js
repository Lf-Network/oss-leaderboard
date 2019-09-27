import { findGreatestLesser, findLeastGreater } from '../util/eventHelper';
import { fetchUsers } from '../..';
import {
  eventQueryGenerator,
  events,
  repositoriesContributedTo,
} from '../constants';

/**
 * Fetch user events within data from: dateFrom and to:dateTo.
 *
 * @param {String} query
 * @param {Date} dateFrom
 * @param {Date} dateTo
 * @returns
 */
export async function fetchUserEventsFromTo(query, dateFrom, dateTo) {
  let userEventList = [];

  try {
    const response = await fetchUsers(query);
    let needAnotherFetch = false;
    const eventList = [];
    let eventListArray = [];

    Object.keys(events).forEach(event => {
      const eventResult = response.data.user[event];
      const { eventArray, needAnotherFetch: fetchMore } = extractRangeData(
        eventResult,
        events[event],
        dateFrom,
        dateTo,
      );

      if (fetchMore) {
        needAnotherFetch = fetchMore;
        const eventFetchMore = Object.assign({}, events[event]);

        if (eventFetchMore.variables.after) {
          eventFetchMore.variables.after.value = eventResult.pageInfo.endCursor;
        } else if (eventFetchMore.variables.before) {
          eventFetchMore.variables.before.value =
            eventResult.pageInfo.endCursor;
        }

        eventList.push(eventFetchMore);
      }

      eventListArray = eventListArray.concat(
        eventArray.map(edge => ({ [event]: edge.node })),
      );
    });

    // For repo contribution.

    const { eventArray, needAnotherFetch: fetchMore } = extractRangeData(
      response.data.user.repositoriesContributedTo,
      repositoriesContributedTo.repositoriesContributedTo,
      dateFrom,
      dateTo,
    );

    userEventList = userEventList.concat(
      eventListArray,
      eventArray.map(edge => ({ ['repositoriesContributed']: edge.node })),
    );

    let repoContributionFetchMore = '';

    needAnotherFetch = needAnotherFetch || fetchMore;

    const repositoriesContributed =
      response.data.user.repositoriesContributedTo;

    repoContributionFetchMore = Object.assign({}, repositoriesContributedTo);

    repoContributionFetchMore.repositoriesContributedTo.variables.after.value =
      repositoriesContributed.pageInfo.endCursor;

    if (needAnotherFetch) {
      const { userEventList: remainingEventList } = await fetchUserEventsFromTo(
        eventQueryGenerator(
          eventList,
          response.login,
          repoContributionFetchMore,
        ),
        dateFrom,
        dateTo,
      );

      userEventList = [...userEventList, ...remainingEventList];
    }
  } catch (err) {
    // eslint-disable-next-line no-console
    console.log('Error fetching user events', err);
  }

  return Object.assign({}, { userEventList });
}

/**
 *
 * @param {Array} currentEvent
 * @param {Object} eventObj
 * @param {Date} fromDate
 * @param {Date} toDate
 */
function extractRangeData(currentEvent, eventObj, fromDate, toDate) {
  const eventResult = Object.assign({}, { ...currentEvent });
  let needAnotherFetch = false;
  let eventArray = [];

  try {
    if (eventResult.edges.length <= 0) {
      return { eventArray: [], needAnotherFetch };
    }

    if (eventObj.variables.before) {
      eventResult.edges = eventResult.edges.reverse();
    }

    const lastDate = new Date(
      eventResult.edges[eventResult.edges.length - 1].node.updatedAt,
    );
    const firstDate = new Date(eventResult.edges[0].node.updatedAt);

    let leftIndex = 0;
    let rightIndex = eventResult.edges.length;

    if (fromDate.getTime() > firstDate.getTime()) {
      leftIndex = findGreatestLesser(
        eventResult.edges,
        0,
        eventResult.edges.length - 1,
        fromDate,
      );
    }

    if (
      lastDate.getTime() >= toDate.getTime() &&
      eventResult.pageInfo.hasNextPage
    ) {
      needAnotherFetch = true;
    } else {
      rightIndex = findLeastGreater(
        eventResult.edges,
        0,
        eventResult.edges.length - 1,
        toDate,
      );
    }

    eventArray = eventResult.edges.slice(leftIndex, rightIndex);
  } catch (err) {
    // eslint-disable-next-line no-console
    console.log(err);
  }

  return { eventArray, needAnotherFetch };
}
