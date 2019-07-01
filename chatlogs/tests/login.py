from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


def login(username):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    user = User.objects.get(username=username)
    return jwt_encode_handler(jwt_payload_handler(user))