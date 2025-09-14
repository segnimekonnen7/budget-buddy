"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create habits table
    op.create_table('habits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('schedule_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('goal_type', sa.String(), nullable=False),
        sa.Column('target_value', sa.Numeric(), nullable=True),
        sa.Column('grace_per_week', sa.Integer(), nullable=False),
        sa.Column('timezone', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("goal_type IN ('check', 'count', 'duration')", name='check_goal_type')
    )
    op.create_index(op.f('ix_habits_user_id'), 'habits', ['user_id'], unique=False)
    
    # Create events table
    op.create_table('events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('habit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('ts', sa.DateTime(timezone=True), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_events_habit_ts', 'events', ['habit_id', 'ts'], unique=False)
    op.create_index('ix_events_payload', 'events', ['payload'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_events_habit_id'), 'events', ['habit_id'], unique=False)
    op.create_index(op.f('ix_events_ts'), 'events', ['ts'], unique=False)
    op.create_index(op.f('ix_events_user_id'), 'events', ['user_id'], unique=False)
    
    # Create streaks table
    op.create_table('streaks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('habit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('length_days', sa.Integer(), nullable=False),
        sa.Column('grace_used', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('habit_id')
    )
    
    # Create reminders table
    op.create_table('reminders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('habit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('window', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('quiet_hours', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('best_hour', sa.Integer(), nullable=True),
        sa.Column('timezone', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('habit_id'),
        sa.CheckConstraint("channel IN ('email')", name='check_channel')
    )
    
    # Create experiments table
    op.create_table('experiments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('variant', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create digest_runs table
    op.create_table('digest_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ran_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('count_sent', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('digest_runs')
    op.drop_table('experiments')
    op.drop_table('reminders')
    op.drop_table('streaks')
    op.drop_table('events')
    op.drop_table('habits')
    op.drop_table('users')
