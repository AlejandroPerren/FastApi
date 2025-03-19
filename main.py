from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bd.database import engine, Base
from routers.movie import routeMovie
from routers.users import login_user

app = FastAPI(
    title='Crud FastApi',
    description='Una API Sencilla',
    version='0.0.1',
)

app.include_router(routeMovie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola que tal</h2>')
