import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


from core.models import db_helper, User, Profile, Post, Order, Product, OrderProductAssociation


async def create_user(
        session: AsyncSession,
        username: str
) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print('user', user)
    return user

async def get_user_by_username(
        session: AsyncSession,
        username: str
) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print('found user', username, user)
    return user

async def create_user_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(
        session: AsyncSession,
) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)


async def create_post(
        session: AsyncSession,
        user_id: int,
        *posts_titles: str,
) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id) for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    print('posts', posts)
    return posts

async def get_users_with_posts(
        session: AsyncSession,

):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        # joinedload(User.posts)
        selectinload(User.posts)
    ).order_by(User.id)
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users: # type: User
        print('**' * 10)
        print(user)
        for post in user.posts:
            print('-', post)


async def get_posts_with_authors(
        session: AsyncSession,
):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts: # type: Post
        print('post', post)
        print('author', post.user)



async def get_users_with_posts_and_profiles(
        session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        joinedload(User.profile),
        selectinload(User.posts)
    ).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users: # type: User
        print('**' * 10)
        print(user, user.profile and user.profile.first_name)#если профиль есть то имя вывод
        for post in user.posts:
            print('-', post)



async def get_profiles_with_users_and_users_with_posts(
        session: AsyncSession,
):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        # .where(User.username == 'sam')
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print('**' * 10)
        print(profile.first_name, profile.user)
        print(profile.user.posts)

async def create_order(
        session: AsyncSession,
        promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order

async def create_product(
        session: AsyncSession,
        name: str,
        description: str,
        price: int
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price
    )
    session.add(product)
    await session.commit()
    return product

async def create_orders_and_products(
        session: AsyncSession,
):

    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode='promo')

    mouse = await create_product(
        session=session,
        name='Mouse',
        description='Greate gaming mouse',
        price=123)
    keyboard = await create_product(
        session=session,
        name='Keyboard',
        description='Greate gaming keyboard',
        price=144
    )
    display = await create_product(
        session=session,
        name='Display',
        description='Greate office display',
        price=333
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products)
        ),
    )

    order_one.products.append(mouse)
    order_one.products.append(keyboard)

    # order_promo.products.append(display)
    # order_promo.products.append(keyboard)
    order_promo.products = [display, keyboard]

    await session.commit()

async def get_orders_with_products_through_secondary(
        session: AsyncSession,
) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)

async def demo_get_orders_with_products_through_secondary(
        session: AsyncSession,
):
    # await create_orders_and_products()
    orders = await get_orders_with_products_through_secondary(
        session=session,
    )
    for order in orders:
        print(order.id, order.promocode, order.created_at, 'products: ')
        for product in order.products: # type: Product
            print('-', product.id, product.name, product.price)


async def get_orders_with_products_with_association(
        session: AsyncSession,
):
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(OrderProductAssociation.product),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)

async def demo_get_orders_with_products_with_association(
        session: AsyncSession,
) -> list[Order]:
    orders = await get_orders_with_products_with_association(session=session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, 'products: ')
        for order_product_details in order.products_details: # type: OrderProductAssociation
            print(
                '-',
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                'qty: ',
                order_product_details.count
            )

async def create_gift_for_existing_orders(
        session: AsyncSession,
):
    orders = await get_orders_with_products_with_association(session=session)
    gift_product = await create_product(
        session=session,
        name='Gift product',
        description='Gift for you',
        price=0,
    )
    for order in orders:
        order.products_details.append(OrderProductAssociation(
            count=1,
            unit_price=0,
            product=gift_product,

        ))

    await session.commit()


async def main_relations(
        session: AsyncSession,
):
    await create_user(session=session, username="john")
    await create_user(session=session, username="alice")
    await create_user(session=session, username="sam")
    user_sam = await get_user_by_username(session=session, username='sam')
    user_john = await get_user_by_username(session=session, username='john')
    # user_bob = await get_user_by_username(session=session, username='bob')
    await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name='John',
    )
    await create_user_profile(
        session=session,
        user_id=user_sam.id,
        first_name='Sam',
        last_name='White',
    )
    await show_users_with_profiles(
        session=session,
    )
    await create_post(
        session,
        user_john.id,
        'SQLA joins',
        'SQLA 2.0'
    )
    await create_post(
        session,
        user_sam.id,
        'FastAPI intro',
        'FastAPI advanced'
        'FastAPI more'
    )
    await get_users_with_posts(
        session=session,
    )
    await get_profiles_with_users_and_users_with_posts(
        session=session,
    )


async def demo_m2m(
        session: AsyncSession,
):
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_association(session=session)
    # await create_gift_for_existing_orders(session=session)

async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)




if __name__ == '__main__':
    asyncio.run(main())