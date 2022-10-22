

def movies(load_from):
    return f"""
    SELECT film.id,
    film.rating as imdb_rating,
    ARRAY_AGG(DISTINCT genre.name) AS genre,
    film.title,
    film.description,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'director') AS director,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'actor') AS actors_names,
    ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'writer') AS writers_names,
    ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE person_film.role = 'actor') AS actors,
    ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE person_film.role = 'writer') AS writers,
    GREATEST(film.modified, MAX(person.modified), MAX(genre.modified)) AS modified
    FROM content.film_work film
    LEFT JOIN content.genre_film_work AS genre_film ON film.id = genre_film.film_work_id
    LEFT JOIN content.genre AS genre ON genre_film.genre_id = genre.id
    LEFT JOIN content.person_film_work AS person_film ON film.id = person_film.film_work_id
    LEFT JOIN content.person AS person ON person_film.person_id = person.id
    WHERE GREATEST(film.modified, person.modified, genre.modified) > '{load_from}'
    GROUP BY film.id
    ORDER BY GREATEST(film.modified, MAX(person.modified), MAX(genre.modified)) ASC
    """
