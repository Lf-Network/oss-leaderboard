import { QUERY_NAMES } from './constants';

const getQuery = (queryName, variables) => {
  switch (queryName) {
    case QUERY_NAMES.MEMBERS_WITH_ROLE: {
      return {
        variables: {
          first: 100
        },
        query:
          'query($first: Int!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}'
      };
    }
    case QUERY_NAMES.FETCH_MORE_MEMBERS: {
      return {
        variables: variables,
        query:
          'query ($first: Int!, $after: String!) {organization(login:leapfrogtechnology) {name, url, membersWithRole (first:$first, after:$after){totalCount, pageInfo {hasNextPage, endCursor}, nodes{login, name}}}}'
      };
    }
  }
};

export default getQuery;
