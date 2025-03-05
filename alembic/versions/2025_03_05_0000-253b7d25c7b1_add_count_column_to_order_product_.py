"""add count column to order product association table

Revision ID: 253b7d25c7b1
Revises: 0e4e9c5306cd
Create Date: 2025-03-05 00:00:44.637891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '253b7d25c7b1'
down_revision: Union[str, None] = '0e4e9c5306cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_product_association', sa.Column('count', sa.Integer(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_product_association', 'count')
    # ### end Alembic commands ###
