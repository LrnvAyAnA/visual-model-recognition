# import rdflib
# from model.dict import ontology
#
# # Загружаем онтологию
# g = rdflib.Graph()
# g.parse("D:/Programming/yoloyo/ontology.rdf", format="xml")  # Замените на нужный формат RDF/XML
#
# def execute_sparql_query(query):
#     """Функция для выполнения SPARQL-запроса к онтологии."""
#     result = g.query(query)
#     return result
#
# def determine_chart_type(detected_elements):
#     # Подсчитаем количество каждого элемента
#     rectangles_count = detected_elements.count("rectangle")
#     axis_count = detected_elements.count("axis")
#     point_count = detected_elements.count("point")
#     sector_count = detected_elements.count("sector")
#     line_count = detected_elements.count("line")
#     detected_set = set(detected_elements)
#
#     best_match = None
#     best_score = -1
#
#     # Определяем типы диаграмм с помощью SPARQL запросов
#     sparql_queries = {
#         "Bar Chart": """
#         PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
#         SELECT ?chart_type
#         WHERE {
#             ?chart_type rdf:type :Bar_chart .
#             ?chart_type :has_axis ?axis .
#             ?chart_type :has_rectangle ?rectangle .
#         }
#         """,
#         "Pie Chart": """
#         PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
#         SELECT ?chart_type
#         WHERE {
#             ?chart_type rdf:type :Pie_chart .
#             ?chart_type :has_sector ?sector .
#         }
#         """,
#         "Scatter Plot": """
#         PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
#         SELECT ?chart_type
#         WHERE {
#             ?chart_type rdf:type :Scatter_plot .
#             ?chart_type :has_point ?point .
#         }
#         """,
#         "Treemap": """
#         PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
#         SELECT ?chart_type
#         WHERE {
#             ?chart_type rdf:type :Treemap .
#             ?chart_type :has_rectangle ?rectangle .
#         }
#         """,
#         "Line Graph": """
#         PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
#         SELECT ?chart_type
#         WHERE {
#             ?chart_type rdf:type :Line_graph .
#             ?chart_type :has_line ?line .
#         }
#         """
#     }
#
#     # Выполним все запросы для всех типов диаграмм
#     for chart_type, sparql_query in sparql_queries.items():
#         result = execute_sparql_query(sparql_query)
#
#         if result:
#             return f"Тип диаграммы: {chart_type} (уверенннность: 90%)"
#
#     # Специальная логика для Bar Chart и Treemap, если запросы не сработали
#     if "rectangle" in detected_set:
#         if "axis" in detected_set:
#             return "Тип диаграммы: Bar Chart (уверенность: 90%)"
#         else:
#             return "Тип диаграммы: Treemap (уверенность: 80%)"
#
#     # Логика для других типов диаграмм
#     best_match = None
#     best_score = 0
#
#     for chart_type, elements in ontology.items():
#         required = elements["required_elements"]
#
#         matched = len(detected_set.intersection(required))
#         score = matched * 2  # Считаем количество совпавших обязательных элементов
#
#         if score > best_score:
#             best_score = score
#             best_match = chart_type
#
#     if best_match is None:
#         return "Не удалось определить тип диаграммы."
#
#     # Строим красивый текст для вывода
#     element_summary = (
#         f"Найдено элементов:\n"
#         f"- Прямоугольники (rectangle): {rectangles_count}\n"
#         f"- Оси (axis): {axis_count}\n"
#         f"- Точки (point): {point_count}\n"
#         f"- Секторы (sector): {sector_count}\n"
#         f"- Линии (line): {line_count}\n"
#     )
#
#     confidence = min(100, 50 + best_score * 10)
#     final_result = f"Тип диаграммы: {best_match} (уверенность: {confidence}%)\n\n{element_summary}"
#     return final_result
import rdflib

# Загружаем онтологию
g = rdflib.Graph()
g.parse("D:/Programming/yoloyo/v2onto.rdf", format="xml")  # Замените путь на актуальный


def execute_sparql_query(query):
    """Функция для выполнения SPARQL-запроса к онтологии."""
    result = g.query(query)
    return result


def determine_chart_type(detected_elements):
    rectangles_count = detected_elements.count("rectangle")
    axis_count = detected_elements.count("axis")
    point_count = detected_elements.count("point")
    sector_count = detected_elements.count("sector")
    line_count = detected_elements.count("line")
    detected_set = set(detected_elements)

    # Формируем SPARQL запросы для каждого типа диаграммы
    sparql_queries = {
        "Bar Chart": """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?chart_type
        WHERE {
            ?chart_type rdf:type :Bar_chart .
            ?chart_type :has_axis ?axis .
            ?chart_type :has_rectangle ?rectangle .
        }
        """,

        "Pie Chart": """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?chart_type
        WHERE {
            ?chart_type rdf:type :Pie_chart .
            ?chart_type :has_sector ?sector .
        }
        """,

        "Scatter Plot": """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?chart_type
        WHERE {
            ?chart_type rdf:type :Scatter_plot .
            ?chart_type :has_point ?point .
        }
        """,

        "Line Graph": """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?chart_type
        WHERE {
            ?chart_type rdf:type :Line_graph .
            ?chart_type :has_line ?line .
        }
        """,

        "Treemap": """
        PREFIX : <http://www.semanticweb.org/yana/ontologies/2025/3/untitled-ontology-11#>
        SELECT ?chart_type
        WHERE {
            ?chart_type rdf:type :Treemap .
            ?chart_type :has_rectangle ?rectangle .
        }
        """
    }

    best_match = None
    best_score = -1
    chtype = None

    # # Логика для выбора подходящего запроса
    # if "rectangle" in detected_set and "axis" in detected_set:
    #     query = sparql_queries["Bar Chart"]
    # elif "sector" in detected_set:
    #     query = sparql_queries["Pie Chart"]
    # elif "point" in detected_set and point_count >= 3:
    #     query = sparql_queries["Scatter Plot"]
    # elif "line" in detected_set:
    #     query = sparql_queries["Line Graph"]
    # elif "rectangle" in detected_set:
    #     query = sparql_queries["Treemap"]
    # else:
    #     return "Не удалось определить тип диаграммы."

    # Выполняем запрос

    if "rectangle" in detected_set and "axis" in detected_set:
        query = sparql_queries["Bar Chart"]
        confidence = min(90, rectangles_count * 10 + axis_count * 15)
    elif "sector" in detected_set:
        query = sparql_queries["Pie Chart"]
        confidence = min(85, sector_count * 20)
    elif "point" in detected_set:
        query = sparql_queries["Scatter Plot"]
        confidence = min(80, point_count * 10)
    elif "line" in detected_set:
        query = sparql_queries["Line Graph"]
        confidence = min(80, line_count * 15)
    elif "rectangle" in detected_set:
        query = sparql_queries["Treemap"]
        confidence = min(85, rectangles_count * 20)
    else:
        return "Не удалось определить тип диаграммы."

    result = execute_sparql_query(query)

    # Проверяем наличие результата
    print(f"Результаты запроса для {query}:")
    for row in result:
        # Преобразуем результат в строку и выводим для отладки
        chtype = str(row[0])  # row[0] содержит URI
        print(f"Тип диаграммы: {chtype}")

        # Печатаем полный URI для отладки
        print(f"Полный URI: {row[0]}")

    # Если результат есть, возвращаем тип диаграммы
    if chtype:
        best_match = chtype  # Тип диаграммы по первому элементу

    if best_match is None:
        return "Не удалось распознать тип диаграммы."

    # Строим красивый текст для вывода
    element_summary = (
        f"Найдено элементов:\n"
        f"- Прямоугольники (rectangle): {rectangles_count}\n"
        f"- Оси (axis): {axis_count}\n"
        f"- Точки (point): {point_count}\n"
        f"- Секторы (sector): {sector_count}\n"
        f"- Линии (line): {line_count}\n"
    )

    # confidence = best_score
    final_result = f"Тип диаграммы: {best_match} (уверенность: {confidence}%)\n\n{element_summary}"
    return final_result



