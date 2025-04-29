import gradio as gr
from model.detector import detect_elements
from model.ontology import determine_chart_type

def process_image(image):
    img_with_boxes, detected_classes = detect_elements(image)
    chart_type = determine_chart_type(detected_classes)
    return img_with_boxes, chart_type

interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="numpy"),
    outputs=[gr.Image(type="numpy"), gr.Textbox()],
    title="Распознавание диаграмм",
    description="Загрузите изображение, чтобы определить тип диаграммы по распознанным элементам."
)

if __name__ == "__main__":
    interface.launch()
