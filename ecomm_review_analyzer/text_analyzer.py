import re
import html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
from ecomm_review_analyzer.data_visualizer import DataVisualizer
from ecomm_review_analyzer.errors import SentimentColumnNameNotExistError, CorpusEmptyError, CombinedTextEmptyError, \
    ColumnNameNotExistError


class TextAnalyzer(DataVisualizer): # inherit from the Class DataVisualizer
    def __init__(self, df: pd.DataFrame, text_column: str = "title_with_review"):
        super().__init__(df)
        text_column = self._validate_data(text_column)
        self.text_column = text_column
        self.SIA = SentimentIntensityAnalyzer()

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Cleans and normalizes a text string.

        This method performs several cleaning operations:
        1. Handles NaN or non-string inputs.
        2. Removes HTML tags using BeautifulSoup.
        3. Removes URLs.
        4. Removes extra whitespaces.

        Args:
            text (str): The raw text string to clean.

        Returns:
            str: The cleaned text string. Returns an empty string if input is invalid.
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""

        # remove el HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text(separator=' ')

        # remove url
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

        # remove extra space
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def analyze_sentiment_vader(self):
        """
        Performs sentiment analysis using the VADER lexicon.

        This method applies text cleaning, calculates the 'compound' polarity score
        for each review, and categorizes the sentiment into 'Positive', 'Negative',
        or 'Neutral' based on the score thresholds:
        - Positive: score >= 0.05
        - Negative: score <= -0.05
        - Neutral: -0.05 < score < 0.05

        Returns:
            TextAnalyzer: The current instance (self) with the enriched DataFrame
            containing 'Polarity Score' and 'Sentiment' columns.
        """
        self.df[self.text_column] = self.df[self.text_column].apply(self._clean_text)

        self.df["Polarity Score"] = self.df[self.text_column].apply(lambda x: self.SIA.polarity_scores(x)["compound"])

        # classify the categories
        self.df["Sentiment"] = "Neutral"
        self.df.loc[self.df["Polarity Score"] >= 0.05, "Sentiment"] = "Positive"
        self.df.loc[self.df["Polarity Score"] <= -0.05, "Sentiment"] = "Negative"

        print("Sentiment analysis complete.")
        return self

    def _plot_absolute_counts(self, x, hue, order, ax):
        """
        Helper function: Plots the absolute count of observations.

        Draws a countplot on the provided axes and adds numerical labels to the bars.

        Args:
            x (str): The name of the column for the x-axis.
            hue (str): The name of the column for color encoding.
            order (list): The order of categories for the x-axis.
            ax (matplotlib.axes.Axes): The axes object to draw the plot on.
        """
        sns.countplot(
            data=self.df,
            # it´s good practice to introduce the whole dataframe which can generate label automatically and easy to use "hue"
            x=x, # x='column_name', use x when we need a vertical bar chart, use y when we need a horizontal bar chart
            hue=hue,
            order=order,
            palette="mako",
            ax=ax
        )
        ax.set_title(f"Absolute counts: {x} VS {hue}")
        ax.set_ylabel("Count")

        # using the "for" will allow each column of the "hue" will list the number at the top
        for container in ax.containers:
            ax.bar_label(container, fmt='%d')

    def _plot_relative_percentages(self, x, hue, order, ax):
        """
        Helper function: Calculates and plots relative percentages.

        Computes the percentage of the 'hue' variable within each 'x' category
        and draws a barplot with percentage labels.

        Args:
            x (str): The name of the column for the x-axis.
            hue (str): The name of the column for color encoding.
            order (list): The order of categories for the x-axis.
            ax (matplotlib.axes.Axes): The axes object to draw the plot on.
        """
        # Group by sentiment -> count recommended -> normalize to %
        percentage_df = self.df.groupby(x)[hue].value_counts(normalize=True).mul(100).rename("Percentage").reset_index()
        # percentage_df = self.df.crosstab(index=self.df[x], columns=self.df[hue], normalize="index").mul(100).stack().reset_index(name='Percentage')

        sns.barplot(
            data=percentage_df,
            x=x,  # x="Sentiment"
            y="Percentage",  # the column "Percentage" comes from percentage_df
            hue=hue,
            order=order,
            palette="mako",
            ax=ax
        )

        ax.set_title(f"Relative %: {hue} within each {x}")
        ax.set_ylabel("Percentage %")
        ax.set_ylim(0, 100)

        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%')

    def plot_sentiment_vs_recommendations(self, x: str ="Sentiment", hue: str ="Recommended IND", order=None):
        """
        Generates a dual-plot comparing Sentiment vs. Recommendations.

        1. Left (Countplot): Absolute number of reviews.
        2. Right (Barplot): Percentage of recommendations within each sentiment.

        Args:
            x (str, optional): The column representing sentiment. Defaults to "Sentiment".
            hue (str, optional): The column representing recommendation status. Defaults to "Recommended IND".
            order (list, optional): The order of x-axis categories. If None, sorts by frequency.

        Returns:
            matplotlib.figure.Figure: The generated figure object. Returns None if an error occurs.
        """

        try:
            x = self._validate_data(x)
            hue = self._validate_data(hue)

            # if the user introduces a fixed order list, the order will follow the requirement of the user
            # if the user haven´t put any order requirement, the order will become the element within the x column ordered by each frequency
            if order is None:
                order = self.df[x].value_counts().sort_values(ascending=True).index

            fig, ax = plt.subplots(1, 2, figsize=(15, 6))

            self._plot_absolute_counts(x, hue, order, ax[0])
            self._plot_relative_percentages(x, hue, order, ax[1])

            fig.tight_layout()
            plt.close(fig)
            return fig

        except Exception as error:
            print(error)
            return None


    def get_stopwords(self, extra_words=None):
        """
        Generates a comprehensive set of stopwords.

        Combines standard stopwords with domain-specific terms (e.g., clothing class names)
        and any additional words provided by the user.

        Args:
            extra_words (list, optional): A list of additional words to exclude from analysis.

        Returns:
            set: A set containing all unique stopwords.
        """

        # in this dataset, it´s better to add: extra_words=["dress", "petite", "made", "will"]
        # the class type of STOPWORDS is a set, we use set(STOPWORDS) to create a copy
        # or in another way: stopwords = STOPWORDS.copy()
        stopwords = set(STOPWORDS)

        # modify stopwords to exclude class types, such as "dresses"
        if "Class Name" in self.df.columns:
            fieldnames = list(self.df["Class Name"].dropna().unique())
            # my_set.update() when we need to add several elements, don´t forget the []!
            stopwords.update([x.lower() for x in fieldnames])

        # to make the function more flexible, allow user to include extra_words in stopwords
        if extra_words:
            stopwords.update([x.lower() for x in extra_words])

        return stopwords

    def _get_combined_text(self, sentiment=None):
        """
        Helper function: Combines text from the DataFrame into a single string.

        Filters the DataFrame based on the specified sentiment (if provided), drops
        missing values, and joins the text column into one large string.

        Args:
            sentiment (str, optional): The sentiment category to filter by (e.g., "Positive").
                If None, uses the entire dataset. Defaults to None.

        Returns:
            str: A single string containing all combined reviews.

        Raises:
            SentimentColumnNameNotExistError: If filtering by sentiment but the column doesn't exist.
            CombinedTextEmptyError: If the resulting text string is empty.
        """
        if sentiment is not None:
            if 'Sentiment' not in self.df.columns:
                raise SentimentColumnNameNotExistError()

            # if the user put sentiment = "Negative" or "Positive", the wordcloud will focus on sentiment analysis
            combined_text = " ".join(
                self.df[self.df["Sentiment"] == sentiment][self.text_column]
                .dropna() # make sure there is no "nan" shown in the wordcloud
                .astype(str)
                .values
            )
        else:
            # by default the sentiment is None, in this case, the analysis is about the whole column of the text
            # combine the text of the whole column of the text into one text string, seperated by space
            combined_text = " ".join(
                self.df[self.text_column]
                .dropna()
                .astype(str)
                .values
            )

        # if the combined_text include no text, then raise error
        if not combined_text.strip():
            raise CombinedTextEmptyError()

        return combined_text

    def plot_wordcloud(self, sentiment=None, stopwords=None, ax=None):
       """
       Generates and plots a Word Cloud to visualize the most frequent words.

        Args:
            sentiment (str, optional): The sentiment to focus on (e.g., "Negative").
                If None, visualizes the entire dataset. Defaults to None.
            stopwords (set, optional): A set of words to exclude from the cloud.
            size (tuple, optional): The size of the figure (width, height). Defaults to (7, 4).

        Returns:
            matplotlib.figure.Figure: The generated figure object. Returns None if an error occurs.
       """
       try:
            combined_text = self._get_combined_text(sentiment)

            wordcloud = WordCloud(width=1600,
                                  height=800,
                                  background_color="black",
                                  stopwords=stopwords
                                  ).generate(combined_text)

            fig, ax, own_fig = self._setup_canvas(ax, figsize=(7, 4), dpi=80, facecolor='k', edgecolor='k')

            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")

            sentiment_label = sentiment if sentiment else ""
            plt.title(f"{sentiment_label} Review Text", fontsize=40, color="y", pad=15)

            if own_fig:
                fig.tight_layout()

            return self._finalize_canvas(fig, ax, own_fig)

       except Exception as error:
            print(error)
            return None


    def _get_top_ngrams_df(self, ngram=1, top_n=20, sentiment=None):
        """
        Helper function: Calculates the frequency of N-grams (word combinations).

        Uses CountVectorizer to find the most frequent unigrams, bigrams, etc.

        Args:
            ngram (int, optional): The n-gram range (1 for unigrams, 2 for bigrams). Defaults to 1.
            top_n (int, optional): The number of top phrases to return. Defaults to 20.
            sentiment (str, optional): The sentiment filter. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the 'Review Word' and its 'frequency'.

        Raises:
            SentimentColumnNameNotExistError: If sentiment column is missing when filtering.
            CorpusEmptyError: If the text corpus is empty after filtering.
        """
        # when the sentiment_analysis is not None, it means that the df only includes the columns which sentiment is "Negative" or "Positive"
        if sentiment is not None:
            if 'Sentiment' not in self.df.columns:
                raise SentimentColumnNameNotExistError()

            corpus = self.df[self.df['Sentiment'] == sentiment][self.text_column].dropna()
        else:
            # Drop missing values just in case to avoid errors during vectorization
            corpus = self.df[self.text_column].dropna()

        if corpus.empty:
            raise CorpusEmptyError()

        # ngram_range=(ngram, ngram) ensures we only look at specific n-grams
        vec = CountVectorizer(stop_words='english', ngram_range=(ngram, ngram)).fit(corpus)

        # It creates a Sparse Matrix (a huge numerical table) where each row is a review and each column is a word
        # If a review mentions "dress" twice, the intersection of that row and the "dress" column gets a 2.
        bag_of_words = vec.transform(corpus)

        # calculate total frequency for each word/phrase
        # axis=0: This tells Python to sum the columns vertically
        # adds up every mention of a specific word across all reviews to get its total frequency in the entire dataset
        sum_words = bag_of_words.sum(axis=0)

        # create a list of tuples: (word, frequency)
        # Pairing: The vec.vocabulary_ acts as a dictionary that knows which word belongs to which column index.
        # We pair the word name (e.g., "fabric") with its total count.
        words_freq = [(word, sum_words[0, index]) for word, index in vec.vocabulary_.items()]

        # sort the list by frequency in descending order and slice the list to get only the top N gram
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        common_words = words_freq[:top_n]

        return pd.DataFrame(common_words, columns=["Review Word", "frequency"])

    def plot_top_ngrams(self, ngram=1, top_n=20, sentiment=None, ax=None):
        """
        Visualizes the top N frequent N-grams using a bar chart.

        Args:
            ngram (int, optional): The n-gram type (1 for unigrams, 2 for bigrams). Defaults to 1.
            top_n (int, optional): The number of top phrases to display. Defaults to 20.
            sentiment (str, optional): The sentiment filter (e.g., "Negative"). Defaults to None.

        Returns:
            matplotlib.figure.Figure: The generated figure object. Returns None if an error occurs.
        """
        try:
            df_ngram = self._get_top_ngrams_df(ngram, top_n, sentiment)

            fig, ax, own_fig = self._setup_canvas(ax, figsize=(10, 5))

            sns.barplot(data=df_ngram,
                        x="Review Word",
                        y="frequency",
                        palette="mako",
                        ax=ax)

            ngram_type = "Unigrams" if ngram == 1 else ("Bigrams" if ngram == 2 else f"{ngram}-grams")
            ax.set_title(f"Top {top_n} {ngram_type}")
            ax.set_xlabel("Review Word")
            ax.set_ylabel("Frequency")
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            if own_fig:
                # fig.tight_layout() or plt.tight_layout(),
                # which allow us to adjust automatically the space between ax[0] and ax[1] to avoid overlapping
                fig.tight_layout()

            return self._finalize_canvas(fig, ax, own_fig)

        except Exception as error:
            print(error)
            return None



