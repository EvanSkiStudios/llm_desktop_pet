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
llm_model = 'huihui_ai/deepseek-r1-abliterated'
messages = []


# --- Main async chat function ---
async def llm_chat(user_prompt):
    global messages

    response = await asyncio.to_thread(
        chat,
        model=llm_model,
        messages=[
            {'role': 'system', 'content': 'You are a Rat that has infinite wisdom. Keep your responses short and concise.'},
            *messages,
            {'role': 'user', 'content': user_prompt}
        ],
        options={
            'num_ctx': 16384,
            'temperature': 0.5,
            'think': False
        },
        stream=False
    )

    messages += [
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': response.message.content},
    ]

    return response.message.content


if __name__ == "__main__":
    while True:
        user_input = input("> ")
        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
