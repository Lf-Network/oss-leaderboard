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

# Acquiring access Token
 to get the access token follow the steps below.
1. Go to the github setting page
2. select Developer settings
3. select Personal access token
4. click on generate new token
5. write the note and select the scopes for which you need access
6. click Generate token button at the bottom of the page


