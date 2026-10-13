import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

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

# مسار المحادثة للذكاء الاصطناعي
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        system_prompt = (
            "You are an expert Calisthenics & Fitness AI Coach. "
            "Use the following knowledge base to answer the user accurately:\n\n"
            f"{knowledge_base}"
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        reply = completion.choices[0].message.content
        return {"response": reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
