#!/usr/bin/env python3

import requests
import json
from math import ceil
from datetime import date

__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.1"

# --------------------------------------------------------------------------------------
# Request Script for querying Duspot Database - Active Listings
# https://portal.duspot.nl/
#
# Note: Retrieving using requests requires a Bearer Authorization token
# The current way to find your current Authorization token (it will expire) is to
# -> Login in to https://portal.duspot.nl  using Name/PW or  Microsoft
# -> F11 -or- Right-click in top menu bar -> Inspect
#    - (either way will pop up Inspection Pane in Browser)
# -> Submit actual filtered query to the db by some material
# -> From bottom window, select Network Tab and find Network request:
#    - status = 200 (successful)
#    - Method = post
#    - file   = getByFilter
#    - type   = json
# -> Selecting getByFilter should show a side menu with Headers
# -> Scroll down to Request Headers
#    - Find "Authorization" and replace the headers dictionary below
#    - In Firefox, hover over the question mark with the field and select copy! Otherwise
#      parts of the *large* bearer token may be omitted and the request will not work
#
# Note: Duspot does not allow filtering by material type. All materials can be fetched
# via pagination and then subsequently filtered (overall )
# --------------------------------------------------------------------------------------


def fetch_all_active_items(token):
    base_url = "https://api.duspot.nl/api/products"

    headers = {
        "Authorization": "Bearer {token}".format(token=token),
        "Content-Type": "application/json",
    }

    active_page = 1
    params = {"published": "true", "spot.active": "true", "page": active_page}

    first_response = None
    # Get the first page
    try:
        first_response = requests.request(
            "GET", base_url, headers=headers, params=params
        )
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    all_records = []
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    if first_response is not None:
        try:
            page_data = first_response.json()
            num_records = page_data["hydra:totalItems"]
            page_size = len(page_data["hydra:member"])
            num_pages = ceil(num_records / page_size)
            for i in range(1, num_pages + 1):
                params["page"] = i
                next_response = requests.request(
                    "GET", base_url, headers=headers, params=params
                )
                page_data = next_response.json()
                all_records.extend(page_data["hydra:member"])
            with open(f"{formatted_date}_duspot_data.json", "w") as fh:
                json.dump(all_records, fh, indent=2)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    token = "YOURTOKENHERE"
    fetch_all_active_items(token)