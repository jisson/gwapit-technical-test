import logging

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from googleapiclient.errors import HttpError
from rest_framework import status, views
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import logout as django_logout
from social.apps.django_app.default.models import UserSocialAuth
from django.http import Http404

from gwapit import services as gwapit_services
from gwapit.serializers import GmailMessageSerializer

logger = logging.getLogger("gwapit")


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def email_list(request):
    """
    Retrieve the last 100 messages from the GMail account of the logged user.

    :return:    A list of gmail messages as a JSon, formatted like:

    [
        {"id":"158211b8c35c683b","threadId":"158211b8c35c683b"},
        {"id":"15820cadb0f102e6","threadId":"15820cadb0f102e6"},
        ...
    ]
    @see: https://developers.google.com/gmail/api/v1/reference/users/messages/list
    """

    user = request.user
    if request.method == 'GET' and user.is_authenticated():

        try:
            social_auth = UserSocialAuth.objects.get(user=user.id)
        except UserSocialAuth.DoesNotExist:
            raise Http404

        try:
            gmail_service = gwapit_services.get_gmail_service(social_auth)
            messages = gwapit_services.retrieve_last_100_emails(gmail_service, social_auth.uid)

            return Response(messages)
        except HttpError as error:
            raise error


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@cache_page(60 * 15)
def get_email_message(request, message_id):
    """
    Retrieve the detail of a message from it id.

    :return: The details of the message as a JSon formatted like:

        {
            "id":"158211b8c35c683b",
            "date":"Tue, 01 Nov 2016 18:16:43 +0000",
            "internal_date":1478024203000,
            "sender":"payments-merchant-center-noreply@google.com",
            "subject":"The subject",
            "snippet":"The snippet"
        }
    @see: https://developers.google.com/gmail/api/v1/reference/users/messages/get
    """

    user = request.user
    if request.method == 'GET' and user.is_authenticated():
        try:
            social_auth = UserSocialAuth.objects.get(user=user.id)
        except UserSocialAuth.DoesNotExist:
            raise Http404

        gmail_service = gwapit_services.get_gmail_service(social_auth)
        message = gwapit_services.get_message(gmail_service, social_auth.uid, message_id)

        message_serializer = GmailMessageSerializer(message)

        return Response(message_serializer.data)


class LogoutView(views.APIView):
    """
    Allow the user to logout from django.
    """

    def post(self, request, format=None):
        django_logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class IndexView(TemplateView):
    """
    View for the single page application template.
    """
    template_name = 'gwapit/index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


# def login(request):
#     return render(request, 'gwapit/login.html')

