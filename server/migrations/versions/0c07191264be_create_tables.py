"""create tables

Revision ID: 0c07191264be
Revises: b336f187f918
Create Date: 2023-06-20 17:13:21.734939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c07191264be'
down_revision = 'b336f187f918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('scientist_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_missions_scientist_id_scientists'), 'scientists', ['scientist_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_missions_planet_id_planets'), 'planets', ['planet_id'], ['id'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('distance_from_earth',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('nearest_star',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('field_of_study',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('avatar',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_scientists_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_scientists_name'), type_='unique')
        batch_op.alter_column('avatar',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('field_of_study',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('nearest_star',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('distance_from_earth',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_missions_planet_id_planets'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_missions_scientist_id_scientists'), type_='foreignkey')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('scientist_id')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
