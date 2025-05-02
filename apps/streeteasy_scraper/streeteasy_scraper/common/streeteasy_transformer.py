import bs4
from db.models import Address
from dataclasses import dataclass


@dataclass
class Unit:
    name: str | None = None
    address: str | None = None


class StreetEasyTransformer:
    def __init__(self):
        pass

    def get_address_data(self, html: str, address: Address) -> Address:
        soup = bs4.BeautifulSoup(html, "html.parser")

        # Get unit data
        unit_data = self.get_unit_data(soup)

        if not unit_data:
            address.status = "success"
            return address

        return address

    @staticmethod
    def get_unit_data(soup: bs4.BeautifulSoup) -> Unit | None:
        building_summary = soup.find(
            "section", attrs={"data-testid": "building-summary-component"}
        )

        if not building_summary:
            return

        unit_name_tag = building_summary.find("h1")
        unit_name = unit_name_tag.get_text(strip=True) if unit_name_tag else None

        unit_address_tag = building_summary.find("h2")
        unit_address = (
            unit_address_tag.get_text(strip=True) if unit_address_tag else None
        )

        return Unit(unit_name, unit_address)

    @staticmethod
    def _has_active_listing() -> bool:
        pass

    @staticmethod
    def _is_address_match() -> bool:
        pass
