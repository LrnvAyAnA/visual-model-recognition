from ultralytics import YOLO

class DiagramDetector:
    def __init__(self, model_path="../runs/detect/train_new/weights/best.pt", confidence=0.25):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, image):
        results = self.model.predict(source=image, save=False, conf=self.confidence)
        classes_detected = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                classes_detected.append(label)
        img_with_boxes = results[0].plot()
        return img_with_boxes, classes_detected


