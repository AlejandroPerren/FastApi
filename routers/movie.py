from fastapi import Path, Query, Request,APIRouter, HTTPException, Depends
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.movies import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

routeMovie = APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        if not auth.credentials:
            raise HTTPException(status_code=403, detail="Token no proporcionado")
        data = validateToken(auth.credentials)
        if data.get('email') != 'string':
            raise HTTPException(status_code=403, detail='Credenciales Incorrectas')


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=3, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=90)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoria de la pelicula', min_length=3, max_length=60)


@routeMovie.get('/movies', tags=['Movies'])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    db.close()
    return JSONResponse(content=jsonable_encoder(data))

@routeMovie.get('/movies/{id}', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    db.close()
    if not data:
        raise HTTPException(status_code=404, detail='Recurso no Encontrado')
    return JSONResponse(content=jsonable_encoder(data))

@routeMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    db.close()
    if not data:
        raise HTTPException(status_code=404, detail='Recurso no Encontrado')
    return JSONResponse(content=jsonable_encoder(data))

@routeMovie.post('/movies', tags=['Movies'])
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)
    db.close()
    return JSONResponse(status_code=201, content={'message': 'Se agregó una nueva película', 'movie': jsonable_encoder(newMovie)})

@routeMovie.put("/movies/{id}", tags=['Movies'])
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        db.close()
        raise HTTPException(status_code=404, detail='Recurso no Encontrado')
    
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    
    db.commit()
    db.refresh(data)
    db.close()
    return JSONResponse(content=jsonable_encoder(data))

@routeMovie.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        db.close()
        raise HTTPException(status_code=404, detail='Recurso no Encontrado')
    
    db.delete(data)
    db.commit()
    db.close()
    return JSONResponse(content={'message': 'Película eliminada'})



