import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/%s" % fruit)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('%s')" % new_fruit)
        return 'Thanks for adding: ' + new_fruit


streamlit.title("Streamlit App - Dinner Menu")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
streamlit.dataframe(my_fruit_list.loc[fruits_selected, :])


# New section for FruityVice Advice (API request)
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit")
  else:
    parsed_response = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(parsed_response)
except URLError as e:
  streamlit.error()


# Snowflake connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
streamlit.header("View and add to fruit list your favourites")
if streamlit.button('Get fruit load list'):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like add to the list?')
if streamlit.button('Add fruit to the list'):
    response = insert_row_snowflake(add_my_fruit)
    streamlit.write(response)

my_cnx.close()
