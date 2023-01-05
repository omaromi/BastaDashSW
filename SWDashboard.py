import streamlit as st
import plotly.express as px
import pandas as pd


# setting streamlit page configurations
st.set_page_config(
    page_title="Basta x Serve Washington Diagnostic Dashboard",
    page_icon="✅",
    layout="wide",
)


@st.experimental_memo(max_entries=2)
def get_data_to_df():
    df = pd.read_csv('joinedservewafordash.csv', index_col=0, dtype=str)

    df['Host Site'] = df['Host Site'].map({
        '1.0': "Chelan-Douglas Community Action Council",
        '4.0': "City Year, Inc. - City Year Seattle",
        '5.0': "CivicWell - CivicSpark WA",
        '6.0': "College Possible - College Possible WA",
        '7.0': "College Success Foundation",
        '8.0': "Common Threads Farm",
        '9.0': "EarthCorps",
        '10.0': "ESD - Washington Service Corps",
        '12.0': "ESD. - Washington Reading Corps",
        '11.0': "ESD. - Public Health AmeriCorps",
        '13.0': "iFoster - TAY AmeriCorps WA",
        '14.0': "NEW ESD 101 - Spokane Service Team",
        '15.0': "Pasco School District 1 - Serve Tri-Cities",
        '16.0': "Port Angeles School District",
        '17.0': "Sea Mar Community Health Center",
        '18.0': "Tacoma Boat Builders - Imagine Justice",
        '19.0': "United Way of Benton and Franklin Counties",
        '20.0': "United Way of King County",
        '24.0': "Vista",
        '21.0': "WA State Dept. of Veteran Affairs - Vet Corps",
        '22.0': "Washington Association of Child Advocate Programs",
        '23.0': "Washington Conservation Corps", })

    df['Age'] = df['Age'].astype(float)

    df['EduLevel'] = df['EduLevel'].map({
        '1.0': "No diploma or GED",
        '2.0': "HS Diploma",
        '3.0': "GED",
        '4.0': "Some College",
        '5.0': "Associate's Degree",
        '6.0': "Technical or vocational certificate",
        '7.0': "Bachelor's Degree",
        '8.0': "Master's Degree or PhD",
    })

    return df.loc[df['Host Site'].astype(str) != "nan"]


big_df = get_data_to_df()

st.sidebar.header("Filter by Host Site here")
hostsite = st.sidebar.multiselect(
    "Select the Host Site:", options=big_df['Host Site'].unique(), default=big_df['Host Site'].unique())


new_df = big_df.query("`Host Site` == @hostsite")

milestone_order = ['Clarity', 'Alignment', 'Search Strategy',
                   'Interviewing & Advancing', 'Clarity Path', 'Path']

milestone_chart = new_df['Milestone Link'].value_counts().reset_index().rename(
    columns={'index': 'Milestone Score', 'Milestone Link': 'Number of Members'})
milestone_chart['Milestone Score'] = pd.Categorical(milestone_chart['Milestone Score'], [
                                                    x for x in milestone_order if x in milestone_chart['Milestone Score'].unique().tolist()], ordered=True)

milestones = milestone_chart.sort_values(by='Milestone Score')
figure_milestones = px.bar(milestones, y='Milestone Score', x='Number of Members', color='Milestone Score',
                           color_discrete_map={
                               'Clarity': "#00A3E1", 'Alignment': "#85C540",
                               'Search Strategy': "#D04D9D", 'Interviewing & Advancing': "#FFC507",
                               'Clarity Path': "#00A3E1", 'Path': "#D04D9D"})


interests = new_df['Interest_primary_proper'].value_counts(
).sort_index().reset_index().rename(columns={'Interest_primary_proper': 'Number of Members', 'index': "Industry of Interest"})
figure_interest = px.bar(interests, y='Industry of Interest',
                         x='Number of Members', color='Industry of Interest')


salary = new_df['A14 Salary Expectation OpenTextLink'].value_counts().reset_index().sort_index().rename(
    columns={'index': 'Salary Expectation', 'A14 Salary Expectation OpenTextLink': 'Number of Members'})
salary_order = ["Honestly, I haven't thought about this",
                "Less than $40,000",
                "Between $40,000 and $59,999",
                "Between $60,000 and $79,999",
                "Between $80,000 and $99,999",
                "$100,000 +"]

salary['Salary Expectation'] = pd.Categorical(salary['Salary Expectation'], [
                                              x for x in salary_order if x in salary['Salary Expectation'].unique().tolist()], ordered=True)

salary_df = salary.sort_values(by='Salary Expectation')
figure_salary = px.bar(salary_df, x='Salary Expectation',
                       y='Number of Members', color='Salary Expectation')

career_goal = new_df['Career_goal_label'].value_counts().reset_index().sort_index().rename(
    columns={'index': 'Next Career Goal', 'Career_goal_label': 'Number of Members'})

figure_careergoal = px.bar(career_goal, x='Next Career Goal',
                           y='Number of Members', color='Next Career Goal')


edulevel = new_df['EduLevel'].value_counts().reset_index().sort_index().rename(
    columns={'index': 'Education Level', 'EduLevel': 'Number of Members'})
edulevel_order = ["No diploma or GED",
                  "HS Diploma",
                  "GED",
                  "Some College",
                  "Associate's Degree",
                  "Technical or vocational certificate",
                  "Bachelor's Degree",
                  "Master's Degree or PhD"]

edulevel['Education Level'] = pd.Categorical(edulevel['Education Level'], [
    x for x in edulevel_order if x in edulevel['Education Level'].unique().tolist()], ordered=True)

edu_df = edulevel.sort_values(by='Education Level')
figure_edulevel = px.bar(edu_df, x='Education Level',
                         y='Number of Members', color='Education Level')


# st.dataframe(new_df)

# modifying the charts
figure_milestones.update_layout(showlegend=False)
figure_careergoal.update_layout(showlegend=False)
figure_salary.update_layout(showlegend=False)
figure_edulevel.update_layout(showlegend=False)
figure_interest.update_layout(showlegend=False)


# displaying everything

st.title('Serve Washington Diagnostic Dashboard')


cola, colb = st.columns([4, 8])

with cola:
    st.subheader("Number of Diagnostic Takers")
    st.metric(label="Number of Diagnostic Takers", value=new_df.shape[0])


with colb:
    st.markdown("### Milestone Distribution")
    st.plotly_chart(figure_milestones, use_container_width=True)

st.markdown("### Industry Interest Distribution")
st.plotly_chart(figure_interest, use_container_width=True)


st.markdown("#### Salary Expectations")
st.plotly_chart(figure_salary, use_container_width=True)

colx, coly = st.columns(2)

with colx:
    st.markdown("#### Education Level")
    st.plotly_chart(figure_edulevel, use_container_width=True)

with coly:
    st.markdown("#### Next Career Goal")
    st.plotly_chart(figure_careergoal, use_container_width=True)
