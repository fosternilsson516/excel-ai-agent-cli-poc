import google.generativeai as genai
from config import Config

class promptAPICaller:
    def __init__(self):
        config = Config()
        self.api_key = config.get_env_var("GEMINI_API_KEY")
        self.endpoint = config.get_env_var("GEMINI_ENDPOINT")       

    def create_prompt(self, query, prompt_prefix, metadata):
        """Creates a prompt for the Gemini API using the extracted metadata and query."""
        prompt = (
            f"{prompt_prefix}\n"
            f"Query: {query}\n"
            f"Metadata:\n{metadata}"
        )
        return prompt      

    def call_gemini_api(self, prompt):
        """Calls the Gemini API and returns the generated response text."""
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.endpoint)
        response = model.generate_content(prompt)
        return response.text          