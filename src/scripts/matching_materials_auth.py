import requests
import json
from msal import PublicClientApplication
import os
from dotenv import load_dotenv

__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.2"

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


class MatchingMaterialsAuth:
    def __init__(self):

        load_dotenv()

        self.client_id = os.getenv("MM_CLIENT_ID")
        self.base_url = "https://matchingmaterials.com/api"
        self.redirect_uri = "https://matchingmaterials.com/signout"

        self.app = PublicClientApplication(
            client_id=self.client_id,
            authority="https://login.microsoftonline.com/common",
        )

        self.scopes = ["https://graph.microsoft.com/User.Read"]

        self.cache_file = ".token_cache.json"
        self._load_cache()

    def _load_cache(self):
        """Load token cache from file if it exists"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                cache_data = json.load(f)
                self.app.token_cache.deserialize(json.dumps(cache_data))

    def _save_cache(self):
        """Save token cache to file"""
        if self.app.token_cache.has_state():
            cache_data = json.loads(self.app.token_cache.serialize())
            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f)

    def get_auth_token(self):
        accounts = self.app.get_accounts()

        if accounts:
            try:
                result = self.app.acquire_token_silent(
                    scopes=scopes, account=accounts[0]
                )
                if result:
                    return result["access_token"]
            except Exception as e:
                print(f"Silent token acquisition failed: {e}")

        try:
            # Start device flow
            flow = self.app.initiate_device_flow(scopes=self.scopes)

            if "user_code" not in flow:
                raise Exception("Failed to create device flow")

            print(
                "\nTo sign in, use a web browser to open the page {} and enter the code {} to authenticate.".format(
                    flow["verification_uri"], flow["user_code"]
                )
            )

            # Complete authentication flow
            result = self.app.acquire_token_by_device_flow(flow)

            if "access_token" in result:
                self._save_cache()
                return result["access_token"]
            else:
                error = result.get("error_description", result.get("error"))
                raise Exception(f"Failed to get token: {error}")

        except Exception as e:
            raise Exception(f"Authentication failed: {e}")


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
    try:
        auth = MatchingMaterialsAuth()
        token = auth.get_auth_token()
        print("Successfully acquired token")
    except Exception as e:
        print(f"Error: {e}")
    if not token:
        print("Failed to obtain access token.")
        return

    response = make_api_request(token)  # sub in material category if desired

    if response.status_code == 200:
        response_to_json(response)
        print("Data successfully fetched and saved to matching_materials.json")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
