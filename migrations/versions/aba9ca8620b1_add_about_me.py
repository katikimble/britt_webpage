"""Add About Me

Revision ID: aba9ca8620b1
Revises: 1bef5b5137f3
Create Date: 2024-06-03 15:48:49.956303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aba9ca8620b1'
down_revision = '1bef5b5137f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('about')
    # ### end Alembic commands ###