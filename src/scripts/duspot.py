#!/usr/bin/env python3

import requests
import json
from math import ceil
from datetime import date
from dotenv import load_dotenv
import os


__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.1"

load_dotenv()
# --------------------------------------------------------------------------------------
# Request Script for querying Duspot Database - Active Listings
# https://portal.duspot.nl/
#
# Note: Duspot does not allow filtering by material type without entering a keyword first.
# Current functionality allows for the addition of keywords.
# --------------------------------------------------------------------------------------


class DuspotClient:
    """A client for interacting with the Duspot API."""

    BASE_URL = "https://api.duspot.nl/api"

    def __init__(self):
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def authenticate(self) -> bool:
        """Authenticate with the API using credentials from environment variables."""
        username = os.getenv("DUSPOT_USERNAME")
        password = os.getenv("DUSPOT_PASSWORD")

        if not username or not password:
            print("Missing credentials in environment variables")
            return False

        payload = {"email": username, "password": password}

        try:
            response = requests.post(f"{self.BASE_URL}/login", json=payload)
            json_response = response.json()

            if "token" in json_response:
                self.token = json_response["token"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                return True

        except requests.exceptions.RequestException as e:
            print("Login failed:", e)

        return False

    def fetch_active_items(self, keyword=None):
        """Fetch all active items, optionally filtered by keyword."""
        if not self.token:
            print("Not authenticated. Call authenticate() first.")
            return []

        params = {"published": "true", "spot.active": "true", "page": 1}

        if keyword:
            params["search"] = keyword

        try:
            # Get first page to determine pagination
            first_response = requests.get(
                f"{self.BASE_URL}/products", headers=self.headers, params=params
            )
            page_data = first_response.json()

            # Calculate pagination
            total_items = page_data["hydra:totalItems"]
            page_size = len(page_data["hydra:member"])
            total_pages = ceil(total_items / page_size)

            # Collect all records
            all_records = []
            for page in range(1, total_pages + 1):
                params["page"] = page
                response = requests.get(
                    f"{self.BASE_URL}/products", headers=self.headers, params=params
                )
                page_data = response.json()
                all_records.extend(page_data["hydra:member"])

            # Save to file
            today = date.today().strftime("%Y-%m-%d")
            filename = f"{today}_duspot_data{'_' + keyword if keyword else ''}.json"

            with open(filename, "w") as fh:
                json.dump(all_records, fh, indent=2)

            return all_records

        except requests.exceptions.RequestException as e:
            print("Failed to fetch items:", e)
        except Exception as e:
            print("Error processing data:", e)

        return []

    def fetch_item_by_id(self, item_id):
        """Fetch a specific item by its ID."""
        if not self.token:
            print("Not authenticated. Call authenticate() first.")
            return None

        try:
            response = requests.get(
                f"{self.BASE_URL}/product/{item_id}", headers=self.headers
            )
            data = response.json()

            with open(f"{item_id}_data.json", "w") as fh:
                json.dump(data, fh, indent=2)

            return data

        except requests.exceptions.RequestException as e:
            print("Failed to fetch item:", e)

        return None


def main():
    client = DuspotClient()

    if client.authenticate():
        # Fetch all active items
        client.fetch_active_items()

        # Fetch items with keyword "staal"
        client.fetch_active_items("staal")

        # Fetch specific item
        client.fetch_item_by_id("some-id")
    else:
        print("Authentication failed")


if __name__ == "__main__":
    main()
