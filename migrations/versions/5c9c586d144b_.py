"""empty message

Revision ID: 5c9c586d144b
Revises: 476c85badf96
Create Date: 2016-10-14 00:31:42.442878

"""

# revision identifiers, used by Alembic.
revision = '5c9c586d144b'
down_revision = '476c85badf96'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmark', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    op.add_column('bookmark', sa.Column('updated_at', sa.TIMESTAMP(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookmark', 'updated_at')
    op.drop_column('bookmark', 'created_at')
    ### end Alembic commands ###