from ultralytics import YOLO

# Загрузка модели
model = YOLO("../runs/detect/train7/weights/best.pt")

def detect_elements(image):
    results = model.predict(source=image, save=False, conf=0.25)
    classes_detected = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            classes_detected.append(label)
    # Вернуть обработанное изображение и список найденных элементов
    img_with_boxes = results[0].plot()
    return img_with_boxes, classes_detected

