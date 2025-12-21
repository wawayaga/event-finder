"""sync models

Revision ID: a59ca783570e
Revises: 45ee2f197449
Create Date: 2025-11-27 20:43:06.580611

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a59ca783570e'
down_revision = '45ee2f197449'
branch_labels = None
depends_on = None

def upgrade():
    # Nothing to drop/create because subcategory is already gone
    pass

def downgrade():
    # Optionally recreate subcategory table if you want a reversible migration
    op.create_table(
        'subcategory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )

