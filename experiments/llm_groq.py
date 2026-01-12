from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

def grok_answer(question: str) -> str:
    try:
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.4
        )

        prompt = f"""
You are an intelligent AI assistant.
Answer clearly with detailed explanation.

Question:
{question}
"""
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    except Exception as e:
        return "⚠️ AI service error. Please try again later."
