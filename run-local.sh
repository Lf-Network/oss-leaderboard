#!/bin/bash
docker build --no-cache --target main -t leaderboard .
docker run --env-file .env --mount type=bind,src="$(pwd)",target=/app leaderboard
