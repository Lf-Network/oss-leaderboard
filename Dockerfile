FROM python:3.12-slim AS main

WORKDIR /app

COPY ["setup.py", "final_html_output.py", "multi_users_fetch.py", "main.py", "README.md", "./"]
COPY ["leaderboard", "./leaderboard"]
COPY ["assets", "./assets"]

RUN pip3 install -U -e .

CMD ["python3", "main.py"]
