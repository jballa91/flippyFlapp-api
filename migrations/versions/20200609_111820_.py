"""empty message

Revision ID: 359492fc3a98
Revises: da2eb1e17a1c
Create Date: 2020-06-09 11:18:20.577634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import json
import os

# revision identifiers, used by Alembic.
revision = '359492fc3a98'
down_revision = 'da2eb1e17a1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('airports', sa.Column('lat', sa.Float(), nullable=False))
    op.add_column('airports', sa.Column('lon', sa.Float(), nullable=False))
    op.drop_column('airports', 'y_coord')
    op.drop_column('airports', 'x_coord')
    # ### end Alembic commands ###
    this_folder = os.path.dirname(__file__)
    the_file = os.path.join(this_folder, '../../test_json/test_json.txt')
    abs_path = os.path.abspath(os.path.realpath(the_file))

    f = open(abs_path, 'r')
    jsonData = f.read()

    parsed = json.loads(jsonData)

    i = 1
    airports_list = []
    for airport in parsed["features"]:
        current_airport = {}
        current_airport["id"] = i
        current_airport["lat"] = airport['geometry']['y']
        current_airport["lon"] = airport['geometry']['x']
        current_airport["name"] = airport['attributes']['Fac_Name']
        current_airport["city"] = airport['attributes']['City']
        current_airport["state"] = airport['attributes']['State_Post_Office_Code']
        current_airport["loc_id"] = airport['attributes']['Loc_Id']
        current_airport["manager_name"] = airport['attributes']['Manager_Name']
        current_airport["manager_phone_number"] = airport['attributes']['Manager_Phone']
        current_airport["fss_phone_number"] = airport['attributes']['Local_Phone_Airport_To_Fss']
        current_airport["sectional_chart"] = airport['attributes']['Sectional_Chart']
        current_airport["elevation"] = airport['attributes']['Elevation']
        current_airport["pattern_altitude"] = airport['attributes']['Pattern_Altitude']
        current_airport["fuel_types"] = airport['attributes']['Fuel_Types']
        atc_tower = airport['attributes']['Atc_Tower']
        current_airport["atc_tower"] = (
            False, True)[atc_tower and atc_tower == 'Y']
        current_airport["ctaf"] = airport['attributes']['Ctaf']
        landing_fee = airport['attributes']['Landing_Fee']
        current_airport["landing_fee"] = (
            False, True)[landing_fee == 'Y']
        airports_list.append(current_airport)
        i += 1
    # airports_list = read_func()
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('airports',))
    airports = sa.Table('airports', meta)
    op.bulk_insert(airports, airports_list)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('airports', sa.Column('x_coord', postgresql.DOUBLE_PRECISION(
        precision=53), autoincrement=False, nullable=False))
    op.add_column('airports', sa.Column('y_coord', postgresql.DOUBLE_PRECISION(
        precision=53), autoincrement=False, nullable=False))
    op.drop_column('airports', 'lon')
    op.drop_column('airports', 'lat')
    # ### end Alembic commands ###
