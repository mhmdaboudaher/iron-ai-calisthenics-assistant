import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ضع مفتاح Groq الجديد والفعال هنا
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
client = Groq(api_key=GROQ_API_KEY)

try:
    with open("Knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_base = f.read()
except Exception:
    knowledge_base = ""

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # تم التحديث إلى النموذج المطلوب
            messages=[
                {
                    "role": "system",
                    "content": f"أنت مدرب كاليستثنيكس (Calisthenics) محترف ومختص بتمارين وزن الجسم فقط. أجب عن سؤال المستخدم باختصار ووضوح مستعيناً بالمعلومات الموجودة في قاعدة المعرفة التالية:\n\n{knowledge_base}"
                },
                {
                    "role": "user",
                    "content": query.question
                }
            ],
            temperature=0.3,
        )
        answer = completion.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"حدث خطأ أثناء معالجة السؤال: {str(e)}"}