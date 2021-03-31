import asyncio
import aiohttp
import json
from aiohttp import web

api_for_request = {
    'api_1': {
        'name': 'chuck-norris-jokes',
        'url': 'https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random',
        'headers': {'accept': "application/json",
                     'x-rapidapi-key': "480132ecb5mshe3ae13823b0d0f4p1a4b01jsn797154c67941",
                     'x-rapidapi-host': "matchilling-chuck-norris-jokes-v1.p.rapidapi.com"},
        'returned': 'value'
    },
    'api_2': {
        'name': 'jokeapi',
        'url': 'https://jokeapi-v2.p.rapidapi.com/joke/Any',
        'querystring': {"format": "json", "blacklistFlags": "nsfw,racist",
                        "idRange": "0-303", "type": "single"},
        'headers': {'x-rapidapi-key': "480132ecb5mshe3ae13823b0d0f4p1a4b01jsn797154c67941",
                    'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com"},
        'returned': 'joke'
    },
    'api_3': {
        'name': 'geek-jokes',
        'url': 'https://geek-jokes.p.rapidapi.com/api',
        'querystring': {"format":"json"},
        'headers': {'x-rapidapi-key': "480132ecb5mshe3ae13823b0d0f4p1a4b01jsn797154c67941",
                    'x-rapidapi-host': "geek-jokes.p.rapidapi.com"},
        'returned': 'joke'
    }
}

async def requester(api):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=api_for_request[api]['url'],
                               headers=api_for_request[api]['headers'],
                               params=api_for_request[api]['querystring']
                               if 'querystring' in api_for_request[api] else None) as response:
            resp = await response.text()
            resp_python = json.loads(resp)
            joke_name = api_for_request[api]['returned']
            jokes = f"\n\njoke of the day from {api_for_request[api]['name']}:\n\n{resp_python[joke_name]}\n\n"
            return jokes


routes = web.RouteTableDef()


@routes.get('/collect_info')
async def handle(request):
    response = await asyncio.gather(*(requester(api) for api in api_for_request))
    return web.Response(text=f"\n\nThe jokes\n\n\n{' '.join(response)}")

app = web.Application()
app.add_routes(routes)
web.run_app(app)
loop = asyncio.get_event_loop()
loop.run_until_complete(requester(api))