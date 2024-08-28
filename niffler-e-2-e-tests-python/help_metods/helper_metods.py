import logging

logger = logging.getLogger("__name__")


def auth_user(browser_page, username, password):
    if browser_page.locator('button.button-icon_type_logout').is_visible():
        browser_page.locator('button.button-icon_type_logout').click()
    else:
        browser_page.fill('input[name=username]', username)
        browser_page.fill('input[name=password]', password)
        browser_page.click('button[type=submit]')


def register_user(browser_page, username, password, password_sub):
    if browser_page.locator('button.button-icon_type_logout').is_visible():
        browser_page.locator('button.button-icon_type_logout').click()
    else:
        browser_page.fill('input[name=username]', username)
        browser_page.fill('input[name=password]', password)
        browser_page.fill('input[name=passwordSubmit]', password_sub)
        browser_page.click('button[type=submit]')


def go_to_page(browser_page, url, route=None):
    browser_page.goto(f"{url}/{route}")
    logger.info(f"Go to URK: {url}/{route}")
    return browser_page


def check_text(browser_page, locator, ecx_text):
    paragraphs = browser_page.locator(locator)
    # Перебираем все найденные элементы и проверяем их текст
    for i in range(paragraphs.count()):
        if paragraphs.nth(i).text_content() == ecx_text:
            print(f"Текст найден в элементе {i + 1}")
            return paragraphs.nth(i).text_content()
        else:
            return None

