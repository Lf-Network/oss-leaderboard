import { QUERY_NAMES } from './constants';

const getQuery = (queryName, variables) => {
  switch (queryName) {
    case QUERY_NAMES.MEMBERS_WITH_ROLE: {
      return {
        variables: {
          first: 100,
        },
        query:
          'query($first: Int!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}',
      };
    }
    case QUERY_NAMES.FETCH_MORE_MEMBERS: {
      return {
        variables: variables,
        query:
          'query ($first: Int!, $after: String!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first, after:$after){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}',
      };
    }
    case QUERY_NAMES.FETCH_USER_EVENTS: {
      return {
        variables: variables,
        query:
          'query($user:String!,$pullRequestsAfter:String,$issuesAfter:String,$issueState:[IssueState!],$pullRequestState:[PullRequestState!]){user(login:$user){email,pullRequests(first:100,after: $pullRequestsAfter,states:$pullRequestState,orderBy: {field: UPDATED_AT, direction: DESC}){pageInfo {hasNextPage, endCursor},edges{node{title,body,updatedAt}}},issues(first:100,after: $issuesAfter,states:$issueState,orderBy: {field: UPDATED_AT, direction: DESC}){pageInfo {hasNextPage, endCursor},edges{node{title,body,updatedAt}}}}}',
      };
    }
  }
};

export default getQuery;
