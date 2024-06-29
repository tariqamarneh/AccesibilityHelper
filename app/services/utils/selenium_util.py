import re
from bs4 import BeautifulSoup, Comment


def extract_and_clean_tags(html_list):
    allowed_tags = ["a", "button", "input", "textarea"]
    cleaned_html_list = []

    for html in html_list:
        soup = BeautifulSoup(html, "html.parser")

        extracted_elements = []
        for tag in allowed_tags:
            for element in soup.find_all(tag):
                for nested in element.find_all(True):
                    if nested.name not in allowed_tags:
                        nested.unwrap()

                for comment in element.find_all(
                    string=lambda text: isinstance(text, Comment)
                ):
                    comment.extract()

                element_text = " ".join(element.stripped_strings)

                new_element = soup.new_tag(element.name)
                for attr, value in element.attrs.items():
                    new_element[attr] = value
                new_element.string = element_text

                element_string = str(new_element)
                element_string = re.sub(r"\n+", "\n", element_string)
                element_string = re.sub(r"(?<=>)\s+|\s+(?=<)", "", element_string)

                extracted_elements.append(element_string)

        cleaned_html_list.append("\n".join(extracted_elements))

    return cleaned_html_list


def extract_and_clean_all_tags(html_body):
    excluded_tags = ["svg", "path", "script", "style"]

    soup = BeautifulSoup(html_body, "html.parser")

    for tag in excluded_tags:
        for element in soup.find_all(tag):
            element.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    def unwrap_nested(element):
        for child in element.find_all(True):
            unwrap_nested(child)
            if child.name not in excluded_tags:
                for nested in child.find_all(True):
                    if nested.name in excluded_tags:
                        nested.decompose()
                    else:
                        nested.unwrap()
                child.string = " ".join(child.stripped_strings)

    for element in soup.body.find_all(True):
        unwrap_nested(element)

    cleaned_html = soup.prettify()
    cleaned_html = re.sub(r"\n+", "\n", cleaned_html)
    cleaned_html = re.sub(r"(?<=>)\s+|\s+(?=<)", "", cleaned_html)

    return cleaned_html
