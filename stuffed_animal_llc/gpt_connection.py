import requests

class GPT_Connection():
    def __init__(self):
        self.url = 'https://api.llm.palantir.tech/preview/openai/deployments/gpt-4/chat/completions'
        self.system_content = "Assistant is a large language model trained by OpenAI."
        self.headers = {
            "Content-Type": "application/json",
            "api-key": "c36f6f565d584058be30acea7d7282c3",
            "Cache-Control": "no-cache"
        }

    def make_request(self, prompt):
        # Make Requests
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.url, json=data, headers=self.headers)

        try:
            response_text = response.json()['choices'][0]['message']['content']
        except Exception as e:
            print("Error with GPT 4 Request, ", response.json())
            response_text = ""
        return response_text
