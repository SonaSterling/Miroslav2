import json
import tkinter as tk
from tkinter import ttk, messagebox

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        # Поля ввода
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Название").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Жанр").grid(row=0, column=2)
        self.genre_entry = tk.Entry(self.frame)
        self.genre_entry.grid(row=0, column=3)

        tk.Label(self.frame, text="Год выпуска").grid(row=1, column=0)
        self.year_entry = tk.Entry(self.frame)
        self.year_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Рейтинг").grid(row=1, column=2)
        self.rating_entry = tk.Entry(self.frame)
        self.rating_entry.grid(row=1, column=3)

        # Кнопка добавления
        self.add_button = tk.Button(self.frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(padx=10, pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0)
        self.genre_filter = tk.Entry(filter_frame)
        self.genre_filter.grid(row=0, column=1)

        tk.Label(filter_frame, text="Фильтр по году").grid(row=0, column=2)
        self.year_filter = tk.Entry(filter_frame)
        self.year_filter.grid(row=0, column=3)

        self.filter_button = tk.Button(filter_frame, text="Фильтровать", command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, padx=5)

        self.clear_filter_button = tk.Button(filter_frame, text="Очистить фильтр", command=self.load_movies)
        self.clear_filter_button.grid(row=0, column=5, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        for col in ("Название", "Жанр", "Год", "Рейтинг"):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10)

        # Загрузка данных
        self.load_data()

        # Обработчики закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        # Проверки
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_to_show = data if data is not None else self.movies
        for movie in data_to_show:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def apply_filter(self):
        genre_filter = self.genre_filter.get().lower()
        year_filter = self.year_filter.get()

        filtered = self.movies
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        if year_filter:
            try:
                year = int(year_filter)
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом")
                return
            filtered = [m for m in filtered if m["year"] == year]

        self.update_table(filtered)

    def save_data(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        except FileNotFoundError:
            self.movies = []
        self.update_table()

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
