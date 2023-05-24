#!/usr/bin/python
import concurrent.futures
import os
import sys
import time
from sys import stdout

import openai
from dotenv import load_dotenv
from tqdm import tqdm


def configure() -> None:
    """Loading environment variable from env file"""
    load_dotenv()


GENERATED_TEST_FILE_LOCATION = "ai/tests/generated_test_file.py"

messages: list[dict[str, str]] = []
system_message = {
    "role": "system",
    "content": """your name is TestBot. you are a software tester. 
                    Your focus is in building and developing automation tools 
                    to perform software testing""",
}

messages.append(system_message)
configure()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_bot(question: str) -> str:
    """
    This method interacts with openapi
    :param question: question that needs to be asked to the gpt model. (type: str)
    """
    global messages
    messages.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
    )
    chat_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response


def extract_code(text) -> str:
    """
    extract the code snippet from between gpt response
    """
    print(text)
    CODE_SEPARATOR = "```"
    start_index = text.find(CODE_SEPARATOR) + 3
    end_index = text.find(CODE_SEPARATOR, start_index)
    if start_index == -1 or end_index == -1:
        return None

    if start_index == -1:
        return None

    return text[start_index:end_index]


def send_command_to_openapi_and_display_progress_bar(command: str, sleep_time=1):
    print("hold on. waiting for a response.. \n")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(chat_bot, command)
        with tqdm(
            total=100, ncols=80, unit="%", bar_format="{percentage:.0f}%|{bar}|"
        ) as progress_bar:
            while not future.done():
                time.sleep(sleep_time)
                progress_bar.update(1)
            return future.result()


def generate_tests() -> str:
    """Generating automated tests by reading yaml files"""
    file_location = input("\nOk. Give me the location to your swagger yaml file.. -> ")
    print(f"\nSchema file location  -> {file_location} \n ", file=stdout)

    try:
        with open(file_location, "r", -1, encoding="utf_8") as file:
            contents = file.read()
            command = f"provide automated tests written in python for this swagger specs : \n {contents}"
            test_code = send_command_to_openapi_and_display_progress_bar(command)
            return extract_code(test_code)
    except FileNotFoundError:
        print("File not found, please check the file path.")
        sys.exit(2)


def write_file(content: str) -> None:
    """Writing contents into a file"""
    os.makedirs(os.path.dirname(GENERATED_TEST_FILE_LOCATION), exist_ok=True)

    try:
        with open(GENERATED_TEST_FILE_LOCATION, "w", -1, encoding="utf_8") as file:
            file.write(content)
            file.close()
    except FileNotFoundError:
        print("Writing tests to file failed. Please try again later", file=sys.stderr)


def display_user_prompts() -> str:
    user_input = input(
        """\n Pick an option?: 
            1) Ask questions interactively
            2) Generate tests
            3) Generate Code snippets
            4) Quit

            (1/2/3/4) ? --> """
    )
    return user_input


def main():
    user_input = ""
    while True:
        user_input = display_user_prompts()

        match user_input:
            case "1":
                while True:
                    command = input("\n ask away -> ")
                    if user_input.lower() == "quit":
                        print("\n bye..See you later \n")
                        sys.exit()
                    if command.lower() == "return":
                        break
                    answer_from_ai = send_command_to_openapi_and_display_progress_bar(
                        command
                    )
                    print(f"\n {answer_from_ai}")
            case "2":
                code = generate_tests()
                if code is None:
                    print("Error, tests could not be generated, try again", sys.stderr)
                print(f"Generated tests -> \n {code}")
                print(
                    f"\n Tests are generated in a file located here -> {GENERATED_TEST_FILE_LOCATION} \n"
                )
                write_file(code)
            case "3":
                print(3)
            case "4":
                print("\n bye..See you later \n")
                sys.exit()
            case _:
                print("Type a number 1-3")
                continue


if __name__ == "__main__":
    main()
