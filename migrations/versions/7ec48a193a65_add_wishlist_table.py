"""add wishlist table

Revision ID: 7ec48a193a65
Revises: 7338262c9022
Create Date: 2026-07-13 21:32:12.944143

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7ec48a193a65'
down_revision: Union[str, Sequence[str], None] = '7338262c9022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'wishlist',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('user_id', 'product_id'),
    )


def downgrade() -> None:
    op.drop_table('wishlist')
    # ### end Alembic commands ###
