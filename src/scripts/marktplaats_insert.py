import requests
import json

__author__ = "Maryanne Wachter"
__contact__ = "mwachter@utsv.net"
__version__ = "0.0.1"

# --------------------------------------------------------------------------------------
# GraphQL Request Script for querying Insert Marktplaats Database by Material Category
# https://marktplaats.insert.nl/materialen
#
# Note: Not all categories listed currently have products,
# so some queries may return empty
# --------------------------------------------------------------------------------------

url = "https://app.insert.nl/graphql"

category_mapping = {"Afbouwtimmerwerk": 104,
                    "Beglazing" :116,
                    "Behangwerk, vloerbedekking en stoffering": 101,
                    "Betonwerk": 56,
                    "Binneninrichting": 73,
                    "Binnenriolering": 155,
                    "Bomen": 166,
                    "Bouwkundige kanaalelementen": 268,
                    "Bouwplaatsvoorzieningen": 207,
                    "Brandbestrijdingsinstallaties": 5,
                    "Buitenriolering en drainage": 45,
                    "Communicatie- en beveiligingsinstallaties": 141,
                    "Coniferen": 223,
                    "Dakbedekkingen": 20,
                    "Dakgoten en hemelwaterafvoeren": 250,
                    "Dekvloeren en vloersystemen": 83,
                    "Elektrotechnische installaties": 78,
                    "Funderingspalen en damwanden": 61,
                    "Gasinstallaties": 119,
                    "Gebouwenbeheersystemen": 682,
                    "Gevelonderhoudinstallaties": 702,
                    "Gevelschermen": 87,
                    "Groenvoorzieningen": 720,
                    "Grondwerken": 330,
                    "Hagen": 283,
                    "Heesters": 288,
                    "Hef- en hijsinstallaties": 234,
                    "Koelinstallaties": 136,
                    "Kozijnen, ramen en deuren": 10,
                    "Liftinstallaties": 85,
                    "Metaal- en kunststofwerk": 132,
                    "Metaalconstructiewerk": 15,
                    "Metselwerk": 331,
                    "Na-isolatie": 188,
                    "Natuur- en kunststeen": 259,
                    "Overige categorieen": 1,
                    "Perslucht- en vacuuminstallaties": 149,
                    "Plafond- en wandsystemen": 70,
                    "Regelinstallaties": 629,
                    "Roltrappen en rolpaden": 695,
                    "Ruwbouwtimmerwerk": 58,
                    "Sanitair": 8,
                    "Sloopwerk": 301,
                    "Stukadoorwerk": 474,
                    "Systeembekledingen": 93,
                    "Technische inrichting": 179,
                    "Tegelwerk": 481,
                    "Terreininrichting": 3,
                    "Terreinverhardingen": 28,
                    "Trappen en balustraden": 26,
                    "Vast planten/ Varens": 295,
                    "Ventilatie- en luchtbehandelingsinstallaties": 76,
                    "Verplaatsbare gebouwen": 712,
                    "Verwarmingsinstallaties": 13,
                    "Voegvulling": 461,
                    "Vooraf vervaardigde steenachtige elementen": 31,
                    "Waterinstallaties": 67,
                    }

# GraphQL Category Query on Category ID
payload = '{{"query":"query category($id: ID, $sector: [String], $category: [ID], $status: [String]){{\\n    category(id: $id sector: $sector category: $category status: $status  ) {{\\n        id\\n        name\\n        producten {{\\n            id\\n            title\\n            url\\n            omschrijving\\n            lengtehoogte\\n            eenheid_lengtehoogte\\n            breedte\\n            eenheid_breedte\\n            hoogtedikte\\n            eenheid_hoogtedikte\\n            hoeveelheid\\n            eenheid_hoeveel\\n            op_aanvraag\\n            adres\\n            postcode\\n            plaats\\n            locatie_gebouw\\n            latitude\\n            longitude\\n        }}\\n    }}\\n}}\\n","variables":{{"id":{category_code}}}}}'
headers = {"Content-Type": "application/json"}

def get_single_category(category):
    category_code = category_mapping[category]
    fullQuery = payload.format(category_code=category_code)
    response = requests.request("POST", url, headers=headers, data=fullQuery)
    return response.json()


# Get all product info based on category

def category_to_json(category):
    text = get_single_category(category)
    with open("{category}.json".format(category=category), "w") as fh:
        json.dump(text, fh, indent=4)


if __name__ == "__main__":
    # Test two categories
    category_to_json("Bomen")
    category_to_json("Gevelschermen")
