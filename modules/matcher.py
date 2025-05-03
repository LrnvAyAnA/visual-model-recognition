# Модуль который запрашивает типы диаграмм и элементы с весами в структуре
import rdflib

class OntologyMatcher:
    def __init__(self, ontology_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ontology_path, format='xml')

    def find_matching_diagrams(self, detected_elements):
        result = {}
        for elem in detected_elements:
            query = """
            PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
            SELECT ?diagram ?weight
            WHERE {
                ?rel a :ElementWeightRelation .
                ?rel :forElement :Rectangle .
                ?rel :forMetric ?diagram .
                ?rel :hasWeightValue ?weight .
            }
            """
            # query = f"""
            # PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
            # SELECT ?diagram ?weight
            # WHERE {{
            #     ?rel a :ElementWeightRelation .
            #     ?rel :forElement :{elem} .
            #     ?rel :forMetric ?diagram .
            #     ?rel :hasWeightValue ?weight .
            # }}
            # """
            qres = self.graph.query(query)
            for row in qres:
                diagram = str(row['diagram'].split('#')[-1])
                weight = float(row['weight'])
                if diagram not in result:
                    result[diagram] = {}
                result[diagram][elem] = weight
        return result
