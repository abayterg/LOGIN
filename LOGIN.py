import requests
from bs4 import BeautifulSoup

# Start a session to keep cookies
session = requests.Session()

# Get the login page to fetch CSRF token and initial cookies
login_url = 'https://ais.usvisa-info.com/es-co/niv/users/sign_in'
url = 'https://ais.usvisa-info.com/es-co/niv/schedule/54777814/payment'
page = session.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Assuming the CSRF token is in a meta tag (common in Rails apps)
csrf_token = soup.find('meta', {'name': 'csrf-token'})['content'] if soup.find('meta', {'name': 'csrf-token'}) else None

print(csrf_token)
login_data = {
   # 'authenticity_token': csrf_token,  # the CSRF token you extracted
    'user[email]': 'betomolinares0315@gmail.com',
    'user[password]': 'AlbertoMolinares132*',
    'policy_confirmed': '1',  # Check this based on how the site handles it
    'commit': 'Iniciar sesión'  # This may or may not be needed; depends on how the server processes it
}

# # Include the CSRF token in your request if it exists
# if csrf_token:
#     login_data['authenticity_token'] = csrf_token

headers = {
    'Referer': login_url,
    'User-Agent': 'Mozilla/5.0'
}

cookies = page.cookies
response = session.post(login_url, data=login_data, headers=headers, cookies=cookies)


# Check if login was successful
if response.ok:
    print("Logged in successfully!")
else:
    print("Failed to log in")

# Assuming you've already logged in and `session` is your established session

response = session.get(url, headers=headers)

for cookie in session.cookies:
    ycookie=cookie
#print(ycookie.name, ycookie.value)
# Check if the request was successful

#session.cookies.set(ycookie.name, ycookie.value, domain='ais.usvisa-info.com')


if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table by its class name directly
    table = soup.find('table', {'class': 'for-layout'})

    # Check if the table is found
    if table:
        rows = table.find_all('tr')
        for row in rows:
            # Extracting all cells in a row
            cells = row.find_all('td')
            if cells:
                # Assuming the first cell is the location and the second is the date
                location = cells[0].text.strip()
                date = cells[1].text.strip()
                print(f"Location: {location}, Date: {date}")
    else:
        print("Table not found.")
else:
    print("Failed to retrieve the page.")

# Inspect the response if necessary

#print(response.text)

# Extract the head of the HTML document
#head = soup.head

# Print the head section
#print(head)