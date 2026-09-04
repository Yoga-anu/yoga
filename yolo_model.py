import os
from typing import Any, List
# pyrefly: ignore [missing-import]
from ultralytics import YOLO

# Load YOLO model
model = YOLO("models/best.pt")
print("Model path:", model.ckpt_path if hasattr(model, "ckpt_path") else "Unknown")
print("Task:", model.task)
print("Classes:", model.names)

# Check if model has custom solar panel classes
loaded_classes = set(model.names.values())
if "person" in loaded_classes or "umbrella" in loaded_classes:
    print("\n" + "!" * 80)
    print(" WARNING: The file 'models/solar_yolov8.pt' is a standard COCO pre-trained model!")
    print(" Please replace it with your actual custom-trained 'best.pt' weights.")
    print("!" * 80 + "\n")


OUTPUT_FOLDER = "runs/outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def detect(image_path):
    results: List[Any] = model.predict(
        source=image_path,
        save=False,       # We handle saving manually to keep one folder
        conf=0.60,
    )
    results = model.predict(
    source=image_path,
    save=False,
    conf=0.50,
    iou=0.35,
)

    detections = []

    for result in results:
        # Save the annotated image to our single fixed output folder
        filename = os.path.basename(image_path)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        result.save(filename=output_path)

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            detections.append({
                "class": result.names[class_id],
                "confidence": round(confidence, 2),
                "output_image": output_path,
            })

    return detections


if __name__ == "__main__":
    # Test script standalone
    test_image_path = "uploads/crack-20_PNG.rf.0ec34747ec924426dfcb2a6eb64bb2a0.jpg"
    print(f"Testing YOLO detection with image: {test_image_path}")
    
    # Run detection
    try:
        detections = detect(test_image_path)
        print("Detections result:")
        print(detections)
    except Exception as e:
        print(f"Error running detection: {e}")


