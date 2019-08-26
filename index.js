'use strict';

import fetch from 'node-fetch';

import 'dotenv/config';

import getQuery from './src/query';
import { QUERY_NAMES, DAYS_TO_CONSIDER, eventTypes } from './src/constants';

let uptoDate = new Date();
uptoDate.setDate(uptoDate.getDate() - DAYS_TO_CONSIDER);

async function fetchUsers(query) {
  let accessToken = process.env.ACCESS_TOKEN;
  try {
    const res = await fetch('https://api.github.com/graphql', {
      method: 'POST',
      body: JSON.stringify(query),
      headers: {
        authorization: `token ${accessToken}`
      }
    });
    return res.json();
  } catch (error) {
    // TODO
  }
}

async function init() {
  const query = getQuery(QUERY_NAMES.MEMBERS_WITH_ROLE);
  try {
    const usersList = await fetchData(query);
    usersList.forEach(async user => {
      const pullRequestQuery = getQuery(QUERY_NAMES.FETCH_USER_EVENTS, {
        user: user.login,
        pullRequestsAfter: null
      });
      const totalPullRequest = await fetchPullRequest(pullRequestQuery);
      console.log(`${user.name || user.login}: ${totalPullRequest}`);
    });
  } catch (error) {
    // TODO
  }
}

const countHowManyLiesWithin = (pullRequests, l, r) => {
  if (l === r) {
    return l;
  }
  const mid = parseInt(l + (r - l) / 2);
  const pullRequestDate = new Date(pullRequests[mid].node.updatedAt);
  if (pullRequestDate.getTime() >= uptoDate.getTime()) {
    return countHowManyLiesWithin(pullRequests, mid + 1, r);
  }
  return countHowManyLiesWithin(pullRequests, l, mid);
};

async function fetchPullRequest(query) {
  const response = await fetchUsers(query);
  const queryVariables = {};
  let totalCounter = {};

  let needAnotherFetch = false;
  Object.values(eventTypes).forEach(event => {
    const eventResult = response.data.user[event];

    totalCounter[event] = 0;
    queryVariables[event] = eventResult;

    if (eventResult.edges.length <= 0) {
      return;
    }

    const lastDate = new Date(
      eventResult.edges[eventResult.edges.length - 1].node.updatedAt
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
        eventResult.edges.length - 1
      );
    }
  });

  if (needAnotherFetch) {
    Object.values(eventTypes).forEach(event => {
      query.variables = Object.assign({}, query.variables, {
        [`${event}After`]: queryVariables[event].pageInfo.endCursor
      });
    });
    let currentCountstotalCounts = await fetchPullRequest(query);

    Object.values(eventTypes).forEach(event => {
      totalCounter[event] += currentCountstotalCounts[event];
    });
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
      usedQuery = getQuery('fetchMoreMembers', {
        first: 100,
        after: pageInfo.endCursor
      });
    } catch (error) {
      // TODO
    }
  } while (hasNextPage);
  console.log(`No of Users: ${users.length}`);
  return users;
}

init();
