import logging

from rest_framework import serializers

__author__ = 'Pierre Rodier | pierre@buffactory.com'


logger = logging.getLogger('gwapit')


class GmailMessage(object):
    """
    Represents an instance of a Gmail message
    """

    __type__ = "GmailMessage"

    def __init__(self, json_data):
        self._create_from_json(json_data)

    def _create_from_json(self, json_data):

        self.id = json_data['id']
        self.snippet = json_data['snippet']
        self.internal_date = json_data['internalDate']

        headers = json_data['payload']['headers']
        for header in headers:
            header_name = header['name']
            if header_name == "Date":
                self.date = header['value']
            elif header_name == "Subject":
                self.subject = header['value']
            elif header_name == "From":
                self.sender = header['value']


class GmailMessageSerializer(serializers.Serializer):
    """
    Api serializer for a Gmail Message
    """

    id = serializers.CharField()
    date = serializers.CharField()
    internal_date = serializers.IntegerField()

    sender = serializers.CharField()
    subject = serializers.CharField()
    snippet = serializers.CharField()
