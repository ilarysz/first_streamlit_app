import streamlit
import pandas
import requests
import snowflake.connector


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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# Transform JSON response into flat table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Show dataframe 
streamlit.dataframe(fruityvice_normalized)
