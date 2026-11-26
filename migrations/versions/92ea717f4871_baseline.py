"""baseline

Revision ID: 92ea717f4871
Revises: None
Create Date: 2026-11-26 06:59:13.988235
"""

from collections.abc import Sequence

import sqlalchemy as sa  # noqa: F401 (used by most migrations, not by empty ones)
from alembic import op  # noqa: F401

# Revision chain: each migration points to the one before it (like a git parent).
revision: str = "92ea717f4871"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass  # baseline: empty on purpose; step 4 adds the first tables


def downgrade() -> None:
    pass
