import os
import sys

from llm_client import LLMClient
from llm_handler import LLMHandler


def main():
    model_name = os.getenv('MODEL_NAME', 'Maoyue/c4ai-command-r7b-12-2024')
    llm_client = LLMClient(model_name)
    llm_handler = LLMHandler(llm_client)

    if len(sys.argv) > 1:
        link = sys.argv[1]
    else:
        link = "https://vk.com/fincultinfo"

    prompt = "Исходя из названия самой ссылки, найди аналогичные сообщества и перечисли их, обращай внимание именно на конец ссылки."
    answer = llm_handler.process_link(link, prompt)
    if answer:
        print(answer)


if __name__ == "__main__":
    main()