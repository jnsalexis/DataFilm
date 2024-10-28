from flask import Flask, render_template, request
import mysql.connector
import math

app = Flask(__name__)

# Connexion à la base de données MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bigdata_films_db"
    )

@app.route('/')
def index():
    # Récupère le numéro de page, par défaut à 1 si non précisé
    page = request.args.get('page', 1, type=int)
    films_per_page = 30
    offset = (page - 1) * films_per_page

    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Requête SQL pour récupérer les films avec limite de pagination
    query = """
        SELECT films.id, films.title, films.release_date, films.vote_average, films.overview,
               GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres,
               films.poster_url, films.backdrop_url
        FROM films
        LEFT JOIN film_genre ON films.id = film_genre.film_id
        LEFT JOIN genres ON film_genre.genre_id = genres.id
        GROUP BY films.id
        ORDER BY films.vote_average DESC, films.vote_count DESC
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (films_per_page, offset))
    movies = cursor.fetchall()

    # Récupérer le nombre total de films pour calculer le nombre de pages
    cursor.execute("SELECT COUNT(*) AS total FROM films")
    total_films = cursor.fetchone()['total']
    total_pages = math.ceil(total_films / films_per_page)

    cursor.close()
    db.close()

    # Passer les films et la pagination au template
    return render_template('index.html', movies=movies, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
