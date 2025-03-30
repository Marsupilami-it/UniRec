from ollama import Client


class LLMClient:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = Client()

    def ask(self, prompt):
        try:
            response = self.client.generate(model=self.model_name, prompt=prompt, stream=False)
            return response['response']
        except Exception as e:
            print(f"Ошибка при взаимодействии с моделью: {e}")
            return None