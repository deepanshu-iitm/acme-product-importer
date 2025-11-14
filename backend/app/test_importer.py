from backend.app.tasks import import_csv_to_db

result = import_csv_to_db("uploads/test.csv")
print(result)