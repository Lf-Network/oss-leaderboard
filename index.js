import fetch from 'node-fetch';

import 'dotenv/config';

import getQuery from './src/query';
import {
  DAYS_TO_CONSIDER,
  eventQueryGenerator,
  events,
  fileName,
  QUERY_NAMES,
  weight,
} from './src/constants';

import { getKeys, getValues } from './src/util/key-value';
import { generateMarkdown } from './src/service/generate-markdown';
import { createMarkdown } from './src/service/create-markdown';
import { fetchUserEventsFromTo } from './src/service/fetchUserEvents';
import { sort } from './src/util/sort';

const uptoDate = new Date();
uptoDate.setDate(uptoDate.getDate() - DAYS_TO_CONSIDER);

export async function fetchUsers(query) {
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
    const usersList = await fetchData(query).catch(err => {
      throw err;
    });
    const usersDetails = {};

    await Promise.all(
      usersList.map(async user => {
        const eventDetails = await fetchUserEventsFromTo(
          eventQueryGenerator(Object.values(events), user.login),
          new Date(),
          uptoDate,
        );
        usersDetails[user.name || user.login] = eventDetails;
      }),
    ).then(() => {
      let leaderBoard = Object.keys(usersDetails).sort((a, b) => {
        return usersDetails[a].userEventList.length >
          usersDetails[b].userEventList.length
          ? -1
          : usersDetails[a].userEventList.length ===
            usersDetails[b].userEventList.length
          ? 0
          : 1;
      });
      leaderBoard = leaderBoard.map(user => {
        const contribution = {};

        Object.keys(usersDetails[user]).forEach(key => {
          const userContribution = usersDetails[user][key];
          if (typeof userContribution === 'number') {
            contribution[key] = userContribution;
          } else if (userContribution.length > 0) {
            userContribution.map(event => {
              const eventKey = Object.keys(event)[0];
              const state = event[eventKey].state || '';
              const generatedKey =
                eventKey + state.charAt(0) + state.substr(1).toLowerCase();
              if (!contribution[generatedKey]) {
                contribution[generatedKey] = 0;
              }
              contribution[generatedKey]++;
            });
          }
        });
        return Object.assign(
          {},
          {
            name: user,
          },
          contribution,
        );
      });

      const keys = getKeys(leaderBoard);
      leaderBoard = leaderBoard.slice(0, 20).reduce((acc, item) => {
        const temp = Object.assign({}, item);
        if (Object.keys(temp).length <= 2) {
          return acc;
        }
        keys.forEach(key => {
          temp[key] = temp[key] || 0;
        });
        acc.push(temp);
        return acc;
      }, []);
      const sortedLeaderBoard = sort(addScore(leaderBoard), 'score', 'desc');
      getValues(sortedLeaderBoard, keys).then(res => {
        generateMarkdown(res, keys).then(contributionData => {
          createMarkdown(fileName, contributionData);
        });
      });
    });
  } catch (error) {
    console.log('Error user fetching', error);
  }
}

function calculateScore(e) {
  return (e.score =
    e.pullRequestsMerged * weight.pullRequestsMerged +
    e.pullRequestsOpen * weight.pullRequestsOpen +
    e.issueComments * weight.issueComments +
    e.issuesOpen * weight.issuesOpen);
}

function addScore(leaderBoard) {
  leaderBoard.forEach(e => {
    e[leaderBoard.indexOf(e)] = calculateScore(e);
  });
  return leaderBoard;
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

init();
