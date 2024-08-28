from faker import Faker
import pytest

from help_metods.helper_metods import auth_user, go_to_page, register_user
from models.spend import SpendAdd

fake = Faker()


@pytest.mark.parametrize('category', ["school"], indirect=True)
@pytest.mark.parametrize('spends', [
    SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 1",
        category="school",
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB"
    )
], indirect=True)
def test_spending_should_be_deleted_after_table_action(browser_page, spends, category):
    browser_page.reload()
    browser_page.wait_for_selector('.spendings-table tbody', timeout=10000)
    element_text = browser_page.locator('.spendings-table tbody').text_content()
    assert 'QA.GURU Python Advanced 1' in element_text


@pytest.mark.parametrize('category', ["test_category"])
def test_add_category(auth, browser_page, category):
    browser_page.click('a.header__link[href="/profile"]')
    browser_page.fill('input[name=category]', category)
    browser_page.locator('button.button', has_text='Create').click()
    element_text = browser_page.locator('ul.categories__list').text_content()
    assert 'test_category' in element_text


def test_auth_invalid_creds(browser_page, envs):
    go_to_page(browser_page, envs.frontend_url_login, "login")
    browser_page.click('a[href*=redirect]')
    auth_user(browser_page, username="1111", password="2222")
    element_text = browser_page.locator('p.form__error').text_content()
    assert 'Bad credentials' in element_text


def test_register_new_user(browser_page, envs):
    go_to_page(browser_page, envs.frontend_url_login, route="login")
    browser_page.click('a[href*=register]')
    register_user(browser_page, username=fake.name(), password="2222", password_sub="2222")
    element_text = browser_page.locator('.form > p.form__paragraph:first-of-type').text_content()
    assert "Congratulations! You've registered!" == element_text


def test_auth_with_register_user(browser_page, envs, register):
    name = register
    auth_user(browser_page, username=name, password=envs.test_password)
    element_text = browser_page.locator('.main-content').text_content()
    assert 'History of spendings' in element_text


def test_register_invalid_pass(browser_page, envs):
    go_to_page(browser_page, envs.frontend_url_login, route="login")
    browser_page.click('a[href*=register]')
    register_user(browser_page, username=fake.name(), password="2222", password_sub="2223")
    element_text = browser_page.locator('span.form__error').text_content()
    assert 'Passwords should be equal' in element_text
    browser_page.click('a[href*=redirect]')


def test_check_tab_friends(browser_page, envs, auth):
    browser_page.click('a[href*=friends]')
    element_text = browser_page.locator('section.main-content__section div').text_content()
    assert 'There are no friends yet!' in element_text


@pytest.mark.parametrize('name, surname', [("test_name", "test_surname")])
def test_save_profile_info(browser_page, envs, register, name, surname):
    user_name = register
    auth_user(browser_page, username=user_name, password=envs.test_password)
    browser_page.click('a[href*=profile]')
    browser_page.fill('input[name=firstname]', name)
    browser_page.fill('input[name=surname]', surname)
    browser_page.click('div.select-wrapper')
    browser_page.click('div[role="option"]:has-text("RUB")')
    browser_page.click('button[type=submit]')
    toast_message = browser_page.wait_for_selector(
        'div.Toastify__toast-body > div:has-text("Profile successfully updated")')
    assert toast_message.is_visible(), "Сообщение о успешном обновлении профиля не найдено."


@pytest.mark.parametrize('amount, date, description', [("222", "test_test", "27/08/2024")])
@pytest.mark.parametrize('category', ["test"])
def test_add_new_spending(browser_page, envs, auth, category, amount, date, description):
    browser_page.click('div.select-wrapper')
    browser_page.click('div[role="option"]:has-text("test")')
    browser_page.fill('input[name=amount]', amount)
    browser_page.fill('div.calendar-wrapper', date)
    browser_page.click('a[href*=main]')
    browser_page.fill('input[name=description]', description)
    browser_page.click('button[type=submit]')
    toast_message = browser_page.wait_for_selector(
        '.Toastify__toast-body > div:has-text("Spending successfully added")')
    assert toast_message.is_visible(), "Сообщение о успешном обновлении профиля не найдено."
