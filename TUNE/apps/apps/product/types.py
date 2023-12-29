from dataclasses import dataclass


@dataclass
class CatalogItem:
    product_id: int
    name: str
    params: dict = None
    provider_id: int = None

