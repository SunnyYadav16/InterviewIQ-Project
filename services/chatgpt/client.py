import openai
from datetime import datetime

from InterviewIQ.settings import OPENAI_KEY


class ChatGPT:
    def __init__(self, prompt, api_key=OPENAI_KEY, n=1, model="gpt-4"):
        openai.api_key = api_key
        self.prompt = prompt
        self.model = model
        self.n = n
        self._get_completion()
        self._id = self.response["id"]
        self._created_at = datetime.fromtimestamp(self.response["created"])

    def _get_completion(self):
        self.response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": self.prompt}],
            n=self.n
        )
        return self.response

    def get_answers(self) -> list:
        """Get the answers from ChatGPT Model

        Returns:
            list: List containing string with answers len of list depends on n
        """
        response = [choice["message"]["content"] for choice in self.response["choices"]]
        return response

    def get_usage(self) -> dict:
        """Returns token used for completion of given prompt

        Returns:
            dict: dict contains completion_tokens, prompt_tokens, total_tokens
        """
        return self.response["usage"]

    @property
    def id(self) -> str:
        """Returns the generated id

        Returns:
            str: id from ChatGPT API
        """
        return datetime.fromtimestamp(self.response["created"])

    @property
    def created_at(self):
        """Returns the generated datetime object in local time

        Returns:
            datetime: datetime object created from timestamp from ChatGPT API
        """
        return datetime.fromtimestamp(self.response["created"])
