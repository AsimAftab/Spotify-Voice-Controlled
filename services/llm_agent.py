import requests

class LLMAgent:
    def __init__(self, model_url="http://localhost:11434/api/generate"):
        self.model_url = model_url

    def query_llm(self, prompt):
        response = requests.post(
            self.model_url,
            json={
                "model": "mistral",
                "prompt": f"Extract the song name from this command: '{prompt}'. Just return the song name, nothing else."
            },
            stream=True
        )

        collected = ""
        for line in response.iter_lines():
            if line:
                part = line.decode('utf-8')
                try:
                    json_part = eval(part)  # quick JSON-safe workaround
                    if 'response' in json_part:
                        collected += json_part['response']
                except:
                    pass

        return collected.strip()
