from urllib.parse import urlencode


def input_address_to_url(input_address: str, streeteasy_base_url: str) -> str:
    encoded_params = urlencode({"utf8": "✓", "search": input_address, "commit": ""})
    return f"{streeteasy_base_url}?{encoded_params}"
