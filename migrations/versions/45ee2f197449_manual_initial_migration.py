"""Manual initial migration

Revision ID: 45ee2f197449
Revises: 
Create Date: 2025-11-27 18:00:33.086682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ee2f197449'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(20), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('image_file', sa.String(20), nullable=False, server_default='default.jpg'),
        sa.Column('password', sa.String(60), nullable=False)
    )
    op.create_table('category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(20))
    )
    op.create_table('subcategory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(20)),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id'), nullable=False)
    )
    op.create_table('post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('address', sa.String(255)),
        sa.Column('latitude', sa.Float),
        sa.Column('longitude', sa.Float),
        sa.Column('date_posted', sa.DateTime, nullable=False),
        sa.Column('event_date', sa.DateTime),
        sa.Column('duration_minutes', sa.Integer),
        sa.Column('image', sa.String(20), server_default='event_default.jpg'),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id'), nullable=False),
        sa.Column('subcategory_id', sa.Integer, sa.ForeignKey('subcategory.id'))
    )

def downgrade():
    pass
