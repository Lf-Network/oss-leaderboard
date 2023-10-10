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
        f.write(
            html_string.format(
                table=df.to_html(
                    index=False,
                    escape=False,
                    formatters={
                        "User Name": link_username,
                    },
                )
            )
        )


def link_username(u: str):
    return f'<a target="_blank" rel="noopener noreferrer" href="https://github.com/{u}">{u}</a>'


def add_user_avatar(df: pd.DataFrame) -> pd.DataFrame:
    image_tag = lambda u: f'<img src="https://github.com/{u}.png?size=20" alt="@{u}" />'
    avatarUrls = df["User Name"].apply(image_tag)
    df.insert(0, "Avatar Url", avatarUrls)

    return df
