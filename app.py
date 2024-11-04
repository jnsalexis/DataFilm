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

    # Récupération des paramètres de recherche
    page = request.args.get('page', 1, type=int)
    title_filter = request.args.get('title', '').strip()
    actor_filter = request.args.get('actor', '').strip()
    genre_filter = request.args.get('genre', '').strip()
    films_per_page = 28
    offset = (page - 1) * films_per_page

    # Récupérer la liste des genres pour le menu déroulant
    cursor.execute("SELECT DISTINCT name FROM genres ORDER BY name;")
    genres = cursor.fetchall()

    # Requête SQL de base pour récupérer les films avec pagination
    query = """
        SELECT films.id, films.title, films.release_date, films.vote_average, films.overview,
               GROUP_CONCAT(DISTINCT genres.name SEPARATOR ', ') AS genres,
               films.poster_url, films.backdrop_url
        FROM films
        LEFT JOIN film_genre ON films.id = film_genre.film_id
        LEFT JOIN genres ON film_genre.genre_id = genres.id
        LEFT JOIN film_acteur ON films.id = film_acteur.film_id
        LEFT JOIN acteurs ON film_acteur.acteur_id = acteurs.id
        WHERE 1=1
    """
    params = []

    # Ajout des filtres
    if title_filter:
        query += " AND films.title LIKE %s"
        params.append(f"%{title_filter}%")
    if actor_filter:
        query += " AND acteurs.name LIKE %s"
        params.append(f"%{actor_filter}%")
    if genre_filter:
        query += " AND genres.name = %s"
        params.append(genre_filter)

    # Ajout du groupement et de l'ordre de pagination
    query += """
        GROUP BY films.id
        ORDER BY films.vote_average DESC, films.vote_count DESC
        LIMIT %s OFFSET %s;
    """
    params.extend([films_per_page, offset])

    cursor.execute(query, tuple(params))
    movies = cursor.fetchall()

    # Calculer le nombre total de pages avec les filtres appliqués
    count_query = """
        SELECT COUNT(DISTINCT films.id) AS total
        FROM films
        LEFT JOIN film_genre ON films.id = film_genre.film_id
        LEFT JOIN genres ON film_genre.genre_id = genres.id
        LEFT JOIN film_acteur ON films.id = film_acteur.film_id
        LEFT JOIN acteurs ON film_acteur.acteur_id = acteurs.id
        WHERE 1=1
    """

    # Ajout des mêmes filtres à la requête de comptage
    count_params = []
    if title_filter:
        count_query += " AND films.title LIKE %s"
        count_params.append(f"%{title_filter}%")
    if actor_filter:
        count_query += " AND acteurs.name LIKE %s"
        count_params.append(f"%{actor_filter}%")
    if genre_filter:
        count_query += " AND genres.name = %s"
        count_params.append(genre_filter)

    cursor.execute(count_query, tuple(count_params))
    total_films = cursor.fetchone()['total']
    total_pages = math.ceil(total_films / films_per_page)

    cursor.close()
    db.close()

    # Renvoyer les filtres, la pagination, et les genres au template
    return render_template(
        'index.html',
        movies=movies,
        page=page,
        total_pages=total_pages,
        max=max,
        min=min,
        title_filter=title_filter,
        actor_filter=actor_filter,
        genre_filter=genre_filter,
        genres=genres
    )

# Route pour afficher les détails d'un film spécifique
@app.route('/movies/<int:film_id>')
def movie_details(film_id):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Requête pour obtenir les informations détaillées du film
    movie_query = """
        SELECT films.id, films.title, films.release_date, films.vote_average, films.overview,
               GROUP_CONCAT(DISTINCT genres.name SEPARATOR ', ') AS genres,
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
