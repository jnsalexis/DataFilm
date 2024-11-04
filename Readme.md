# Documentation de l'API DataFilm

Cette API permet de gérer des informations sur les films, notamment de les lister, de filtrer par titre, acteur ou genre, et de consulter les détails de chaque film.

## Base URL
Toutes les requêtes de l'API sont basées sur cette URL :

http://localhost:5000/

## Endpoints disponibles

### 1. Liste des films avec filtres et pagination

- **Endpoint** : `/movies`
- **Méthode** : `GET`
- **Description** : Cet endpoint retourne une liste de films avec la possibilité de filtrer par titre, acteur, et genre. Les résultats sont paginés.

#### Paramètres de requête :
- `page` (int, facultatif) : Numéro de la page pour la pagination. Par défaut, 1.
- `title` (string, facultatif) : Filtre par le titre du film.
- `actor` (string, facultatif) : Filtre par le nom de l'acteur.
- `genre` (string, facultatif) : Filtre par genre du film.

#### Réponse : JSON contenant les informations suivantes :
- `movies` (array) : Liste des films avec les informations suivantes pour chaque film :
  - `id` (int) : Identifiant du film.
  - `title` (string) : Titre du film.
  - `release_date` (date) : Date de sortie du film.
  - `vote_average` (float) : Note moyenne des votes.
  - `overview` (string) : Résumé du film.
  - `genres` (string) : Genres du film sous forme de chaîne séparée par des virgules.
  - `poster_url` (string) : URL de l'affiche du film.
  - `backdrop_url` (string) : URL du fond d'écran du film.
- `page` (int) : Numéro de la page actuelle.
- `total_pages` (int) : Nombre total de pages avec les filtres appliqués.
- `title_filter`, `actor_filter`, `genre_filter` (string) : Les valeurs des filtres de recherche appliqués.
- `genres` (array) : Liste des genres disponibles pour le filtrage.

#### Exemple de requête :
```http
GET /movies?page=2&title=Matrix&actor=Keanu&genre=Sci-Fi
```
#### Exemple de réponse :
```json
{
  "movies": [
    {
      "id": 1,
      "title": "The Matrix",
      "release_date": "1999-03-31",
      "vote_average": 8.7,
      "overview": "A computer hacker learns from mysterious rebels...",
      "genres": "Action, Sci-Fi",
      "poster_url": "https://example.com/poster.jpg",
      "backdrop_url": "https://example.com/backdrop.jpg"
    }
  ],
  "page": 2,
  "total_pages": 10,
  "title_filter": "Matrix",
  "actor_filter": "Keanu",
  "genre_filter": "Sci-Fi",
  "genres": [
    {"name": "Action"},
    {"name": "Sci-Fi"}
  ]
}
```

### 2. Détails d'un film spécifique
- **Endpoint** : `/movies/<film_id>`
- **Méthode** : `GET`
- **Description** : Cet endpoint retourne les détails complets d'un film spécifique, y compris sa liste d'acteurs.

#### Paramètres d'URL :
- **film_id** (int) : Identifiant unique du film.

**Réponse : JSON contenant les informations suivantes pour le film spécifié :**
- `movie` (object) :
- `id` (int) : Identifiant du film.
- `title` (string) : Titre du film.
- `release_date` (date) : Date de sortie du film.
- `vote_average` (float) : Note moyenne des votes.
- `overview` (string) : Résumé du film.
- `genres` (string) : Genres du film sous forme de chaîne séparée par des virgules.
- `poster_url` (string) : URL de l'affiche du film.
- `backdrop_url` (string) : URL du fond d'écran du film.
- `actors` (array) : Liste des acteurs du film avec les informations suivantes :
- `name` (string) : Nom de l'acteur.

#### Exemple de requête :
```http 
GET /movies/1
```
#### Exemple de réponse :
```json
{
  "movie": {
    "id": 1,
    "title": "The Matrix",
    "release_date": "1999-03-31",
    "vote_average": 8.7,
    "overview": "A computer hacker learns from mysterious rebels...",
    "genres": "Action, Sci-Fi",
    "poster_url": "https://example.com/poster.jpg",
    "backdrop_url": "https://example.com/backdrop.jpg"
  },
  "actors": [
    {"name": "Keanu Reeves"},
    {"name": "Laurence Fishburne"}
  ]
}
```

## Notes
- **Connexion à la base de données** : La base de données MySQL doit être configurée correctement pour utiliser l'application. Assurez-vous que les informations de connexion dans connect_to_db() sont exactes.
- **Gestion des erreurs** : En cas de problème de connexion ou de requêtes malformées, l'API retournera une erreur HTTP appropriée.