import fetch from 'node-fetch';

import 'dotenv/config';

import getQuery from './src/query';
import { QUERY_NAMES, DAYS_TO_CONSIDER } from './src/constants';

let usersList = [];

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
    await fetchData(query);
  } catch (error) {
    // TODO
  }

  usersList.forEach(async user => {
    const pullRequestQuery = getQuery(QUERY_NAMES.FETCH_USER_EVENTS, {
      user: user.login,
      pullRequestsAfter: null
    });
    const totalPullRequest = await fetchPullRequest(pullRequestQuery);
    console.log(`${user.name || user.login}: ${totalPullRequest}`);
  });
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
  const pullRequests = response.data.user.pullRequests.edges;
  const pageInfo = response.data.user.pullRequests.pageInfo;
  if (pullRequests.length <= 0) {
    return 0;
  }
  const lastPullRequestDate = new Date(
    pullRequests[pullRequests.length - 1].node.updatedAt
  );

  let totalCounts = 0;

  if (lastPullRequestDate.getTime() >= uptoDate.getTime()) {
    totalCounts += pullRequests.length;
    if (pageInfo.hasNextPage) {
      query.variables.pullRequestsAfter.pageInfo.endCursor;
      totalCounts += fetchPullRequest(query);
    }
  }
  totalCounts += countHowManyLiesWithin(
    pullRequests,
    0,
    pullRequests.length - 1
  );

  return totalCounts;
}

async function fetchData(query) {
  const response = await fetchUsers(query);
  usersList = [
    ...usersList,
    ...response.data.organization.membersWithRole.nodes
  ];
  const pageInfo = response.data.organization.membersWithRole.pageInfo;
  if (pageInfo.hasNextPage) {
    const query = getQuery('fetchMoreMembers', {
      first: 100,
      after: pageInfo.endCursor
    });

    fetchData(query);
  }
  console.log(usersList.length);
}

init();
