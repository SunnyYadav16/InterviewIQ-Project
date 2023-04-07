from common.api_auth import BasicAuthentication, Session
from common.logging import logger


class Response:
    """
    Base response class for handling HTTP requests to the external API.
    """

    def __init__(self, response):
        self.__response = response

        self.status_code = self.__response.status_code
        self.data = None
        self.indicates_failure = False
        self.error_message = None
        self.status = True
        self.total_counts = 0

        if self.__response.status_code > 202:
            self.__handle_unexpected_status_code()
        else:
            self.__extract_response_data()

    def __handle_unexpected_status_code(self):
        self.indicates_failure = True
        self.status = False

        if self.__response.status_code >= 400:
            self.__handle_service_error()

    def __extract_response_data(self):
        self.data = self.__response.json()

    def __handle_service_error(self):
        try:
            self.error_message = self.__response.json().get("message")
            self.error = self.__response.json()
        except Exception:
            # Handle when the response is not a json
            # and just a 404 or 500/02/03 error or HTML Page
            if self.status_code == 404:
                self.error_message = "Resource not found"
                self.error = {"message": "Not found"}
            else:
                self.error_message = "Internal server error"
                self.error = {"message": "Internal server error"}
        logger.error(
            f"external service error: {self.error_message} | {self.status_code}"
        )


class APIClient:
    """
    Base API client class for calling HTTP external API

    e.g.:
    client = APIClient()
    client.connect("<<username>>", "<<password>>")
    res = client.post("api/users/2", {})
    """

    def __init__(self):
        self.session = None

    def connect(self, username: str = None, password: str = None):
        self.session = Session(BasicAuthentication.get_access_token(username, password))

    def build_url(self, path: str):
        return f"{self.session.base_url}/{path}"

    def post(self, path: str, data: dict) -> dict:
        return self._run_request("post", path, data)

    def get(self, path: str, params: dict = None) -> dict:
        return self._run_request("get", path, params=params)

    def update(self, path: str, data: dict = None) -> dict:
        return self._run_request("put", path, data)

    def delete(self, path: str, data: dict = None) -> dict:
        return self._run_request("delete", path)

    def patch(self, path: str, data: dict) -> dict:
        return self._run_request("patch", path, data)

    def _run_request(
        self, name: str, path: str, data: dict = None, params: dict = None
    ) -> Response:
        request = getattr(self.session, name)
        url = self.build_url(path)
        logger.info(f"Calling external {name.upper()} API request: {url}")
        raw_response = request(url, json=data, params=params)
        logger.info(f"Response from external API: {raw_response}")
        response = Response(raw_response)

        return response
