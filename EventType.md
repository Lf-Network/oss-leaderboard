# Docs

Documentation for event types provided by GraphQL Github API v4.

## List all types defined in the schema and get details about each:

```
query {
  __schema {
    types {
      name
      kind
      description
      fields {
        name
      }
    }
  }
}
```

### Get details about User type.

```
query{
  __type(name: "User") {
    name
    kind
    description
    fields {
      name,
      description,
      args{
        name,
        description
      }
      type {
        fields {
          name,
          description
        }
      }
    }
  }
}
```

### Get details about user with name JohnDoe.

```
query{
  user(login:"JohnDoe"){
    bio,
    avatarUrl,
    company,
    email,
    issueComments(first:5){
      edges{
        node{
          body,
          url
        }
      }
    },
    commitComments(first:5){
      edges{
        node{
          url
        }
      }
    }
    ...
  }
}
```

### Issue event

Triggered when an issue is opened, edited, deleted, transferred, pinned, unpinned, closed, reopened, assigned, unassigned, labeled, unlabeled, locked, unlocked, milestoned, or demilestoned.

Below query fetch `first 5` item with fields `body`

```
issues(first:5){
  edges{
    node{
      body
    }
  }
}
```

## Comments on issue event.

Triggered when an issue comment is created, edited, or deleted.

Below query fetch `first 5` item with fields `body and url`

```
issueComments(first:5){
  edges{
    node{
      body,
      url
    }
  }
}
```

## Comments on commit event.

Triggered when a commit comment is created.

Below query fetch `first 5` item with fields `url`

```
commitComments(first:5){
  edges{
    node{
      url
    }
  }
}
```

### Pull Request event

Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened, edited, closed, reopened, synchronize, ready_for_review, locked, unlocked or when a pull request review is requested or removed.

Below query fetch `first 5` item with fields `body`

```
pullRequests(first:20){
  edges{
    node{
      body
    }
  }
}
```
