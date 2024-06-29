from typing import Literal

from langchain.agents import tool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from app.common.logging.loggers import file_logging
from app.services.selenium.webdriver import SingletonWebDriver
from app.services.utils.selenium_util import (
    extract_and_clean_all_tags,
    extract_and_clean_tags,
)

singleton_webdriver = SingletonWebDriver()
driver = singleton_webdriver.get_driver()

selenium_selectors = {
    "css_selector": By.CSS_SELECTOR,
    "xpath": By.XPATH,
}


@tool
def get_all_html_tags() -> str:
    """Return the full HTML code for a page, DON'T use this tool unless if the user request is not doable"""
    body = driver.find_element(By.TAG_NAME, "body")
    body = body.get_attribute("outerHTML")
    clean_tags = extract_and_clean_all_tags(body)
    return clean_tags


@tool
def get_html_tags(action_type: Literal["type", "press"]) -> str:
    """Return related HTML tags to search from based on the action, the action could ONLY be type or press"""
    if action_type == "type":

        inputs = driver.find_elements(By.TAG_NAME, "input")
        inputs_html = [
            input_element.get_attribute("outerHTML") for input_element in inputs
        ]
        clean_inputs = extract_and_clean_tags(inputs_html)

        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        textareas_html = [
            textarea_element.get_attribute("outerHTML")
            for textarea_element in textareas
        ]
        clean_textareas = extract_and_clean_tags(textareas_html)
        return [clean_inputs, clean_textareas]

    elif action_type == "press":

        a = driver.find_elements(By.TAG_NAME, "a")
        a_html = [a_element.get_attribute("outerHTML") for a_element in a]
        clean_a = extract_and_clean_tags(a_html)

        buttons = driver.find_elements(By.TAG_NAME, "button")
        buttons_html = [
            button_element.get_attribute("outerHTML") for button_element in buttons
        ]
        clean_buttons = extract_and_clean_tags(buttons_html)
        return [clean_a, clean_buttons]


@tool
def do_action(
    action_type: Literal["type", "press", "excute_js"],
    selector: Literal["css_selector", "xpath"],
    selector_value: str,
    input: str,
) -> str:
    """
    Do a selenium action, like press a button or type somthing in an input field, or excute js code on the current page.

    Args:
        action_type: The type of action to perform, it could be type, press or excute_js.
        selector: The selector type to use, it should be css_selector or xpath ONLY.
        selector_value: The value of css_selector or xpath to use.
        input: The input to type in the input field, if the action_type is press, set this to an empty string, and if the action_type is excute_js set this to js code.
    """
    try:
        if action_type == "type":
            actions = ActionChains(driver)
            type = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (selenium_selectors[selector], selector_value)
                )
            )
            actions.move_to_element(type).click().send_keys(input).perform()

        elif action_type == "press":
            actions = ActionChains(driver)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (selenium_selectors[selector], selector_value)
                )
            )
            actions.move_to_element(button).click().perform()
        elif action_type == "excute_js":
            driver.execute_script(input)

        return "action done successfully"

    except Exception as e:
        file_logging.warning(e)
        return "error occurred while doing the action, please check the values and try again"


tools = [get_html_tags, do_action, get_all_html_tags]
