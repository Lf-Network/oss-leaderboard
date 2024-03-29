# score weights for each of the sub types
T1S1 = 1  # score for 'PR opened in a repo not owned by the user'
T1S2 = 0.6  # score for 'PR opened in a repo owned by the user'
T2S1 = 0.5  # score for 'PR reviewed that is opened by the user and contributed in the repo owned by the user'
T2S2 = 0.5  # score for 'PR reviewed that is not opened by the user and contributed in the repo owned by the user'
T2S3 = 0.5  # score for 'PR reviewed that is opened by the user and contributed in the repo not owned by the user'
T2S4 = 0.5  # score for 'PR reviewed that is not opened by the user and contributed in the repo not owned by the user'
T3S1 = 0.3  # score for 'Issue created in a repo owned by the user'
T3S2 = 0.3  # score for 'Issue created in a repo not owned by the user'
T4S1 = 0.1  # score for 'Commented on an issue created by user in the repo owned by the user'
T4S2 = 0.1  # score for 'Commented on an issue not created by user in the repo owned by the user'
T4S3 = 0.1  # score for 'Commented on an issue created by user in the repo not owned by the user'
T4S4 = 0.1  # score for 'Commented on an issue not created by user in the repo not owned by the user'
T5S1 = 0  # score for 'Repo created by the user'
