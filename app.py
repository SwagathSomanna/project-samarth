import streamlit as st
# --- Custom Page Setup ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0b3d2e; /* bright blue */
    background-image: linear-gradient(to bottom right, #2196f3, #0b3d2e);
    color: #f1f8f5;
}

/* 🧭 Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d4d38;
    border-right: 1px solid #1a6b4a;
}

/* 📋 Headings and text */
h1, h2, h3, h4, h5, h6 {
    color: #e6ffee;
    font-weight: 600;
}
p, label, span, div {
    color: #e6ffee;
}

/* 🔘 Input boxes, text areas, and buttons */
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div {
    background-color: lightblack;
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid #1c6f4b;
}
button[kind="primary"] {
    background-color: #1f7a52 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: none !important;
}
button[kind="primary"]:hover {
    background-color: #249e65 !important;
}

/* 🧩 Cards or containers */
.stMarkdown, .stTextInput, .stButton, .stSelectbox {
    background-color: rgba(13, 61, 45, 0.6);
    padding: 10px;
    border-radius: 12px;
}

/* Footer or small text */
footer {
    visibility: hidden;
}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)
from qa_engine import answer_question, STATES
import matplotlib.pyplot as plt

st.set_page_config(page_title="Project Samarth", layout="wide")
st.title("🌾 Project Samarth — Agri × Climate Q&A Prototype (Enhanced)")

st.markdown("Ask questions combining agriculture and climate (rainfall + temperature) data. Examples:\n- Compare the average annual rainfall in Karnataka and Maharashtra for the last 3 years\n- List top 3 crops produced in each state for the last 5 years\n- Analyze trend of Rice and correlate with temperature in Karnataka\n")

q = st.text_input("Enter your question", value="Compare the average annual rainfall in Karnataka and Maharashtra for the last 3 years")

if st.button("Get Answer"):
    with st.spinner("Analyzing data..."):
        answer, table, sources = answer_question(q)

    st.subheader("Answer")
    st.write(answer)

    if table is not None:
        st.subheader("Result Table")
        st.dataframe(table)

        # If table contains year and numeric columns, try to plot (series)
        try:
            if 'year' in table.columns:
                fig, ax = plt.subplots()
                for state in table['state'].unique():
                    series = table[table['state']==state].sort_values('year')
                    ax.plot(series['year'], series.iloc[:,2], label=state)
                ax.set_xlabel('Year')
                ax.set_ylabel(table.columns[2])
                ax.legend()
                st.pyplot(fig)
            else:
                # attempt rainfall or production plots if aggregated results
                if 'avg_rainfall_mm' in table.columns:
                    fig, ax = plt.subplots()
                    ax.bar(table['state'], table['avg_rainfall_mm'])
                    ax.set_ylabel('Average annual rainfall (mm)')
                    st.pyplot(fig)
                elif 'production_tonnes' in table.columns:
                    fig, ax = plt.subplots()
                    ax.bar(table['state'] + ' - ' + table['crop'], table['production_tonnes'])
                    ax.set_ylabel('Production (tonnes)')
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
        except Exception as e:
            st.write('Could not generate plot:', e)

    if sources:
        st.subheader("Data Sources / Provenance")
        for s in sources:
            st.markdown(f"- [{s['title']}]({s['url']}) — rows used: `{s.get('rows_used','')}`")


st.sidebar.header('Quick Controls')
st.sidebar.write('Available states (demo):')
for s in STATES:
    st.sidebar.write('-', s)
