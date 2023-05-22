import getopt
import os
import sys

import openai
from dotenv import load_dotenv


def configure() -> None:
    """Loading environment variable from env file"""
    load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def show_options() -> None:
    """
    This function displays different option about how this script can be used
    """
    user_prompt: str = "Usage: python testbot.py -i <inputfile> -o <outputfile>"
    if len(sys.argv) != 2:
        print(
            f"Error! Invalid number of arguments provided. Correct {user_prompt}",
            file=sys.stderr,
        )
        sys.exit(0)
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(user_prompt)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: python testbot.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print(f"ifile name is : {arg}")
        elif opt in ("-o", "--ofile"):
            print(f"ofile name is : {arg}")


def main() -> None:
    """Main function"""
    configure()
    show_options()


if __name__ == "__main__":
    main()
