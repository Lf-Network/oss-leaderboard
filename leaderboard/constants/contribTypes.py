scores = {
    "T1": {
        "description": "PR Opened",
        "subtypes": {
            "T1S1": {
                "description": "PR opened in a repo not owned by the user",
                "weight": 1
            },
            "T1S2": {
                "description": "PR opened in a repo owned by the user",
                "weight": 0.6
            }
        }
    },
    "T2": {
        "description": "PR Reviewed",
        "subtypes": {
            "T2S1": {
                "description": "PR reviewed that is opened by the user and contributed in the repo owned by the user",
                "weight": 0.5
            },
            "T2S2": {
                "description": "PR reviewed that is not opened by the user and contributed in the repo owned by the user",
                "weight": 0.5
            },
            "T2S3": {
                "description": "PR reviewed that is opened by the user and contributed in the repo not owned by the user",
                "weight": 0.5
            },
            "T2S4": {
                "description": "PR reviewed that is not opened by the user and contributed in the repo not owned by the user",
                "weight": 0.5
            }
        }
    },
    "T3": {
        "description": "Issue",
        "subtypes": {
            "T3S1": {
                "description": "Issue created in a repo owned by the user",
                "weight": 0.3
            },
            "T3S2": {
                "description": "Issue created in a repo not owned by the user",
                "weight": 0.3
            }
        }
    },
    "T4": {
        "description": "PR/Issue Comments",
        "subtypes": {
            "T4S1": {
                "description": "Commented on an issue created by user in the repo owned by the user",
                "weight": 0.1
            },
            "T4S2": {
                "description": "Commented on an issue not created by user in the repo owned by the user",
                "weight": 0.1
            },
            "T4S3": {
                "description": "Commented on an issue created by user in the repo not owned by the user",
                "weight": 0.1
            },
            "T4S4": {
                "description": "Commented on an issue not created by user in the repo not owned by the user",
                "weight": 0.1
            }
        }
    },
    "T5": {
        "description": "Repo Created",
        "subtypes": {
            "T5S1": {
                "description": "Repo created by the user",
                "weight": 0
            }
        }
    }
}

