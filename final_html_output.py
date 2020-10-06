import os
import pandas as pd


def final_html_output(df: pd.DataFrame) -> str:
    """Get final html output
    Args:
        df: dataframe object

    Returns:
        html string
    """
    with open("./assets/index.html") as file:
        html_string = file.read()

    if not os.path.exists("build"):
        os.mkdir("build")
        
    with open("build/index.html", "w") as f:
        f.write(html_string.format(table=df.to_html(index=False)))
