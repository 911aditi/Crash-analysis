
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

df = sns.load_dataset ('car_crashes')
st.title("Explore the Insights here👇")

# states filter
states = st.sidebar.multiselect('Select States',
                        options = sorted(df['abbrev'].unique()),        
                        default = sorted(df['abbrev'].unique())
)

# alcohol involvement filter
min_alc,max_alc = st.sidebar.slider('Alcohol',
                                    min_value = float(df['alcohol'].min()),
                                    max_value = float(df['alcohol'].max()),
                                    value = (float(df['alcohol'].min()),float(df['alcohol'].max())))

# speeding_involvement filter
min_speed,max_speed = st.sidebar.slider('Speeding',
                                        min_value = float(df['speeding'].min()),
                                        max_value = float(df['speeding'].max()),
                                        value = (float(df['speeding'].min()),float(df['speeding'].max())))

# total crashes filter
min_total,max_total = st.sidebar.slider('Total Crashes',
                                        min_value = float(df['total'].min()),
                                        max_value = float(df['total'].max()),
                                        value = (float(df['total'].min()),float(df['total'].max())))

# insurance premium filter
min_ins,max_ins = st.sidebar.slider('Insurance Premium',
                                    min_value = float(df['ins_premium'].min()),
                                    max_value = float(df['ins_premium'].max()),
                                    value = (float(df['ins_premium'].min()),float(df['ins_premium'].max())))

filtered_df = df[
    (df['abbrev'].isin(states)) &
    (df['ins_premium'].between(min_ins,max_ins))&
    (df['total'].between(min_total,max_total)) &
    (df['speeding'].between(min_speed, max_speed))&
    (df['alcohol'].between (min_alc, max_alc))
]

st.dataframe(filtered_df)

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>The primary columns in the dataset include: </p>", unsafe_allow_html=True)
st.markdown("""
            **total:** Total number of drivers involved in fatal collisions per billion vehicle-miles of travel.<br>
            **speeding:** Percentage of drivers involved in fatal collisions who were speeding.<br>
            **alcohol:** Percentage of drivers involved in fatal collisions who were alcohol-impaired.<br>
            **not_distracted:** Percentage of drivers involved in fatal collisions who were not distracted.<br>
            **no_previous:** Percentage of drivers involved in fatal collisions who had no previous accidents.<br>
            **ins_premium:** Average annual car insurance premium in the state (in USD).<br>
            **ins_losses:** Average insurance losses per insured vehicle year (in USD).""",unsafe_allow_html=True)

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>Top 10 states by insurance premiums: </p>", unsafe_allow_html=True)
top10 = filtered_df.sort_values('ins_premium',ascending=False).head(10)
fig = px.bar(top10,x='abbrev',y='ins_premium',color = 'ins_premium',
             color_continuous_scale='Viridis',
             labels={'abbrev':'State Abbreviation','ins_premium':'Insurance Premium'}
             )
st.plotly_chart(fig)
st.subheader("CONCLUSION📊")
st.markdown("State with abbreviation NJ has the highest insurance premium rate.")

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>Progressive total crashes by state: </p>", unsafe_allow_html=True)
df_sorted = filtered_df.sort_values('total')
fig = px.line(df_sorted,x='abbrev',y='total',
              markers=True,
              labels={'abbrev':'State'}
             )
st.plotly_chart(fig)
st.subheader("CONCLUSION📊")
st.markdown("State with abbreviation DC has lowest total crashes while state with abbreviation SC has the highest total crashes.")

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>Distribution of total crashes: </p>", unsafe_allow_html=True)
fig = px.histogram(filtered_df,x='total',nbins=30,
                   labels={'total':'Total Crashes'}
                  )
st.plotly_chart(fig)
st.subheader("CONCLUSION📊")
st.markdown("Majority of states have total crashes between 12 to 18.")

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>Insurance premium vs insurance losses: </p>", unsafe_allow_html=True)
fig = px.scatter(filtered_df,x='ins_premium',y='ins_losses',
                 color='abbrev',        
                 labels={'ins_premium':'Insurance Premium','ins_losses':'Insurance Losses','abbrev':'State Abbreviation'}            
)
st.plotly_chart(fig)
st.subheader("CONCLUSION📊")
st.markdown("There is a positive correlation between insurance premium and insurance losses.")

st.markdown("<p style='color:brown; text-align: left; font-size:22px; font-weight:bold'>Pairplot of car crashes: </p>", unsafe_allow_html=True)
fig = px.scatter_matrix(filtered_df,
                        dimensions=['total', 'speeding', 'alcohol', 'not_distracted'],
                        color='ins_premium',
                        color_continuous_scale='Viridis'
                       )
fig.update_layout(width=1000, height=900)
st.plotly_chart(fig)
st.subheader("CONCLUSION📊")
st.markdown("The pairplot reveals positive correlations among speeding, alcohol impairment, and total crashes.")
             