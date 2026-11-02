class ETLError(Exception):
    """Base exception for the ETL framework."""
    pass


class ExtractionError(ETLError):
    """Raised when extracting data from a source fails."""
    pass


class ValidationError(ETLError):
    """Raised when data validation encounters an error."""
    pass


class LoadingError(ETLError):
    """Raised when saving extracted data fails."""
    pass