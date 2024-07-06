"""create account table

Revision ID: 18c39446000d
Revises: 
Create Date: 2024-07-02 10:31:02.265833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18c39446000d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'account',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password', sa.String(128), nullable=False),
        sa.Column('is_admin', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.current_timestamp())
    )


def downgrade() -> None:
    op.drop_table('account')

