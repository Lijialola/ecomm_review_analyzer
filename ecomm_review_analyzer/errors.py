class DataFrameNoneError(Exception):
    """Exception raised when the DataFrame is None."""
    def __init__(self, message="Error: The DataFrame is None."):
        self.message = message
        super().__init__(self.message)

class DataFrameEmptyError(Exception):
    """Exception raised when the DataFrame is empty."""
    def __init__(self, message="Error: The DataFrame is empty with 0 rows. Nothing to clean."):
        self.message = message
        super().__init__(self.message)

class ColumnNameNotStringError(Exception):
    """Exception raised when the column name is not a string."""
    def __init__(self, message="Error: The name of the column must be a string."):
        self.message = message
        super().__init__(self.message)

class ColumnNameEmptyError(Exception):
    """Exception raised when the column name is empty or just spaces."""
    def __init__(self, message="Error: The column name cannot be empty or just spaces."):
        self.message = message
        super().__init__(self.message)

class ColumnNameNotExistError(Exception):
    """Exception raised when the column name is not found in the DataFrame."""
    def __init__(self, column_name):
        self.column_name = column_name
        self.message = f"Error: The column '{column_name}' doesn't exist in this DataFrame."
        super().__init__(self.message)

class SentimentColumnNameNotExistError(Exception):
    """Exception raised when the "Sentiment" column name doesn't exist in the DataFrame."""
    def __init__(self, message="Error: 'Sentiment' column not found. Run sentiment analysis first."):
        self.message = message
        super().__init__(self.message)

class CorpusEmptyError(Exception):
    """Exception raised when corpus is empty."""
    def __init__(self, message="Warning: Corpus is empty for the selected filters."):
        self.message = message
        super().__init__(self.message)

class CombinedTextEmptyError(Exception):
    """Exception raised when the combined text is empty."""
    def __init__(self, message="Error: No text available for WordCloud."):
        self.message = message
        super().__init__(self.message)

