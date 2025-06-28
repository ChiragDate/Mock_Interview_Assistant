from utils.config import GROQ_API_KEY

# from langchain.chat_models import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage

# def generate_completion(prompt: str, model: str = "llama3-8b-8192", max_tokens: int = 500, temperature: float = 0.7) -> str:
#     """Generates text completion using LangChain's ChatGroq."""
#     try:
#         # Initialize the ChatGroq model
#         chat = ChatGroq(
#             model=model,
#             temperature=temperature,
#             max_tokens=max_tokens
#         )

#         # Construct the conversation
#         messages = [
#             SystemMessage(content="You are a helpful AI assistant."),
#             HumanMessage(content=prompt)
#         ]

#         # Generate the response
#         response = chat(messages)

#         # Return the content safely
#         if response.content:
#             return response.content.strip()
#         else:
#             print("Warning: LLM response content is empty.")
#             return "Error: No content in response."

#     except Exception as e:
#         print(f"Error during LangChain-Groq call: {e}")
#         return f"Error: Could not generate completion - {e}"


from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def generate_completion(prompt: str, model: str = "llama3-8b-8192", max_tokens: int = 500, temperature: float = 0.7) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
