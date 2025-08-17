"""Add candidate photo and details

Revision ID: 0003_candidate_details
Revises: 0002_auth_and_remove_ip
Create Date: 2025-08-16 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0003_candidate_details'
down_revision = '0002_auth_and_remove_ip'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Modify candidates table
    op.alter_column('candidates', 'position',
                    existing_type=sa.String(),
                    nullable=False)
    
    op.alter_column('candidates', 'bio',
                    existing_type=sa.String(),
                    type_=sa.Text(),
                    existing_nullable=True)
    
    op.add_column('candidates',
                  sa.Column('manifesto', sa.Text(), nullable=True))
    
    op.add_column('candidates',
                  sa.Column('achievements',
                           postgresql.JSONB(),
                           server_default='[]',
                           nullable=False))
    
    op.add_column('candidates',
                  sa.Column('photo_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('candidates', 'photo_url')
    op.drop_column('candidates', 'achievements')
    op.drop_column('candidates', 'manifesto')
    
    op.alter_column('candidates', 'bio',
                    existing_type=sa.Text(),
                    type_=sa.String(),
                    existing_nullable=True)
    
    op.alter_column('candidates', 'position',
                    existing_type=sa.String(),
                    nullable=True)
