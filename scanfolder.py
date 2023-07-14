#! /usr/bin/env python3

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

### obtained from Drive URL https://drive.google.com/drive/folders/1xUYFsuettxU_SN1siO_zwhhA24non-5o
#bhfolderID = "1xUYFsuettxU_SN1siO_zwhhA24non-5o" # top-level folder containing Black Hole run subfolders

bhfolderID = "132ZYZBKgAwii1Ps0NX2sX1y-yERHB6ir" # m1.0_p16_b2.0_300k_plt50 folder


# Example downloader from: https://www.programcreek.com/python/example/103497/googleapiclient.http.MediaIoBaseDownload
def download_file(service, file_id, location, filename, mime_type):

    if 'vnd.google-apps' in mime_type:
        request = service.files().export_media(fileId=file_id,
                mimeType='application/pdf')
        filename += '.pdf'
    else:
        request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(location + filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request, 1024 * 1024 * 1024)
    done = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
        except:
            fh.close()
            os.remove(location + filename)
            sys.exit(1)
        print(f'\rDownload {int(status.progress() * 100)}%.', end='')
        sys.stdout.flush()
    print('') 


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        some = False
        nextPageToken = None

        while True:

            # Call the Drive v3 API

            results = service.files().list(
                q="'%s' in parents" % bhfolderID,
                pageSize=50,
                fields='nextPageToken, files(id, name, size)',
                pageToken=nextPageToken).execute()

            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            for item in items:
                print('{0:>8}K  {1}  {2}'.format(((int(item['size'])+1023))//1024, item['id'], item['name']))

            nextPageToken = results.get('nextPageToken', None)
            if nextPageToken is None:
                break

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
