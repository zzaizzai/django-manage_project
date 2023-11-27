"""create tables

Revision ID: ff2bb1d92d0e
Revises: 
Create Date: 2023-11-22 22:46:58.668387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ff2bb1d92d0e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('project_comment')
    # op.drop_table('projects')
    # op.drop_index('accounts_customuser_groups_customuser_id_bc55088e', table_name='accounts_customuser_groups')
    # op.drop_index('accounts_customuser_groups_group_id_86ba5f9e', table_name='accounts_customuser_groups')
    # op.drop_table('accounts_customuser_groups')
    # op.drop_table('project_member')
    # op.drop_index('django_session_expire_date_a5c62663', table_name='django_session')
    # op.drop_index('django_session_session_key_c0390e0f_like', table_name='django_session')
    # op.drop_table('django_session')
    # op.drop_index('auth_permission_content_type_id_2f476e4b', table_name='auth_permission')
    # op.drop_table('auth_permission')
    # op.drop_index('auth_group_name_a6ea08ec_like', table_name='auth_group')
    # op.drop_table('auth_group')
    # op.drop_table('django_content_type')
    # op.drop_table('django_migrations')
    # op.drop_index('accounts_customuser_username_722f3555_like', table_name='accounts_customuser')
    # op.drop_table('accounts_customuser')
    # op.drop_index('auth_group_permissions_group_id_b120cbf9', table_name='auth_group_permissions')
    # op.drop_index('auth_group_permissions_permission_id_84c5c92e', table_name='auth_group_permissions')
    # op.drop_table('auth_group_permissions')
    # op.drop_index('accounts_customuser_user_permissions_customuser_id_0deaefae', table_name='accounts_customuser_user_permissions')
    # op.drop_index('accounts_customuser_user_permissions_permission_id_aea3d0e5', table_name='accounts_customuser_user_permissions')
    # op.drop_table('accounts_customuser_user_permissions')
    # op.drop_table('master_department')
    # op.drop_index('django_admin_log_content_type_id_c4bce8eb', table_name='django_admin_log')
    # op.drop_index('django_admin_log_user_id_c564eba6', table_name='django_admin_log')
    # op.drop_table('django_admin_log')
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('django_admin_log',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('action_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('object_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('object_repr', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('action_flag', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('change_message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('content_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.CheckConstraint('action_flag >= 0', name='django_admin_log_action_flag_check'),
    sa.ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], name='django_admin_log_content_type_id_c4bce8eb_fk_django_co', initially='DEFERRED', deferrable=True),
    sa.ForeignKeyConstraint(['user_id'], ['accounts_customuser.id'], name='django_admin_log_user_id_c564eba6_fk_accounts_customuser_id', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name='django_admin_log_pkey')
    )
    op.create_index('django_admin_log_user_id_c564eba6', 'django_admin_log', ['user_id'], unique=False)
    op.create_index('django_admin_log_content_type_id_c4bce8eb', 'django_admin_log', ['content_type_id'], unique=False)
    op.create_table('master_department',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('datetime_created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('datetime_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='master_department_pkey')
    )
    op.create_table('accounts_customuser_user_permissions',
    sa.Column('id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('customuser_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('permission_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['customuser_id'], ['accounts_customuser.id'], name='accounts_customuser__customuser_id_0deaefae_fk_accounts_', initially='DEFERRED', deferrable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], name='accounts_customuser__permission_id_aea3d0e5_fk_auth_perm', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name='accounts_customuser_user_permissions_pkey'),
    sa.UniqueConstraint('customuser_id', 'permission_id', name='accounts_customuser_user_customuser_id_permission_9632a709_uniq')
    )
    op.create_index('accounts_customuser_user_permissions_permission_id_aea3d0e5', 'accounts_customuser_user_permissions', ['permission_id'], unique=False)
    op.create_index('accounts_customuser_user_permissions_customuser_id_0deaefae', 'accounts_customuser_user_permissions', ['customuser_id'], unique=False)
    op.create_table('auth_group_permissions',
    sa.Column('id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('permission_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['auth_group.id'], name='auth_group_permissions_group_id_b120cbf9_fk_auth_group_id', initially='DEFERRED', deferrable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], name='auth_group_permissio_permission_id_84c5c92e_fk_auth_perm', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name='auth_group_permissions_pkey'),
    sa.UniqueConstraint('group_id', 'permission_id', name='auth_group_permissions_group_id_permission_id_0cd325b0_uniq')
    )
    op.create_index('auth_group_permissions_permission_id_84c5c92e', 'auth_group_permissions', ['permission_id'], unique=False)
    op.create_index('auth_group_permissions_group_id_b120cbf9', 'auth_group_permissions', ['group_id'], unique=False)
    op.create_table('accounts_customuser',
    sa.Column('id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('last_login', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=254), autoincrement=False, nullable=False),
    sa.Column('is_staff', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('date_joined', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('department_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_manager', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='accounts_customuser_pkey'),
    sa.UniqueConstraint('username', name='accounts_customuser_username_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('accounts_customuser_username_722f3555_like', 'accounts_customuser', ['username'], unique=False)
    op.create_table('django_migrations',
    sa.Column('id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('app', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('applied', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='django_migrations_pkey')
    )
    op.create_table('django_content_type',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('app_label', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('model', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='django_content_type_pkey'),
    sa.UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq'),
    postgresql_ignore_search_path=False
    )
    op.create_table('auth_group',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='auth_group_pkey'),
    sa.UniqueConstraint('name', name='auth_group_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('auth_group_name_a6ea08ec_like', 'auth_group', ['name'], unique=False)
    op.create_table('auth_permission',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('content_type_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('codename', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], name='auth_permission_content_type_id_2f476e4b_fk_django_co', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name='auth_permission_pkey'),
    sa.UniqueConstraint('content_type_id', 'codename', name='auth_permission_content_type_id_codename_01ab375a_uniq')
    )
    op.create_index('auth_permission_content_type_id_2f476e4b', 'auth_permission', ['content_type_id'], unique=False)
    op.create_table('django_session',
    sa.Column('session_key', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('session_data', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('expire_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('session_key', name='django_session_pkey')
    )
    op.create_index('django_session_session_key_c0390e0f_like', 'django_session', ['session_key'], unique=False)
    op.create_index('django_session_expire_date_a5c62663', 'django_session', ['expire_date'], unique=False)
    op.create_table('project_member',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_manager', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='project_member_pkey')
    )
    op.create_table('accounts_customuser_groups',
    sa.Column('id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('customuser_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['customuser_id'], ['accounts_customuser.id'], name='accounts_customuser__customuser_id_bc55088e_fk_accounts_', initially='DEFERRED', deferrable=True),
    sa.ForeignKeyConstraint(['group_id'], ['auth_group.id'], name='accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name='accounts_customuser_groups_pkey'),
    sa.UniqueConstraint('customuser_id', 'group_id', name='accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq')
    )
    op.create_index('accounts_customuser_groups_group_id_86ba5f9e', 'accounts_customuser_groups', ['group_id'], unique=False)
    op.create_index('accounts_customuser_groups_customuser_id_bc55088e', 'accounts_customuser_groups', ['customuser_id'], unique=False)
    op.create_table('projects',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('user_created_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_completed_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('datetime_created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('datetime_completed', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('datetime_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('date_due', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('datetime_cancled', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('is_canceled', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_completed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='projects_pkey')
    )
    op.create_table('project_comment',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('user_created_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('datetime_created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('datetime_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='project_comment_pkey')
    )
    # ### end Alembic commands ###
