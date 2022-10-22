
def create_table_person():
    return """
    CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE);
    """


def create_table_genre():
    return """
    CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE);
    """


def create_table_film_work():
    return """
    CREATE TABLE IF NOT EXISTS content.film_work (
        id uuid PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        creation_date DATE,
        file_path TEXT,
        rating FLOAT,
        type TEXT NOT NULL,
        created TIMESTAMP WITH TIME ZONE,
        modified TIMESTAMP WITH TIME ZONE);
    """


def create_table_genre_film_work():
    return"""
    CREATE TABLE IF NOT EXISTS content.genre_film_work (
        id uuid PRIMARY KEY,
        genre_id uuid NOT NULL,
        film_work_id uuid NOT NULL,
        created TIMESTAMP WITH TIME ZONE);
    """


def create_table_person_film_work():
    return """
    CREATE TABLE IF NOT EXISTS content.person_film_work (
        id uuid PRIMARY KEY,
        film_work_id uuid NOT NULL,
        person_id uuid NOT NULL,
        role TEXT NOT NULL,
        created TIMESTAMP WITH TIME ZONE);
    """


def create_schema():
    return"""
    CREATE SCHEMA IF NOT EXISTS content;
    """
