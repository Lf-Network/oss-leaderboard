FROM laudio/pyodbc:1.0.33 AS main

WORKDIR /app

COPY ["setup.py", "README.md", "main.py", "./"]
COPY ["leaderboard", "./leaderboard"]

RUN pip install . 

CMD ["python", "main.py"]


# STAGE: test
# -----------
# Image used for running tests.FROM main AS test
FROM main AS test

RUN pip install .[dev]

COPY ["tests", "./"]

CMD pytest -vvv
