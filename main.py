# -*- coding: utf-8 -*-
from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

# الاتصال بـ Groq API عبر OpenAI SDK
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.post("/chat")
def chat(payload: dict):
    try:
        user_message = payload.get("message", "")
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": user_message}]
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error_details": str(e)}