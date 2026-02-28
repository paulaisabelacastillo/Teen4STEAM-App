from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your Groq API Key
client = Groq(api_key="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")

chat_history = [
    {
        "role": "system",
        "content": (
            "You are My Tutor AI, a professional STEAM mentor for teens (12-18). "
            "STRICT UNIFIED TEXT RULE: You must respond in ONE SINGLE SOLID BLOCK of text. "
            "DO NOT use line breaks. DO NOT use paragraphs. DO NOT use the Enter key. "
            "If you use more than one paragraph, you are failing. "
            "LENGTH: The entire text block must be between 3 to 5 lines long. "
            "LANGUAGE: Mirror the user's language (English or Spanish). "
            "CONTENT: Advanced STEAM explanation + real-world use + logic challenge. "
            "EMOJIS: Exactly 2 emojis at the very end of the solid block."
        )
    }
]

class Question(BaseModel):
    text: str

@app.post("/ask")
async def ask_tutor(question: Question):
    global chat_history
    try:
        # Add user message to history
        chat_history.append({"role": "user", "content": question.text})

        # Keep context of the last 10 messages
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            temperature=0.7,
        )
        
        answer = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
        
        return {"answer": answer}
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Connection error.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)