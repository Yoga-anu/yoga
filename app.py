# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.responses import FileResponse

from typing import List
import shutil
import os

from yolo_model import detect, OUTPUT_FOLDER
from llm_model import explain_detection
from database import save_result


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- Home Page ----------------
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# ---------------- Prediction ----------------
@app.post("/predict")
async def predict(images: List[UploadFile] = File(...)):

    results = []

    for image in images:

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)

        # Save uploaded image
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Run YOLO detection
        detections = detect(image_path)

        if detections:
            explanation = explain_detection(detections)
            output_image = detections[0]["output_image"]

            save_result(
                image.filename,
                detections[0]["class"],
                detections[0]["confidence"],
                explanation
            )

            filename = os.path.basename(output_image)
            result_api = f"http://127.0.0.1:8000/result/{filename}"

            print("Output image:", output_image)
            print("Result API:", result_api)

        else:
            explanation = "No hotspot detected."
            output_image = None
            result_api = None

        results.append({
            "image_name": image.filename,
            "detections": detections,
            "explanation": explanation,
            "output_image": output_image,
            "result_image_api": result_api
        })

    return {
        "status": "success",
        "total_images": len(images),
        "results": results
    }


# ---------------- Result Image ----------------
@app.get("/result/{filename}")
async def get_result(filename: str):

    image_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)