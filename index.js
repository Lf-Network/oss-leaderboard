// import { graphql, buildSchema } from 'graphql';
// import fetch from 'node-fetch';
const fetch = require('node-fetch');

var membersWithRoleQuery = {
  variables: {
    first: 100
  },
  query:
    'query($first: Int!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}'
};

var memberStatuses = {
  variables: {
    first: 100
  },
  query:
    'query {organization(login:leapfrogtechnology) {name, url, memberStatuses (first:100) {totalCount,nodes{user{login}}}}}'
};

function getQuery(after) {
  return {
    variables: {
      first: 100,
      after: after
    },
    query:
      'query ($first: Int!, $after: String!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first, after:$after){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}'
  };
}

let usersList = [];

async function fetchUsers(query) {
  var accessToken = '2966f6db8b2b2f652588d61ab827948d625bf94b';

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
    console.log(error);
  }
}

function init() {
  fetchData(membersWithRoleQuery);
}

async function fetchData(query) {
  const response = await fetchUsers(query);
  usersList = [
    ...usersList,
    ...response.data.organization.membersWithRole.nodes
  ];
  const pageInfo = response.data.organization.membersWithRole.pageInfo;
  console.log(pageInfo);
  if (pageInfo.hasNextPage) {
    const query = getQuery(pageInfo.endCursor);

    fetchData(query);
  }
  console.log(usersList.length);
}

init();
