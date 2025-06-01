from model.detection import DiagramDetector
from modules.matcher import OntologyMatcher
from core.utils import fill_weights_table, parse_weights

diagram_mapping = {
    "BarChart": "Bar_chart",
    "ScatterPlot": "Scatter_plot",
    "LineGraph": "Line_graph",
    "Treemap": "Treemap",
    "PieChart": "Pie_chart"
}


def process_image(image, weight_data=None, return_weights_table=False):
    if image is None:
        return None, "Изображение не выбрано", None, None

    try:
        detector = DiagramDetector()
        img_with_boxes, detected_classes = detector.detect(image)

        # Защита от неправильного формата изображения
        import numpy as np
        from PIL import Image

        # Преобразование к RGB и dtype=uint8
        if isinstance(img_with_boxes, Image.Image):
            img_with_boxes = img_with_boxes.convert("RGB")
            img_with_boxes = np.array(img_with_boxes)
        elif isinstance(img_with_boxes, np.ndarray):
            if img_with_boxes.dtype != np.uint8:
                img_with_boxes = img_with_boxes.astype(np.uint8)

        matcher = OntologyMatcher("ontology/ontologyLastLast.rdf")
        all_diagram_data = matcher.get_all_diagram_data()

        custom_weights = parse_weights(weight_data) if weight_data is not None else None

        similarity_scores = matcher.calculate_similarity(
            all_diagram_data, detected_classes, custom_weights
        )
        normalized_scores = similarity_scores
        # normalized_scores = {
        #     diagram_mapping.get(diagram, diagram): score
        #     for diagram, score in similarity_scores.items()
        # }
        sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

        result_text = "Оценка возможных типов диаграмм:\n"
        for diagram, score in sorted_scores:
            result_text += f"- {diagram}: {score}%\n"

        result_text += "\nРаспознанные элементы:\n"
        element_counts = {elem: detected_classes.count(elem) for elem in set(detected_classes)}
        for elem, count in element_counts.items():
            result_text += f"- {elem}: {count}\n"
        print("Распознанные элементы:", detected_classes)
        print("Вес legend для PieChart:", all_diagram_data["Pie_chart"].get("legend"))
        if return_weights_table:
            headers, table = fill_weights_table(detected_classes, all_diagram_data, weight_data)
            return img_with_boxes, result_text, headers, table

        return img_with_boxes, result_text

    except Exception as e:
        return None, f"Ошибка при обработке: {e}", None, None
