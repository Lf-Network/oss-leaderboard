""" GraphQL Query to fetch data. """

query = """
query ossQuery($timedelta: DateTime!, $username: String!, $dataCount: Int!) {
  user(login: $username) {
    username: login
    id
    contributionsCollection(from: $timedelta) {
      hasAnyContributions
      pullRequestReviewContributions(first: $dataCount) {
        totalCount
        pageInfo {
          hasNextPage
        }
        edges {
          cursor
          node {
            repository {
              id
              name
              owner {
                id
                login
              }
            }
            pullRequestReview {
              ReviewState: state
              pullRequest {
                id
                author {
                  login
                  ... on User {
                    id
                  }
                }
                url
                state
                merged
                mergedBy {
                  login
                }
              }
              reactions {
                totalCount
              }
              createdAt
              updatedAt
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
              repository {
                id
                owner {
                  id
                }
              }
              reactions {
                totalCount
              }
              labels(first: $dataCount) {
                edges {
                  node {
                    name
                  }
                }
              }
              url
              comments {
                totalCount
              }
              state
              closed
              createdAt
              updatedAt
            }
          }
        }
      }
      pullRequestContributions(first: $dataCount) {
        totalCount
        pageInfo {
          hasNextPage
        }
        edges {
          node {
            pullRequest {
              repository {
                id
                owner {
                  id
                }
              }
              state
              title
              closed
              merged
              mergedAt
              mergedBy {
                login
                ... on User {
                  id
                }
              }
              labels(first: $dataCount) {
                edges {
                  node {
                    name
                  }
                }
              }
              commits {
                totalCount
              }
              createdAt
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
              isFork
              parent {
                id
                owner {
                  id
                  login
                }
              }
              isTemplate
              isFork
              isArchived
              isDisabled
              forkCount
              stargazers {
                totalCount
              }
              createdAt
              updatedAt
            }
          }
        }
      }
    }
  }
}
"""
