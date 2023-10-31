# Django and GraphQL API for Pokemons

This is a small project to explore the async capabilities of Django ORM and how to integrate Strawberry GraphQL inside Django.
The project has two management commands to create Pokemons by type and to create Pokemons by move.

## Requirements

The project requires a PostgreSQL database and Redis for cache. This repository contains a Makefile and a docker compose configuration to 
run the project using Docker. These are the two suggested ways to run the project in your local:

### Docker Setup

You must have Docker Desktop running in your local and then follow these steps:

1. Clone this repository (`git clone https://github.com/josernestodavila/pokemon.git`).
2. Change to the project directory (`cd pokemon`).
3. Run `make run`. Once the containers are up open your web browser and go to the next step.
4. In your web browser go to `http://localhost:5500/graphql/`. You should see the graphql web UI.

### Hybrid setup

The hybrid setup leverages running PostgreSQL and Redis in Docker and the Django project running from your local machine. It requires at least
Python 3.11.6.

1. Clone this repository (`git clone https://github.com/josernestodavila/pokemon.git`).
2. Change to the project directory (`cd pokemon`).
3. Run `docker compose up -d database redis`. Once the containers are running.
4. Run `make venv`. This command creates a Python virtual environment and installs the project's dependencies.

## Loading data into the database

As mentioned above, you can load data by querying the Pokemon API, you can use two management commands to load data into the database.

### Get Pokemon by type.

To get all the pokemons of one type you can use the `get_pokemon_by_type` management command.

- Run the command with `python manage.py get_pokemon_by_type lighting` to get all the pokemons of type `lighting`.
If you are running the project in docker you can use the command like this: `docker exec -ti pokemon-api-1 python manage.py get_pokemon_by_type lighting`.

You can check the Pokemon API to see all the different types available.

### Get Pokemon by move.

In the same way, you can use the `get_pokemon_by_move` management command to get all the pokemons that can learn a given move.

- Run the command with ` python manage.py get_pokemon_by_move roar` to get all the pokemons that can learn the `roar` move. If you are running the project with docker
you can run the command like this: `docker exec -ti pokemon-api-1 python manage.py get_pokemon_by_move roar`. This command creates the pokemons and also the association to the move table.
