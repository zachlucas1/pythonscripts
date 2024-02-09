#https://community.jumpcloud.com/t5/community-scripts/python-script-for-bulk-user-creation-via-jumpcloud-api/m-p/1054

import requests
import getpass

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
    url = "https://console.jumpcloud.com/api/systemusers"
    api_key = getpass.getpass('Enter a JumpCloud Admin API Key: ')

    try:
        with open("/mnt/c/Users/zach.lucas/Downloads/users - Sheet1.csv", "r") as file:
            next(file)  # Skip header
            for line in file:
                data = line.strip().split(',')
                if len(data) == 6:
                    firstname, lastname, username, password, email, displayname = data
                    create_user(api_key, url, firstname, lastname, username, password, email, displayname)
                else:
                    print("Invalid data format in CSV.")
    except FileNotFoundError:
        print("users.csv not found.")

if __name__ == '__main__':
    main()
    
