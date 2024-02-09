import getpass
import gspread
import requests

# Authenticates with json file
client = gspread.service_account(filename='googleapikey.json')

# Prompts for date of new hires, converts to a string so no data type issues
date = str(input('Please input the date for new hires:'))

# Opens Staff Updates workbook and points to worksheet inputted
workbook = client.open('Staff Updates').worksheet(date)

# Stores the first column values in a list
names = workbook.col_values(1)

# Gets rid of column header
names.pop(0)

# Extracts first name
firstNames = [name.split(' ')[0] for name in names]

# Extracts last name
lastNames = [name.split()[-1] for name in names]

# Generates emails
emails = [name.lower().replace(' ', '.') + '@arivo.com' for name in names]

# Generates usernames
usernames = [email.split('@')[0] for email in emails]

# Define the function to create user in JumpCloud
def create_user(api_key, url, firstname, lastname, username, email, displayname):
    password = "Red123!@#"
    payload = {
        "activated": True,
        "displayname": displayname,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
        "password_never_expires": False,
        "password_expired": True,
        "state": "ACTIVATED",
        "username": username
    }

    headers = {"x-api-key": api_key, "content-type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        user_id = response.json().get('id')  # Extract user ID from response
        print(f"User {username} created successfully.")

        # Expire user's password
        expire_url = f"https://console.jumpcloud.com/api/systemusers/{user_id}/expire"
        expire_response = requests.post(expire_url, headers=headers)
        expire_response.raise_for_status()
        print(f"Password for user {username} expired successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create user {username}: {e}")

def main():
    url = "https://console.jumpcloud.com/api/systemusers"
    api_key = getpass.getpass('Enter a JumpCloud Admin API Key: ')

    # Create users
    for first_name, last_name, username, email in zip(firstNames, lastNames, usernames, emails):
        create_user(api_key, url, first_name, last_name, username, email, f"{first_name} {last_name}")

if __name__ == '__main__':
    main()
