from __future__ import annotations

from typing import Final

from fastapi import Depends, FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from httpx import AsyncClient

from .cfg import BASE_DIR
from .manga_arab.exceptions import NoResults
from .manga_arab.getters import get_details, read_chapter, search

DEBUG = True
app:Final = FastAPI(DEBUG=DEBUG,docs_url=None)

app.mount("/static", StaticFiles(directory=BASE_DIR.joinpath('static')), name="static")
templates = Jinja2Templates(directory=BASE_DIR.joinpath("templates"))


@app.on_event('startup')
def startup():
    setattr(app.state,'session',AsyncClient())

@app.on_event('shutdown')
async def shutdown():
   await app.state.session.aclose()


def session_dep(request:Request)->AsyncClient:
    return request.app.state.session


@app.get('/',name='home')
async def home(request: Request):
    return templates.TemplateResponse('search-home.html',{'request':request})

@app.post('/search',name='search')
async def search_view(request:Request,session:AsyncClient = Depends(session_dep),search_term:str = Form(...)):
    try:
        results = await search(session,search_term)
        context = {'request':request,'search_term':search_term,'results':results}
    except NoResults:
        context = {'request':request,'search_term':search_term}
    return templates.TemplateResponse('search-home.html',context)


@app.get('/manga/{manga_slug}/',name='manga_detail')
async def manga_detail(request:Request,manga_slug:str,session:AsyncClient = Depends(session_dep)):
    result= await get_details(session,manga_slug)
    context = {'request':request,'manga':result}
    return templates.TemplateResponse('manga-detail.html',context)

@app.get('/category/{cat_slug}/',name='category-detail')
def category_detail(request:Request,cat_slug:str):
    pass


@app.get('/anime/{anime_slug}/{chapter_id}/',name='read_chapter')
async def read_chapter_view(request:Request,anime_slug:str,chapter_id:int,session:AsyncClient = Depends(session_dep)):
    imgs = await read_chapter(session,anime_slug,chapter_id)
    print(imgs)
    context = {'request':request,'imgs':imgs}
    return templates.TemplateResponse('read-chapter.html',context)
