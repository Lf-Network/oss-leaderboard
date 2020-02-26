""" GraphQL Query to fetch data. """

query = """
query ossQuery($timedelta: DateTime!, $username: String!, $dataCount: Int!) {
  user(login: $username) {
    username:login
    contributionsCollection(from:$timedelta) {
      hasAnyContributions
      pullRequestReviewContributions(first: $dataCount) {
        totalCount
        pageInfo{
          hasNextPage
        }
        edges {
          cursor
          node {
            repository {
              id
              nameWithOwner
            }
            pullRequestReview {
              state
              createdAt
              lastEditedAt
              pullRequest {
                id
                title
                url
                state
                merged
                mergedBy {
                  login
                }
              }
            }
          }
        }
      }
      issueContributions(first: $dataCount) {
        totalCount
        pageInfo {
          hasNextPage
        }
        edges {
          cursor
          node {
            issue {
              reactions {
                totalCount
              }
              url
              comments {
                totalCount
              }
              closed
              createdAt
              state
              title
              updatedAt
            }
          }
        }
      }
      pullRequestContributions(first: $dataCount) {
        totalCount
        edges {
          node {
            pullRequest {
              author {
                login
              }
              closed
              closedAt
              merged
              mergedAt
              mergedBy {
                login
              }
              number
              state
              title
              updatedAt
            }
          }
        }
      }
      repositoryContributions(first: $dataCount) {
        totalCount
        edges {
          node {
            repository {
              id
              name
              createdAt
              isArchived
              isDisabled
              isFork
              isLocked
              isMirror
              isTemplate
              pushedAt
              updatedAt
              forkCount
              isFork
              stargazers(first: $dataCount) {
                totalCount
              }
            }
          }
        }
      }
    }
  }
}
"""
