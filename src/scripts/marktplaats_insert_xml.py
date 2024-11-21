import requests
import xmltodict
import json

__author__ = "Alessio Vigorito"
__contact__ = "alessio.vigorito@summum.engineering"
__version__ = "0.0.1"


def fetch_xml_data(xml_url): 
    # Fetch XML data from a given URL
    response = requests.get(xml_url)
    if response.status_code == 200:
        return xmltodict.parse(response.content)  # Parse XML into a dictionary
    raise RuntimeError(f"Failed to fetch XML data. Status code: {response.status_code}")

def parse_xml_data(data):
    # Navigate the dictionary to extract materials
    materials = data.get('root', {}).get('materials', {}).get('material', [])
    return [
        {
            'ID': material.get('id', ''),
            'URL': material.get('url', ''),
            'Project Name': material.get('project_name', ''),
            'Category': material.get('category', ''),
            'Sub Category': material.get('sub_category', ''),
            'Material Name': material.get('material_name', ''),
            'Description': material.get('description', ''),
            'Length': material.get('length', ''),
            'Length Unit': material.get('length_unit', ''),
            'Width': material.get('width', ''),
            'Width Unit': material.get('width_unit', ''),
            'Height': material.get('height', ''),
            'Height Unit': material.get('height_unit', ''),
            'Amount': material.get('amount', ''),
            'Amount Unit': material.get('amount_unit', ''),
            'Price': material.get('price', ''),
            'Price Per': material.get('price_per', ''),
            'City': material.get('city', ''),
            'Available From': material.get('available_from', ''),
            'Available To': material.get('available_to', ''),
            'Status': material.get('status', ''),
            'Quality Aesthetic': material.get('quality_aesthetic', ''),
            'Updated At': material.get('updated_at', ''),
            'Images': [
                {
                    'Name': img.get('name', ''),
                    'URL': img.get('url', '')
                } for img in material.get('image', [])
            ]
        }
        for material in (materials if isinstance(materials, list) else [materials]) 
    ]

def main():
    xml_url = 'https://marktplaats.insert.nl/feed/'
    data = fetch_xml_data(xml_url)
    materials = parse_xml_data(data)

    print(json.dumps(materials, indent=4))

if __name__ == "__main__":
    main()
