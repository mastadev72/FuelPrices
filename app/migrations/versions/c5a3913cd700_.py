"""empty message

Revision ID: c5a3913cd700
Revises: 
Create Date: 2022-10-12 16:53:31.093101

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c5a3913cd700'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fuel_prices',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('provider', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('type_alt', sa.String(), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.Column('last_updated', sa.DateTime(), nullable=False),
                    sa.Column('change_rate', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fuel_prices')
    # ### end Alembic commands ###
