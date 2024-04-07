import argparse
import xml.etree.ElementTree as ET
import requests

# Function to fetch car information based on VIN
def get_car_info(vin):
    # URL for the API endpoint to fetch car information
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    
    try:
        # Sending GET request to the API
        response = requests.get(url)
        # Extracting JSON data
        data = response.json()
        
        # Checking if the response contains results
        if data["Results"]:
            # Extracting car information from the response
            car_info = data["Results"][0]
            return car_info
        else:
            print("Error: No car information found for the provided VIN.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to organize car information and remove "Not Available" entries
def organize_car_info(car_info):
    organized_info = []
    for attribute, value in car_info.items():
        if value != 'Not Available':
            organized_info.append((attribute, value))
    return organized_info

# Function to save car information to a text file
def save_to_txt(filename, car_brand, organized_info):
    with open(filename, 'w') as file:
        file.write(car_brand.upper() + '\n')
        for attribute, value in organized_info:
            file.write(f"{attribute}: {value}\n")

# Function to save car information to an XML file
def save_to_xml(filename, car_brand, organized_info):
    root = ET.Element("CarInformation")
    brand_element = ET.SubElement(root, "Brand")
    brand_element.text = car_brand.upper()
    for attribute, value in organized_info:
        attribute_element = ET.SubElement(root, attribute.replace(' ', ''))
        attribute_element.text = value

    tree = ET.ElementTree(root)
    tree.write(filename)

# Function to print car information in a formatted manner
def print_car_info(car_brand, organized_info):
    print(car_brand.upper())
    for attribute, value in organized_info:
        print(f"{attribute}: {value}")

# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vin', type=str, help='VIN number of the car', required=True)
    parser.add_argument('-f', '--filename', type=str, help='File to save the car information (txt or xml)', default=None)
    parser.add_argument('--show-help', action='help', help='Show this help message and exit')
    
    args = parser.parse_args()
    
    vin = args.vin
    filename = args.filename
    
    # Fetch car information
    car_info = get_car_info(vin)
    if car_info:
        # Extract car brand
        car_brand = car_info.get('Make', 'Unknown')
        
        # Organize and remove "Not Available" entries
        organized_info = organize_car_info(car_info)
        
        # Display car information
        print_car_info(car_brand, organized_info)
        
        # Save car information to a file if filename is provided
        if filename:
            file_extension = filename.split('.')[-1]
            if file_extension == 'txt':
                save_to_txt(filename, car_brand, organized_info)
            elif file_extension == 'xml':
                save_to_xml(filename, car_brand, organized_info)
            print(f"Car information saved to {filename}")

if __name__ == "__main__":
    main()
