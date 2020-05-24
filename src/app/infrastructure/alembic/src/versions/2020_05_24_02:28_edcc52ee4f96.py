"""refactoring

Revision ID: edcc52ee4f96
Revises: 4c8364a60782
Create Date: 2020-05-24 02:28:04.555688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edcc52ee4f96'
down_revision = '4c8364a60782'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wallethistory', sa.Column('wallet_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'wallethistory', 'wallet', ['wallet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wallethistory', type_='foreignkey')
    op.drop_column('wallethistory', 'wallet_id')
    # ### end Alembic commands ###