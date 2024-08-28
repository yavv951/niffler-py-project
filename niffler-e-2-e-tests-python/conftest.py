import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from playwright.sync_api import sync_playwright

from clients.spends_client import SpendsHttpClient
from databases.spends_clients import SpendDb
from help_metods.helper_metods import auth_user, go_to_page, register_user
from models.config import Envs

fake = Faker()


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD"),
        frontend_url_login=os.getenv("FRONTEND_URL_LOGIN")
    )


@pytest.fixture()
def auth(envs, browser_page):
    browser_page.goto(envs.frontend_url)
    browser_page.locator('a[href*=redirect]').click()
    auth_user(browser_page, username=envs.test_username, password=envs.test_password)
    browser_page.wait_for_function("window.sessionStorage.getItem('id_token') !== null", timeout=5000)
    token = browser_page.evaluate("() => window.sessionStorage.getItem('id_token')")
    return token


@pytest.fixture()
def register(envs, browser_page):
    go_to_page(browser_page, envs.frontend_url_login, route="login")
    browser_page.click('a[href*="/register"]')
    user_name = fake.name()
    register_user(browser_page, username=user_name, password=envs.test_password, password_sub=envs.test_password)
    browser_page.click('a[href*="/redirect"]')
    yield user_name


@pytest.fixture()
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture()
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture()
def category(request, spends_client, spend_db):
    name = request.param
    category = spends_client.add_category(name)
    yield category.category
    spend_db.delete_categories(category.id)


@pytest.fixture()
def spends(request, spends_client, category):
    data = request.param
    data.category = category
    test_spend = spends_client.add_spends(data)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture()
def browser_page(spend_db):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()
