import requests


class graphQL:

    headers = {"Authorization": "token <token_here>"}

    """docstring for graphQL"""

    def __init__(self):
        super(graphQL, self).__init__()

    def run_query(
        self, query, variables
    ):  # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=self.headers,
        )
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(
                "Query failed to run by returning code of {}. {}".format(
                    request.status_code, query
                )
            )

    def getClosedIssuesActors(self):
        listOfNames = []
        query = """
			query($owner: String!, $name: String!) { 
				repository(owner: $owner, name: $name){
				  issues(states: CLOSED, first:10){
					edges{
					  node{
						... on Issue{
						  timeline(last: 100){
							edges{
							  node{
								__typename
								... on ClosedEvent{
								  actor{
									login
								  }
								}
							  }
							}
						  }
						}
					  }
					}
				  }
				}
			}"""

        variables = {"owner": "tatmush", "name": "Saturday-THORN-Dev-Rank"}

        result = self.run_query(query, variables)  # execute query
        print(result)
