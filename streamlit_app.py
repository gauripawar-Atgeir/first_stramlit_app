import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#let's pick a fruit list here so they can pick fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)
#New section to display fruityvice api response
#--streamlit.header('Fruityvice fruit Advice!')
#--fruit_choice = streamlit.text_input('what food would you like information about?','kiwi')
#--streamlit.write('The user entered', fruit_choice)

#import requests
#--fruityvice_response= requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) 
#just write data to screen
# take json version of response and normalize it
#--fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#--streamlit.dataframe(fruityvice_normalized)

#try catch code

#New section to display fruityvice api response
#--streamlit.header('Fruityvice fruit Advice!')
#--try:
#--  fruit_choice = streamlit.text_input('what food would you like information about?')
#--  if not fruit_choice:
#--    streamlit.error("Please select a fruit to get information.")
#--  else:
#--    fruityvice_response= requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#--    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#--    streamlit.dataframe(fruityvice_normalized)
    
#--except URLError as e:
#--  streamlit.error()

#Function code
#Create the repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response= requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#New section to display fruityvice api response
streamlit.header('Fruityvice fruit Advice!')
try:
    fruit_choice = streamlit.text_input('what food would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
  
  
# dont run anything past here while we troubleshott
#--streamlit.stop()
#-- my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#-- my_cur = my_cnx.cursor()
#-- my_cur.execute("SELECT * from fruit_load_list")
#-- my_data_rows = my_cur.fetchall()
#-- streamlit.header("The Fruit Load List Contains:")
#-- streamlit.dataframe(my_data_rows)

streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * FROM fruit_load_list")
         return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)


#-- add_my_fruit = streamlit.text_input('what food would you like information about?','jackfruit')
#-- streamlit.write('Thanks for adding', add_my_fruit)

#allow the end user to add a fruit in list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('from streamlit')")
            return "Thanks for adding" + new_fruit
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to th List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    

 #my_cur.execute("insert into fruit_load_list values ('from streamlit')")
