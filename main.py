# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

app = FastAPI()

# 1. إعدادات CORS للسماح بالاتصال من الواجهة الأمامية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. مسار ترحيبي جذري لمنع ظهور Not Found عند فتح الرابط الرئيسي
@app.get("/")
def home():
    return {"status": "Iron-AI Backend is running successfully!"}

@app.options("/chat")
def options_chat():
    return {}

# 3. نقطة الاتصال الرئيسية للدردشة
@app.post("/chat")
def chat(payload: dict):
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"error": "OPENAI_API_KEY is missing in environment variables"}

        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )

        user_message = payload.get("message", "")
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": user_message}]
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# 4. ربط المنفذ لمنصة Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)