"""Initial migration after reset

Revision ID: 084c439057b5
Revises: 
Create Date: 2024-07-29 10:47:58.179438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '084c439057b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Set default role where it is currently null
    op.execute("UPDATE ManagerAccounts SET Role = 'manager' WHERE Role IS NULL")

    # Alter the column to not allow null values
    with op.batch_alter_table('ManagerAccounts', schema=None) as batch_op:
        batch_op.alter_column('Role', existing_type=sa.String(length=20), nullable=False)

    # Add Name column to GateAccounts, allowing nulls initially
    with op.batch_alter_table('GateAccounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Name', sa.String(length=50), nullable=True))

def downgrade():
    # Downgrade the database by reversing the upgrade
    with op.batch_alter_table('ManagerAccounts', schema=None) as batch_op:
        batch_op.alter_column('Role', existing_type=sa.String(length=20), nullable=True)

    with op.batch_alter_table('GateAccounts', schema=None) as batch_op:
        batch_op.drop_column('Name')

    # ### end Alembic commands ###
