#!/usr/bin/python

import concurrent.futures
import os
import time

import openai
from dotenv import load_dotenv
from tqdm import tqdm

openai.api_key = "YOUR_API_KEY"

prompt = "Hello, how are you?"
temperature = 0.7
length = 30

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_text(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=temperature,
        max_tokens=length,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text


print("hmmm. let me think! \n")
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(generate_text, prompt, openai.api_key)
    with tqdm(
        total=100,
        ncols=80,
        unit="%",
        bar_format="{percentage:.0f}%|{bar}|",
    ) as progress_bar:
        while not future.done():
            time.sleep(0.1)
            progress_bar.update(1)
        text = future.result()
        if text.endswith("\n"):
            text = text[:-1]
        prompt += text
        progress_bar.update(100 - progress_bar.n)

print(prompt)
