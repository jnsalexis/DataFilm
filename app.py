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
def home():
    return get_movies()

@app.route('/movies')
def get_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Paramètres de pagination
    page = request.args.get('page', 1, type=int)
    films_per_page = 28
    offset = (page - 1) * films_per_page

    # Requête SQL pour récupérer les films avec une limite de pagination
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

    # Calculer le nombre total de pages
    cursor.execute("SELECT COUNT(*) AS total FROM films")
    total_films = cursor.fetchone()['total']
    total_pages = math.ceil(total_films / films_per_page)

    cursor.close()
    db.close()

    # Passer les informations de pagination, ainsi que les fonctions `max` et `min`
    return render_template(
        'index.html',
        movies=movies,
        page=page,
        total_pages=total_pages,
        max=max,
        min=min
    )

# Route pour afficher les détails d'un film spécifique
@app.route('/movies/<int:film_id>')
def movie_details(film_id):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Requête pour obtenir les informations détaillées du film
    movie_query = """
        SELECT films.id, films.title, films.release_date, films.vote_average, films.overview,
               GROUP_CONCAT(genres.name SEPARATOR ', ') AS genres,
               films.poster_url, films.backdrop_url
        FROM films
        LEFT JOIN film_genre ON films.id = film_genre.film_id
        LEFT JOIN genres ON film_genre.genre_id = genres.id
        WHERE films.id = %s
        GROUP BY films.id;
    """
    cursor.execute(movie_query, (film_id,))
    movie = cursor.fetchone()

    # Requête pour obtenir la liste des acteurs du film
    actor_query = """
        SELECT acteurs.name
        FROM film_acteur
        JOIN acteurs ON film_acteur.acteur_id = acteurs.id
        WHERE film_acteur.film_id = %s;
    """
    cursor.execute(actor_query, (film_id,))
    actors = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('movie_details.html', movie=movie, actors=actors)

if __name__ == '__main__':
    app.run(debug=True)
