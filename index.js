import fetch from 'node-fetch';

import 'dotenv/config';

import getQuery from './src/query';
import {
  DAYS_TO_CONSIDER,
  QUERY_NAMES,
  STATES,
  eventTypes,
} from './src/constants';

const uptoDate = new Date();
uptoDate.setDate(uptoDate.getDate() - DAYS_TO_CONSIDER);

async function fetchUsers(query) {
  const accessToken = process.env.ACCESS_TOKEN;
  try {
    const res = await fetch('https://api.github.com/graphql', {
      method: 'POST',
      body: JSON.stringify(query),
      headers: {
        authorization: `token ${accessToken}`,
      },
    });
    return res.json();
  } catch (error) {
    // TODO
    throw error.response;
  }
}

async function init() {
  const query = getQuery(QUERY_NAMES.MEMBERS_WITH_ROLE);
  try {
    const usersList = await fetchData(query);
    usersList.forEach(async user => {
      const openedEvents = await fetchUserEvents(
        getQuery(QUERY_NAMES.FETCH_USER_EVENTS, {
          user: user.login,
          pullRequestState: STATES.OPEN,
          issueState: STATES.OPEN,
        }),
      );
      const closedEvents = await fetchUserEvents(
        getQuery(QUERY_NAMES.FETCH_USER_EVENTS, {
          user: user.login,
          pullRequestState: STATES.CLOSED,
          issueState: STATES.CLOSED,
        }),
      );
      console.log(
        `${user.name || user.login}: ${JSON.stringify({
          open: openedEvents,
          closed: closedEvents,
        })}`,
      );
    });
  } catch (error) {
    // TODO
  }
}

async function fetchUserEvents(query) {
  const queryVariables = {};
  const totalCounter = {};
  try {
    const response = await fetchUsers(query).catch(err => {
      throw err.response;
    });
    let needAnotherFetch = false;
    Object.values(eventTypes).forEach(event => {
      const eventResult = response.data.user[event];
      totalCounter[event] = 0;
      queryVariables[event] = eventResult;

      if (eventResult.edges.length <= 0) {
        return;
      }

      const lastDate = new Date(
        eventResult.edges[eventResult.edges.length - 1].node.updatedAt,
      );

      if (lastDate.getTime() >= uptoDate.getTime()) {
        totalCounter[event] += eventResult.edges.length;
        if (eventResult.pageInfo.hasNextPage) {
          needAnotherFetch = true;
        }
      } else {
        totalCounter[event] += countHowManyLiesWithin(
          eventResult.edges,
          0,
          eventResult.edges.length - 1,
        );
      }
    });

    if (needAnotherFetch) {
      Object.values(eventTypes).forEach(event => {
        query.variables = Object.assign({}, query.variables, {
          [`${event}After`]: queryVariables[event].pageInfo.endCursor,
        });
      });
      const currentCountstotalCounts = await fetchUserEvents(query);

      Object.values(eventTypes).forEach(event => {
        totalCounter[event] += currentCountstotalCounts[event];
      });
    }
  } catch (err) {
    console.log('Error fetching user events', err);
  }
  return totalCounter;
}

async function fetchData(query) {
  let hasNextPage = false;
  let usedQuery = query;
  let users = [];

  do {
    try {
      const response = await fetchUsers(usedQuery);
      users = [...users, ...response.data.organization.membersWithRole.nodes];
      const pageInfo = response.data.organization.membersWithRole.pageInfo;
      hasNextPage = pageInfo.hasNextPage;
      usedQuery = getQuery(QUERY_NAMES.FETCH_MORE_MEMBERS, {
        first: 100,
        after: pageInfo.endCursor,
      });
    } catch (error) {
      // TODO
    }
  } while (hasNextPage);
  console.log(`No of Users: ${users.length}`);
  return users;
}

/**
 * Binary search to count total events which lies after target date
 *
 * @param {*} events Array of events.
 * @param {*} l Left bound.
 * @param {*} r Right bound.
 */
const countHowManyLiesWithin = (events, l, r) => {
  if (l === r) {
    return l;
  }
  const mid = parseInt(l + (r - l) / 2);
  const midEventDate = new Date(events[mid].node.updatedAt);
  if (midEventDate.getTime() >= uptoDate.getTime()) {
    return countHowManyLiesWithin(events, mid + 1, r);
  }
  return countHowManyLiesWithin(events, l, mid);
};

init();
