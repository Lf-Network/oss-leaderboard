test_query = """
{{
  user(login: "{username}") {{
    followers(last: 5) {{
      edges {{
        node {{
          name
        }}
      }}
    }}
  }}
}}
"""
