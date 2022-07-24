import os

from gen3config import Config

DEFAULT_CFG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config-default.yaml"
)

print(DEFAULT_CFG_PATH)

class ChatbotConfig(Config):
    def __init__(self, *args, **kwargs):
        super(ChatbotConfig, self).__init__(*args, **kwargs)
        self["MAXIMUM_REQUEST_LENGTH"] = 50


config = ChatbotConfig(DEFAULT_CFG_PATH)
