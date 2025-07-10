# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  "Choose the fruits you want in your customized smoothie!"
)




cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose upto five fruits:",
    my_dataframe,
    max_selections=5
)

if ingredient_list:
    #st.text(ingredient_list)
    ingredients_string=''
    for fruit_choosen in ingredient_list:
        ingredients_string+=fruit_choosen+', '
    #st.write(ingredients_string)
    title= st.text_input("Name on Smoothie:")
    st.write("The name on your smoothie will be:" title)
    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order) values (('""" + ingredients_string + """'),('""" + title + """'))"""
    #st.write(my_insert_stmt)
    
    time_to_insert= st.button("Submit Order")
  
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {title}!", icon="✅")





