# pyrefly: ignore [missing-import]
from ultralytics import YOLO

model = YOLO("models/best.pt")

results = model.predict(
    source="uploads/Imgdirty_187_1_jpg.rf.e6428098ec311f0513f0028d1075cfc3.jpg",
    save=True,
    conf=0.1
)

print(results)