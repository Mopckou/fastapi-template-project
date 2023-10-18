"""create tables

Revision ID: ca312e3f7f2a
Revises: 
Create Date: 2023-07-01 16:17:43.822438

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'ca312e3f7f2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(50), unique=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('middle_name', sa.String(50), nullable=True),
        sa.Column('last_name', sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('user')
