import getQuery from '../query';
import { QUERY_NAMES } from '../constants';
import { fetchUsers } from '../..';

/**
 * Fetch user list of organization.
 *
 * @param {String} query
 * @param {Array} users
 * @returns
 */
export async function fetchOrganizationUsers(query, users = []) {
  let hasNextPage = false;
  let usedQuery = query;

  try {
    const response = await fetchUsers(usedQuery);

    users = [...users, ...response.data.organization.membersWithRole.nodes];

    const pageInfo = response.data.organization.membersWithRole.pageInfo;

    hasNextPage = pageInfo.hasNextPage;
    usedQuery = getQuery(QUERY_NAMES.FETCH_MORE_MEMBERS, {
      first: 100,
      after: pageInfo.endCursor,
    });
    if (hasNextPage) {
      return fetchOrganizationUsers(usedQuery, users);
    } else {
      return Promise.resolve(users);
    }
  } catch (error) {
    // TODO
  }

  return Promise.resolve(users);
}
