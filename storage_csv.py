import csv
from istorage import IStorage
import matplotlib.pyplot as plt
import requests
from fuzzywuzzy import fuzz
from termcolor import colored
import random


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the CSV
        file and returns the data.

        For example, the function may return:
        {
          "Titanic": {
            "rating": 9,
            "year": 1999
          },
          "..." {
            ...
          },
        }
        """
        movies = {}
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['title'].strip()
                rating = row['rating'].strip()
                year = row['year'].strip()
                poster_url=row['poster_url']
                movies[title] = {
                    'rating': rating,
                    'year': year,
                    'poster_url':poster_url
                }
        return movies

    def add_movie(self, title, year, rating, poster):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year, poster])

        print(f"Added movie: {title}")

    def delete_movie(self, title):
        movies = self.list_movies()

        if title in movies:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['title', 'rating', 'year', 'poster_url'])
                for movie_title, movie_data in movies.items():
                    if movie_title != title:
                        writer.writerow([
                            movie_title,
                            str(movie_data['rating']),
                            str(movie_data['year']),
                            movie_data.get('poster_url', '')
                        ])
            print(f"Deleted movie: {title}")
        else:
            print(f"Movie not found: {title}")

    def update_movie(self, title, notes):
        movies = self.list_movies()

        if title in movies:
            movies[title]['notes'] = notes

            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['title', 'rating', 'year', 'poster_url'])
                for movie_title, movie_data in movies.items():
                    writer.writerow([
                        movie_title,
                        str(movie_data['rating']),
                        str(movie_data['year']),
                        movie_data.get('poster_url', '')
                    ])
            print(f"Updated movie: {title}")
        else:
            print(f"Movie not found: {title}")

    def statistics(self):
        movies = self.list_movies()
        ratings = [movie["rating"] for movie in movies.values()]
        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)
        mid = len(ratings) // 2
        if len(ratings) % 2 == 0:
            median_rating = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
        else:
            median_rating = sorted_ratings[mid]
        best_movies = [name for name, movie in movies.items() if movie["rating"] == max(ratings)]
        worst_movies = [name for name, movie in movies.items() if movie["rating"] == min(ratings)]
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating}")
        print("Best movie(s):")
        for movie in best_movies:
            print(f"{movie}: {movies[movie]}")
        print("Worst movie(s):")
        for movie in worst_movies:
            print(f"{movie}: {movies[movie]}")

    def random_movie(self):
        movies = self.list_movies()
        name, rating = random.choice(list(movies.items()))
        print(f"Random movie: {name}, {rating}")

    def search_movie(self, title):
        movies = self.list_movies()
        matches = []
        for movie, rating in movies.items():
            # use partial_ratio to get a score of how similar the query is to the movie name
            score = fuzz.partial_ratio(title.lower(), movie.lower())
            if score >= 70:  # consider a match if score is above 70
                matches.append((movie, rating, score))

        if not matches:
            print(colored("No movies found.", "red"))
        else:
            matches.sort(key=lambda x: x[2], reverse=True)  # sort by score
            print(f"The movie {title} does not exist. Do you mean:")
            for movie, rating, score in matches:
                print(f"{movie}, {rating} (match score: {score})")

    def sort_by_rating(self):
        movies = self.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        for movie, data in sorted_movies:
            print(f"{movie}: {data['rating']}")

    def create_rating_histogram(self):
        movies = self.list_movies()
        ratings = [movie["rating"] for movie in movies.values()]

        # create histogram plot
        plt.hist(ratings, bins=10, range=(0, 10), edgecolor='black')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.title('Rating Histogram')

        # save plot to file
        filename = input("Enter filename to save plot to: ")
        plt.savefig(filename)

        print(f"Histogram saved to {filename}")

    def generate_website(self):
        movies = self.list_movies()

        # Generate movie grid HTML code
        movie_grid_html = ""
        for title, movie in movies.items():
            if 'poster_url' in movie:
                poster_url = movie['poster_url']
            else:
                poster_url = ""
            movie_grid_html += f"""
                <li >
                    <div class="movie">
                        <img class="movie-poster" src="{poster_url}" alt="{title}"/>
                        <h2 class="movie-title">{title}</h2>
                        <div class="movie-year"> {movie['year']}</div>
                    <div>
                </li>
            """

        # Load template from file
        with open("_static/index_template.html", "r") as fileObj:
            template = fileObj.read()

        # Replace placeholders with actual values
        template = template.replace("__TEMPLATE_TITLE__", "My Movie App")
        template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

        # Write generated HTML code to file
        with open("_static/index.html", "w") as fileObj:
            fileObj.write(template)

        print("Website was generated successfully.")
