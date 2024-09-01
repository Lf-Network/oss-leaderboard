import os
import pandas as pd


def final_html_output(df: pd.DataFrame) -> str:
    """
    Get final html output

    This function reads an HTML file, replaces a placeholder with a table generated from a pandas DataFrame,
    and writes the resulting HTML to a file.

    Args:
        df: A pandas DataFrame containing the data to be displayed in the table.

    Returns:
        A string containing the final HTML output.
    """
    html_string = read_html_file("./assets/index.html")
    output_file_path = create_output_file_path("build/index.html")

    with open(output_file_path, "w") as f:
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

    return read_file(output_file_path)


def read_html_file(file_path: str) -> str:
    """
    Read HTML file

    Args:
        file_path (str): The path to the HTML file.

    Returns:
        str: The contents of the HTML file.
    """
    with open(file_path) as file:
        return file.read()


def create_output_file_path(file_path: str) -> str:
    """
    Create output file path

    Args:
        file_path (str): The path to the output file.

    Returns:
        str: The path to the output file.
    """
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    return file_path


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
