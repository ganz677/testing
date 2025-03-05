from contextlib import asynccontextmanager

from fastapi import FastAPI
from users.views import router as users_router
from api_v1 import router as api_router_v1

from core.settings import settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router_v1, prefix=settings.api_v1_prefix)
app.include_router(users_router)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host='0.0.0.0', port=8000, reload=True)