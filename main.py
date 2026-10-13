import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# إعداد العميل لربط Groq API
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# تحميل ملف المعلومات المخصصة (Knowledge Base)
def load_knowledge():
    if os.path.exists("Knowledge.txt"):
        with open("Knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

knowledge_base = load_knowledge()

class ChatRequest(BaseModel):
    message: str

# المسار الرئيسي لفتح صفحة index.html
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# مسار المحادثة للذكاء الاصطناعي (استبدل الجزء القديم بهذا الكود)
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": f"أنت مساعد تدريبي مختص. استخدم المعلومات التالية للإجابة: {knowledge_base}"},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
