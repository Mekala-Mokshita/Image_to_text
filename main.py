import os
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Gemini API key is missing")

genai.configure(api_key=API_KEY)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def upload_image():
    return """
    <html>
        <body>
            <h2>IMAGE ANALYSIS</h2>
            <form action="/result" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

@app.post("/result", response_class=HTMLResponse)
async def result(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(img)

    return f"""
    <html>
        <body>
            <h2>Result</h2>
            <p>{response.text}</p>
        </body>
    </html>
    """