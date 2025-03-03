from contextlib import asynccontextmanager

from fastapi import FastAPI
from users.views import router as users_router
from api_v1 import router as api_router_v1

from core.settings import settings

from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router_v1, prefix=settings.api_v1_prefix)
app.include_router(users_router)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)