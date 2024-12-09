import requests
import json
import os

__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.1"

# --------------------------------------------------------------------------------------
# Azure Request Script for querying Matching Materials Database by Material Category
# www.matchingmaterials.com
#
# Note: Retrieving using requests requires a Bearer Authorization token
# The current way to find your current Authorization token (it will expire) is to
# -> Login in to matchingmaterials.com using Microsoft
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
# There *should* be a way to automatically get a token from Microsoft
# *without* this browser interaction
# --------------------------------------------------------------------------------------


url = "https://tradingrawmaterial.azurewebsites.net/api/buildingmaterialrequest/getByFilter"

material_categories = {
    "Hout": "a5324d42-9b67-479c-8c50-1b69d252d578",
    "Kalk en cement, bindmiddelen, mortels": "18b17613-50a2-43cd-9d92-d6109582d4c3",
    "Metaal": "98b6445e-d575-432b-8e0a-03b8d7967e3e",
    "Glas": "fcef02d6-b3a5-4c34-ae93-017b59d8e09d",
    "Kunststoffen, rubbers": "3db93d81-1898-496c-aea9-f28085ab5ff6",
    "Anorganische materialen": "8dc9b54a-7949-4abc-abf5-bd26ac13a19a",
    "Bevestigingsmiddelen, voegvullingen": "a0daff86-f4bd-495d-b326-1e0f9f7c0e9f",
}

payload = json.dumps(
    {
        "offers": True,
        "questions": True,
        "tender": True,
        "execution": True,
        "production": True,
        "private": True,
        "onlyPublic": False,
        "ownOrganization": False,
        "organizationId": "",
        "organizationName": "",
        "productClassificationId": "",
        "subTypeId": "",
        "materialId": "",
    }
)

token = "YOURACTIVETOKENHERE"
headers = {
    "Authorization": "Bearer {token}".format(token=token),
    "Content-Type": "application/json",
}


response = requests.request("POST", url, headers=headers, data=payload)


# Currently fetches all materials
# To fetch specific material, sub in relevant material category hash into payload.materialId
def response_to_json(response):
    with open("matching_materials.json", "w") as fh:
        response = response.json()
        json.dump(response, fh, indent=4)


response_to_json(response)
