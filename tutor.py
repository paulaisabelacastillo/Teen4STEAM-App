from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

app = FastAPI()

# Configuración de CORS para que tu HTML pueda comunicarse con este servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# REEMPLAZA EL TEXTO ABAJO CON TU NUEVA API KEY
client = OpenAI(api_key="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")

chat_history = [
    {
        "role": "system",
        "content": (
            "You are My Tutor AI, a professional STEAM mentor for teens (12-18). "
            "STRICT UNIFIED TEXT RULE: You must respond in ONE SINGLE SOLID BLOCK of text. "
            "DO NOT use line breaks. DO NOT use paragraphs. DO NOT use the Enter key. "
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
        # Añadir mensaje del usuario
        chat_history.append({"role": "user", "content": question.text})

        # Mantener historial corto para eficiencia
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]

        # Usamos gpt-4o-mini por ser rápido y eficiente
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            temperature=0.7,
        )
        
        answer = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
        
        return {"answer": answer}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Check API Key or Connection.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)