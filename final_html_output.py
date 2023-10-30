import os
import pandas as pd

from leaderboard.constants import contribTypes


def final_html_output(df: pd.DataFrame) -> str:
    """Get final html output

    This function reads an HTML file, replaces a placeholder with a table generated from a pandas DataFrame,
    and writes the resulting HTML to a file.

    Args:
        df: A pandas DataFrame containing the data to be displayed in the table.

    Returns:
        A string containing the final HTML output.
    """
    with open("./assets/index.html") as file:
        html_string = file.read()

    if not os.path.exists("build"):
        os.mkdir("build")

    with open("build/index.html", "w") as f:
        f.write(
            html_string.format(
                table=df.apply(format_row, axis=1).to_html(
                    index=False,
                    escape=False,
                )
            )
        )


def format_row(row: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the data in the given DataFrame row.

    Args:
        row (pd.DataFrame): A DataFrame representing a row of data.

    Returns:
        pd.DataFrame: The formatted DataFrame row.
    """

    username = row["User Name"]
    row["User Name"] = format_username(username)
    row[contribTypes.T1] = format_open_pr(username, row[contribTypes.T1])

    return row


def format_username(username: str) -> str:
    """
    Format username with avatar image and clickable link to redirect to user's profile.

    Args:
        username (str): The username to format.

    Returns:
        str: The formatted username HTML string.
    """

    link_html = '<a target="_blank" rel="noopener noreferrer" href="https://github.com/{}">{}</a>'
    img_html = '<img src="https://github.com/{}.png?size=20" width="20" height="20" alt="@{}" />'

    link_image = link_html.format(username, img_html.format(username, username))
    link_username = link_html.format(username, username)

    return f'<div class="username">{link_image} {link_username}</div>'


def format_open_pr(username: str, value: str) -> str:
    """
    Formats an pr opened value to link to frogtoberfest checker.

    Args:
        username (str): The username associated with the pull request.
        value (str): The value to be displayed as the link text.

    Returns:
        str: The formatted HTML code with the link.
    """

    checker_link_html = '<a target="_blank" rel="noopener noreferrer" href="https://frogtoberfest.lftechnology.com/user/{}">{}</a>'
    link_checker = checker_link_html.format(username, value)

    return link_checker
