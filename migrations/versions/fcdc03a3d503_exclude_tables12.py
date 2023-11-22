"""exclude tables12

Revision ID: fcdc03a3d503
Revises: d5d1ba960db7
Create Date: 2023-11-23 01:08:21.433352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcdc03a3d503'
down_revision: Union[str, None] = 'd5d1ba960db7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aaa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('my_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('my_model')
    op.drop_table('aaa')
    # ### end Alembic commands ###
