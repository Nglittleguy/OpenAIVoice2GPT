import urllib.request
from bs4 import BeautifulSoup


webUrl = urllib.request.urlopen('https://marriott.com/default.mi')
if(webUrl.code == 200):
    htmldata = webUrl.read()

    soup = BeautifulSoup(htmldata, 'html.parser')

    # Find all input fields
    input_fields = soup.find_all("input")

    # Extract attributes or data from the input fields
    for field in input_fields:
        # Get the value of the 'name' attribute
        name = field.get("name")
        
        # Get the value of the 'type' attribute
        field_type = field.get("type")
        
        # Print the name and type of each input field
        print(f"Name: {name}, Type: {field_type}")