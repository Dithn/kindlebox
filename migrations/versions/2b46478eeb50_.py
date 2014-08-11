"""empty message

Revision ID: 2b46478eeb50
Revises: d7fc2abf989
Create Date: 2014-08-10 23:38:50.200231

"""

# revision identifiers, used by Alembic.
revision = '2b46478eeb50'
down_revision = 'd7fc2abf989'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'book_hash',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'book_hash',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    ### end Alembic commands ###