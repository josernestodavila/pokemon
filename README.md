# Django and GraphQL API for Pokemons

This is a small project to explore the async capibilities of Django ORM and how to integrate Strawberry GraphQL inside Django.
The project has to management commands to create Pokemons by type and to create Pokemons by move.

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

The hybrid setup leverage on running PostgreSQL and Redis in Docker and the Django project running from your local machine. It requires at least
Python 3.11.6.

1. Clone this repository (`git clone https://github.com/josernestodavila/pokemon.git`).
2. Change to the project directory (`cd pokemon`).
3. Run `docker compose up -d database redis`. Once the containers are running.
4. Run `make venv`. This command creates a Python virtual environment and install the project's dependencies.

