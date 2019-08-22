// const fetch = require('node-fetch');
import fetch from 'node-fetch';

import 'dotenv/config';

import getQuery from './src/query';

let usersList = [];

async function fetchUsers(query) {
  var accessToken = process.env.ACCESS_TOKEN;
  try {
    const res = await fetch('https://api.github.com/graphql', {
      method: 'POST',
      body: JSON.stringify(query),
      headers: {
        authorization: `token ${accessToken}`
      }
    });
    return res.json();
  } catch (error) {}
}

function init() {
  const query = getQuery('membersWithRole');
  fetchData(query);
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
