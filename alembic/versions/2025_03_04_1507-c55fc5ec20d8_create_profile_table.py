"""Create profile table

Revision ID: c55fc5ec20d8
Revises: 5cd3498cc761
Create Date: 2025-03-04 15:07:52.531202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c55fc5ec20d8'
down_revision: Union[str, None] = '5cd3498cc761'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###
