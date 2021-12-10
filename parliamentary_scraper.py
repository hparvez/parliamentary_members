from bs4 import BeautifulSoup
from urllib.request import urlopen

# Dictionary to take member name and URL of their site
members_dict = {}

# Iterate over 33 pages [this should be updated if there's more or less pages]
for i in range(1, 34):
    # Define base URL
    url = f"https://members.parliament.uk/members/Commons?page={i}"
    html = urlopen(url)

    # Parse URL
    bs = BeautifulSoup(html.read(), "html.parser")

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
    html = urlopen(link)
    bs = BeautifulSoup(html, "html.parser")

    # Extract the address
    address = bs.find(class_="col-md-5").contents

    # Clean up the formatting
    address_formatted = []
    for line in address:
        try:
            address_formatted.append(line.strip())
        except:
            pass

    # Create record in dictionary
    names_address_dict[name] = ", ".join(address_formatted)

print(names_address_dict)
