"""Add new fields to tasks table

Revision ID: 001
Revises:
Create Date: 2026-02-06 11:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if columns exist before adding them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('tasks')]

    if 'priority' not in columns:
        op.add_column('tasks', sa.Column('priority', sa.String(), server_default='medium', nullable=False))
    if 'tags' not in columns:
        op.add_column('tasks', sa.Column('tags', sa.String(), nullable=True))
    if 'recurrence_rule' not in columns:
        op.add_column('tasks', sa.Column('recurrence_rule', sa.String(), nullable=True))
    if 'recurrence_end_date' not in columns:
        op.add_column('tasks', sa.Column('recurrence_end_date', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove new columns from tasks table
    op.drop_column('tasks', 'recurrence_rule')
    op.drop_column('tasks', 'recurrence_end_date')
    op.drop_column('tasks', 'tags')
    op.drop_column('tasks', 'priority')