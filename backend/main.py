from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import os
import io
import urllib.request
from PIL import Image

from image_processor import processor

app = FastAPI(title="Smart Practical AI - Auto Healing Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str
    font_id: str = "font_1"
    page_id: str = "page_1"
    ink_color: str = "blue"
    student_name: str = ""
    roll_number: str = ""
    college_name: str = ""
    subject_code: str = ""
    date: str = ""
    page_numbering: bool = True
    lab_header: bool = True
    font_size: int = 38
    line_gap: int = 48
    margin_left: int = 130
    top_margin: int = 190
    header_x: int = 130
    header_y: int = 50
    realism_factor: int = 3
    stealth_scanner_effect: bool = False
    ink_smudge_level: int = 0
    uneven_lighting: bool = False

def get_safe_font(font_id: str):
    """
    🛠️ AUTO-HEALING FONT MANAGER:
    Yeh system kabhi app ko crash nahi hone dega!
    """
    # Agar folder nahi hai toh khud bana dega
    os.makedirs("assets/fonts", exist_ok=True)
    
    requested_font = f"assets/fonts/{font_id}.ttf"
    default_font = "assets/fonts/font_1.ttf"

    # 1. Jo font maanga hai, agar wo hai toh de do
    if os.path.exists(requested_font):
        return requested_font
        
    # 2. Agar nahi mila, toh check karo font_1.ttf hai kya?
    if os.path.exists(default_font):
        print(f"[WARNING] {font_id} missing. Auto-shifting to font_1.ttf")
        return default_font

    # 3. 🚨 GOD MODE: Agar koi bhi font nahi hai, toh internet se Auto-Download kar lo!
    print("\n[AUTO-HEAL] No fonts found! Downloading a Premium Handwriting Font automatically...")
    try:
        # Google Fonts ka ek best handwriting font (Shadows Into Light) download kar rahe hain
        font_url = "https://github.com/google/fonts/raw/main/ofl/shadowsintolight/ShadowsIntoLight-Regular.ttf"
        urllib.request.urlretrieve(font_url, default_font)
        print("[AUTO-HEAL] Font Downloaded Successfully! System Recovered.\n")
        return default_font
    except Exception as e:
        print(f"[CRITICAL ERROR] Internet connection failed during Auto-Heal: {e}")
        return None

@app.post("/generate")
def generate_document(req: GenerateRequest):
    # 🛡️ Engine chalne se pehle Auto-Healing check
    font_path = get_safe_font(req.font_id)
    if not font_path:
        raise HTTPException(status_code=500, detail="Backend lacks fonts and Auto-Download failed. Please check internet connection.")

    page_style = "ruled"
    if "blank" in req.page_id.lower(): page_style = "blank"
    elif "grid" in req.page_id.lower(): page_style = "grid"

    try:
        pages_bytes = processor.compile_document(req, font_path, page_style)
        if not pages_bytes:
            raise HTTPException(status_code=500, detail="Compilation failed.")

        pil_images = [Image.open(io.BytesIO(pb)).convert("RGB") for pb in pages_bytes]
        pdf_buffer = io.BytesIO()
        pil_images[0].save(
            pdf_buffer, format="PDF", save_all=True, append_images=pil_images[1:], resolution=300.0
        )
        pdf_buffer.seek(0)
        return Response(content=pdf_buffer.getvalue(), media_type="application/pdf")
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Isko maine Live Deployment (Render.com) ke hisaab se set kar diya hai
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)