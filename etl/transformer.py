import re
from copy import deepcopy


class DataTransformer:
    """Validates, cleans and transforms extracted records."""

    def __init__(
        self,
        required_fields=None,
        email_fields=None,
        positive_number_fields=None,
        text_fields=None
    ):
        self.required_fields = required_fields or []
        self.email_fields = email_fields or []
        self.positive_number_fields = positive_number_fields or []
        self.text_fields = text_fields or []

        self.rejected_records = []

    def validate(self, record):
        """Checks whether a record meets validation rules."""

        reasons = []

        # Check required fields
        for field in self.required_fields:
            value = record.get(field)

            if value is None or str(value).strip() == "":
                reasons.append(f"Missing required field: {field}")

        # Check email format
        for field in self.email_fields:
            email = record.get(field)

            if email:
                pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

                if not re.match(pattern, str(email).strip()):
                    reasons.append(f"Invalid email: {field}")

        # Check positive numbers
        for field in self.positive_number_fields:
            value = record.get(field)

            if value is not None and str(value).strip() != "":
                try:
                    if float(value) <= 0:
                        reasons.append(
                            f"{field} must be greater than zero"
                        )

                except (ValueError, TypeError):
                    reasons.append(f"{field} must be numeric")

        return reasons

    def clean(self, record):
        """Normalises text fields."""

        cleaned_record = deepcopy(record)

        for field in self.text_fields:
            value = cleaned_record.get(field)

            if isinstance(value, str):
                cleaned_record[field] = " ".join(
                    value.strip().split()
                ).title()

        # Normalise email addresses
        for field in self.email_fields:
            value = cleaned_record.get(field)

            if isinstance(value, str):
                cleaned_record[field] = value.strip().lower()

        return cleaned_record

    def transform(self, records):
        """Validates and transforms a collection of records."""

        valid_records = []
        self.rejected_records = []

        for record in records:

            reasons = self.validate(record)

            if reasons:
                self.rejected_records.append({
                    "record": record,
                    "reasons": reasons
                })

            else:
                cleaned_record = self.clean(record)
                valid_records.append(cleaned_record)

        return valid_records, self.rejected_records