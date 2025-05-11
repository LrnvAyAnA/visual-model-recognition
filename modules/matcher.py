import rdflib

class OntologyMatcher:
    def __init__(self, ontology_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ontology_path, format='xml')

    def get_all_diagram_data(self):
        result = {}
        query = """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?metric ?element ?weight
        WHERE {
            ?rel a :ElementWeightRelation .
            ?rel :forElement ?element .
            ?rel :forMetric ?metric .
            ?rel :hasWeightValue ?weight .
            FILTER (?weight > 0)
        }
        """
        qres = self.graph.query(query)
        for row in qres:
            # Приводим к короткому виду:
            diagram_metric = str(row['metric'].split('#')[-1])
            diagram_name = diagram_metric.replace('Metric', '')  # Убираем Metric

            element = str(row['element'].split('#')[-1]).replace('1', '').lower()  # Например Rectangle1 -> rectangle
            weight = float(row['weight'])

            if diagram_name not in result:
                result[diagram_name] = {}
            result[diagram_name][element] = weight

        return result

    def calculate_similarity(self, all_diagram_data, detected_elements):
        similarity_scores = {}

        # Переводим найденные элементы в нижний регистр для сопоставления
        detected_elements_set = set(elem.lower() for elem in detected_elements)

        for diagram_name, elements_weights in all_diagram_data.items():
            total_possible_weight = sum(elements_weights.values())
            total_detected_weight = 0

            # Проверяем, есть ли хоть одно совпадение найденных элементов с элементами диаграммы
            intersection = detected_elements_set & set(elements_weights.keys())
            if not intersection:
                continue  # Пропускаем диаграммы без общих элементов

            for elem, weight in elements_weights.items():
                if elem in detected_elements_set:
                    total_detected_weight += weight  # Учитываем только найденные элементы

            # Рассчитываем уверенность
            similarity = (total_detected_weight / total_possible_weight) * 100 if total_possible_weight > 0 else 0
            similarity_scores[diagram_name] = round(similarity, 2)

        return similarity_scores

    def get_recommendations(self, best_diagram):
        category_query = f"""
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?category
        WHERE {{
            :{best_diagram} rdfs:subClassOf ?category .
        }}
        """
        category_result = self.graph.query(category_query)
        category_uri = None

        for row in category_result:
            category_uri = str(row['category'].split('#')[-1])
            print(f"Category for {best_diagram}: {category_uri}")

        if not category_uri:
            print(f"No category found for {best_diagram}. No recommendations.")
            return []

        # Теперь ищем все диаграммы в этой категории
        recommendations_query = f"""
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?diagram
        WHERE {{
            ?diagram rdfs:subClassOf :{category_uri} .
            FILTER (?diagram != :{best_diagram})
        }}
        """
        rec_results = self.graph.query(recommendations_query)

        recommendations = []
        for row in rec_results:
            diag_name = str(row['diagram'].split('#')[-1])
            recommendations.append(diag_name)

        return recommendations
