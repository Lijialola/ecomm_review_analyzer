import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import math

# import the package
# make sure the folder 'ecomm_review_analyzer' is in the same directory or installed
import ecomm_review_analyzer as era

# Page Configuration
st.set_page_config(
    page_title="Women's E-Commerce Insights",
    page_icon="🛍️",
    layout="wide",  # Layout set to wide
    initial_sidebar_state="expanded"  # Expand sidebar by default for easier upload
)

# Sidebar: File Upload
st.sidebar.header("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload Reviews CSV", type=["csv"])

# Main Title of the website
st.title("👗 Women's E-Commerce Clothing Reviews Analysis")
st.markdown("Workflow: **Loading** ➡️ **Visualization** ➡️ **Text Analysis**")

if uploaded_file is not None:
    # ---DATA LOADER---
    st.header("1. 📊 Data Loading & Cleaning")

    # Read the uploaded file into a DataFrame
    raw_data = pd.read_csv(uploaded_file)

    # Instantiate DataLoader, the DataLoader constructor takes no arguments based on the class definition
    loader = era.DataLoader(df=raw_data)

    with st.expander("Show Original (Raw) Data"):
        st.dataframe(loader.df.head(10))

    with st.spinner("Cleaning and processing dataset..."):
        # chain the cleaning methods
        loader.clean_data()

        # run the specific processing to create 'Age Group' and 'title_with_review'
        loader.process_ecommerce_data()

        # get the cleaned dataframe
        df_clean = loader.df

    st.success("Step 1 Complete: Data cleaned and processed!")

    # --- DATA VISUALIZER---
    st.divider()
    st.header("2. 📈 Data Distribution & Visualization")

    viz = era.DataVisualizer(df_clean)

    # Column Selector
    all_columns = df_clean.columns.tolist()

    # determine default columns (only if they exist in the dataset)
    default_cols = [c for c in ["Age", "Positive Feedback Count"] if c in all_columns]

    selected_cols = st.multiselect(
        "Please select the columns to display (multiple choices):",
        options=all_columns,
        default=default_cols
    )

    if not selected_cols:
        st.info("Please select at least one column above to generate charts.")
    else:
        # dynamic Layout: 2 charts per row
        cols_per_row = 2
        # Use math.ceil to calculate required rows
        n_rows = math.ceil(len(selected_cols) / cols_per_row)

        for i in range(n_rows):
            st_cols = st.columns(cols_per_row)

            for j in range(cols_per_row):
                index = i * cols_per_row + j

                if index < len(selected_cols):
                    col_name = selected_cols[index]

                    with st_cols[j]:
                        st.subheader(f"Distribution: {col_name}")

                        # Logic: Use log scale automatically if 'Feedback' is in the column name
                        use_log = True if "Feedback" in col_name else False

                        # Call the plot_histogram method
                        # Note: 'log_scale' is passed via **kwargs to sns.histplot inside the class
                        fig = viz.plot_histogram(column_name=col_name, log_scale=use_log)

                        if fig:
                            # Adapt to Streamlit theme (transparent background)
                            fig.patch.set_alpha(0)
                            # don´t use use_container_width=True, as per the warning in the terminal:
                            # `use_container_width` will be removed after 2025-12-31.
                            # For `use_container_width=True`, use `width='stretch'`.
                            # For `use_container_width=False`, use `width='content'`.
                            st.pyplot(fig, width="stretch")


    # Bar Charts Section
    default_bar_cols = [c for c in ["Class Name", "Department Name", "Division Name"] if c in all_columns]

    selected_bar_cols = st.multiselect(
        "Please select categorical columns for Bar Charts:",
        options=all_columns,
        default=default_bar_cols,
        key="bar_multiselect"  # unique key to avoid conflict
    )

    if not selected_bar_cols:
        st.info("Please select at least one column above.")
    else:
        cols_per_row = 2
        n_rows = math.ceil(len(selected_bar_cols) / cols_per_row)
        for i in range(n_rows):
            st_cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                index = i * cols_per_row + j
                if index < len(selected_bar_cols):
                    col_name = selected_bar_cols[index]
                    with st_cols[j]:
                        st.subheader(f"Count: {col_name}")
                        fig = viz.plot_bar_chart(column_name=col_name)
                        if fig:
                            fig.patch.set_alpha(0)
                            st.pyplot(fig, width="stretch")

    # Pie Charts
    st.subheader("Review Proportions (Pie Chart)")

    if "Recommended IND" in df_clean.columns:
            fig_pie_1 = viz.plot_general_pie_chart(column_name="Recommended IND", size=(3, 3))
            if fig_pie_1:
                st.pyplot(fig_pie_1, width="content")

    # Heatmaps
    st.header("Categorical Pivot Heatmaps")

    # use tabs and columns to organize heatmaps nicely
    tab1, tab2 = st.tabs(["Division Analysis", "Class Analysis"])

    with tab1:
        if "Division Name" in df_clean.columns and "Department Name" in df_clean.columns:
            st.caption("Division Name vs Department Name")
            fig_heatmap = viz.plot_heatmap_comparison(row_col="Division Name", col_col="Department Name")
            if fig_heatmap:
                st.pyplot(fig_heatmap, width="stretch")

    with tab2:
        if "Class Name" in df_clean.columns and "Department Name" in df_clean.columns:
            st.caption("Class Name vs Department Name")
            fig_heatmap_2 = viz.plot_heatmap_comparison(row_col="Class Name", col_col="Department Name")
            if fig_heatmap_2:
                st.pyplot(fig_heatmap_2, width="stretch")

    st.info("Step 2 Complete: Statistical charts generated.")

    # ---TEXT ANALYZER ---
    st.divider()
    st.header("3. 🧠 Text & Sentiment Analysis")

    # Instantiate TextAnalyzer
    text_viz = era.TextAnalyzer(df_clean)

    with st.spinner("Running VADER Sentiment Analysis (this might take a moment)..."):
        # This method updates the internal dataframe of the analyzer instance
        text_viz.analyze_sentiment_vader()
        df_final = text_viz.df  # Retrieve the updated df with sentiment scores

    # Display KPIs
    m1, m2, m3 = st.columns(3)
    sentiment_col = 'Polarity Score'

    m1.metric("Total Reviews Analyzed", len(df_final))

    if sentiment_col in df_final.columns:
        m2.metric("Avg Sentiment Score", round(df_final[sentiment_col].mean(), 2))

    if 'Rating' in df_final.columns:
        m3.metric("Avg Rating", f"{round(df_final['Rating'].mean(), 1)} / 5")

    # NLP Charts - Displayed one after another for clarity
    st.subheader("Sentiment vs. Recommendation")
    fig_sent_rec = text_viz.plot_sentiment_vs_recommendations(x="Sentiment", hue="Recommended IND", order=["Negative","Neutral","Positive"])
    if fig_sent_rec:
        st.pyplot(fig_sent_rec, width="stretch")

    fig_sent_rating = text_viz.plot_sentiment_vs_recommendations(x="Rating", hue="Recommended IND")
    if fig_sent_rating:
        st.pyplot(fig_sent_rating, width="stretch")


    my_stopwords = text_viz.get_stopwords(extra_words=["dress", "petite", "made", "will"])

    st.subheader("Wordcloud of Reviews")
    col1, col2 = st.columns(2)
    with col1:
        fig_pos = text_viz.plot_wordcloud(sentiment="Positive", stopwords=my_stopwords)
        if fig_pos:
            st.pyplot(fig_pos, width="stretch")
    with col2:
        fig_neg = text_viz.plot_wordcloud(sentiment="Negative", stopwords=my_stopwords)
        if fig_neg:
            st.pyplot(fig_neg, width="stretch")

    st.subheader("Top N-Grams (Frequent Phrases)")

    fig_ng_2 = text_viz.plot_top_ngrams(ngram=2, sentiment="Negative")
    if fig_ng_2:
            st.pyplot(fig_ng_2, width="stretch")

    fig_ng_3 = text_viz.plot_top_ngrams(ngram=3, sentiment="Negative")
    if fig_ng_3:
            st.pyplot(fig_ng_3, width="stretch")

    st.success("Step 3 Complete: Deep text insights generated!")

    # --- Data Explorer ---
    st.divider()
    st.header("4. Review Explorer")

    if 'Department Name' in df_final.columns:
        dept_options = df_final['Department Name'].dropna().unique()
        selected_dept = st.selectbox("Filter by Department:", dept_options)

        # Columns to display in the explorer
        display_cols = ['Review Text', 'Rating', sentiment_col, 'Sentiment']
        display_cols = [c for c in display_cols if c in df_final.columns]

        # Filter and display data
        filtered_data = df_final[df_final['Department Name'] == selected_dept][display_cols].head(20)
        st.dataframe(filtered_data, width="stretch")

else:
    # Initial State when no file is uploaded
    st.info("Please upload a CSV file to begin the analysis.")
    st.image("https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1000&q=80")

st.sidebar.markdown("---")
st.sidebar.info("Sequence: DataLoader ➔ DataVisualizer ➔ TextAnalyzer")