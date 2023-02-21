import requests
import re

from settings import COLORS_WEBSITE_NAME, HEX_PREFIX, HEX_REGEX, WEBSITE_KEY


class ColorNamesCreator:
    def __init__(self):
        self.hex_reg = re.compile(HEX_REGEX)

    def validate_hex_color(self, color: str) -> bool:
        if self.hex_reg.match(color):
            return True
        return False

    def truncate_hex_name(self, color: str) -> str:
        if HEX_PREFIX in color:
            return color[2:]
        return color

    def request_color_name(self, color: str) -> str:
        color = self.truncate_hex_name(color)

        response = requests.get(COLORS_WEBSITE_NAME + WEBSITE_KEY + color)
        if response.status_code != 200:
            raise ValueError(f"Wrong response, status code: {response.status_code}.")

        color_name = response.json()['name']['value']

        return color_name


    