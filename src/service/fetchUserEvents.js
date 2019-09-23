import { findGreatestLesser, findLeastGreater } from '../util/eventHelper';
import { fetchUsers } from '../..';
import { eventQueryGenerator, events } from '../constants';

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
  const userContribution = {};

  try {
    const response = await fetchUsers(query);
    let needAnotherFetch = false;
    const eventList = [];

    Object.keys(events).forEach(event => {
      const eventResult = response.data.user[event];

      if (eventResult.edges.length <= 0) {
        return;
      }
      if (events[event].variables.before) {
        eventResult.edges = eventResult.edges.reverse();
      }

      const lastDate = new Date(
        eventResult.edges[eventResult.edges.length - 1].node.updatedAt,
      );
      const firstDate = new Date(eventResult.edges[0].node.updatedAt);

      let leftIndex = 0;
      let rightIndex = eventResult.edges.length;

      if (dateFrom.getTime() > firstDate.getTime()) {
        leftIndex = findGreatestLesser(
          eventResult.edges,
          0,
          eventResult.edges.length - 1,
          dateFrom,
        );
      }

      if (lastDate.getTime() >= dateTo.getTime()) {
        if (eventResult.pageInfo.hasNextPage) {
          needAnotherFetch = true;

          const eventFetchMore = Object.assign({}, events[event]);

          if (eventFetchMore.variables.after) {
            eventFetchMore.variables.after.value =
              eventResult.pageInfo.endCursor;
          } else if (eventFetchMore.variables.before) {
            eventFetchMore.variables.before.value =
              eventResult.pageInfo.endCursor;
          }

          eventList.push(eventFetchMore);
        }
      } else {
        rightIndex = findLeastGreater(
          eventResult.edges,
          0,
          eventResult.edges.length - 1,
          dateTo,
        );
      }

      userEventList = userEventList.concat(
        eventResult.edges
          .slice(leftIndex, rightIndex)
          .map(edge => ({ [event]: edge.node })),
      );
    });

    if (needAnotherFetch) {
      const { userEventList: remainingEventList } = await fetchUserEventsFromTo(
        eventQueryGenerator(eventList, response.login),
        dateFrom,
        dateTo,
      );

      userEventList = userEventList.concat(remainingEventList);
    }
    if (!userContribution.repositoriesContributedTo) {
      userContribution.repositoriesContributedTo = response.data.user
        .repositoriesContributedTo
        ? response.data.user.repositoriesContributedTo.totalCount
        : 0;
    }
  } catch (err) {
    // eslint-disable-next-line no-console
    console.log('Error fetching user events', err);
  }

  return Object.assign({}, { userEventList }, userContribution);
}
