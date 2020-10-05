import os
import pandas as pd


def final_html_output(df: pd.DataFrame) -> str:
    """Get final html output
    Args:
        df: dataframe object

    Returns:
        html string
    """
    html_string = """
  <html>
    <head>
      <title>Opensource Leaderboard Leapforg</title>
    </head>
    <link rel="stylesheet" type="text/css" href="../assets/style.css" />
    <body>
      <div class="leaderboard">
        <img
        class="leaderboard__img"
        src="../assets/LF_Opensource.svg"
        alt="Leapfrog Opensource Logo"
        />
        <h1>Frogtoberfest Leaderboard</h1>
        <div class="leaderboard__table">
          {table}
          </section>
        </div>
    </body>
  </html>

    """
    if not os.path.exists("build"):
        os.mkdir("build")
    with open("build/index.html", "w") as f:
        f.write(html_string.format(table=df.to_html(index=False)))
        f.close()
