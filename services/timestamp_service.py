from datetime import datetime


class TimestampService:
    @staticmethod
    def apply_timestamp_to_document(dict):
        try:
            dict["date_created"] = datetime.now()
        except Exception as e:
            print(f"An error occurred while applying timestamp to document: {e}")
