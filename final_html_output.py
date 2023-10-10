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
                        "User Name": format_username,
                    },
                )
            )
        )


def format_username(u: str):
    """Format username with avatar image and clickable link to redirect to user's profile"""

    link_html = '<a target="_blank" rel="noopener noreferrer" href="https://github.com/{}">{}</a>'
    img_html = '<img src="https://github.com/{}.png?size=20" alt="@{}" />'

    link_image = link_html.format(u, img_html.format(u, u))
    link_username = link_html.format(u, u)

    return f'<div class="username">{link_image} {link_username}</div>'
