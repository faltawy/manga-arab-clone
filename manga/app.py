from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
from .manga_arab.getters import Getter
from .manga_arab.exceptions import NoResults

BASE_DIR = pathlib.Path(__file__).parent
DEBUG = True
app = FastAPI(DEBUG=DEBUG)

app.mount("/static", StaticFiles(directory=BASE_DIR.joinpath('static')), name="static")
templates = Jinja2Templates(directory=BASE_DIR.joinpath("templates"))
getter = Getter()

@app.get('/',name='home')
async def home(request: Request):
    return templates.TemplateResponse('search-home.html',{'request':request})

@app.post('/search',name='search')
async def search(request:Request,search_term:str = Form(...)):
    try:
        results = await getter.search(search_term)
        context = {'request':request,'search_term':search_term,'results':results}
    except NoResults:
        context = {'request':request,'search_term':search_term}
    return templates.TemplateResponse('search-home.html',context)




@app.get('/manga/{manga_slug}/',name='manga_detail')
async def manga_detail(request:Request,manga_slug:str):
    result= await getter.get_details(manga_slug)
    print(result)
    context = {'request':request,'manga':result}
    return templates.TemplateResponse('manga-detail.html',context)

@app.get('/category/{cat_slug}/',name='category-detail')
def category_detail(request:Request,cat_slug:str):
    pass


@app.get('/anime/{anime_slug}/{chapter_id}/',name='read_chapter')
async def read_chapter(request:Request,anime_slug:str,chapter_id:int):
    imgs = await getter.read_chapter(anime_slug,chapter_id)
    context = {'request':request,'imgs':imgs}
    return templates.TemplateResponse('read-chapter.html',context)

