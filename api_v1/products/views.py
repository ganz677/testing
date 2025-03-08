from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud
from .schemas import (
    ProductCreate,
    Product,
    ProductUpdate,
    ProductUpdatePartial
)

from .dependencies import product_by_id

from core.models import db_helper


router = APIRouter(tags=["Products"])


@router.get(
    "/",
    response_model=list[Product],
)
async def get_products(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get(
    "/{product_id}/",
    response_model=Product,
)
async def get_product(
        product: Product = Depends(product_by_id),
):
    return product

@router.put(
    '/{product_id}/'
)
async def update_product(
        product_update: ProductUpdate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        product: Product = Depends(product_by_id),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        )


@router.patch(
    '/{product_id}/'
)
async def update_product(
        product_update: ProductUpdatePartial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        product: Product = Depends(product_by_id),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
        )


@router.delete('/{product_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        product: Product = Depends(product_by_id),
) -> None:
    await crud.delete_product(product=product, session=session)

