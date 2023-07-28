import urllib.request
from bs4 import BeautifulSoup


webUrl = urllib.request.urlopen('https://www.cbc.ca')
if(webUrl.code == 200):
    htmldata = webUrl.read()

    soup = BeautifulSoup(htmldata, 'html.parser')

    # Find all input fields
    input_fields = soup.find_all("h3")
    content = "".join(soup.get_text(' ', strip=True))
    print(content)
    # # Extract attributes or data from the input fields
    # for field in input_fields:
        
    #     # Print the name and type of each input field
    #     print(f"Heading: {field}")