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

### Acquiring Access Token

 To get the Access Token follow the link below.

```
[](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)
```


### Github Version 4 API Endpoint

 Github APIv4 uses GraphQL. It provides a single endpoint. You need to send a POST request with a json query object in the request body.

```
endpoint:  https://api.github.com/graphql
```





