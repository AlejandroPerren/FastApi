from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title='Crud FastApi',
    description='Una API Sencilla',
    version='0.0.1',
)

movies = []

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola que tal</h2>')

@app.get('/movies', tags=['Movies'])
def get_movie():
    return movies

@app.post('/movies', tags=['Movies'])
def create_movie(
    id: int = Body(), 
    title: str = Body(), 
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    new_movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movies.append(new_movie)

    return new_movie  

@app.put("/movies/{id}", tags=['Movies'])
def update_movie(
    id: int, 
    title: str = Body(), 
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    for item in movies:
        if item["id"] == id:
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return item 
    return {"error": "Movie not found"} 

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return {"message": "Movie deleted successfully"} 
    return {"error": "Movie not found"}  
