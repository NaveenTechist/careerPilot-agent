from llm.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate("Say Hello.")

print(response)
