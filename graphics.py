import matplotlib.pyplot as plt
def draw_truth_table(img_name: str, variable_count: int):
    """Отрисовать таблицу истинности для выбранных значений в формате .png"""
    table_data = []

    for i in range(2 ** variable_count): # 🔴 РАЗОБРАТЬСЯ
        # бинарное представление числа i с ведущими нулями
        row = list(map(int, format(i, f"0{variable_count}b")))
        table_data.append(row)

    fig, ax = plt.subplots() # создаем субплоты
    ax.axis('off') # убираем оси с нумерацией
    table = ax.table(cellText=table_data, colLabels=['A','B', 'C', 'D'], loc='center', cellLoc='center')

    plt.savefig(f'{img_name}.png')