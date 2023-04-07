import base64
from abc import ABC, abstractmethod

import requests
from django.conf import settings


class Authentication(ABC):
    """
    Abstract class for authentication
    """

    @abstractmethod
    def get_access_token(self):
        """
        Get the Access Token for Authentication
        """


class Session(requests.Session):
    """
    Base class for external API session.
    """

    def __init__(self, authentication: Authentication, base_url: str = None):
        super().__init__()
        self.headers = {"Content-Type": "application/json"}
        self.base_url = base_url if base_url else settings.API_URL
        # Add Token to the header
        self.headers["Authorization"] = authentication.access_token


class BasicAuthentication(Authentication):
    """
    Get Access Token using Basic Authentication for given external credentials.
    """

    @classmethod
    def get_access_token(cls, username=None, password=None):
        credentials = cls()
        username = username
        password = password
        credentials.access_token = "Basic " + base64.b64encode(
            f"{username}:{password}".encode("utf-8")
        ).decode("utf-8")
        return credentials
