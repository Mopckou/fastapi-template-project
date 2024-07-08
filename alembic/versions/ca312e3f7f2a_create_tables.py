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
        sa.Column('id', sa.Uuid, primary_key=True),
        sa.Column('email', sa.String(50), unique=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('middle_name', sa.String(50), nullable=True),
        sa.Column('last_name', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, server_default=func.now())
    )
    op.create_table(
        'passwords',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Uuid, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('hash', sa.String(100), nullable=False),
        sa.Column('salt', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, server_default=func.now())
    )
    op.create_table(
        'spaces',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('parent_id', sa.Integer),
        sa.Column('name', sa.String(256), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, server_default=func.now())
    )
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, server_default=func.now())
    )
    op.create_table(
        'projects_spaces',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('space_id', sa.Integer, sa.ForeignKey('spaces.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('password')
    op.drop_table('spaces')
    op.drop_table('projects')
    op.drop_table('projects_spaces')
