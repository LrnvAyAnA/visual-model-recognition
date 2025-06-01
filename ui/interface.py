import gradio as gr
from core.process import process_image
from core.utils import validate_and_fix_weights

# UI функция: распознавание и обновление таблицы весов
def process_and_update_table(image):
    image_with_boxes, result_text, headers, table_data = process_image(image, return_weights_table=True)

    # Сброс уведомлений
    return (
        image_with_boxes,
        result_text,
        gr.update(headers=headers, value=table_data),
        ""
    )


# UI функция: перераспознавание с ручными весами
def process_with_weights(image, weight_table):
    # Валидируем и фиксируем значения вручную введённых весов
    cleaned_table, had_error = validate_and_fix_weights(weight_table)

    # Запускаем распознавание и расчёт
    image_with_boxes, result_text, headers, table_data = process_image(
        image, cleaned_table, return_weights_table=True
    )

    datatypes = ["str"] + ["number"] * (len(headers) - 1)

    return (
        image_with_boxes,
        result_text,
        gr.update(
            headers=headers,
            value=table_data,
            datatype=datatypes,
            col_count=(len(headers), "fixed"),
            row_count=(len(table_data), "fixed")
        ),
        "⚠️ Значение вне допустимого диапазона [0, 1] — будет обрезано." if had_error else ""
    )


with gr.Blocks() as interface:
    # О СИСТЕМЕ
    with gr.Row():
        with gr.Column(scale=4):
            pass
        with gr.Column(scale=1):
            info_button = gr.Button("О системе")
        info_state = gr.State(False)

    info_box = gr.Markdown(visible=False)


    def toggle_info(is_visible):
        if is_visible:
            return gr.update(visible=False), False
        else:
            return gr.update(visible=True, value="""
    ### Что делает система
    Это прототип рекомендательной системы, которая распознаёт структуру визуальной диаграммы по изображению и предлагает наиболее подходящие базовые типы визуализаций.
    ---
    ### Как пользоваться
    1. Загрузите изображение диаграммы.
    2. Система распознаёт визуальные элементы.
    3. Вы получаете список наиболее вероятных типов визуализаций.
    4. При необходимости — настраиваете веса признаков вручную.
    """), True


    info_button.click(fn=toggle_info, inputs=info_state, outputs=[info_box, info_state])

    with gr.Row():
        image_input = gr.Image(type="numpy", label="Загрузите изображение диаграммы")
        image_output = gr.Image(type="numpy", label="Результат с распознанными элементами", width=300)

    with gr.Row():
        result_box = gr.Textbox(label="Текстовый результат", lines=12)
        notification_box = gr.Textbox(label="Уведомление", interactive=False)

    gr.Markdown("### Ручная настройка весов элементов")

    weight_table = gr.Dataframe(
        headers=["Элемент"],
        datatype=["str"],
        value=[],
        interactive=True,
        row_count=(1, "dynamic"),
        label="Таблица весов",
        type="pandas"
    )

    with gr.Row():
        update_button = gr.Button("Перераспознать с новыми весами")
        reset_button = gr.Button("Сбросить веса по умолчанию")

    # Загрузка изображения
    image_input.change(
        fn=process_and_update_table,
        inputs=image_input,
        outputs=[image_output, result_box, weight_table, notification_box]
    )



    # Перераспознавание
    update_button.click(
        fn=process_with_weights,
        inputs=[image_input, weight_table],
        outputs=[image_output, result_box, weight_table, notification_box]
    )

    # Сброс весов
    reset_button.click(
        fn=process_and_update_table,
        inputs=image_input,
        outputs=[image_output, result_box, weight_table, notification_box]
    )


    # def show_info():
    #     return gr.update(value="""
    # ### 🧩 **Что делает система**
    # Это прототип рекомендательной системы, которая распознаёт структуру визуальной диаграммы на изображении и предлагает наиболее подходящие базовые типы визуализаций на основе онтологии.
    #
    # ---
    #
    # ### 📋 **Как пользоваться**
    # 1. Загрузите изображение диаграммы (можно перетянуть или выбрать вручную).
    # 2. Система автоматически распознает визуальные элементы (прямоугольники, подписи, круги и т.п.).
    # 3. Отображаются предложения по типу визуализации с указанием степени соответствия.
    # 4. При необходимости можно вручную изменить веса признаков, чтобы уточнить рекомендации.
    # """, visible=True)
    #
    #
    # info_button.click(fn=show_info, outputs=info_output)

if __name__ == "__main__":
    interface.launch()