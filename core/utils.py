import pandas as pd

def fill_weights_table(detected_classes, all_diagram_data, old_table=None):
    detected_elements = sorted(set(elem.lower() for elem in detected_classes))

    # Получаем список диаграмм, в которых есть хотя бы один элемент с весом > 0
    relevant_diagrams = []
    for diagram, weights in all_diagram_data.items():
        if any(elem in weights and weights[elem] > 0 for elem in detected_elements):
            relevant_diagrams.append(diagram)

    relevant_diagrams.sort()
    headers = ["Элемент"] + relevant_diagrams

    # Чтение старых значений, строгое соответствие названий
    previous_values = {}
    if isinstance(old_table, pd.DataFrame):
        expected_headers = ["Элемент"] + relevant_diagrams
        if list(old_table.columns) == expected_headers:
            for _, row in old_table.iterrows():
                element_name = str(row["Элемент"]).strip().lower()
                if element_name in detected_elements:
                    for diag in relevant_diagrams:
                        key = (element_name, diag)
                        try:
                            weight = float(row[diag])
                        except Exception:
                            weight = None
                        if weight is not None:
                            previous_values[key] = weight

    # Сбор таблицы
    table_data = []
    for elem in detected_elements:
        row = [elem]
        for diag in relevant_diagrams:
            key = (elem, diag)
            weight = previous_values.get(key, all_diagram_data.get(diag, {}).get(elem, 0.0))
            row.append(weight)
        table_data.append(row)

    return headers, table_data

def parse_weights(weight_data):
    if weight_data is None or weight_data.empty:
        return {}

    weight_dict = {}

    for i, row in weight_data.iterrows():
        element = str(row.iloc[0]).strip().lower()
        weight_dict[element] = {}

        for diagram in weight_data.columns[1:]:
            try:
                value = float(row[diagram])
                # Ограничение значений в пределах [0, 1]
                if value < 0 or value > 1:
                    print(f"⚠️ Было введено значение вне допустимого диапазона [0, 1] — будет обрезано.")
                clamped_value = min(max(value, 0.0), 1.0)
                weight_dict[element][diagram] = clamped_value
            except (ValueError, TypeError):
                weight_dict[element][diagram] = 0.0  # дефолт, если ошибка

    print("PARSED CUSTOM WEIGHTS:", weight_dict)
    return weight_dict

def validate_and_fix_weights(table):
    had_error = False
    for i, row in table.iterrows():
        for j in range(1, len(row)):
            val = row.iloc[j]
            try:
                num = float(val)
                if num < 0.0 or num > 1.0:
                    raise ValueError
                table.iat[i, j] = round(num, 2)
            except:
                table.iat[i, j] = 0.0
                had_error = True
    return table, had_error
