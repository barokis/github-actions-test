
import json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds_dict = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))

def get_values(spreadsheet_id, range_name):
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    val = get_values(spreadsheet_id, "A:B")
    print(val)
