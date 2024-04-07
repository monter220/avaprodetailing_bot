"""test

Revision ID: ab8cba4fd4bf
Revises: 
Create Date: 2024-04-07 21:40:21.973904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab8cba4fd4bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True, comment='Название'),
    sa.Column('description', sa.String(), nullable=True, comment='Описание'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paytype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True, comment='Название'),
    sa.Column('description', sa.String(), nullable=True, comment='Описание'),
    sa.Column('address', sa.String(length=250), nullable=True, comment='Адрес автомойки'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True, comment='Название'),
    sa.Column('description', sa.String(), nullable=True, comment='Описание'),
    sa.Column('cost', sa.Integer(), nullable=True, comment='Минимальная сумма услуги'),
    sa.Column('default_bonus', sa.Integer(), nullable=True, comment='Минимальный бонус по услуге'),
    sa.Column('category_id', sa.Integer(), nullable=True, comment='Категория услуги'),
    sa.Column('point_id', sa.Integer(), nullable=True, comment='Автомойка, на которой оказывается услуга'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['point_id'], ['point.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('surname', sa.String(length=100), nullable=False, comment='Фамилия'),
    sa.Column('name', sa.String(length=100), nullable=False, comment='Имя'),
    sa.Column('patronymic', sa.String(length=100), nullable=True, comment='Отчество'),
    sa.Column('date_birth', sa.Date(), nullable=False, comment='Дата рождения'),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('reg_date', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('is_ban', sa.Boolean(), nullable=True),
    sa.Column('point_id', sa.Integer(), nullable=True),
    sa.Column('bonus', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['point_id'], ['point.id'], ),
    sa.ForeignKeyConstraint(['role'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('brand', sa.String(), nullable=False, comment='Марка'),
    sa.Column('model', sa.String(), nullable=False, comment='Модель'),
    sa.Column('license_plate_number', sa.String(), nullable=False, comment='Гос номер'),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license_plate_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    op.drop_table('user')
    op.drop_table('service')
    op.drop_table('role')
    op.drop_table('point')
    op.drop_table('paytype')
    op.drop_table('category')
    # ### end Alembic commands ###
