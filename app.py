import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

#display image
image = Image.open('img/md-duran-1VqHRwxcCCw-unsplash.jpg')
st.image(image, width = 700)
st.title ('Trends in PhD recipients in the US')


#About
expander_bar = st.beta_expander('About')
expander_bar.markdown("""
**Data Source**: National Science Foundation \n 
**Duration**: 1987-2017 \n
**Python Libraries**: streamlit, pandas, PIL, plotly \n
**References**: [Streamlit documentation](https://docs.streamlit.io/en/stable/api.html), Data Professor [YouTube Channel](https://www.youtube.com/watch?v=ZZ4B0QUHuNc)
""")

#fGraph I: Median Salaries

#load data
@st.cache
def load_salaries_data():
    data = pd.read_excel('data/sed17-sr-tab049.xlsx', skiprows = 3)
    data.columns = ['Field', 'Academia', 'Industry', 'Government', 'Nonprofit', 'Other']
    return data

salaries = load_salaries_data()

#set widgets
st.sidebar.title('Setup for Graph I')
empl_category = st.sidebar.selectbox('Employment categories', sorted(['Academia', 'Industry', 'Government', 'Nonprofit', 'Other']))
st.subheader(f'Graph I: Median Salaries for doctorial recipients in {empl_category} (2017)')

fields = salaries['Field'].unique().tolist()
default_list = ['All fields', 'Life sciences', 'Science and engineering', 'Physical sciences and earth sciences','Mathematics and computer sciences','Psychology and social sciences ', 'Engineering', 'Non-science and engineering']
selected_fields = st.sidebar.multiselect('Field of Study', fields, default_list)

#filter data
selected_salaries_df = salaries[salaries['Field'].isin(selected_fields)][['Field', empl_category]].sort_values(by = empl_category, ascending = False)


# plot bar chart
x = selected_salaries_df['Field'].tolist()
fig1 = go.Figure(go.Bar(x = x, y = selected_salaries_df[selected_salaries_df.columns[1]], marker_color='#484848'))
fig1.update_layout(template='ggplot2')
st.plotly_chart(fig1, use_container_width=True)



#Graph II: Number of PhD recipients  by field of study
#load data
@st.cache
def load_status_data():
    data = pd.read_excel('data/sed17-sr-tab017.xlsx')
    data = data.set_index('Year', drop=True)
    return data
status = load_status_data()

#set widgets
st.sidebar.title('Setup for Graph II')
study_category = st.sidebar.selectbox('Field of Study', sorted(['All fields', 'Life sciences', 'Physical sciences and earth sciences',
                                                               'Mathematics and computer sciences', 'Psychology and social sciences','Engineering','Humanities and arts',
                                                               'Other']))
st.subheader(f'Graph II: Number of Doctorate Recipients  for {study_category} (1987-2017)')

#filter data for graph (w/o checkbox)
selected_status_df = status[[study_category]]

#filter data (w/ checkbox)
mapping = {'All fields': ['U.S. citizen or permanent resident',
       'Temporary visa holder'], 'Life sciences': ['U.S. citizen or permanent resident.1', 'Temporary visa holder.1'],
          'Physical sciences and earth sciences':['U.S. citizen or permanent resident.2', 'Temporary visa holder.2'],
           'Mathematics and computer sciences':['U.S. citizen or permanent resident.3', 'Temporary visa holder.3'],
           'Psychology and social sciences': ['U.S. citizen or permanent resident.4', 'Temporary visa holder.4'],
           'Engineering': ['U.S. citizen or permanent resident.5', 'Temporary visa holder.5'],
           'Education':['U.S. citizen or permanent resident.6', 'Temporary visa holder.6'],
           'Humanities and arts':['U.S. citizen or permanent resident.7', 'Temporary visa holder.7'],
           'Other': ['U.S. citizen or permanent resident.8', 'Temporary visa holder.8']
          }
mapping[study_category].insert(0, study_category)
selected_filtered_status_df = status[mapping[study_category]]

#If checkbox is checked, the graph with citizenship status will be displayed.
show_status = st.sidebar.checkbox('Show Citizenship Status')
if show_status:
    fig3 = go.Figure(data=[

        go.Bar(name='U.S. citizen or permanent resident', x=selected_filtered_status_df.index,
               y=selected_filtered_status_df.iloc[:, 1:2].squeeze(), marker_color='#20283E'),
        go.Bar(name='Temporary visa holder', x=selected_filtered_status_df.index, y=selected_filtered_status_df.iloc[:, 2:3].squeeze(),
               marker_color='#DBAE58')

    ])

    fig3.update_layout(barmode='group', template='ggplot2')
    st.plotly_chart(fig3, use_container_width=True)
else:
    fig2 = px.bar(selected_status_df, x=selected_status_df.index, y=study_category, template='ggplot2')
    fig2.update_traces(marker_color='#20283E')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
*Other* category includes agricultural sciences and natural resources; biological and biomedical sciences; and health sciences.  
*Life sciences* category includes other non-science and engineering fields not shown separately.

""")

#Graph III: Countries of origin of temporary visa holders earning PhD at US universities (2017)

#load data
@st.cache
def load_country_data():
    data = pd.read_excel('data/sed17-sr-tab025.xlsx', skiprows = 3)
    data = data.drop([0, 1]).reset_index(drop=True)
    data.columns = ['country', 'rank', 'recipients']
    return data
countries = load_country_data()

#set widgets
st.sidebar.title('Setup for Graph III')
n = st.sidebar.slider('Number of top countries', 1, 35,5)
st.subheader(f'Graph III: Top {n} Countries of Origin of Temporary Visa Holders (2017')

#filter data
selected_country_data = countries[:n]

# plot bar chart
fig4 = go.Figure(go.Bar(
    x = selected_country_data['country'],
    y = selected_country_data['recipients'], marker_color='#484848'
))
fig4.update_layout(template='ggplot2')
st.plotly_chart(fig4, use_container_width=True)
