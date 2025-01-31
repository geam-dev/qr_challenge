"""Initial migration

Revision ID: fd98dceaed9e
Revises: 
Create Date: 2025-01-07 08:23:17.674542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd98dceaed9e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    schema='qr_challenge'
    )
    op.create_table('qr_codes',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('size', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['qr_challenge.users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    schema='qr_challenge'
    )
    op.create_index(op.f('ix_qr_challenge_qr_codes_user_uuid'), 'qr_codes', ['user_uuid'], unique=False, schema='qr_challenge')
    op.create_table('scans',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('qr_uuid', sa.UUID(), nullable=False),
    sa.Column('ip', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['qr_uuid'], ['qr_challenge.qr_codes.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    schema='qr_challenge'
    )
    op.create_index(op.f('ix_qr_challenge_scans_qr_uuid'), 'scans', ['qr_uuid'], unique=False, schema='qr_challenge')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_qr_challenge_scans_qr_uuid'), table_name='scans', schema='qr_challenge')
    op.drop_table('scans', schema='qr_challenge')
    op.drop_index(op.f('ix_qr_challenge_qr_codes_user_uuid'), table_name='qr_codes', schema='qr_challenge')
    op.drop_table('qr_codes', schema='qr_challenge')
    op.drop_table('users', schema='qr_challenge')
    # ### end Alembic commands ###
