import os
from sys import stdout

import openai
from dotenv import load_dotenv


def configure() -> None:
    """Loading environment variable from env file"""
    load_dotenv()


messages: list[dict[str, str]] = []
system_message = {
    "role": "system",
    "content": """you are a software tester. 
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
    messages.append({"role": "user", "content": question})

    print(f"questions_history -> {messages}")

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    chat_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response


def generate_tests() -> None:
    """Generating automated tests by reading yaml files"""
    file_location = input("Enter file location to the swagger yaml file : \n")
    print(f" File name -> {file_location} \n ", file=stdout)

    try:
        with open(file_location, "r", -1, encoding="utf_8") as file:
            contents = file.read()
            test_code = chat_bot(
                f"provide automated tests written in python for this swagger specs : \n {contents}"
            )
            print(f"List of tests -> {test_code}")
    except FileNotFoundError:
        print("File not found, please check the file path.")


user_input = ""
while True:
    user_input = input(
        """ Pick an option?: 
        1) Ask questions interactively
        2) Generate tests
        3) Generate Code snippets

        (1/2/3) ? : """
    )
    chosen_option: str = ""

    match user_input:
        case "1":
            chosen_option = "ask"
            break
        case "2":
            chosen_option = "generate tests"
            generate_tests()
            break
        case "3":
            chosen_option = "code"
            break
        case _:
            print("Type a number 1-3")
            continue


# def main() -> None:
#     """Main function"""
#     print("$$$$$ MAIN FUNCTION")
#     configure()


# if __name__ == "__main__":
#     main()
