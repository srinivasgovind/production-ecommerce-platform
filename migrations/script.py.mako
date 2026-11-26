"""${message}

Revision ID: ${up_revision}
Revises: ${repr(down_revision)}
Create Date: ${create_date}
"""

from collections.abc import Sequence

import sqlalchemy as sa  # noqa: F401 (used by most migrations, not by empty ones)
from alembic import op  # noqa: F401
${imports if imports else ""}
# Revision chain: each migration points to the one before it (like a git parent).
revision: str = ${repr(up_revision)}
down_revision: str | Sequence[str] | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
