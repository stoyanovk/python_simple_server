"""create index in names

Revision ID: 27a7412cfb17
Revises: 
Create Date: 2023-02-16 22:18:19.196432

"""
from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "27a7412cfb17"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("idx_name", "names", ["name"])


def downgrade() -> None:
    pass
