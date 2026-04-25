# visualizer.py
import tkinter as tk
from tkinter import ttk
from typing import List, Dict
import alts
from main import make_zade
from zade import Alternative

class BellmanZadeVisualizer:
    def __init__(self, root: tk.Tk, alternatives: List[Alternative]):
        self.root = root
        self.root.title("Метод Беллмана-Заде")
        self.alternatives = alternatives

        # Получаем результаты расчёта
        self.best_alt, self.scores = make_zade(alternatives)

        # Собираем все имена критериев (Constraints + Goals)
        sample = alternatives[0]
        self.criteria_names = [c.name for c in sample.constraints]
        self.goal_names = [g.name for g in sample.goals]
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        style.configure('Normal.TLabel', background='white')
        style.configure('Best.TLabel', background='lightgreen')
        style.configure('Normal.TFrame', background='white')
        style.configure('Best.TFrame', background='lightgreen')

        # Заголовки столбцов
        idx = 0
        columns = ["Альтернатива"] + self.criteria_names
        for _, col_name in enumerate(columns):
            lbl = ttk.Label(self.root, text=col_name, borderwidth=1, relief="solid",
                            anchor="center", background="lightgray")
            lbl.grid(row=0, column=idx, sticky="nsew", padx=1, pady=1)
            idx += 1

        columns = list(self.goal_names)
        for _, col_name in enumerate(columns):
            lbl = ttk.Label(self.root, text=col_name, borderwidth=1, relief="solid",
                            anchor="center", background="pale goldenrod")
            lbl.grid(row=0, column=idx, sticky="nsew", padx=1, pady=1)
            idx += 1

        columns = ["Результат"]
        for _, col_name in enumerate(columns):
            lbl = ttk.Label(self.root, text=col_name, borderwidth=1, relief="solid",
                            anchor="center", background="lightgray")
            lbl.grid(row=0, column=idx, sticky="nsew", padx=1, pady=1)
            idx += 1

        # Строки с данными
        for row_idx, alt in enumerate(self.alternatives, start=1):
            is_best = (alt.name == self.best_alt.name)
            label_style = 'Best.TLabel' if is_best else 'Normal.TLabel'
            frame_style = 'Best.TFrame' if is_best else 'Normal.TFrame'

            # Название альтернативы
            ttk.Label(self.root, text=alt.name, style=label_style,
                      borderwidth=1, relief="solid").grid(row=row_idx, column=0, sticky="nsew")

            col = 1
            # Constraints
            for c in alt.constraints:
                self._create_progress_cell(row_idx, col, c.value, frame_style, label_style)
                col += 1
            # Goals
            for g in alt.goals:
                self._create_progress_cell(row_idx, col, g.value, frame_style, label_style)
                col += 1

            # Итоговая оценка
            score = self.scores[alt.name]
            self._create_progress_cell(row_idx, col, score, frame_style, label_style)

        # Настройка растяжения колонок и строк
        for i in range(len(columns)):
            self.root.columnconfigure(i, weight=1)
        for i in range(len(self.alternatives) + 1):
            self.root.rowconfigure(i, weight=1)

    def _create_progress_cell(self, row: int, col: int, value: float,
                              frame_style: str, label_style: str):
        frame = ttk.Frame(self.root, style=frame_style, borderwidth=1, relief="solid")
        frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        # Прогресс-бар
        pb = ttk.Progressbar(frame, maximum=1.0, value=value, length=80)
        pb.pack(side=tk.LEFT, padx=3, pady=3, fill=tk.X, expand=True)
        # Числовое значение
        lbl = ttk.Label(frame, text=f"{value:.2f}", style=label_style, width=5)
        lbl.pack(side=tk.LEFT, padx=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = BellmanZadeVisualizer(root, alts.formats)
    root.mainloop()
