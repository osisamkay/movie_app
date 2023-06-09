import requests
from termcolor import colored

class MovieApp:
    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage object.

        Args:
            storage (IStorage): The storage object to use for movie operations.
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        List all the movies stored in the storage.
        """
        movies = self._storage.list_movies()
        print("Listing movies:")
        for title, details in movies.items():
            print(f"Title: {title}")
            print(f"Year: {details['year']}")
            print(f"Rating: {details['rating']}")
            print(f"Poster: {details['poster_url']}")
            print()

    def _command_add_movie(self):
        """
        Add a movie to the storage by searching the movie details using the Omdb API.
        """
        title = input("Enter the movie title: ")
        response = self._search_movie(title)

        if response["Response"] == "True":

            year = response["Year"],
            rating = response["imdbRating"],
            poster_url = response["Poster"]
            print(year, rating, poster_url)
            self._storage.add_movie(title, year, rating, poster_url)
            print(f"Added movie: {title}")
        else:
            print(f"Failed to add movie: {title}")

    def _command_delete_movie(self):
        """
        Delete a movie from the storage.
        """
        title = input("Enter the movie title to delete: ")
        self._storage.delete_movie(title)
        print(f"Deleted movie: {title}")

    def _command_update_movie(self):
        """
        Update the notes for a movie in the storage.
        """
        title = input("Enter the movie title to update: ")
        notes = input("Enter the movie notes: ")
        self._storage.update_movie(title, notes)
        print(f"Updated movie: {title}")

    def _command_statistics(self):
        """
        Generate and display statistics about the movies in the storage.
        """
        self._storage.statistics()

    def _command_random_movies(self):
        """
        Display random movies from the storage.
        """
        self._storage.random_movie()

    def _command_search_movies(self):
        """
        Search for movies in the storage based on a given title.
        """
        title = input("Enter the movie title to search")
        self._storage.search_movie(title)

    def _command_sort_by_rating(self):
        """
        Sort the movies in the storage by rating.
        """
        self._storage.sort_by_rating()

    def _command_create_rating_histogram(self):
        """
        Create a rating histogram for the movies in the storage.
        """
        self._storage.create_rating_histogram()

    def _command_generate_website(self):
        """
        Generate a website showcasing the movies in the storage.
        """
        self._storage.generate_website()

    @staticmethod
    def _search_movie(title):
        """
        Search for a movie using the Omdb API.

        Args:
            title (str): The title of the movie to search.

        Returns:
            dict: Movie details obtained from the Omdb API.
        """
        url = f"http://www.omdbapi.com/?t={title}&apikey=608f304e"

        try:
            response = requests.get(url)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def run(self):
        """
        Run the movie app and display the menu to the user.
        """
        while True:
            print()
            print("Menu:")
            menus = ["Exit", "List Movies", "Add Movie", "Delete Movie", "Update Movie", "Stats", "Random Movie",
                     "Search Movie", "Movies sorted by rating", "Create Rating Histogram", "Generate website"]
            for menu in menus:
                print(colored(f'{menus.index(menu)}. {menu}', "yellow"))

            choice = input("Enter your choice (1-5): ")
            print()

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_statistics()
            elif choice == "6":
                self._command_random_movies()
            elif choice == "7":
                self._command_search_movies()
            elif choice == "8":
                self._command_sort_by_rating()
            elif choice == "9":
                self._command_create_rating_histogram()
            elif choice == "10":
                self._command_generate_website()
            elif choice == "0":
                print("Exiting the Movie App...")
                break
            else:
                print("Invalid choice. Please try again.")
                print()


