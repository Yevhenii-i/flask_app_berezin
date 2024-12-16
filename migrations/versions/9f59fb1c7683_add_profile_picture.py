"""Add profile picture

Revision ID: 9f59fb1c7683
Revises: 826ef062dba2
Create Date: 2024-12-16 15:04:15.169577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f59fb1c7683'
down_revision = '826ef062dba2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=20), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.drop_column('image_file')

    # ### end Alembic commands ###
