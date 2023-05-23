import streamlit as st
import pandas as pd
import seaborn as sns
from UI import *

st.set_page_config(page_title="Descriptive Analytics ", page_icon="📈", layout="wide")  
heading()

if 'number_of_rows' not in st.session_state:
    st.session_state['number_of_rows']=3
    st.session_state['type']='Categorical'
    

increment=st.sidebar.button('show more columns ➕')
if increment:
  st.session_state.number_of_rows +=1
decrement=st.sidebar.button('show fewer columns ➖')
if decrement:
 st.session_state.number_of_rows -=1

df=pd.read_excel('data.xlsx', sheet_name='Sheet1')


 

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.markdown("##")

st.sidebar.header("Add New Product")
options_form=st.sidebar.form("Option Form")
location=options_form.selectbox("Location",{"Urban","Rural"})
state=options_form.selectbox("State",{"Dodoma","Kilimanjaro","Dar es Salaam","Kigoma","Iringa","Mwanza"})
region=options_form.selectbox("Region",{"East","Midwest","Northeast","Central"})
investment=options_form.number_input("Investment")
construction=options_form.selectbox("Construction",{"Frame","Metal Clad","Fire Resist","Masonry"})
businesstype=options_form.selectbox("Business Type",{"Manufacturing","Apartment","Office Bldg","Farming","Construction","Recreation","Hospitality","Organization","Retail","Other"})
earthquake=options_form.selectbox("Earthquake",{"Yes","No"})
flood=options_form.selectbox("Flood",{"Yes","No"})
rating=options_form.number_input("Rating")
add_data=options_form.form_submit_button(label="Add new record")

if add_data:
 if investment  !="" or location !="":
     df = pd.concat([df, pd.DataFrame.from_records([{ 
         'Location': location,
         'State':state,
         'Region':region,
         'Investment':int(investment),
         'Construction':construction,
         'BusinessType':businesstype,
         'Earthquake':earthquake,
         'Flood':flood,
         'Rating':float(rating)
         }])])
     try:
        df.to_excel("data.xlsx",index=False)
     except:
        st.warning("Close dataset")
     st.success("New record has been added successfully !")
 else:
    st.sidebar.error("product name required")



#st.dataframe(df_selection,use_container_width=True)
shwdata = st.multiselect('Filter :', df.columns, default=["Location","State","Region","Investment","Construction","BusinessType","Earthquake"])
st.dataframe(df.tail(st.session_state['number_of_rows']),use_container_width=True,)

 
 