import pandas as pd

from typing import Any


def final_html_output(df: pd.DataFrame) -> str:
    """
    Get final html output

    This function reads an HTML file, replaces a placeholder with a table generated from a pandas DataFrame.

    Args:
        df: A pandas DataFrame containing the data to be displayed in the table.

    Returns:
        A string containing the final HTML output.
    """
    html_string = read_file("./assets/index.html")

    html_string = html_string.format(
                table=df.to_html(
                    index=False,
                    escape=False,
                    formatters={
                        "User Name": format_username,
                    },
                )
            )

    return html_string


def read_file(file_path: str) -> str:
    """
    Read file

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file.
    """
    with open(file_path) as file:
        return file.read()


def format_username(username: Any) -> str:
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
