from rest_framework import authentication,exceptions
from django.contrib.auth.models import User,Group
import uuid
from rest_framework.authtoken.models import Token
from HELPEX import keyconfig as senv
from clients.models import Client
from .encryption import encrypted_to_raw as decrypt

class CustomBaseAuthentication(authentication.BaseAuthentication):
    """Calls authenticate function"""
    authorization = None
    user_token_name = None
    user_token = None
    app_version = None

    def __init__(self, user_token_name):
        self.user_token_name = user_token_name

    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError as e:
            return False

    def _raise_incomplete(self):
        raise exceptions.AuthenticationFailed(
            {"message": "Insufficient Request Parameters", "status": 0}
        )

    def _check_headers(self, request_headers):
        """
        Checks if Token Key Authorization exists
        """
        if "HTTP_X_AUTHORIZATION" not in request_headers or self.user_token_name not in request_headers:
            self._raise_incomplete()

    def _set_authorization_origin(self, request_headers):
        """
        sets authorization as a variable

        Seperate origins can have seperate origin tokens
        """
        self.authorization = str(request_headers['HTTP_X_AUTHORIZATION'])

    def _set_user_token(self, request_headers):
        """
        Sets user token variable for authentication
        """
        try:
            self.user_token = decrypt(str(request_headers[self.user_token_name]))
        except Exception as e:
            raise exceptions.AuthenticationFailed(
                {"message": "Invalid User Token", "status": 0}
            )

    def _validate_authorization_origin(self):
        """
        Checks if given authorization tokens
        """
        # pass
        if self.authorization == senv.AUTHORIZATION:
            pass
        else:
            raise exceptions.AuthenticationFailed(
                {"message": "Invalid Request Source"}
            )
    
    def _get_user(self):
        """
        Gets user and returns user
        """
        _user_type = self.user_token_name.replace("HTTP_X_", "").replace("_ID", "").lower()
        token = Token.objects.filter(key = self.user_token)
        if token.exists():
            token = token.first()
            user = token.user
            if Client.objects.filter(auth_user=user).exists():
                return(user,None)
        
        raise exceptions.AuthenticationFailed(
            {"message": "Invalid User ID Header", "status": 0}
        )
        
    def authenticate(self, request):
        self._check_headers(request.META)
        self._set_authorization_origin(request.META)
        self._set_user_token(request.META)
        self._validate_authorization_origin()
        return self._get_user()


class ClientAuthentication(CustomBaseAuthentication):
    def __init__(self):
        super().__init__(user_token_name="HTTP_X_CLIENT_ID")


