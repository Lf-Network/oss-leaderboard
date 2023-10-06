FROM python:3.11-slim AS main

COPY ["setup.py", "final_html_output.py", "multi_users_fetch.py", "main.py", "README.md", "./"]
COPY ["leaderboard", "./leaderboard"]

RUN pip install -U -e .

CMD ["python", "main.py"]
