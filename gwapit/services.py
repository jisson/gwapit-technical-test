import logging

from googleapiclient.errors import HttpError

from oauth2client.client import GoogleCredentials
from oauth2client import GOOGLE_TOKEN_URI
import httplib2
from apiclient import discovery
from django.conf import settings

from gwapit.serializers import GmailMessage

logger = logging.getLogger("gwapit")


def get_google_credentials(user_data):
    """
    Retrieve google credentials based on user_data of a user.

    :param user_data:   The oauth data of a user
    :return:            Google Credentials allowing to use google services
    """

    access_token = user_data['access_token']
    refresh_token = None
    token_expiry = user_data['expires']
    token_uri = GOOGLE_TOKEN_URI
    user_agent = 'Python client library'
    revoke_uri = None

    gCreds = GoogleCredentials(
        access_token,
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        refresh_token,
        token_expiry,
        token_uri,
        user_agent,
        revoke_uri=revoke_uri
    )
    return gCreds


def get_gmail_service(user_social_auth):
    """
    Retrieve the gmail service allowing to fetch user's emails.

    :param user_social_auth:    The oauth data of a user
    :return:                    An instance of the GMail service
    """

    credentials = get_google_credentials(user_social_auth.extra_data)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    return service


def get_message(gmail_service, user_uid, message_id):
    """
    Retrieve a gmail message from its ID

    :param gmail_service:   An instance of the Gmail service
    :param user_uid:        The google uid of a user
    :param message_id:      The id of the message to retrieve
    :return:                An instance of 'gwapit.serializers.GmailMessage' as a gmail message
    """

    try:
        message = gmail_service.users().messages().get(userId=user_uid, id=message_id).execute()
        message = GmailMessage(message)
        return message
    except HttpError as error:
        logger.error('An error occurred: %s' % error)
        raise error


def retrieve_last_100_emails(gmail_service, user_uid):
    """
    Retrieve the last 100 gmail messages of a user.

    :param gmail_service:   An instance of the GMail service
    :param user_uid:        The google uid of a user
    :return:                The list of the last 100 messages of the user
    """

    try:
        response = gmail_service.users().messages().list(userId=user_uid, maxResults=100).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except HttpError as error:
        logger.error('An error occurred: %s' % error)
        raise error


# def get_messages_from_gmail(user_social_auth):
#
#     credentials = get_google_credentials(user_social_auth.extra_data)
#
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('gmail', 'v1', http=http)
#
#     user_uid = user_social_auth.uid
#     messages = retrieve_last_100_emails(service, user_uid)
#
#     message_objects = []
#     for message in messages:
#         message_objects.append(get_message(service, user_uid, message['id']))
#
#     # logger.debug(message_objects[-1])
#     return message_objects
