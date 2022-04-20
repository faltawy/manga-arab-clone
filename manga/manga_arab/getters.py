from .utils import MangaArabApi
from typing import List
from .models import AnimeManga
from .exceptions import (ConnectionError,NoResults)
mangapi = MangaArabApi
from aiohttp import ClientSession
class Getter:
    def __init__(self,session:ClientSession):
        self.session = session
    
    async def search(self,search_term:str) ->List[AnimeManga]:
        querystring = {"name":str(search_term).lower(),"API_key":mangapi.API_key}

        response =await self.session.get(mangapi.get_endpoint('search'),params=querystring)

        if not response.is_success:
            raise ConnectionError
        else:
            resp_data =response.json()
            if len(resp_data['data']) == 0:
                raise NoResults(search_term)
            else:
                results = [AnimeManga(**d) for d in resp_data['data']]        
            return results
    
    async def get_details(self,anime_slug:str)->AnimeManga:
        url = mangapi.get_endpoint('manga-info')%(anime_slug)
        querystring = {"API_key":mangapi.API_key}
        resp= await self.session.get(url,params=querystring)
        _details = resp.json()
        try:
            details = _details.get('data').get('infoManga')[0]
            return AnimeManga(**details)
        except Exception as e:
            print(e)
            raise NoResults(anime_slug)

    async def read_chapter(self,anime_slug:str,chapter:int):
        querystring = {"API_key":mangapi.API_key}
        url = mangapi.get_endpoint('read-chapter')%(anime_slug,str(chapter))
        try:
            response = await self.session.get(url,params=querystring)
            chapter_data =response.json()
            return chapter_data.get('pages_url')
        except:
            NoResults(anime_slug + str(chapter))




# async def search(search_term:str) -> List[AnimeManga]:
#     querystring = {"name":str(search_term).lower(),"API_key":mangapi.API_key}
#     async with ClientSession() as session:
#         response = await session.get(mangapi.get_endpoint('search'),params=querystring)
#         if not response.ok:
#             raise ConnectionError
#         else:
#             resp_data = await response.json()
#             if len(resp_data['data']) == 0:
#                 raise NoResults(search_term)
#             else:
#                 results = [AnimeManga(**d) for d in resp_data['data']]
                
#                 return results


# async def get_details(anime_slug)-> AnimeManga:
#     url = mangapi.get_endpoint('manga-info')%(anime_slug)
#     querystring = {"API_key":mangapi.API_key}
#     response = await get(url,params=querystring)
#     _details = await response.json()
#     try:
#         __details  = await _details.get('data')
#         details = await __details.get('infoManga')[0]
#         return AnimeManga(**details)
#     except:
#         raise NoResults(anime_slug)


# async def read_chapter(anime_slug:str,chapter:int):
#     querystring = {"API_key":mangapi.API_key}
#     url = mangapi.get_endpoint('read-chapter')%(anime_slug,str(chapter))
#     try:
#         response = await get(url,params=querystring)
#     except:
#         NoResults(anime_slug + str(chapter))
#     chapter_data =await response.json()
#     return chapter_data.get('pages_url')
