"""Add a column

Revision ID: f1ba2c950fcb
Revises: 27a7412cfb17
Create Date: 2023-02-16 22:34:25.821977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1ba2c950fcb"
down_revision = "27a7412cfb17"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("names", sa.Column("last_visit", sa.DateTime))


def downgrade() -> None:
    op.drop_column("names", "last_visit")
