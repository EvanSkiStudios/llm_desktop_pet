import os
import asyncio
from dotenv import load_dotenv
from ollama import chat

from utility_scripts.system_logging import setup_logger

# --- Logger ---
logger = setup_logger(__name__)

# --- Environment ---
load_dotenv()
os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API")

# --- LLM model ---
llm_model = 'gemma4:31b-cloud'
# llm_model = 'ISABEL:latest'
messages = []


# --- Main async chat function ---
async def llm_chat(user_prompt, photos=None, system_prompt=None):
    global messages

    print('Thinking...')

    if photos is not None:
        user_response = {'role': 'user', 'content': user_prompt, 'images': photos}
    else:
        user_response = {'role': 'user', 'content': user_prompt}

    if system_prompt is not None:
        system_messages = [
            {'role': 'system', 'content': system_prompt},
            *messages,
            user_response
        ]
    else:
        system_messages = [
            *messages,
            user_response
        ]

    response = await asyncio.to_thread(
        chat,
        model=llm_model,
        messages=system_messages,
        options={
            'num_ctx': 16384,
            'temperature': 0.6,
            'think': False
        },
        stream=False
    )

    messages += [
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': response.message.content},
    ]

    # DANGER
    if photos is not None:
        for image in photos:
            os.remove(image)

    return response.message.content


if __name__ == "__main__":
    while True:
        user_input = input("> ")
        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
