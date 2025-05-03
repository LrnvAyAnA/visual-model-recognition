from ultralytics import YOLO

class DiagramDetector:
    def __init__(self, model_path="../runs/detect/train7/weights/best.pt", confidence=0.25):
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
# # Загрузка модели
# model = YOLO("../runs/detect/train7/weights/best.pt")
#
# def detect_elements(image):
#     results = model.predict(source=image, save=False, conf=0.25)
#     classes_detected = []
#     for r in results:
#         for box in r.boxes:
#             cls_id = int(box.cls[0])
#             label = model.names[cls_id]
#             classes_detected.append(label)
#     # Обработанное изображение и список найденных элементов
#     img_with_boxes = results[0].plot()
#     return img_with_boxes, classes_detected


# def get_diagram_weights():
#     query = """
#     SELECT ?diagramType ?element ?weight
#     WHERE {
#         ?relation a :ElementWeightRelation .
#         ?relation :forMetric ?diagramType .
#         ?relation :forElement ?element .
#         ?relation :hasWeightValue ?weight .
#     }
#     """
#     results = g.query(query, initNs={"": "http://www.example.org/ontology#"})
#
#     weights = {}
#     for row in results:
#         diagram_type = row["diagramType"].split("#")[-1]
#         element = row["element"].split("#")[-1]
#         weight = float(row["weight"])
#         if diagram_type not in weights:
#             weights[diagram_type] = {}
#         weights[diagram_type][element] = weight
#     return weights

#
# def match_diagram_type_with_weights(detected_elements):
#     weights = get_diagram_weights()
#     scores = {}
#     for diagram_type, elements_weights in weights.items():
#         total_weight = sum(elements_weights.values())
#         matched_weight = sum(
#             weight for element, weight in elements_weights.items() if element in detected_elements
#         )
#         if total_weight == 0:
#             continue
#         score = (matched_weight / total_weight) * 100
#         scores[diagram_type] = round(score, 2)
#     return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

# def get_recommendations(best_type):
#     prefix = "http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#"
#     diagram_uri = f":{best_type}"
#
#     query = f"""
#     PREFIX : <{prefix}>
#
#     SELECT ?similarDiagram
#     WHERE {{
#         ?diagram a :DiagramType .
#         ?diagram :hasCategory ?category .
#         ?similarDiagram :hasCategory ?category .
#         FILTER (?diagram = {diagram_uri} && ?similarDiagram != {diagram_uri})
#     }}
#     """
#     return query


