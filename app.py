import pandas as pd
import ast
import streamlit as st
from streamlit_tags import st_tags

st.set_page_config(
    page_title="🎓 Global University Explorer",
    page_icon=":school:",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("list_of_univs.csv")

    # st.write("Columns read from list_of_univs.csv:", df.columns.tolist())
    
    if 'State-Province' in df.columns:
        df.rename(columns={'State-Province': 'state-province'}, inplace=True)
    
    if 'state-province' not in df.columns:
        df['state-province'] = None
    
    df['state-province'] = df['state-province'].astype(str).str.strip()
    df['state-province'].replace({'nan': None, 'None': None, '': None}, inplace=True)
    
    for col in ['web_pages', 'domains']:
        if col in df.columns:
            try:
                df[col] = df[col].apply(ast.literal_eval)
            except:
                df[col] = df[col].str.strip("[]").str.replace("'", "").str.split(", ")
    
    return df

df = load_data()


@st.cache_data
def load_rankings():
    rankings_df = pd.read_csv("QS World University Rankings 2025 (Top global universities).csv", encoding='latin1')
    
    rankings_df['Location'] = rankings_df['Location'].str.strip()
    rankings_df['Institution_Name'] = rankings_df['Institution_Name'].str.strip()
    
    rankings_df['RANK_2025'] = pd.to_numeric(rankings_df['RANK_2025'], errors='coerce')
    
    return rankings_df

rankings_df = load_rankings()
combined_df = pd.merge(
    df,
    rankings_df[['Institution_Name', 'Location', 'RANK_2025', 'Overall_Score', 'Academic_Reputation_Score', 'Employer_Reputation_Score']],
    left_on=['name', 'country'],
    right_on=['Institution_Name', 'Location'],
    how='left'
)
combined_df.drop(columns=['Institution_Name', 'Location'], inplace=True)

st.markdown("""
<style>
    .university-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        background-color: white;
        color: #333;
    }
    .university-card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .website-link {
        color: #1e88e5 !important;
        text-decoration: none;
    }
    .country-select {
        margin-bottom: 20px;
    }
    .stMarkdown h2 {
        color: #1e88e5;
    }
    .compare-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1);
        background-color: #f9f9f9;
        min-height: 250px;
    }
    .compare-card h4 {
        color: #007bff;
        margin-top: 0;
    }
    .compare-card p {
        margin-bottom: 5px;
        font-size: 0.9em;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏛️ University Explorer","⚖️ Compare Universities", "📊 Visualizations"])
st.sidebar.title("🔍 Filters")
st.sidebar.markdown("---")



countries = sorted(df['country'].dropna().unique())
selected_country = st.sidebar.selectbox("Select Country", countries, key='country_select')

state_options = ['All'] + sorted(df[df['country'] == selected_country]['state-province'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Filter by State/Province", state_options)

search_query = st.sidebar.text_input("Search by University Name")

if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()


domain_options = sorted(set(domain for sublist in df['domains'].dropna() for domain in sublist))


st.title("🌍 Global University Explorer")
st.markdown("Explore universities worldwide with detailed information about each institution.")

filtered_df = df[df['country'] == selected_country].copy()

if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['state-province'] == selected_state]

if search_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]


col1, col2, col3 = st.columns(3)
col1.metric("Total Universities", len(filtered_df))
col2.metric("Countries Represented", len(df['country'].unique()))
col3.metric("Unique Domains", len(domain_options))

if page == "🏛️ University Explorer":
    top5_df = rankings_df[rankings_df['Location'] == selected_country].nsmallest(5, 'RANK_2025')

    if not top5_df.empty:
        st.subheader(f"🏆 Top 5 Universities in {selected_country} (QS 2025 Rankings)")
        for _, row in top5_df.iterrows():
            st.markdown(f"""
            <div class="university-card">
                <h3>{row['Institution_Name']}</h3>
                <p><strong>QS Rank:</strong> {row['RANK_2025']}</p>
                <p><strong>Location:</strong> {row['Location']}</p>
            </div>
            """, unsafe_allow_html=True)


    if not filtered_df.empty:
        st.subheader(f"🏛️ Universities in {selected_country}" + (f" ({selected_state})" if selected_state != 'All' else ""))
        for _, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="university-card">
                    <h3>{row['name']}</h3>
                    <p><strong>Location:</strong> {row.get('country', 'Not specified')}</p>
                    <p><strong>Domains:</strong> {', '.join(row['domains']) if isinstance(row['domains'], list) else row['domains']}</p>
                    <p><strong>Website:</strong> {' | '.join([f'<a class="website-link" href="{url}" target="_blank">{url}</a>' for url in row['web_pages']]) if isinstance(row['web_pages'], list) else 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No universities found matching your criteria. Try adjusting your filters.")

    st.markdown("---")
    if st.button("💾 Export Filtered Data to CSV"):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="filtered_universities.csv", mime='text/csv')
elif page == "⚖️ Compare Universities":
    st.title("⚖️ Compare Universities")
    st.markdown("Select up to three universities to view their key details side-by-side.")

    university_names = sorted(combined_df[combined_df['RANK_2025'].notna()]['name'].dropna().unique())

    col_select1, col_select2, col_select3 = st.columns(3)

    with col_select1:
        uni1_name = st.selectbox("University 1", [''] + university_names, key='uni_select_1')
    with col_select2:
        uni2_name = st.selectbox("University 2", [''] + university_names, key='uni_select_2')
    with col_select3:
        uni3_name = st.selectbox("University 3", [''] + university_names, key='uni_select_3')

    selected_unis = [uni for uni in [uni1_name, uni2_name, uni3_name] if uni]

    if selected_unis:
        st.subheader("Comparison Results")
        
        comparison_df = combined_df[combined_df['name'].isin(selected_unis)].set_index('name')
        
        display_columns = [
            'country', 'state-province', 'web_pages', 'domains',
            'RANK_2025', 'Overall_Score', 'Academic_Reputation_Score', 'Employer_Reputation_Score'
        ]
        
        comparison_display_df = comparison_df[display_columns].T.fillna('N/A')

        comparison_display_df.index.name = "Attribute"

        def format_list_display(item):
            if isinstance(item, list):
                return ' | '.join([f"<a class='website-link' href='{url}' target='_blank'>{url.split('//')[-1].split('/')[0]}</a>" for url in item])
            return item

        for col in ['web_pages', 'domains']:
            if col in comparison_display_df.index:
                comparison_display_df.loc[col] = comparison_display_df.loc[col].apply(format_list_display)

        cols_for_display = st.columns(len(selected_unis))

        for i, uni_name in enumerate(selected_unis):
            with cols_for_display[i]:
                card_content = f"<div class='compare-card'>"
                card_content += f"<h4>{uni_name}</h4>"
                
                if uni_name in comparison_display_df.columns:
                    for attr, value in comparison_display_df[uni_name].items():
                        if attr == 'country':
                            card_content += f"<p><strong>Country:</strong> {value.title()}</p>"
                        elif attr == 'state-province' and value != 'N/A':
                             card_content += f"<p><strong>State/Province:</strong> {value}</p>"
                        elif attr == 'web_pages':
                            card_content += f"<p><strong>Website:</strong> {value}</p>"
                        elif attr == 'domains':
                            card_content += f"<p><strong>Domains:</strong> {value}</p>"
                        elif attr == 'RANK_2025':
                            card_content += f"<p><strong>QS Rank (2025):</strong> {value}</p>"
                        elif attr == 'Overall_Score':
                            card_content += f"<p><strong>Overall Score:</strong> {value}</p>"
                        elif attr == 'Academic_Reputation_Score':
                            card_content += f"<p><strong>Academic Rep. Score:</strong> {value}</p>"
                        elif attr == 'Employer_Reputation_Score':
                            card_content += f"<p><strong>Employer Rep. Score:</strong> {value}</p>"
                else:
                    card_content += "<p>Data not found for this university.</p>"
                
                card_content += f"</div>"
                st.markdown(card_content, unsafe_allow_html=True)
    else:
        st.info("Select universities from the dropdowns above to compare them.")
elif page == "📊 Visualizations":
    st.title("📊 University Statistics Dashboard")
    st.markdown("Explore patterns, trends, and distributions based on the current filters.")

    st.subheader("🌍 Top 10 Countries by Number of Universities")
    st.bar_chart(df['country'].value_counts().head(10))

    st.subheader("🕸️ Most Common Domains")
    domain_series = pd.Series([domain for sublist in df['domains'].dropna() for domain in sublist])
    top_domains = domain_series.value_counts().head(10)
    st.bar_chart(top_domains)

    st.subheader("📌 Filtered University Count")
    st.write(f"🔎 Showing **{len(filtered_df)}** universities based on applied filters.")
    st.markdown("---")