from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """Retrieve a list of movies from the storage."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Add a movie to the storage.

        Args:
            title (str): The title of the movie.
            year (str): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL or path to the movie's poster.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie from the storage.

        Args:
            title (str): The title of the movie to be deleted.

        Returns:
            None
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Update the notes for a movie in the storage.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The updated notes for the movie.

        Returns:
            None
        """
        pass
