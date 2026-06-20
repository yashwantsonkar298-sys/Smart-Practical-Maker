from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import os
import io
import urllib.request
from PIL import Image

try:
    from .image_processor import processor
except ImportError:
    from image_processor import processor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
FONT_DOWNLOADS = {
    "font_1": "https://raw.githubusercontent.com/google/fonts/main/ofl/shadowsintolight/ShadowsIntoLight-Regular.ttf",
    "font_2": "https://raw.githubusercontent.com/google/fonts/main/ofl/indieflower/IndieFlower-Regular.ttf",
    "font_3": "https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%5Bwght%5D.ttf",
    "font_4": "https://raw.githubusercontent.com/google/fonts/main/ofl/gloriahallelujah/GloriaHallelujah.ttf",
    "font_5": "https://raw.githubusercontent.com/google/fonts/main/ofl/patrickhand/PatrickHand-Regular.ttf",
    "font_6": "https://raw.githubusercontent.com/google/fonts/main/apache/permanentmarker/PermanentMarker-Regular.ttf",
    "font_7": "https://raw.githubusercontent.com/google/fonts/main/ofl/kalam/Kalam-Regular.ttf",
    "font_8": "https://raw.githubusercontent.com/google/fonts/main/ofl/handlee/Handlee-Regular.ttf",
    "font_9": "https://raw.githubusercontent.com/google/fonts/main/ofl/architectsdaughter/ArchitectsDaughter-Regular.ttf",
    "font_10": "https://raw.githubusercontent.com/google/fonts/main/apache/schoolbell/Schoolbell-Regular.ttf",
}
FONT_ALIASES = {
    "vani": "font_8",
    "photo_1": "font_8",
    "photo_2": "font_5",
    "photo_3": "font_3",
    "photo_4": "font_7",
    "photo_6": "font_3",
    "photo_7": "font_7",
}

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
    os.makedirs(FONT_DIR, exist_ok=True)
    
    safe_font_id = FONT_ALIASES.get(font_id, font_id)
    safe_font_id = safe_font_id if safe_font_id in FONT_DOWNLOADS else "font_1"
    requested_font = os.path.join(FONT_DIR, f"{safe_font_id}.ttf")
    default_font = os.path.join(FONT_DIR, "font_1.ttf")

    # 1. Jo font maanga hai, agar wo hai toh de do
    if os.path.exists(requested_font):
        return requested_font

    try:
        print(f"[AUTO-HEAL] Downloading handwriting profile {safe_font_id}...")
        urllib.request.urlretrieve(FONT_DOWNLOADS[safe_font_id], requested_font)
        return requested_font
    except Exception as e:
        print(f"[WARNING] Could not download {safe_font_id}: {e}")
        
    # 2. Agar nahi mila, toh check karo font_1.ttf hai kya?
    if os.path.exists(default_font):
        print(f"[WARNING] {safe_font_id} missing. Auto-shifting to font_1.ttf")
        return default_font

    # 3. 🚨 GOD MODE: Agar koi bhi font nahi hai, toh internet se Auto-Download kar lo!
    print("\n[AUTO-HEAL] No fonts found! Downloading a Premium Handwriting Font automatically...")
    try:
        # Google Fonts ka ek best handwriting font (Shadows Into Light) download kar rahe hain
        urllib.request.urlretrieve(FONT_DOWNLOADS["font_1"], default_font)
        print("[AUTO-HEAL] Font Downloaded Successfully! System Recovered.\n")
        return default_font
    except Exception as e:
        print(f"[CRITICAL ERROR] Internet connection failed during Auto-Heal: {e}")
        return None

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-assignment-maker",
        "font_profiles": len(FONT_DOWNLOADS) + len(FONT_ALIASES),
    }

@app.post("/generate")
def generate_document(req: GenerateRequest):
    # 🛡️ Engine chalne se pehle Auto-Healing check
    font_path = get_safe_font(req.font_id)
    if not font_path:
        raise HTTPException(status_code=500, detail="Backend lacks fonts and Auto-Download failed. Please check internet connection.")

    page_style = "ruled"
    page_id = req.page_id.lower()
    if "abes" in page_id or "practical" in page_id:
        page_style = "abes_practical"
    elif "blank" in page_id:
        page_style = "blank"
    elif "grid" in page_id:
        page_style = "grid"

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
