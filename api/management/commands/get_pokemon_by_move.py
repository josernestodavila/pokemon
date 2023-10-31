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
    help = "Retrieves Pokemon information by move"

    def add_arguments(self, parser):
        parser.add_argument("move_name", type=str, help="The name of the Pokemon move to search for")

    def handle(self, *args, **options):
        move_name = options["move_name"]
        url = f"https://pokeapi.co/api/v2/move/{move_name}/"

        async def get_pokemon():
            async with aiohttp.ClientSession() as session:
                move_json = await fetch(session, url)
                move = await get_or_create_move(session, url)

                pokemon_urls = [pokemon["url"] for pokemon in move_json["learned_by_pokemon"]]

                bar = Bar(f"Downloading Pokemons for move: {move_name}", max=len(pokemon_urls))
                pokemon_download_coroutines = []
                for pokemon_url in pokemon_urls:
                    pokemon_download_coroutines.append(get_or_create_pokemon(session, pokemon_url))
                    bar.next()

                pokemons = await asyncio.gather(*pokemon_download_coroutines)

                await Pokemon.moves.through.objects.abulk_create(
                    [
                        Pokemon.moves.through(
                            pokemon_id=pokemon.id,
                            move_id=move.id,
                        )
                        for pokemon in pokemons
                    ],
                    ignore_conflicts=True,
                )
                bar.finish()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_pokemon())
