from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title='Crud FastApi',
    description='Una API Sencilla',
    version='0.0.1',
)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=3, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=90)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoria de la pelicula', min_length=3, max_length=60)
    

movies = []

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola que tal</h2>')

@app.get('/movies', tags=['Movies'])
def get_movie():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item.id == id:
            return JSONResponse(content=item.model_dump())
    return JSONResponse(content={"error": "Movie not found"}, status_code=404)

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    return category

@app.post('/movies', tags=['Movies'])
def create_movie(movie: Movie):
    new_movie = movie
    movies.append(new_movie)
    return JSONResponse(status_code=201 ,content={'message': 'Se agrego una nueva pelicula', 'movies': [m.model_dump() for m in [new_movie]]}) 

@app.put("/movies/{id}", tags=['Movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category,
            return JSONResponse(content={'message': 'Se ha modificado la pelicula'})
    return {"error": "Movie not found"} 

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Movie deleted successfully"}) 
    return {"error": "Movie not found"}  
