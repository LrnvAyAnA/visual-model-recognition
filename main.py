import gradio as gr
from model.detection import DiagramDetector
from modules.matcher import OntologyMatcher
from ontology.ontology import determine_chart_type

def process_image(image):
    detector = DiagramDetector()
    img_with_boxes, detected_classes = detector.detect(image)
    # chart_type = determine_chart_type(detected_classes)
    matcher = OntologyMatcher(ontology_path="C:/Users/Yana/PycharmProjects/prototype/ontology/ontologyV3.rdf")
    matching_diagrams = matcher.find_matching_diagrams(detected_classes)
    return img_with_boxes, matching_diagrams
    # return img_with_boxes, chart_type

interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="numpy"),
    outputs=[gr.Image(type="numpy"), gr.Textbox()],
    title="Распознавание диаграмм",
    description="Загрузите изображение, чтобы определить тип диаграммы по распознанным элементам."
)

if __name__ == "__main__":
    interface.launch()
