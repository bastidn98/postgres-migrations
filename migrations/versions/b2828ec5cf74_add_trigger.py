"""add trigger

Revision ID: b2828ec5cf74
Revises: 2c1ff7d3332f
Create Date: 2023-08-09 20:57:23.085284

"""
from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision = 'b2828ec5cf74'
down_revision = '2c1ff7d3332f'
branch_labels = None
depends_on = None

def upgrade():
    with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/client_family/check_client_head_trigger.sql') as f:
        trigger_sql = f.read()

    op.execute(trigger_sql)

    x=1

def downgrade():
    op.execute("DROP TRIGGER trig_check_client_family_head_constraint ON \"client_family\";")
    op.execute("DROP FUNCTION check_client_family_head_constraint();")

if __name__ == "__main__":
    upgrade()