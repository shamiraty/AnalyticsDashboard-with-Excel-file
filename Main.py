import streamlit as st
import pandas as pd 
import streamlit.components.v1 as stc
import plotly.express as px
import time
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

#page behaviour
st.set_page_config(page_title="Descriptive Analytics ", page_icon="🌎", layout="wide")  

#remove default theme
theme_plotly = None # None or streamlit

 
# CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#load excel file
df=pd.read_excel('data.xlsx', sheet_name='Sheet1')


#2. switcher
st.sidebar.header("Please Filter Here:")
region= st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
location = st.sidebar.multiselect(
    "Select the Location:",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "Select the Construction:",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
     
    
)
df_selection = df.query(
    "Region == @region & Location ==@location & Construction == @construction"
)

#method/function

def HomePage():
  #1. print dataframe
 with st.expander("🧭 My database"):
  #st.dataframe(df_selection,use_container_width=True)
  shwdata = st.multiselect('Filter :', df_selection.columns, default=[])
  st.dataframe(df_selection[shwdata],use_container_width=True)

 #2. compute top Analytics
 
 total_investment = float(df_selection['Investment'].sum())
 investment_mode = float(df_selection['Investment'].mode())
 investment_mean = float(df_selection['Investment'].mean())
 investment_median= float(df_selection['Investment'].median()) 
 rating = float(df_selection['Rating'].sum())

 #3. columns
 total1,total2,total3,total4,total5 = st.columns(5,gap='large')
 with total1:

    st.info('Total Investment', icon="🔍")
    st.metric(label = 'sum TZS', value= f"{total_investment:,.0f}")
    
 with total2:
    st.info('Most frequently', icon="🔍")
    st.metric(label='Mode TZS', value=f"{investment_mode:,.0f}")

 with total3:
    st.info('Investment Average', icon="🔍")
    st.metric(label= 'Mean TZS',value=f"{investment_mean:,.0f}")

 with total4:
    st.info('Investment Marging', icon="🔍")
    st.metric(label='Median TZS',value=f"{investment_median:,.0f}")

 with total5:
    st.info('Ratings', icon="🔍")
    st.metric(label='Rating',value=numerize(rating),help=f"""Total rating: {rating}""")
    
 st.markdown("""---""")

 #graphs
 
def Graphs():
 total_investments = int(df_selection["Investment"].sum())
 average_rating = round(df_selection["Rating"].mean(), 1)
 star_rating = ":star:" * int(round(average_rating, 0))
 average_investment = round(df_selection["Investment"].mean(), 2)

#1. simple bar graph
 investment_by_businessType = (
    df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
 )
 fig_investment = px.bar(
    investment_by_businessType,
    x="Investment",
    y=investment_by_businessType.index,
    orientation="h",
    title="Investment by Business Type",
    color_discrete_sequence=["#0083B8"] * len(investment_by_businessType),
    template="plotly_white",
 )

 fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
 )

#2. simple line graph------------------
 investment_by_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
 fig_state = px.line(
    investment_by_state,
    x=investment_by_state.index,
     orientation="v",
    y="Investment",
    title="Investment by Region ",
    color_discrete_sequence=["#0083B8"] * len(investment_by_state),
    template="plotly_white",
 )
 fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
 )

 left_column, right_column,center = st.columns(3)
 left_column.plotly_chart(fig_state, use_container_width=True)
 right_column.plotly_chart(fig_investment, use_container_width=True)

 #pie chart
 with center:
  fig = px.pie(df_selection, values='Rating', names='State', title='Regions by Ratings')
  fig.update_layout(legend_title="Regions", legend_y=0.9)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#-----PROGRESS BAR-----

def ProgressBar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
  target=3000000000
  current=df_selection['Investment'].sum()
  percent=round((current/target*100))
  my_bar = st.progress(0)

  if percent>100:
    st.subheader("Target 100 complited")
  else:
   st.write("you have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
   for percent_complete in range(percent):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1,text="Target percentage")

#-----SIDE BAR-----
 
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
         #menu_title=None,
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast", #option
        default_index=0, #option
        )
 if selected=="Home":   
    try:
     HomePage()
     Graphs()
    except:
        st.warning("one or more options are mandatory ! ")
     
    
 if selected=="Progress":
   try:
    ProgressBar()
    Graphs()
   except:
    st.warning("one or more options are mandatory ! ")
 
#print side bar
sideBar()

footer="""<style>
 

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
height:5%;
bottom: 0;
width: 100%;
background-color: #243946;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with  ❤ by <a style='display: block; text-align: center;' href="https://www.heflin.dev/" target="_blank">Samir.s.s</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

