import rdflib

class OntologyMatcher:
    def __init__(self, ontology_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ontology_path, format='xml')

    def get_weights_for_elements(self, detected_elements, similarity_scores=None):
        detected_elements_lower = set(elem.lower() for elem in detected_elements)
        relevant_diagrams = similarity_scores.keys() if similarity_scores else self.get_all_diagram_data().keys()

        weight_rows = []

        all_data = self.get_all_diagram_data()
        for element in detected_elements_lower:
            row = [element]
            for diagram in relevant_diagrams:
                row.append(all_data.get(diagram, {}).get(element, 0.0))
            weight_rows.append(row)

        headers = ["Элемент"] + list(relevant_diagrams)
        return headers, weight_rows

    def get_all_diagram_data(self):
        result = {}
        query = """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?metric ?element ?weight ?diagramClass
        WHERE {
            ?rel a :ElementWeightRelation .
            ?rel :forElement ?element .
            ?rel :forMetric ?metric .
            ?rel :hasWeightValue ?weight .

            ?metric :forDiagramType ?diagramInstance .
            ?diagramInstance a ?diagramClass .

            FILTER (?diagramClass != owl:NamedIndividual && ?weight > 0)
        }
        """
        qres = self.graph.query(query)
        for row in qres:
            # Достаём имя типа диаграммы из IRI (после #)
            diagram_name = str(row['diagramClass'].split('#')[-1])
            element = str(row['element'].split('#')[-1]).replace('1', '').lower()
            weight = float(row['weight'])

            if diagram_name not in result:
                result[diagram_name] = {}
            result[diagram_name][element] = weight

        return result
    # def get_all_diagram_data(self):
    #     result = {}
    #     query = """
    #     PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
    #     SELECT ?metric ?element ?weight
    #     WHERE {
    #         ?rel a :ElementWeightRelation .
    #         ?rel :forElement ?element .
    #         ?rel :forMetric ?metric .
    #         ?rel :hasWeightValue ?weight .
    #         FILTER (?weight > 0)
    #     }
    #     """
    #     qres = self.graph.query(query)
    #     for row in qres:
    #         # приводим к короткому виду
    #         diagram_metric = str(row['metric'].split('#')[-1])
    #         diagram_name = diagram_metric.replace('Metric', '')  # Убираем Metric
    #
    #         element = str(row['element'].split('#')[-1]).replace('1', '').lower()
    #         weight = float(row['weight'])
    #
    #         if diagram_name not in result:
    #             result[diagram_name] = {}
    #         result[diagram_name][element] = weight
    #
    #     return result

    def calculate_similarity(self, all_diagram_data, detected_elements, custom_weights=None, penalty_lambda=0.2):
        similarity_scores = {}

        detected_elements_set = set(elem.lower() for elem in detected_elements)

        for diagram_name, elements_weights in all_diagram_data.items():
            total_possible_weight = 0.0
            matched_weight = 0.0
            penalty_weight = 0.0

            for elem, weight in elements_weights.items():
                # если есть пользовательские веса берём их
                if custom_weights and elem in custom_weights and diagram_name in custom_weights[elem]:
                    weight = custom_weights[elem][diagram_name]

                total_possible_weight += weight

                if elem in detected_elements_set:
                    matched_weight += weight

            # штраф за каждый лишний элемент
            for detected in detected_elements_set:
                if detected not in elements_weights:
                    for diag, elems in all_diagram_data.items():
                        if diag == diagram_name:
                            continue
                        if detected in elems:
                            w = elems[detected]
                            if custom_weights and detected in custom_weights and diag in custom_weights[detected]:
                                w = custom_weights[detected][diag]
                            penalty_weight += w
                            break  # находим первый подходящий вес

            raw_score = (matched_weight - penalty_lambda * penalty_weight)
            similarity = max((raw_score / total_possible_weight) * 100
                             if total_possible_weight > 0 else 0, 0)
            final_score = round(similarity, 2)
            if final_score > 0:
                similarity_scores[diagram_name] = final_score

        return similarity_scores


    # def get_recommendations(self, best_diagram):
    #     category_query = f"""
    #     PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT ?category
    #     WHERE {{
    #         :{best_diagram} rdfs:subClassOf ?category .
    #     }}
    #     """
    #     category_result = self.graph.query(category_query)
    #     category_uri = None
    #
    #     for row in category_result:
    #         category_uri = str(row['category'].split('#')[-1])
    #         print(f"Category for {best_diagram}: {category_uri}")
    #
    #     if not category_uri:
    #         print(f"No category found for {best_diagram}. No recommendations.")
    #         return []
    #
    #     # все диаграммы в категории
    #     recommendations_query = f"""
    #     PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT ?diagram
    #     WHERE {{
    #         ?diagram rdfs:subClassOf :{category_uri} .
    #         FILTER (?diagram != :{best_diagram})
    #     }}
    #     """
    #     rec_results = self.graph.query(recommendations_query)
    #
    #     recommendations = []
    #     for row in rec_results:
    #         diag_name = str(row['diagram'].split('#')[-1])
    #         recommendations.append(diag_name)
    #
    #     return recommendations
