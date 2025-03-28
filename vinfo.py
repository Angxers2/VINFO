import argparse
import xml.etree.ElementTree as ET
import requests
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def load_ascii_art(file_path='ascii_images.txt'):
    """
    Load ASCII art from a text file
    
    Args:
        file_path (str): Path to the ASCII art text file
    
    Returns:
        dict: Dictionary of brand logos
    """
    car_logos = {}
    
    try:
        with open(file_path, 'r') as file:
            current_brand = None
            current_logo = []
            
            for line in file:
                line = line.rstrip('\n')
                
                # Check if this is a brand header
                if line.endswith(':'):
                    # Save previous brand's logo if exists
                    if current_brand and current_logo:
                        car_logos[current_brand.lower()] = '\n'.join(current_logo)
                        current_logo = []
                    
                    # Set new current brand
                    current_brand = line[:-1]
                elif line:
                    # Accumulate logo lines
                    current_logo.append(line)
            
            # Save last brand's logo
            if current_brand and current_logo:
                car_logos[current_brand.lower()] = '\n'.join(current_logo)
    
    except FileNotFoundError:
        print(Fore.RED + f"Warning: ASCII art file '{file_path}' not found.")
    except Exception as e:
        print(Fore.RED + f"Error reading ASCII art file: {e}")
    
    # Add a default logo if no logos loaded
    if not car_logos:
        car_logos['default'] = '''
 ┌─────────────┐
 │  CAR INFO   │
 └─────────────┘
        '''
    
    return car_logos

def get_car_info(vin):
    """
    Fetch car information from NHTSA API
    
    Args:
        vin (str): Vehicle Identification Number
    
    Returns:
        dict or None: Car information or None if not found
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("Results"):
            return data["Results"][0]
        else:
            print(Fore.RED + f"Error: No information found for VIN {vin}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Network Error: {e}")
        return None
    except ValueError as e:
        print(Fore.RED + f"JSON Parsing Error: {e}")
        return None

def organize_car_info(car_info):
    """
    Organize and extract key details from car information
    
    Args:
        car_info (dict): Raw car information
    
    Returns:
        dict: Organized car details
    """
    # Extract all non-empty values
    details = {}
    for key, value in car_info.items():
        if value and value.strip() and value.lower() != 'not available':
            details[key] = value
    
    return details

def print_car_info(car_logos, car_brand, car_details):
    """
    Print car information with color and ASCII art
    
    Args:
        car_logos (dict): Dictionary of car logos
        car_brand (str): Car manufacturer
        car_details (dict): Car details
    """
    # Display brand logo
    logo = car_logos.get(car_brand.lower(), car_logos.get('default', ''))
    print(Fore.GREEN + logo)
    
    # Print car information with color
    print(Fore.YELLOW + f"\n{car_brand.upper()} VIN DETAILS:")
    print(Fore.CYAN + "-" * 40)
    
    # Sort and print details
    sorted_details = sorted(car_details.items())
    for attribute, value in sorted_details:
        print(f"{Fore.MAGENTA}{attribute}: {Fore.WHITE}{value}")

def save_to_txt(filename, car_brand, car_details):
    """Save car information to a text file"""
    with open(filename, 'w') as file:
        file.write(f"{car_brand.upper()} VIN DETAILS\n")
        file.write("-" * 40 + "\n")
        
        # Sort details for consistent output
        sorted_details = sorted(car_details.items())
        for attribute, value in sorted_details:
            file.write(f"{attribute}: {value}\n")

def save_to_xml(filename, car_brand, car_details):
    """Save car information to an XML file"""
    root = ET.Element("CarInformation")
    brand_element = ET.SubElement(root, "Brand")
    brand_element.text = car_brand.upper()
    
    # Sort details for consistent output
    sorted_details = sorted(car_details.items())
    for attribute, value in sorted_details:
        # Remove spaces and invalid XML tag characters
        safe_tag = ''.join(c for c in attribute.replace(' ', '_') if c.isalnum() or c == '_')
        attr_element = ET.SubElement(root, safe_tag)
        attr_element.text = value
    
    tree = ET.ElementTree(root)
    tree.write(filename)

def main():
    # Load ASCII art logos
    car_logos = load_ascii_art()
    
    parser = argparse.ArgumentParser(description='VIN Decoder - Retrieve detailed vehicle information')
    parser.add_argument('-v', '--vin', type=str, help='Vehicle Identification Number', required=True)
    parser.add_argument('-f', '--filename', type=str, help='File to save car information (txt or xml)')
    parser.add_argument('--ascii-file', type=str, default='ascii_images.txt', 
                        help='Path to ASCII art file (default: ascii_images.txt)')
    
    args = parser.parse_args()
    
    # Reload ASCII art if a custom file is specified
    if args.ascii_file != 'ascii_images.txt':
        car_logos = load_ascii_art(args.ascii_file)
    
    car_info = get_car_info(args.vin)
    if car_info:
        car_brand = car_info.get('Make', 'Unknown')
        car_details = organize_car_info(car_info)
        
        print_car_info(car_logos, car_brand, car_details)
        
        if args.filename:
            file_extension = args.filename.split('.')[-1].lower()
            if file_extension == 'txt':
                save_to_txt(args.filename, car_brand, car_details)
            elif file_extension == 'xml':
                save_to_xml(args.filename, car_brand, car_details)
            print(Fore.GREEN + f"\nCar information saved to {args.filename}")

if __name__ == "__main__":
    main()