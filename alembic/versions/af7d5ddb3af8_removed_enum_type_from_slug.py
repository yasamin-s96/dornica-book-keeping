"""removed enum type from slug

Revision ID: af7d5ddb3af8
Revises: c62d3af46933
Create Date: 2024-09-21 15:36:42.539345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'af7d5ddb3af8'
down_revision: Union[str, None] = 'c62d3af46933'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permissions', 'slug',
               existing_type=mysql.ENUM('READ', 'CREATE', 'UPDATE', 'DELETE'),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.create_unique_constraint(None, 'permissions', ['slug'])
    op.alter_column('roles', 'slug',
               existing_type=mysql.ENUM('ADMIN', 'MANAGER', 'USER'),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.create_unique_constraint(None, 'roles', ['slug'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles', type_='unique')
    op.alter_column('roles', 'slug',
               existing_type=sa.String(length=20),
               type_=mysql.ENUM('ADMIN', 'MANAGER', 'USER'),
               existing_nullable=False)
    op.drop_constraint(None, 'permissions', type_='unique')
    op.alter_column('permissions', 'slug',
               existing_type=sa.String(length=20),
               type_=mysql.ENUM('READ', 'CREATE', 'UPDATE', 'DELETE'),
               existing_nullable=False)
    # ### end Alembic commands ###
