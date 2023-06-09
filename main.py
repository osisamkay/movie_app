from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

storage_type = input("Enter storage type (json/csv): ")

if storage_type == "json":
    storage = StorageJson('movies.json')
elif storage_type == "csv":
    storage = StorageCsv('movies.csv')
else:
    print("Invalid storage type. Exiting...")
    exit()

movie_app = MovieApp(storage)
movie_app.run()
