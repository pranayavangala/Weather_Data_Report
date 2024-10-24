"""Add temperature and precipitation columns to weather_data

Revision ID: 7ca12237b70d
Revises: 
Create Date: 2024-10-24 13:27:07.602234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ca12237b70d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('station_id', sa.String(length=50), nullable=False),
    sa.Column('avg_max_temp', sa.Float(), nullable=True),
    sa.Column('avg_min_temp', sa.Float(), nullable=True),
    sa.Column('total_precipitation', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('weather_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_temperature', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('min_temperature', sa.Float(), nullable=True))
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('precipitation',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.drop_constraint('unique_date_station', type_='unique')
        batch_op.drop_column('created_at')
        batch_op.drop_column('min_temp')
        batch_op.drop_column('max_temp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weather_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_temp', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('min_temp', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True))
        batch_op.create_unique_constraint('unique_date_station', ['date', 'station_id'])
        batch_op.alter_column('precipitation',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.drop_column('min_temperature')
        batch_op.drop_column('max_temperature')

    op.drop_table('weather_stats')
    # ### end Alembic commands ###