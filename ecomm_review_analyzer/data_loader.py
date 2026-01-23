import pandas as pd
from IPython.core.display_functions import display
from ecomm_review_analyzer.errors import DataFrameEmptyError, DataFrameNoneError

class DataLoader:
    def __init__(self, df=None):
        """
        Initializes the DataLoader.

        Args:
            df (pd.DataFrame, optional): A pandas DataFrame to be processed.
                Defaults to an empty DataFrame if None is provided.
        """
        if df is not None:
            self.df = df
        else:
            self.df = pd.DataFrame()

    def load_data(self, file_path):
        """
        Loads data from a CSV file into a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file to be loaded.

        Returns:
            DataLoader: The current instance of the class (self) to allow method chaining.
            None: If an error occurs during the loading process (e.g., file not found).
        """
        try:
            # alternative method to load the data when to instantiate the class but the df is None
            self.df = pd.read_csv(file_path)
            return self

        except Exception as error:
            print(error)
            return None

    def clean_data(self):
        """
        Performs initial cleaning on the DataFrame structure.

        This method handles common artifacts such as removing the 'Unnamed: 0' index column
        if it exists and sanitizing column names by stripping leading/trailing whitespace.

        Returns:
            DataLoader: The current instance of the class (self) with cleaned metadata.
        """
        if self.df is not None:
            if "Unnamed: 0" in self.df.columns:

                # inplace=True is to drop the column in the original df,
                # and Python will return None to indicate the process has been done
                # if don´t put inplace=True, will create a new modified df, which is much safer
                self.df = self.df.drop(columns=["Unnamed: 0"])

            # df.columns = [name1, name2, etc.] is a way to change the column name of the df
            self.df.columns = [col.strip() for col in self.df.columns]

        return self

    def show_summary(self):
        """
        Displays a comprehensive summary of the DataFrame structure and content.

        This method prints the total dimensions (rows and columns) and renders a summary table
        containing data types, unique value counts, and missing value counts for each column.
        It also displays the first 3 rows of the dataset for a quick preview.

        Returns:
            DataLoader: The current instance of the class (self) to allow method chaining.

        Raises:
            DataFrameNoneError: If the DataFrame has not been loaded (is None).
            DataFrameEmptyError: If the DataFrame contains 0 rows.
            Exception: Propagates any other unexpected exceptions that occur.
        """
        try:
            if self.df is None:
                raise DataFrameNoneError()

            if self.df.empty:
                raise DataFrameEmptyError()

            print(f"Total Rows: {self.df.shape[0]} | Total Columns: {self.df.shape[1]}")

            summary = pd.DataFrame({
                'Data Type': self.df.dtypes,
                'Unique Values': self.df.nunique(),
                'Missing Values': self.df.isnull().sum()
            })

            print("\n--- Column Summary ---")
            display(summary)

            print("\n--- Data Sample (First 3 rows) ---")
            display(self.df.head(3))
            return self

        except Exception as error:
            print(error)
            raise error

    def _process_text_columns(self):
        """Helper: Handles missing values in Title/Review and creates the combined column."""
        if "Title" in self.df.columns and "Review Text" in self.df.columns:
            # filling missing values of the column "Title" as there are too much missing values in this column (instead of dropping the entire column)
            self.df["Title"] = self.df["Title"].fillna("")

            self.df = self.df.dropna(subset=["Review Text"])

            # merging Title with the review_text
            self.df["title_with_review"] = self.df["Title"] + " " + self.df["Review Text"]

    def _create_age_groups(self):
        """Helper: Transforms continuous 'Age' into categorical 'Age Group'."""
        if 'Age' in self.df.columns:
            step = 10

            # if the age is 34, then the process is (34 // 10)* 10 = 30
            start_age = (self.df["Age"] // step) * step
            # the end_age become 30 + (10-1) = 39
            end_age = start_age + (step - 1)

            # create a new column called "Age Group", if the age is 34, then the category will be 30-39
            self.df["Age Group"] = (
                    start_age.astype(int).astype(str) + "-" + end_age.astype(int).astype(str)
            )

    def process_ecommerce_data(self):
        """
        Executes domain-specific preprocessing logic for the E-Commerce dataset.

        This pipeline performs the following transformation steps:
        1. Removes duplicate records.
        2. Handles missing values: fills missing 'Title' with empty strings and drops rows
           missing 'Review Text'.
        3. Feature Engineering: Creates a 'title_with_review' combined column.
        4. Data Transformation: Converts the continuous 'Age' column into a categorical
           'Age Group' column (e.g., '30-39', '40-49') using floor division logic.

        Returns:
            DataLoader: The current instance of the class (self) with the transformed DataFrame.
            None: If an error occurs during processing (e.g., DataFrame is None).
        """
        try:
            if self.df is None:
                raise DataFrameNoneError()

            # show original data length:
            initial_count = len(self.df)

            # remove duplicate of the whole dataframe
            self.df = self.df.drop_duplicates()
            # create new column called "title_with_review" by merging Title with the review_text
            self._process_text_columns()
            # create a new column called "Age Group"
            self._create_age_groups()

            # show the final cleaned dataset and show the number of removed records
            final_count = len(self.df)
            removed_count = initial_count - final_count

            print(f"Data processing complete.")
            print(f"Removed {removed_count} records.")
            print(f"Final data shape: {self.df.shape}")

            return self

        except Exception as error:
            print(error)
            return None
