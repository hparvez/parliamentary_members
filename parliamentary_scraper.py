import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


# Dictionary to take member name and URL of their site
members_dict = {}

# Define header
user_agent = 'Mozilla/5.0'
headers={'User-Agent':user_agent} 

# Iterate over 33 pages [this should be updated if there's more or less pages]
for i in range(1, 34):
    # Define base URL
    url = f"https://members.parliament.uk/members/Commons?page={i}"
    driver.get(url)
    html = driver.page_source

    # Parse URL
    bs = BeautifulSoup(html, "html.parser")

    # Extract HTML for each individual member
    members_full = bs.find_all(class_="card card-member")

    # Loop through each member and fill in dictionary
    link_prefix = "https://members.parliament.uk/"
    for details in members_full:
        members_dict[details.find(class_="primary-info").contents[0].strip()] = link_prefix + details["href"]


# Dictionary to take name and formatted address
names_address_dict = {}

# Loop through each name and get the address
for name, link in members_dict.items():
    
    # Parse HTML of individual page
    driver.get(link)
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    
    # Find all matching addreses (this will be 1 for many cases)
    addresses = bs.select(".card-contact-info .col-md-5")
    # If there's more than 1 address, take the address that's not Westminister
    if len(addresses) > 1:
        # Iterate over all addresses
        for address in addresses:
            # Clean up the address
            clean_address = ", ".join(list(address.stripped_strings))
            if "House of Commons" not in clean_address:
                # Create record in dictionary
                names_address_dict[name] = clean_address
    else:
        clean_address = ", ".join(list(addresses[0].stripped_strings))
        # Create record in dictionary
        names_address_dict[name] = clean_address


# Open CSV file
with open("results.csv", "w") as file:
    # Create instance of DictWriter
    w = csv.DictWriter(file, fieldnames=["Name", "Address"])
    # Iterate over dictionary and write rows to CSV
    for key, value in names_address_dict.items():
        w.writerow({"Name": key, "Address": value})
