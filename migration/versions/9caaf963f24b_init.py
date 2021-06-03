"""'init'

Revision ID: dd2c1a098202
Revises: 
Create Date: 2021-06-03 13:40:58.991242

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import mysql

from magicmirror.tools.db.choices import CheckStatus, ActionStatus

# revision identifiers, used by Alembic.
revision = 'dd2c1a098202'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mm_permission',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('permission', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('permission')
    )
    op.create_table('mm_record',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('question', sa.String(length=512), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('source', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mm_record_question'), 'mm_record', ['question'], unique=False)
    op.create_table('mm_role',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('role')
    )
    op.create_table('mm_tag',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('tag', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('tag')
    )
    op.create_table('mm_role_permission',
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('permission', sa.String(length=128), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['permission'], ['mm_permission.permission'], ),
    sa.ForeignKeyConstraint(['role'], ['mm_role.role'], ),
    sa.PrimaryKeyConstraint('role', 'permission')
    )
    op.create_table('mm_user',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_activate', sa.Boolean(), nullable=True),
    sa.Column('login_num', sa.Integer(), nullable=True),
    sa.Column('login_fail_num', sa.Integer(), nullable=True),
    sa.Column('last_login_attempt', sa.DateTime(), nullable=True),
    sa.Column('last_login_date', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['mm_role.role'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_index(op.f('ix_mm_user_email'), 'mm_user', ['email'], unique=True)
    op.create_index(op.f('ix_mm_user_phone'), 'mm_user', ['phone'], unique=True)
    op.create_table('mm_question',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('uid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('question', sa.String(length=512), nullable=False),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(CheckStatus, impl=sa.Integer()), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('modify_by', sa.String(length=64), nullable=True),
    sa.Column('action', sqlalchemy_utils.types.choice.ChoiceType(ActionStatus, impl=sa.Integer()), nullable=True),
    sa.ForeignKeyConstraint(['create_by'], ['mm_user.name'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['modify_by'], ['mm_user.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mm_question_question'), 'mm_question', ['question'], unique=True)
    op.create_index(op.f('ix_mm_question_uid'), 'mm_question', ['uid'], unique=True)
    op.create_table('mm_answer',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('delete_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(CheckStatus, impl=sa.Integer()), nullable=True),
    sa.Column('action', sqlalchemy_utils.types.choice.ChoiceType(ActionStatus, impl=sa.Integer()), nullable=True),
    sa.Column('create_by', sa.String(length=64), nullable=True),
    sa.Column('modify_by', sa.String(length=64), nullable=True),
    sa.Column('question_id', sa.BIGINT(), nullable=True),
    sa.ForeignKeyConstraint(['create_by'], ['mm_user.name'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['modify_by'], ['mm_user.name'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['mm_question.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mm_answer_uid'), 'mm_answer', ['uid'], unique=True)
    op.create_table('mm_question_question',
    sa.Column('similarity_with', sa.BIGINT(), nullable=False),
    sa.Column('similarity_to', sa.BIGINT(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['similarity_to'], ['mm_question.id'], ),
    sa.ForeignKeyConstraint(['similarity_with'], ['mm_question.id'], ),
    sa.PrimaryKeyConstraint('similarity_with', 'similarity_to')
    )
    op.create_table('mm_question_tag',
    sa.Column('question_id', sa.BIGINT(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['mm_question.id'], ),
    sa.ForeignKeyConstraint(['tag'], ['mm_tag.tag'], ),
    sa.PrimaryKeyConstraint('question_id', 'tag')
    )


def downgrade():
    op.drop_table('mm_question_tag')
    op.drop_table('mm_question_question')
    op.drop_index(op.f('ix_mm_answer_uid'), table_name='mm_answer')
    op.drop_table('mm_answer')
    op.drop_index(op.f('ix_mm_question_uid'), table_name='mm_question')
    op.drop_index(op.f('ix_mm_question_question'), table_name='mm_question')
    op.drop_table('mm_question')
    op.drop_index(op.f('ix_mm_user_phone'), table_name='mm_user')
    op.drop_index(op.f('ix_mm_user_email'), table_name='mm_user')
    op.drop_table('mm_user')
    op.drop_table('mm_role_permission')
    op.drop_table('mm_tag')
    op.drop_table('mm_role')
    op.drop_index(op.f('ix_mm_record_question'), table_name='mm_record')
    op.drop_table('mm_record')
    op.drop_table('mm_permission')
