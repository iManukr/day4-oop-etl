from abc import ABC, abstractmethod
import csv
import requests

from .errors import ExtractionError


class DataExtractor(ABC):
    """Abstract base class for all data extractors."""

    def __init__(self, source):
        self.source = source

    @abstractmethod
    def extract(self):
        """Every subclass must implement this method."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(source='{self.source}')"


class CSVExtractor(DataExtractor):
    """Extracts records from a CSV file."""

    def extract(self):
        try:
            with open(self.source, mode="r", encoding="utf-8-sig",
                      newline="") as file:

                reader = csv.DictReader(file)
                records = list(reader)

                if not reader.fieldnames:
                    raise ExtractionError("CSV file has no headers.")

                return records

        except ExtractionError:
            raise

        except (OSError, csv.Error) as error:
            raise ExtractionError(
                f"Failed to extract CSV data: {error}"
            ) from error

    def __repr__(self):
        return f"CSVExtractor(file='{self.source}')"


class APIExtractor(DataExtractor):
    """Extracts records from a REST API."""

    def extract(self):
        try:
            response = requests.get(self.source, timeout=15)

            response.raise_for_status()

            records = response.json()

            if not isinstance(records, list):
                raise ExtractionError(
                    "API response must contain a list of records."
                )

            if not all(isinstance(record, dict) for record in records):
                raise ExtractionError(
                    "API response contains invalid record structures."
                )

            return records

        except ExtractionError:
            raise

        except requests.RequestException as error:
            raise ExtractionError(
                f"API extraction failed: {error}"
            ) from error

        except ValueError as error:
            raise ExtractionError(
                f"API returned invalid JSON: {error}"
            ) from error

    def __repr__(self):
        return f"APIExtractor(url='{self.source}')"