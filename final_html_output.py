import os
import pandas as pd

def final_html_output(df: pd.DataFrame) -> str:
    """ Get final html output
    Args:
        df: dataframe object

    Returns:
        html string
    """    
    html_string = '''
    <html>
        <head><title>Opensource Leaderboard</title></head>
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <body class="container">
            <h1>OPENSOURCE LEADERBOARD</h1>
            {table}
        </body>
    </html>
    '''
    if not os.path.exists('build'):
        os.mkdir('build')
    with open('build/index.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(index=False)))
        f.close()
        
    