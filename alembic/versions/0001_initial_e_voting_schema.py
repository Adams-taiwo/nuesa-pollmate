from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial_e_voting_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # Explicitly define enum labels
    user_role = postgresql.ENUM(
        'admin', 'voter', 'candidate',
        name='user_role',
        create_type=False
    )
    user_role.create(bind, checkfirst=True)

    election_status = postgresql.ENUM(
        'scheduled', 'ongoing', 'closed', 'cancelled',
        name='election_status',
        create_type=False
    )
    election_status.create(bind, checkfirst=True)

    # Users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('matric_number', sa.String(), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            'role',
            user_role,
            nullable=False,
            server_default='voter'
        ),
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False),
    )
    op.create_index('ix_users_matric_number', 'users', ['matric_number'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])

    # Elections
    op.create_table(
        'elections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'status',
            election_status,
            nullable=False,
            server_default='scheduled'
        ),
        sa.Column(
            'allow_multiple_choices',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')),
        sa.Column('max_choices_per_voter', sa.Integer(), nullable=True),
        sa.Column(
            'is_published',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')),
        sa.Column(
            'created_by',
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('users.id'),
            nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False),
    )

    # Candidates
    op.create_table(
        'candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('election_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elections.id'), nullable=False),
        sa.Column('position', sa.String(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_candidates_election_id', 'candidates', ['election_id'])
    op.create_unique_constraint('uq_candidates_user_id', 'candidates', ['user_id'])

    # Votes
    op.create_table(
        'votes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('voter_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('election_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elections.id'), nullable=False),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=True),
        sa.Column('ballot_token', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('extra_data', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_votes_election_id', 'votes', ['election_id'])
    op.create_index('ix_votes_candidate_id', 'votes', ['candidate_id'])
    op.create_unique_constraint('uq_votes_election_voter', 'votes', ['election_id', 'voter_id'])

    # Audit logs
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('actor_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target_type', sa.String(), nullable=False),
        sa.Column('target_id', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('extra_data', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('ix_audit_logs_actor_id', 'audit_logs', ['actor_id'])


def downgrade() -> None:
    op.drop_index('ix_audit_logs_actor_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_created_at', table_name='audit_logs')
    op.drop_table('audit_logs')

    op.drop_constraint('uq_votes_election_voter', 'votes', type_='unique')
    op.drop_index('ix_votes_candidate_id', table_name='votes')
    op.drop_index('ix_votes_election_id', table_name='votes')
    op.drop_table('votes')

    op.drop_constraint('uq_candidates_user_id', 'candidates', type_='unique')
    op.drop_index('ix_candidates_election_id', table_name='candidates')
    op.drop_table('candidates')

    op.drop_table('elections')

    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_matric_number', table_name='users')
    op.drop_table('users')

    election_status = postgresql.ENUM(name='election_status')
    election_status.drop(op.get_bind(), checkfirst=True)

    user_role = postgresql.ENUM(name='user_role')
    user_role.drop(op.get_bind(), checkfirst=True)
