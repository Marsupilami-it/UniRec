import os
import sys

from ml.llm_client import LLMClient
from ml.llm_handler import LLMHandler


def find_societies_by_link(link):
    model_name = os.getenv('MODEL_NAME', 'Maoyue/c4ai-command-r7b-12-2024')
    llm_client = LLMClient(model_name)
    llm_handler = LLMHandler(llm_client)

    prompt = "Исходя из названия самой ссылки, найди аналогичные сообщества и перечисли их, обращай внимание именно на конец ссылки."
    return llm_handler.process_link(link, prompt)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        link = sys.argv[1]
    else:
        link = "https://vk.com/fincultinfo"

    answer = find_societies_by_link(link)
    print(answer)
    