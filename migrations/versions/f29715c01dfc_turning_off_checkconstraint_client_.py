"""turning off CheckConstraint client cannot equal family head

Revision ID: f29715c01dfc
Revises: 12e4e0e5ac80
Create Date: 2023-11-09 17:20:13.294225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f29715c01dfc'
down_revision = '12e4e0e5ac80'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('check_client_head_entry_constraint', 'client_family', type_='check')


def downgrade():
    op.create_check_constraint(
        'check_client_head_entry_constraint', 
        'client_family', 
        'client != family_head'
    )