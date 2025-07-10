# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  "Choose the fruits you want in your customized smoothie!"
)




cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

title= st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", title)

ingredient_list = st.multiselect(
    "Choose upto five fruits:",
    my_dataframe,
    max_selections=5
)

if ingredient_list:
    # st.text(ingredient_list)
    ingredients_string=''
    for fruit_choosen in ingredient_list:
        ingredients_string+=fruit_choosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        st.subheader(fruit_choosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sd_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
      
    
    my_insert_stmt = """insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + title + """')"""
    st.write(my_insert_stmt)
    time_to_insert= st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {title}!", icon="✅")




# my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#             values ('""" + ingredients_string + """')"""
  
        
    #st.write(my_insert_stmt)
    
    
  
 






