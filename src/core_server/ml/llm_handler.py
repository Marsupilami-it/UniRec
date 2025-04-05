from ml.llm_client import LLMClient


class LLMHandler:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def process_link(self, link, prompt):
        prompt_with_link = f"{prompt} Ссылка: {link}"
        return self.llm_client.ask(prompt_with_link)
