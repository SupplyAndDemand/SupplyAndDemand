import requests
import json
import msal
import os
from dotenv import load_dotenv

__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.2"

load_dotenv()

# Microsoft Azure configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

API_URL = "https://tradingrawmaterial.azurewebsites.net/api/buildingmaterialrequest/getByFilter"

material_categories = {
    "Hout": "a5324d42-9b67-479c-8c50-1b69d252d578",
    "Kalk en cement, bindmiddelen, mortels": "18b17613-50a2-43cd-9d92-d6109582d4c3",
    "Metaal": "98b6445e-d575-432b-8e0a-03b8d7967e3e",
    "Glas": "fcef02d6-b3a5-4c34-ae93-017b59d8e09d",
    "Kunststoffen, rubbers": "3db93d81-1898-496c-aea9-f28085ab5ff6",
    "Anorganische materialen": "8dc9b54a-7949-4abc-abf5-bd26ac13a19a",
    "Bevestigingsmiddelen, voegvullingen": "a0daff86-f4bd-495d-b326-1e0f9f7c0e9f",
}


def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_silent(SCOPE, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error: {result.get('error')}")
        print(f"Error description: {result.get('error_description')}")
        return None


def make_api_request(access_token, material_id=None):
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
            "materialId": material_id or "",
        }
    )

    headers = {
        "Authorization": "Bearer {token}".format(token=access_token),
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response


def response_to_json(response):
    with open("matching_materials.json", "w") as fh:
        json.dump(response, fh, indent=4)


def main():
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token.")
        return

    response = make_api_request(access_token)  # sub in material category if desired

    if response.status_code == 200:
        response_to_json(response)
        print("Data successfully fetched and saved to matching_materials.json")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
