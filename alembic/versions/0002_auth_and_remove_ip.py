"""Auth fields and remove ip_address

Revision ID: 0002_auth_and_remove_ip
Revises: 0001_initial_e_voting_schema
Create Date: 2025-08-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_auth_and_remove_ip'
down_revision = '0001_initial_e_voting_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add password hash and salt fields to users table
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False, server_default=''))
    op.add_column('users', sa.Column('salt', sa.String(), nullable=False, server_default=''))
    
    # Remove ip_address from votes table
    op.drop_column('votes', 'ip_address')


def downgrade() -> None:
    # Add back ip_address to votes
    op.add_column('votes', sa.Column('ip_address', sa.String(), nullable=True))
    
    # Remove auth fields from users
    op.drop_column('users', 'salt')
    op.drop_column('users', 'hashed_password')
