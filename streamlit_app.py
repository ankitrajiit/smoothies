# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be ", name_on_order)

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    f"""Choose the fruits which you want in the smoothie.
    """
)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col(SEARCH_ON))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list=st.multiselect('Choose upto 5 ingredients ', my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string+=x + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader( x +'Nutrition values')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+x)
        #st.text(smoothiefroot_response)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""',"""+ """'""" + name_on_order + """')"""
    time_to_insert=st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")










