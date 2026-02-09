"""change_datetime_to_timezone_aware

Revision ID: 167b6b694e40
Revises: cd6c6b91a997
Create Date: 2026-02-09 21:23:07.645081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '167b6b694e40'
down_revision: Union[str, Sequence[str], None] = 'cd6c6b91a997'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
            ALTER TABLE tasks 
            ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE 
            USING created_at AT TIME ZONE 'UTC'
        """)

    op.execute("""
            ALTER TABLE tasks 
            ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE 
            USING updated_at AT TIME ZONE 'UTC'
        """)

    op.execute("""
            ALTER TABLE tasks 
            ALTER COLUMN completed_at TYPE TIMESTAMP WITH TIME ZONE 
            USING completed_at AT TIME ZONE 'UTC'
        """)

    op.execute("""
            ALTER TABLE tasks 
            ALTER COLUMN due_date TYPE TIMESTAMP WITH TIME ZONE 
            USING due_date AT TIME ZONE 'UTC'
        """)

    op.execute("""
            ALTER TABLE users 
            ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE 
            USING created_at AT TIME ZONE 'UTC'
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE tasks ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE tasks ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE tasks ALTER COLUMN completed_at TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE tasks ALTER COLUMN due_date TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE users ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE")
