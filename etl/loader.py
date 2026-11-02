import csv
import json
import os

from .errors import LoadingError


class DataLoader:
    """Loads transformed records into CSV or JSON files."""

    def __init__(self, destination):

        self.destination = destination

        extension = os.path.splitext(destination)[1].lower()

        if extension not in [".csv", ".json"]:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                "Use CSV or JSON."
            )

        self.extension = extension

    def load(self, records):
        """Writes records to the destination file."""

        if not records:
            return 0

        try:
            # Create destination directory if it doesn't exist
            directory = os.path.dirname(self.destination)

            if directory:
                os.makedirs(directory, exist_ok=True)

            if self.extension == ".csv":

                fieldnames = list(records[0].keys())

                with open(
                    self.destination,
                    mode="w",
                    encoding="utf-8",
                    newline=""
                ) as file:

                    writer = csv.DictWriter(
                        file,
                        fieldnames=fieldnames,
                        extrasaction="ignore"
                    )

                    writer.writeheader()
                    writer.writerows(records)

            elif self.extension == ".json":

                with open(
                    self.destination,
                    mode="w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        records,
                        file,
                        indent=4,
                        default=str
                    )

            return len(records)

        except (OSError, csv.Error, TypeError, ValueError) as error:
            raise LoadingError(
                f"Failed to load data into {self.destination}: {error}"
            ) from error