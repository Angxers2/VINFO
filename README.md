# VINFO

VINFO is a Python script that fetches detailed information about a car based on its Vehicle Identification Number (VIN) using the National Highway Traffic Safety Administration (NHTSA) API. It allows you to retrieve information such as the car's make, model, year, and other relevant details, and optionally save this information to a text or XML file.

## Features

- Fetches car information based on VIN
- Supports saving information to a text file or an XML file
- Displays detailed information about the car in the console

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Angxers2/VINFO.git
   ```

2. Navigate to the directory:
   ```bash
   cd VINFO
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using the following command:

```bash
python3 vinfo.py -v VIN [-f FILENAME]
```

Replace `VIN` with the Vehicle Identification Number of the car you want to fetch information for. Optionally, specify a `FILENAME` to save the information to a text or XML file.

For more detailed usage instructions, see the [Help](help.txt) file.

## Examples

1. Fetch car information and display in the console:
   ```bash
   python3 vinfo.py -v ABC123456789DEF
   ```

2. Fetch car information and save to a text file:
   ```bash
   python3 vinfo.py -v ABC123456789DEF -f car_info.txt
   ```

3. Fetch car information and save to an XML file:
   ```bash
   python3 vinfo.py -v ABC123456789DEF -f car_info.xml
   ```

