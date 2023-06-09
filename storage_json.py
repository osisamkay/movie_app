from istorage import IStorage
import json
import matplotlib.pyplot as plt
import requests
from fuzzywuzzy import fuzz
from termcolor import colored
import random


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initialize the StorageJson with the file path of the JSON database.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies' information in the database.

        The function loads the information from the JSON file and returns the data.

        Returns:
            dict: A dictionary containing the movies' information.
                Example:
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
        with open(self.file_path, 'r') as file:
            movies = json.load(file)
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Add a movie to the database.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL of the movie poster.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

        movies[title] = {
            'year': year,
            'rating': rating,
            'poster_url': poster
        }

        with open(self.file_path, 'w') as file:
            json.dump(movies, file)

        print(f"Added movie: {title}")

    def delete_movie(self, title):
        """
        Delete a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

        if title in movies:
            del movies[title]
            with open(self.file_path, 'w') as file:
                json.dump(movies, file)
            print(f"Deleted movie: {title}")
        else:
            print(f"Movie not found: {title}")

    def update_movie(self, title, notes):
        """
        Update the notes for a movie in the database.

        Args:
            title (str): The title of the movie to update.
            notes (str): The notes to update for the movie.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

        if title in movies:
            movies[title]['notes'] = notes
            with open(self.file_path, 'w') as file:
                json.dump(movies, file)
            print(f"Updated movie: {title}")
        else:
            print(f"Movie not found: {title}")

    def statistics(self):
        """
        Generate and display statistics about the movies in the database.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

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
        """
        Get a random movie from the database and print its information.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)
        name, rating = random.choice(list(movies.items()))
        print(f"Random movie: {name}, {rating}")

    def search_movie(self, title):
        """
        Search for movies in the database based on a partial title match.

        Args:
            title (str): The partial title to search for.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)
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
        """
        Print the movie database sorted by rating in descending order.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        for movie, data in sorted_movies:
            print(f"{movie}: {data['rating']}")

    def create_rating_histogram(self):
        """
        Create a histogram plot of movie ratings and save it to a file.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

        # get ratings from movie database
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
        """
        Generate a static website with movie information.

        Returns:
            None
        """
        with open(self.file_path, 'r') as file:
            movies = json.load(file)

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
