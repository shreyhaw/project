import tkinter as tk
from tkinter import ttk, messagebox

class MovieRecommendationSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, title, genre, rating, year, length):
        """Add a new movie with given title, genre, rating, year, and length."""
        movie = {'title': title, 'genre': genre, 'rating': rating, 'year': year, 'length': length, 'score': self.calculate_score(genre, rating, year, length)}
        self.movies.append(movie)
        print(f"Movie '{title}' added successfully!")

    def calculate_score(self, genre, rating, year, length):
        """Calculate the score of a movie based on its genre, rating, year, and length."""
        score = 0
        
        # Assign points based on rating
        if rating >= 9:
            score += 50
        elif rating >= 8:
            score += 40
        elif rating >= 7:
            score += 30
        elif rating >= 6:
            score += 20
        else:
            score += 10

        # Assign additional points based on genre
        if genre.lower() in ['drama', 'action', 'sci-fi', 'crime']:
            score += 20
        elif genre.lower() in ['comedy', 'romance', 'biography']:
            score += 10
        else:
            score += 5

        # Assign points based on year
        if year >= 2000:
            score += 10
        else:
            score += 5

        # Assign points based on length
        if length >= 120:
            score += 10
        else:
            score += 5

        return score

    def search_movies(self, search_type, search_term):
        """Search for movies by title or genre."""
        if search_type not in ['title', 'genre']:
            raise ValueError("search_type must be either 'title' or 'genre'")

        results = [movie for movie in self.movies if movie[search_type].lower() == search_term.lower()]
        return results

    def recommend_movies(self, top_n):
        """Recommend top N movies based on score."""
        sorted_movies = self.merge_sort(self.movies, key=lambda x: x['score'], reverse=True)
        return sorted_movies[:top_n]

    def delete_movie(self, title):
        """Delete a movie by title."""
        for movie in self.movies:
            if movie['title'].lower() == title.lower():
                self.movies.remove(movie)
                print(f"Movie '{title}' deleted successfully!")
                return
        print(f"Movie '{title}' not found!")

    def merge_sort(self, arr, key=lambda x: x, reverse=False):
        """Helper function to sort movies using merge sort based on a key."""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key=key, reverse=reverse)
        right = self.merge_sort(arr[mid:], key=key, reverse=reverse)

        return self.merge(left, right, key, reverse)

    def merge(self, left, right, key, reverse):
        """Merge helper for merge sort."""
        result = []
        while left and right:
            if reverse:
                if key(left[0]) > key(right[0]):
                    result.append(left.pop(0))
                else:
                    result.append(right.pop(0))
            else:
                if key(left[0]) < key(right[0]):
                    result.append(left.pop(0))
                else:
                    result.append(right.pop(0))

        result.extend(left if left else right)
        return result


class MovieRecommendationGUI:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Movie Recommendation System")

        # Frame for Adding Movies
        self.add_frame = ttk.LabelFrame(self.root, text="Add Movie")
        self.add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.title_label = ttk.Label(self.add_frame, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.genre_label = ttk.Label(self.add_frame, text="Genre:")
        self.genre_label.grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = ttk.Entry(self.add_frame)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        self.rating_label = ttk.Label(self.add_frame, text="Rating:")
        self.rating_label.grid(row=2, column=0, padx=5, pady=5)
        self.rating_entry = ttk.Entry(self.add_frame)
        self.rating_entry.grid(row=2, column=1, padx=5, pady=5)

        self.year_label = ttk.Label(self.add_frame, text="Year:")
        self.year_label.grid(row=3, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(self.add_frame)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5)

        self.length_label = ttk.Label(self.add_frame, text="Length (min):")
        self.length_label.grid(row=4, column=0, padx=5, pady=5)
        self.length_entry = ttk.Entry(self.add_frame)
        self.length_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Movie", command=self.add_movie)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Frame for Searching Movies
        self.search_frame = ttk.LabelFrame(self.root, text="Search Movie")
        self.search_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.search_type_label = ttk.Label(self.search_frame, text="Search by:")
        self.search_type_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_type = ttk.Combobox(self.search_frame, values=["title", "genre"])
        self.search_type.grid(row=0, column=1, padx=5, pady=5)

        self.search_term_label = ttk.Label(self.search_frame, text="Search term:")
        self.search_term_label.grid(row=1, column=0, padx=5, pady=5)
        self.search_term_entry = ttk.Entry(self.search_frame)
        self.search_term_entry.grid(row=1, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_movies)
        self.search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.search_results = tk.Text(self.search_frame, height=10, width=50)
        self.search_results.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for Recommending Movies
        self.recommend_frame = ttk.LabelFrame(self.root, text="Recommend Movies")
        self.recommend_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.top_n_label = ttk.Label(self.recommend_frame, text="Top N:")
        self.top_n_label.grid(row=0, column=0, padx=5, pady=5)
        self.top_n_entry = ttk.Entry(self.recommend_frame)
        self.top_n_entry.grid(row=0, column=1, padx=5, pady=5)

        self.recommend_button = ttk.Button(self.recommend_frame, text="Recommend", command=self.recommend_movies)
        self.recommend_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.recommend_results = tk.Text(self.recommend_frame, height=10, width=50)
        self.recommend_results.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Frame for Deleting Movies
        self.delete_frame = ttk.LabelFrame(self.root, text="Delete Movie")
        self.delete_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.delete_title_label = ttk.Label(self.delete_frame, text="Title:")
        self.delete_title_label.grid(row=0, column=0, padx=5, pady=5)
        self.delete_title_entry = ttk.Entry(self.delete_frame)
        self.delete_title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.delete_frame, text="Delete Movie", command=self.delete_movie)
        self.delete_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        rating = float(self.rating_entry.get())
        year = int(self.year_entry.get())
        length = int(self.length_entry.get())

        self.system.add_movie(title, genre, rating, year, length)
        messagebox.showinfo("Success", f"Movie '{title}' added successfully!")

    def search_movies(self):
        search_type = self.search_type.get()
        search_term = self.search_term_entry.get()

        results = self.system.search_movies(search_type, search_term)
        self.search_results.delete(1.0, tk.END)
        for movie in results:
            self.search_results.insert(tk.END, f"Title: {movie['title']}, Genre: {movie['genre']}, Rating: {movie['rating']}, Year: {movie['year']}, Length: {movie['length']} min, Score: {movie['score']}\n")

    def recommend_movies(self):
        top_n = int(self.top_n_entry.get())

        results = self.system.recommend_movies(top_n)
        self.recommend_results.delete(1.0, tk.END)
        for movie in results:
            self.recommend_results.insert(tk.END, f"Title: {movie['title']}, Genre: {movie['genre']}, Rating: {movie['rating']}, Year: {movie['year']}, Length: {movie['length']} min, Score: {movie['score']}\n")

    def delete_movie(self):
        title = self.delete_title_entry.get()

        self.system.delete_movie(title)
        messagebox.showinfo("Success", f"Movie '{title}' deleted successfully!")


# Create the main application window
root = tk.Tk()
system = MovieRecommendationSystem()
app = MovieRecommendationGUI(root, system)
root.mainloop()
