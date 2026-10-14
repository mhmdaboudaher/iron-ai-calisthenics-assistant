import os
import io
import sys
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

# ضبط الترميز لدعم النصوص والحروف العربية
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = FastAPI()

# تهيئة عميل Groq باستخدام مكتبة OpenAI القياسية
client = OpenAI(
    api_key="ضع_مفتاح_GROQ_الخاص_بك_هنا",  # ضع مفتاحك الذي يبدأ بـ gsk_
    base_url="https://api.groq.com/openai/v1"
)

# تعريف نموذج البيانات المستقبلة لتشمل الرسالة والذاكرة
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

# المسار الرئيسي لفتح صفحة index.html
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# مسار المحادثة الذكية مع دعم الذاكرة
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # بناء قائمة الرسائل بدءاً برسالة النظام
        messages = [{"role": "system", "content": "أنت مدرب كاليستثنكس خبير ومساعد ذكي."}]
        
        # إضافة السجل السابق إن وجد
        if request.history:
            messages.extend(request.history)
            
        # إضافة الرسالة الجديدة من المستخدم
        messages.append({"role": "user", "content": request.message})

        # إرسال الطلب إلى نموذج Groq (مثل llama-3.3-70b-versatile أو mixtral-8x7b-32768)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        
        return {"response": completion.choices[0].message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # قراءة المنفذ من نظام التشغيل واستخدام 8008 محلياً
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)