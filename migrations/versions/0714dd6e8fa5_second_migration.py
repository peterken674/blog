"""Second migration.

Revision ID: 0714dd6e8fa5
Revises: d1ecb766dfe6
Create Date: 2021-06-20 16:23:28.970329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0714dd6e8fa5'
down_revision = 'd1ecb766dfe6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fname', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('lname', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('pass_secure', sa.String(length=255), nullable=True))
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'subscribed')
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('subscribed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.drop_column('users', 'pass_secure')
    op.drop_column('users', 'lname')
    op.drop_column('users', 'fname')
    # ### end Alembic commands ###