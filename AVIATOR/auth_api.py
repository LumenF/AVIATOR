import os

from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == os.environ.get('TOKEN_AUTH'):
            return token
