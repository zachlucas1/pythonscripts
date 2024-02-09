from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the necessary scopes and credentials
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
SERVICE_ACCOUNT_FILE = 'googleapikey.json'

# Authenticate with the Google Admin SDK using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('admin', 'directory_v1', credentials=credentials)

# Function to create a new Google account
def create_google_account(first_name, last_name, password):
    user = {
        'name': {
            'givenName': first_name,
            'familyName': last_name
        },
        'password': password,
        'primaryEmail': f"{first_name}.{last_name}@arivo.com"  # Replace 'your-domain.com' with your actual domain
    }
    try:
        response = service.users().insert(body=user).execute()
        print(f"Google account for {first_name}.{last_name}@arivo.com created successfully.")
    except Exception as e:
        print(f"Failed to create Google account for {first_name}.{last_name}@arivo.com: {e}")

# Example usage
if __name__ == '__main__':
    create_google_account("John", "Doe", "P@ssw0rd")
