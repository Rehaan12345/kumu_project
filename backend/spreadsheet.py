import requests, os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_sheets(api_key):
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()

def get_vals(collection):
    sheets = authenticate_sheets(os.environ.get("SHEETS_API"))
    # Assuming a maximum of 23 "TO" elements for each "FROM" (Z) -> If we ever reach more, simple adjust "Z" to be higher, etc.
    try:
        result = sheets.values().get(spreadsheetId=os.environ.get("SHEET_ID"), range = f"{collection}!A2:Z100000000").execute()
        values = result.get("values")
        return values
    except Exception as e:
        return {"status": f"Failure to get_vals: {e}"}

def update_sheet(collection_id, values, row, col_ind):

    # col_ind == 0 means that values[0] is "FROM", otherwise, the whole of values is just "TO"

    # try:
    #     if col_ind == 0:
    #         create_doc("All", values)
    # except Exception as e:
    #     return {"status": f"Failed to update_sheet in db: {e}"}

    sheets = authenticate_sheets(os.environ.get("SHEETS_API"))

    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    print(f"33 - {values}")

    requests = [
        {
            'insertDimension': {
                'range': {
                    'sheetId': collection_id, 
                    'dimension': 'ROWS',
                    'startIndex': row,
                    'endIndex': row
                },
                'inheritFromBefore': False
            }
        },
        {
            'updateCells': {
                'rows': [
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': value}} for value in values
                        ]
                    }
                ],
                'fields': 'userEnteredValue',
                'start': {
                    'sheetId': collection_id,
                    'rowIndex': row,
                    'columnIndex': col_ind
                }
            }
        }
    ]

    body = { "requests": requests }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=os.environ.get("SHEET_ID"),
            body=body
        ).execute()
        return {"status": f"Success: {response}"}
    except Exception as e:
        return {"status": f"Failure: {e}"}