import gradio as gr
from model.detection import DiagramDetector
from modules.matcher import OntologyMatcher

diagram_mapping = {
    "BarChart": "Bar_chart",
    "ScatterPlot": "Scatter_plot",
    "LineGraph": "Line_graph",
    "Treemap": "Treemap",
    "PieChart": "Pie_chart"
}
def process_image(image):
    detector = DiagramDetector()
    img_with_boxes, detected_classes = detector.detect(image)

    # matcher = OntologyMatcher(ontology_path="D:/Programming/yoloyo/ontology/ontologyV3.rdf")
    matcher = OntologyMatcher(ontology_path="ontology/ontologyLast.rdf")

    # Получаем полную таблицу элементов для всех диаграмм
    all_diagram_data = matcher.get_all_diagram_data()
    # Сопоставление и расчёт вероятностей
    similarity_scores = matcher.calculate_similarity(all_diagram_data, detected_classes)

    # Обновляем ключи словаря на "красивые" с помощью словаря mapping
    normalized_scores = {}
    for diagram, score in similarity_scores.items():
        normalized_name = diagram_mapping.get(diagram, diagram)  # если не найдено, оставить как есть
        normalized_scores[normalized_name] = score

    # Сортировка по убыванию вероятности
    sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

    # Определяем лучший тип диаграммы
    best_diagram, best_score = sorted_scores[0]

    # Строим текст результата
    result_text = f"Тип диаграммы: {best_diagram} (уверенность: {best_score}%)\n\n"
    result_text += "Оценка всех типов:\n"
    for diagram, score in sorted_scores:
        result_text += f"- {diagram}: {score}%\n"

    # Список найденных элементов
    result_text += "\nНайдено элементов:\n"
    element_counts = {elem: detected_classes.count(elem) for elem in set(detected_classes)}
    for elem, count in element_counts.items():
        result_text += f"- {elem}: {count}\n"

    # Получаем рекомендации
    recommendations = matcher.get_recommendations(best_diagram)
    if recommendations:
        result_text += "\nРекомендуемые альтернативы:\n"
        result_text += ", ".join(recommendations)
    else:
        result_text += "\nНет рекомендуемых альтернатив."

    # # Вычисляем степени соответствия
    # similarity_scores = matcher.calculate_similarity(all_diagram_data, detected_classes)
    #
    # if not similarity_scores:
    #     result_text = "Не удалось сопоставить с какими-либо известными типами диаграмм."
    # else:
    #     # Сортируем по убыванию уверенности
    #     sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    #
    #     # Самый вероятный тип диаграммы
    #     best_diagram, best_score = sorted_scores[0]
    #     result_text = f"Наиболее вероятный тип диаграммы: {best_diagram} (уверенность: {best_score}%)\n\n"
    #
    #     # Оценка всех типов диаграмм
    #     result_text += "Оценка всех типов диаграмм:\n"
    #     for diagram, score in sorted_scores:
    #         result_text += f"- {diagram}: {score}%\n"
    #
    # # Считаем количество каждого найденного элемента
    # element_counts = {}
    # for elem in detected_classes:
    #     elem_lower = elem.lower()
    #     element_counts[elem_lower] = element_counts.get(elem_lower, 0) + 1
    #
    # result_text += "\nНайдено элементов:\n"
    # for elem, count in element_counts.items():
    #     result_text += f"- {elem.capitalize()}: {count}\n"

    return img_with_boxes, result_text


# Интерфейс
interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="numpy"),
    outputs=[gr.Image(type="numpy"), gr.Textbox()],
    title="Распознавание диаграмм",
    description="Загрузите изображение, чтобы определить тип диаграммы по распознанным элементам."
)

if __name__ == "__main__":
    interface.launch()
