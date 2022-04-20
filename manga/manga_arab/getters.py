from .utils import MangaArabApi
from typing import List
from .models import AnimeManga
from .exceptions import (ConnectionError,NoResults)
from httpx import AsyncClient

mangapi = MangaArabApi
async def search(session:AsyncClient,search_term:str) ->List[AnimeManga]:
    querystring = {"name":str(search_term).lower(),"API_key":mangapi.API_key}
    response =await session.get(mangapi.get_endpoint('search'),params=querystring)

    if not response.is_success:
        raise ConnectionError
    else:
        resp_data = response.json()
        if len(resp_data['data']) == 0:
            raise NoResults(search_term)
        else:
            results = [AnimeManga(**d) for d in resp_data['data']]        
        return results
    
async def get_details(session:AsyncClient,anime_slug:str)->AnimeManga:
    url = mangapi.get_endpoint('manga-info')%(anime_slug)
    querystring = {"API_key":mangapi.API_key}
    resp= await session.get(url,params=querystring)
    _details = resp.json()
    try:
        details = _details.get('data').get('infoManga')[0]
        return AnimeManga(**details)
    except Exception as e:
        print(e)
        raise NoResults(anime_slug)

async def read_chapter(session:AsyncClient,anime_slug:str,chapter:int):
    querystring = {"API_key":mangapi.API_key}
    url = mangapi.get_endpoint('read-chapter')%(anime_slug,str(chapter))
    try:
        response = await session.get(url,params=querystring)
        chapter_data =response.json()
        return chapter_data.get('pages_url')
    except:
        NoResults(anime_slug + str(chapter))