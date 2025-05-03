import re
from dataclasses import dataclass

import bs4
from db.models import Address

from streeteasy_scraper.config import Settings


@dataclass
class Unit:
    name: str | None = None
    address: str | None = None


class StreetEasyTransformer:
    def __init__(self, settings: Settings):
        self.settings = settings

    def update_address(self, html: str, address: Address) -> None:
        soup = bs4.BeautifulSoup(html, "html.parser")

        # Get unit data
        unit_data = self._get_unit_data(soup)

        if not unit_data:
            address.status = "success"
            return None

        # Get address data
        has_active_listing = self._has_active_listing(html)
        is_address_match = self._is_address_match(
            address.input_address, unit_data.address
        )

        # Update address
        address.streeteasy_unit_name = unit_data.name
        address.streeteasy_unit_address = unit_data.address
        address.has_active_listing = has_active_listing
        address.is_address_match = is_address_match
        address.status = "success"

    @staticmethod
    def _get_unit_data(soup: bs4.BeautifulSoup) -> Unit | None:
        building_summary = soup.find(
            "section", attrs={"data-testid": "building-summary-component"}
        )

        if not building_summary:
            return None

        assert isinstance(building_summary, bs4.element.Tag)

        unit_name_tag = building_summary.find("h1")
        unit_name = unit_name_tag.get_text(strip=True) if unit_name_tag else None

        unit_address_tag = building_summary.find("h2")
        unit_address = (
            unit_address_tag.get_text(strip=True) if unit_address_tag else None
        )

        return Unit(unit_name, unit_address)

    def _has_active_listing(self, html: str) -> bool:
        """Checks if html has no results"""
        lowered_html = html.lower()
        return not any(
            pattern.lower() in lowered_html
            for pattern in self.settings.NO_RESULTS_PATTERNS
        )

    def _is_address_match(self, input_address: str, unit_address: str | None) -> bool:
        if not unit_address:
            return False

        addresses = [input_address, unit_address]
        cleaned_addresses = [self._clean_address(address) for address in addresses]
        return len(set(cleaned_addresses)) == 1

    @staticmethod
    def _clean_address(address: str) -> str:
        pattern = re.compile(r"(?<=\d)(?:st|nd|rd|th)\b|\W+")
        return " ".join(pattern.sub(" ", address.lower()).split())
