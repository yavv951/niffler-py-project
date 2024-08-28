import logging
from urllib.parse import urljoin

import requests

from models.spend import Spend, SpendAdd, Category

logger = logging.getLogger("__name__")


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def __str__(self):
        return f"SpendsHttpClient(base_url={self.base_url})"

    def __repr__(self):
        return f"SpendsHttpClient(base_url={self.base_url}, session_id={id(self.session)})"

    def get_categories(self) -> list[Category]:
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        logger.info(f"Response body: {response}")
        response.raise_for_status()
        return response.json()

    def get_spends(self) -> list[Spend]:
        url = urljoin(self.base_url, "/api/spends/all")
        logger.info(f"URL: {url}")
        response = self.session.get(url)
        logger.info(f"Response: {response.status_code}")
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> Category:
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            "category": name
        })
        logger.info(f"Response: {response.status_code}")
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    def add_spends(self, spend: SpendAdd):
        url = urljoin(self.base_url, "/api/spends/add")
        logger.info(f"URL: {url} "
                    f"and request body: {spend}")
        response = self.session.post(url, json=spend.model_dump())
        logger.info(f"Response status: {response.status_code}")
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/spends/remove")
        logger.info(f"URL: {url}")
        response = self.session.delete(url, params={"ids": ids})
        logger.info(f"Response: {response.status_code}")
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
