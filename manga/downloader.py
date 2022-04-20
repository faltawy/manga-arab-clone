from io import BytesIO
from cfg import BASE_DIR
import aiofiles
from httpx import AsyncClient

STORAGE = BASE_DIR.parent.joinpath('download/')

files = ['https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/01.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/02.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/03.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/04.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/05.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/06.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/07.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/08.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/09.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/10.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/11.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/12.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/13.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/14.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/15.jpg', 
'https://onma.me/uploads/manga/jujutsu-kaisen/chapters/128/16.jpg']


client =AsyncClient()
import asyncio

async def get_file(session:AsyncClient,url:str):
    req = await session.get(url)
    url_parts = url.split('/')
    manga_name = url_parts[url_parts.index('chapters') - 1]
    chapter_index = (url_parts[url_parts.index('chapters') + 1])
    page_name = (url_parts[-1])
    return {'req':req,'name':manga_name,'chapter':chapter_index,'page':page_name}



async def write_file(data:dict):
    path = STORAGE.joinpath(data.get('name'),data.get('chapter'))
    if not path.exists:
        path.mkdir()
    async with aiofiles.open(path.joinpath(data.get('page')),'wb') as page:
        await page.write(data.get('req').content)

file = (asyncio.run(get_file(client,files[1])))
asyncio.run(write_file(file))