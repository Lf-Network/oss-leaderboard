# Docs

Documentation for how the leaderboard works.

## GitHub API docs


### Organization members

`GET` all members of an organization:

```
endpoint: https://api.github.com/orgs/{org_name}/members

authorization: yes
```

### Activities

`GET` activities of an user:

```
endpoint: https://api.github.com/users/{username}/events
```

### Acquiring access Token
 to get the access token follow the steps below.
1. Go to the github setting page
2. select Developer settings
3. select Personal access token
4. click on generate new token
5. write note and select the scopes for which you need access
6. click Generate token button at the bottom of the page

```
[Tutorial to generate Access Token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)
```


### Github Version 4 API Endpoint
 Github APIv4 uses GraphQL. it provides a single endpoint. You need to send a POST request with a json query object in the request body.

```
endpoint:  https://api.github.com/graphql
```


### GraphQL Operations
Github's GraphQL API allows two types of Operation. Query and Mutation. Query is used to fetch data from the API. It is equivalent to 'GET' request in REST API. another allowed operation is Mutation. it is similar to 'POST/PATCH/DELETE' method operations in REST API. 

since we only need to fetch data from the API. we'll be using queries only. 

Queries are structured like this:

```
query {
  JSON objects to return
}
```


