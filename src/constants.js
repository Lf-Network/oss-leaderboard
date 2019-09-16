export const QUERY_NAMES = {
  MEMBERS_WITH_ROLE: 'membersWithRole',
  FETCH_MORE_MEMBERS: 'fetchMoreMembers',
  FETCH_USER_EVENTS: 'fetchUserEvents',
  USER_EVENTS_QUERY: 'userEventsQuery',
};

export const DAYS_TO_CONSIDER = 7;

export const eventTypes = {
  PULL_REQUESTS: 'pullRequests',
  ISSUES: 'issues',
};

export const STATES = {
  OPEN: 'OPEN',
  CLOSED: 'CLOSED',
};

export const eventQueryGenerator = (events, user) => {
  const variables = {};
  let query =
    'query($user:String!,:variable_declaration){user(login:$user){login,repositoriesContributedTo{totalCount},:event_type}}';
  let variableDeclaration = '';
  let eventType = '';

  events.forEach(event => {
    Object.values(event.variables).forEach(variable => {
      variables[variable.name] = variable.value;
      variableDeclaration += '$' + variable.name + ':' + variable.type + ',';
    });
    eventType += event.query + ',';
  });

  query = query.replace(':variable_declaration', variableDeclaration);
  query = query.replace(':event_type', eventType);

  return {
    variables: Object.assign({}, { user }, variables),
    query,
  };
};

export const events = {
  pullRequests: {
    variables: {
      after: {
        name: 'pullRequestAfter',
        type: 'String',
        value: null,
        eventName: 'pullRequests',
      },
    },
    query:
      'pullRequests(first:100,states:[OPEN,MERGED],after: $pullRequestAfter,orderBy: {field: UPDATED_AT, direction: DESC}){pageInfo {hasNextPage, endCursor},edges{node{updatedAt,state}}}',
  },
  issues: {
    variables: {
      after: {
        name: 'issueAfter',
        type: 'String',
        value: null,
        eventName: 'issues',
      },
    },
    query:
      'issues(first:100,after: $issueAfter,states:OPEN,orderBy: {field: UPDATED_AT, direction: DESC}){pageInfo {hasNextPage, endCursor},edges{node{updatedAt,state}}}',
  },
  issueComments: {
    variables: {
      before: {
        name: 'issueCommentBefore',
        type: 'String',
        value: null,
        eventName: 'issueComments',
      },
    },
    query:
      'issueComments(last:100,before: $issueCommentBefore){pageInfo {hasNextPage, endCursor},edges{node{updatedAt}}}',
  },
};

export const fileName = 'oss-leaderboard.md';

export const keys = {
  name: 'Name',
  pullRequestsMerged: 'PR Merged',
  pullRequestsOpen: 'PR Opened',
  issueOpen: 'Issue Opened',
  issueComments: 'Issue Comments',
  repositoriesContributed: 'Repos Contributed',
};
