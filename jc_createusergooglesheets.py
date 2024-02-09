import requests
import getpass
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to authenticate with Google Sheets API and fetch data
def get_data_from_google_sheet(sheet_id, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet.get_all_values()

def create_user(api_key, url, firstname, lastname, username,
                password, email, displayname):
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
    api_key = getpass.getpass('Enter a JumpCloud Admin API Key: ')
    sheet_id = 'YOUR_GOOGLE_SHEET_ID'  # Replace with your Google Sheet ID
    sheet_name = 'Sheet1'  # Replace with the name of your sheet

    try:
        data = get_data_from_google_sheet(sheet_id, sheet_name)
        for row in data[1:]:  # Skip header
            if len(row) == 6:
                firstname, lastname, username, password, email, displayname = row
                create_user(api_key, url, firstname, lastname, username, password, email, displayname)
            else:
                print("Invalid data format in Google Sheet.")
    except Exception as e:
        print(f"Failed to fetch data from Google Sheet: {e}")

if __name__ == '__main__':
    main()
