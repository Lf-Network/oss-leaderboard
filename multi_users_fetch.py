""" Fetch contributions for multiple users """

import json
import pandas as pd
from typing import Dict
from copy import deepcopy

from leaderboard.queries.query import query
from leaderboard.fetch_data import execute_query
from leaderboard.utils.formatter import convert_to_intermediate_table


def fetch_contributions_for_multi_users(
    user_list: list, variables: Dict
) -> pd.DataFrame:

    list = []
    for userName in user_list:
        variables["username"] = userName

        page_info_T1 = {"hasNextPage": True, "endCursor": None}

        page_info_T2 = {"hasNextPage": True, "endCursor": None}

        page_info_T3 = {"hasNextPage": True, "endCursor": None}

        page_info_T4 = {"hasPreviousPage": True, "startCursor": None}

        page_info_T5 = {"hasNextPage": True, "endCursor": None}

        while True:
            params = deepcopy(variables)

            params["pullReqCursor"] = page_info_T1["endCursor"]

            params["pullreqreviewcursor"] = page_info_T2["endCursor"]

            params["issueCursor"] = page_info_T3["endCursor"]

            params["issueCommentsCursor"] = page_info_T4["startCursor"]

            params["repoCursor"] = page_info_T5["endCursor"]

            if page_info_T4["hasPreviousPage"]:
                params["issueCommentDataCount"] = variables["dataCount"]
            else:
                params["issueCommentDataCount"] = 0

            result = execute_query(query, params)

            flat_data = convert_to_intermediate_table(
                json.dumps(result.json(), indent=4), variables["timedelta"]
            )

            list.append(flat_data["intermediate_table"])

            if page_info_T1["hasNextPage"]:
                page_info_T1 = flat_data["page_info"]["page_info_T1"]

            if page_info_T2["hasNextPage"]:
                page_info_T2 = flat_data["page_info"]["page_info_T2"]

            if page_info_T3["hasNextPage"]:
                page_info_T3 = flat_data["page_info"]["page_info_T3"]

            if page_info_T4["hasPreviousPage"]:
                page_info_T4 = flat_data["page_info"]["page_info_T4"]

            if page_info_T5["hasNextPage"]:
                page_info_T5 = flat_data["page_info"]["page_info_T5"]

            if (
                not page_info_T1["hasNextPage"]
                and not page_info_T2["hasNextPage"]
                and not page_info_T3["hasNextPage"]
                and not page_info_T4["hasPreviousPage"]
                and not page_info_T5["hasNextPage"]
            ):
                break

    combined = pd.concat(list)

    return combined
