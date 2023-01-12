import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import home, users, auth

app = FastAPI(title='API for Social Media')

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(home.router)
app.include_router(users.router)
app.include_router(auth.router)


if __name__ == '__main__':
    uvicorn.run(app)
