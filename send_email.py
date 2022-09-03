
import json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import smtplib, ssl

creds_dict = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')
spreadsheet_id = os.environ.get('SPREADSHEET_ID')

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
    val = get_values(spreadsheet_id, "A:C")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(USERNAME,PASSWORD)
        for row in val['values']:
            server.sendmail(USERNAME,row[1],row[2])

