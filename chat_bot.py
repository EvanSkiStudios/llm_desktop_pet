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
messages = []


# --- Main async chat function ---
async def llm_chat(user_prompt, photo=None):
    global messages

    print('Thinking...')

    if photo is not None:
        user_response = {'role': 'user', 'content': user_prompt, 'images': [photo]}
    else:
        user_response = {'role': 'user', 'content': user_prompt}

    response = await asyncio.to_thread(
        chat,
        model=llm_model,
        messages=[
            # {'role': 'system', 'content': 'You are a Rat that has infinite wisdom. Keep your responses short and concise.'},
            *messages,
            user_response
        ],
        options={
            'num_ctx': 16384,
            'temperature': 0.6,
            'think': True
        },
        stream=False
    )

    messages += [
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': response.message.content},
    ]

    # DANGER
    os.remove(photo)

    return response.message.content


if __name__ == "__main__":
    while True:
        user_input = input("> ")
        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
