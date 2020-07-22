import re
import os
import time
import csv
from enum import Enum

import pytest


class FAQ_STATUS_CODES(Enum):
    NOT_TESTED = 0
    EXPECTED_ANSWER = 1
    SUGGESTION_LIST_EXPECTED_ANSWER = 2
    UNEXPECTED_ANSWER = 3
    SUGGESTION_LIST_UNEXPECTED_ANSWER = 4
    TIMEOUT_WAITING_FOR_REPLIES = 5
    SUGGESTION_LIST_TIMEOUT_WAITING_FOR_REPLIES = 6


EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U0001f9fc"
                           "🤧"
                           u"\u200d"
                           "✉️"
                           "☝"
                           "®"
                           "✅"
                           "]+", flags=re.UNICODE)
char_groups = "a-zA-Z0-9\w\s\d\(\)\!\¡\?\¿áéíóúÁÉÍÓÚ\.\-#,:ñ@"
BOLD_FORMAT_PATTERN = "\*[" + char_groups + "]+\*"
ITALICS_FORMAT_PATTERN = r"_[" + char_groups + "]+_"


def wa_faqs_semantic_search(
        cms_api, bot_slug,
        botrunner_api,
        user_id, faq_state,
        selenium_wa_page,
        faq_tests_dir
):
    pass_dir, fail_dir = create_faqs_dirs(faq_tests_dir)
    # Create tests dir if it doesn't exists:
    bot_semantic = cms_api.get_semantic_search(bot_slug)
    faqs = cms_api.get_questions_and_answers(bot_semantic)
    for key, value in faqs.items():
        value["key"] = key
        value["cleaned_answer"] = string_cleaner(value["answer"]).strip()
        value["received_answer"] = ""
        value["result_code"] = FAQ_STATUS_CODES.NOT_TESTED.value
        value["result_code_description"] = FAQ_STATUS_CODES.NOT_TESTED.name
    for key, value in faqs.items():
        do_faq(
            key, value, selenium_wa_page,
            botrunner_api, user_id, faq_state,
            faq_tests_dir
        )

    return faqs


def create_faqs_dirs(faq_tests_dir):
    os.makedirs(faq_tests_dir, exist_ok=True)
    pass_dir = os.path.join(faq_tests_dir, "PASS")
    os.makedirs(pass_dir, exist_ok=True)
    fail_dir = os.path.join(faq_tests_dir, "FAIL")
    os.makedirs(fail_dir, exist_ok=True)
    return pass_dir, fail_dir


def string_cleaner(string):
    string = EMOJI_PATTERN.sub(r'', string)  # no emoji
    string = string.replace("\xa0", " ")
    bold_formats = re.findall(BOLD_FORMAT_PATTERN, string)
    for bold in bold_formats:
        string = string.replace(bold, bold[1:-1])

    italic_formats = re.findall(ITALICS_FORMAT_PATTERN, string)

    for italic in italic_formats:
        string = string.replace(italic, italic[1:-1])

    return string


def do_faq(
        key, value, selenium_wa_page,
        botrunner_api, user_id, faq_state,
        faq_tests_dir
):
    pass_dir, fail_dir = create_faqs_dirs(faq_tests_dir)

    try:
        last_message = None
        messages = selenium_wa_page.get_all_messages_elements()
        if len(messages) > 0:
            last_message = messages[-1]
        botrunner_api.change_state(
            user_id=user_id,
            state_name=faq_state,
        )
        selenium_wa_page.send_and_wait_for_n(None, 1, last_element=last_message)
    except TimeoutError as e:
        return

    try:
        question = value["question"].strip()
        answer = value["cleaned_answer"]
        value["question"] = question
        selenium_wa_page.send_and_wait_for_n(question, 2)
        messages = selenium_wa_page.get_messages_texts_faqs(
            selenium_wa_page.get_all_messages_elements()[-2:]
        )
        value["received_answer"] = messages[0].strip()
        # Answer text doesn't match with expected message
        if messages[0].strip() != answer.strip():
            selenium_wa_page.driver.save_screenshot(
                os.path.join(fail_dir, f"{key}.png")
            )
            value["result_code"] = FAQ_STATUS_CODES.UNEXPECTED_ANSWER.value
            value["result_code_description"] = FAQ_STATUS_CODES.UNEXPECTED_ANSWER.name
        else:
            selenium_wa_page.driver.save_screenshot(
                os.path.join(pass_dir, f"{key}.png")
            )
            value["result_code"] = FAQ_STATUS_CODES.EXPECTED_ANSWER.value
            value["result_code_description"] = FAQ_STATUS_CODES.EXPECTED_ANSWER.name

    except TimeoutError as e:
        selenium_wa_page.driver.save_screenshot(
            os.path.join(fail_dir, f"{key}.png")
        )
        value["received_answer"] = selenium_wa_page.get_all_messages_elements()[-1].text.strip()
        # Validate if the answer contains the question.

        if question in value["received_answer"]:
            # Case 2 scenario
            #  question in suggestion list
            index = None
            # Separate by lines and clean empty lines
            for i, suggestion in enumerate([a for a in value["received_answer"].split("\n") if a][1:], 1):

                if question in suggestion:
                    index = i
                    break
            # Try except ...
            if index is not None:
                try:
                    selenium_wa_page.send_and_wait_for_n(str(index), 2)
                    messages = selenium_wa_page.get_messages_texts(
                        selenium_wa_page.get_all_messages_elements()[-2:]
                    )
                    value["received_answer"] = messages[0].strip()
                    if messages[0].strip() == answer.strip():
                        # Submit option and succeded
                        value["result_code"] = FAQ_STATUS_CODES.SUGGESTION_LIST_EXPECTED_ANSWER.value
                        value["result_code_description"] = FAQ_STATUS_CODES.SUGGESTION_LIST_EXPECTED_ANSWER.name
                    else:
                        # Tried option and failed
                        value["result_code"] = FAQ_STATUS_CODES.SUGGESTION_LIST_UNEXPECTED_ANSWER.value
                        value["result_code_description"] = FAQ_STATUS_CODES.SUGGESTION_LIST_UNEXPECTED_ANSWER.name
                except TimeoutError as e:
                    # Timeout (waiting for 2 messages)d
                    value["result_code"] = FAQ_STATUS_CODES.SUGGESTION_LIST_TIMEOUT_WAITING_FOR_REPLIES.value
                    value[
                        "result_code_description"] = FAQ_STATUS_CODES.SUGGESTION_LIST_TIMEOUT_WAITING_FOR_REPLIES.name
        else:
            # Timeout (waiting for 2 messages)
            value["result_code"] = FAQ_STATUS_CODES.TIMEOUT_WAITING_FOR_REPLIES.value
            value["result_code_description"] = FAQ_STATUS_CODES.TIMEOUT_WAITING_FOR_REPLIES.name


def create_faqs_dirs(faq_tests_dir):
    os.makedirs(faq_tests_dir, exist_ok=True)
    pass_dir = os.path.join(faq_tests_dir, "PASS")
    os.makedirs(pass_dir, exist_ok=True)
    fail_dir = os.path.join(faq_tests_dir, "FAIL")
    os.makedirs(fail_dir, exist_ok=True)
    return pass_dir, fail_dir


def write_results(
        file_path,
        results
):
    # Write csv
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["ID", "QUESTION", "EXPECTED ANSWER", "CLEANED ANSWER", "RECEIVED ANSWER", "RESULT CODE",
                             "RESULT CODE DESCRIPTION"])

        for result in results:
            csv_writer.writerow([
                result["key"],
                result["question"],
                result["answer"],
                result["cleaned_answer"],
                result["received_answer"],
                result["result_code"],
                result["result_code_description"],
            ])
