import httplib2
import os

import json

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '../data/client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    response = service.users().messages().list(userId='me').execute();
    messages = []
    data = []

    print "---- Processing messages request ----"
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', pageToken=page_token).execute()
        messages.extend(response['messages']);

    print "---- " + str(len(messages)) + " messages received ----"
    # At this point, all the messages are in messages
    print "---- Processing messages received ----"

    messageIndex = 0

    # NOTE(hugo): header's name we need to look for in the json file and their correspondance in the json file we will create
    tags = {"From" : "sender", "To" :"receiver" , "Subject" : "subject", "Date" : "date"}
    # TODO(hugo): maybe create a dict of string -> bool to see if we have found all the tags we were looking for
    # TODO(hugo): see if we can write at the end of one file so as to process the mails one after the other
    # rather than getting them all and then process them all
    
    for m in messages:

        # Just a hack to see where we are in the computation
        messageIndex += 1
        if messageIndex % 50 == 0:
            print "---- Processing message " + str(messageIndex) + " ----"

        messageId = m['id']
        message = service.users().messages().get(userId='me', id=messageId, fields='payload/headers').execute()
        jsonMessage = {}
        headers = message["payload"]["headers"]
        for header in headers:
            if header["name"] in tags.keys():
                jsonMessage[tags[header["name"]]] = header["value"]
        data.append(jsonMessage)
                
    jsonData = json.dumps(data, indent=4,separators=(' , ',' : '))
    #print jsonData
    f = open("../data/mails-data.json", "w")
    f.write(jsonData)
    f.close()


if __name__ == '__main__':
    main()
