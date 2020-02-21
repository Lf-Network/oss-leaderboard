FROM laudio/pyodbc:1.0.32 AS main

WORKDIR /app

COPY ["setup.py", "README.md", "main.py", "./"]
COPY ["leaderboard", "./leaderboard"]

RUN pip install . 

CMD ["python", "main.py"]
