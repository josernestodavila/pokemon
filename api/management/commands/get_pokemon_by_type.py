import aiohttp
import asyncio
from progress.bar import Bar

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.management.base import BaseCommand

from api.models import Pokemon
from api.utils import fetch, get_or_create_move, get_or_create_pokemon


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class Command(BaseCommand):
    help = "Retrieves Pokemon information by type"

    def add_arguments(self, parser):
        parser.add_argument("type_name", type=str, help="The name of the Pokemon type to search for")

    def handle(self, *args, **options):
        type_name = options["type_name"]
        url = f"https://pokeapi.co/api/v2/type/{type_name}/"

        async def get_pokemon():
            async with aiohttp.ClientSession() as session:
                response = await fetch(session, url)
                pokemon_urls = [pokemon["pokemon"]["url"] for pokemon in response["pokemon"]]

                for pokemon_url in pokemon_urls:
                    pokemon = await get_or_create_pokemon(session, pokemon_url)

                    move_ids = []

                    moves_bar = Bar(f"Downloading Moves for {pokemon.name}", max=len(response["moves"]))

                    for move in response["moves"]:
                        move_url = move.get("url")

                        self.stdout.write(f"URL {move['url']}")
                        if not move_url:
                            continue

                        move = await get_or_create_move(session, move_url)
                        move_ids.append(move.id)

                        moves_bar.next()
                    moves_bar.finish()

                    pokemon_moves_objects = [
                        Pokemon.moves.through(pokemon_id=pokemon.id, move_id=move_id) for move_id in move_ids
                    ]

                    if pokemon_moves_objects:
                        created_pokemon_moves = await Pokemon.moves.through.objects.abulk_create(
                            pokemon_moves_objects, ignore_conflicts=True
                        )
                        self.stdout.write(f"Created {len(created_pokemon_moves)} Pokemon moves")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_pokemon())
