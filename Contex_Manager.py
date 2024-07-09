import psycopg2

class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg2.connect(database='my_database', 
                                     user='postgres',
                                     password='123', 
                                     host='localhost', 
                                     port=5432)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

def create_tables():
    create_authors_table = """
    CREATE TABLE IF NOT EXISTS authors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_authors_table)
            conn.commit()

# -----------------------------CRUD operations------------------------------
def create_author(name):
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO authors (name) VALUES (%s)", (name,))
            conn.commit()

def read_authors():
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM authors")
            return cursor.fetchall()

def update_author(author_id, new_name):
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE authors SET name = %s WHERE id = %s", (new_name, author_id))
            conn.commit()

def delete_author(author_id):
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM authors WHERE id = %s", (author_id,))
            conn.commit()

# create_tables()

create_author("New Author")
authors = read_authors()
print("Authors:", authors)

update_author(authors[-1][0], "Updated Author")
authors = read_authors()
print("Updated Authors:", authors)

delete_author(authors[-1][0])
authors = read_authors()
print("Final Authors:", authors)