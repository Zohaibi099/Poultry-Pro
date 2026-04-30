from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests

# === Disease Detection ===
from model_loader import predict

# 🔐 Load environment variables
print("🔄 Loading environment variables...")
load_dotenv("api.env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 🔍 Debug API key
if OPENROUTER_API_KEY:
    print("✅ API Key Loaded Successfully")
    print("🔑 Key Preview:", OPENROUTER_API_KEY[:15] + "...")
else:
    print("❌ API Key NOT Loaded. Check api.env file!")

# === Poultry Data ===
try:
    with open("poultry_faq.txt", "r", encoding="utf-8") as f:
        poultry_data = f.read()
    print("✅ Poultry FAQ loaded")
except Exception as e:
    print("❌ Error loading poultry_faq.txt:", e)
    poultry_data = ""

# === FastAPI App ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print("📡 Root endpoint hit")
    return {"message": "🐔 Poultry Pro API running 🚀"}


# === OpenRouter Call ===
def ask_openrouter(user_input: str, context: str):
    print("\n📨 New Chat Request")
    print("👤 User Input:", user_input)

    if not OPENROUTER_API_KEY:
        return "❌ API Key missing. Check backend."

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Poultry Pro App"
    }

    payload = {
    "model": "deepseek/deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are PoultryProBot, a professional poultry assistant.\n\n"

                "STRICT RULES:\n"
                "1. Only answer if the user clearly asks about poultry (chickens, farming, diseases, feed, vaccination).\n"
                "2. If the message is vague (e.g. hi, hello, g, ok), ask what they want.\n"
                "3. Do NOT guess or assume missing details.\n"
                "4. Keep answers short (max 6-8 lines).\n"
                "5. Use simple Urdu-English mix (no Hindi words).\n"
                "6. Format using clean bullet points (no # or * symbols).\n"
                "7. Be practical and farmer-friendly.\n\n"

                "FOR DISEASE QUESTIONS:\n"
                "- Give: symptoms + prevention + treatment (short)\n\n"

                "FOR NON-POULTRY QUESTIONS:\n"
                "- Politely say you only help with poultry topics.\n\n"

                "IMPORTANT:\n"
                "- If context is not relevant to the question, ignore it.\n"
                "- Do not dump full information. Only give what is asked.\n\n"

                f"Context:\n{context}"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
}

    try:
        print("🌐 Sending request to OpenRouter...")

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print("📥 Status Code:", response.status_code)

        data = response.json()
        print("📦 Response received")

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print("❌ Network Error:", e)
        return "⚠️ Network error while contacting AI service."

    except Exception as e:
        print("❌ Unexpected Error:", e)
        print("🔎 Raw Response:", response.text if 'response' in locals() else "No response")
        return "⚠️ Error processing AI response."


# === Chat Route ===
@app.post("/chat")
async def chat(request: Request):
    print("\n📡 /chat endpoint hit")

    try:
        data = await request.json()
        user_input = data.get("message", "")

        if not user_input:
            return {"reply": "⚠️ Empty message received."}

        reply = ask_openrouter(user_input, poultry_data)

        cleaned_reply = reply.replace("#", "").replace("*", "").strip()

        print("🤖 Reply Sent:", cleaned_reply)

        return {"reply": cleaned_reply}

    except Exception as e:
        print("❌ Chat Route Error:", e)
        return {"reply": "⚠️ Server error in chat route."}


# === Disease Detection Route ===
@app.post("/predict")
async def predict_disease(image: UploadFile = File(...)):
    print("\n📡 /predict endpoint hit")

    try:
        result = predict(image.file)
        disease = result["disease"]

        print("🦠 Predicted Disease:", disease)

        if disease == "Unknown":
            return {
                "disease": "Unknown",
                "tips": "❗Unrecognized image. Upload clear poultry fecal image."
            }

        return {"disease": disease}

    except Exception as e:
        print("❌ Prediction Error:", e)
        return {"disease": "Error", "tips": "⚠️ Prediction failed."}


# === Run Server (optional) ===
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)