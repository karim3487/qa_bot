import requests


# def send_message_to_api_sync(message_text):
#     url = ""
#     data = {'message': message_text}
#
#     response = requests.post(url, data=data)
#     result = response.json()
#     return result

# def add_answer(answer):
#     url = ""
#     data = {'answer': answer}
#
#     response = requests.post(url, data=data)
#     result = response.json()
#     return result


def send_message_to_api(message_text: str) -> int:
    """
    Sends the provided message to an API.

    Args:
        message_text (str): The text to be sent to the API.

    Returns:
        int: An integer code indicating the result of the operation.
            - 1 if the input is a question and there is a response available in the system.
            - 2 if the input is a question, but there is no response available in the system.
            - 3 if the input is not a question.

    This function sends the input message to an external API for processing. If the text is determined
    to be a question and a corresponding response exists in the system, it returns 1. If it's a
    question with no available response, it returns 2. If the input is not a question, it returns 3.
    """
    match message_text:
        case "a":
            return 1
        case "b":
            return 2
        case "c":
            return 3


def add_answer(answer):
    return {'status_code': 200}
