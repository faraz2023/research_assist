from research_assist.gsuite.docs.GoogleDocsService import GoogleDocsService
import datetime
from typing import Any, Dict, List


class GoogleDocsGenerator:
    """
    A class to generate and manipulate Google Docs documents.

    Attributes:
        docs_service (GoogleDocsService): The service object for interacting with Google Docs API.
    """

    def __init__(self) -> None:
        """
        Initializes the GoogleDocsGenerator and builds the Google Docs service.
        """
        self.docs_service = GoogleDocsService().build()

    @staticmethod
    def default_document_name(document_title: str) -> str:
        """
        Generates a default document name based on the current date and the provided title.

        Args:
            document_title (str): The title of the document.

        Returns:
            str: A formatted document name including the current date.
        """
        return f"{datetime.date.today().strftime('%m-%d-%Y')}_{document_title}"

    def create_doc_template_header(self, document_title: str, doc_id: str) -> int:
        """
        Creates a header template for the document, including the title and the current date.

        Args:
            document_title (str): The title of the document.
            doc_id (str): The ID of the document to update.

        Returns:
            int: The index after the inserted header.
        """
        # add template header
        title_template = f"""
        {document_title}
        """
        template = f"""
        Written on {datetime.date.today()} at {datetime.datetime.now().strftime("%H:%M:%S")}
        """
        requests: List[Dict[str, Any]] = [
            {
                "insertText": {
                    "location": {
                        "index": 1,
                    },
                    "text": title_template,
                }
            },
            {
                "insertText": {
                    "location": {
                        "index": len(title_template) + 1,
                    },
                    "text": template,
                }
            },
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": len(title_template),
                    },
                    "paragraphStyle": {
                        "namedStyleType": "TITLE",
                        "spaceAbove": {"magnitude": 1.0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 1.0, "unit": "PT"},
                    },
                    "fields": "namedStyleType,spaceAbove,spaceBelow",
                }
            },
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": len(title_template) + 1,
                        "endIndex": len(title_template) + len(template),
                    },
                    "paragraphStyle": {
                        "namedStyleType": "SUBTITLE",
                        "spaceAbove": {"magnitude": 1.0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 1.0, "unit": "PT"},
                    },
                    "fields": "namedStyleType,spaceAbove,spaceBelow",
                }
            },
        ]
        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )
        end_index = len(title_template) + len(template) + 2
        return end_index

    def write_text_to_doc(self, start_index: int, text: str, doc_id: str) -> int:
        """
        Writes text to the document at the specified index.

        Args:
            start_index (int): The index at which to insert the text.
            text (str): The text to insert.
            doc_id (str): The ID of the document to update.

        Returns:
            int: The index after the inserted text.
        """
        end_index = start_index + len(text)

        requests: List[Dict[str, Any]] = [
            {
                "insertText": {
                    "location": {
                        "index": start_index,
                    },
                    "text": text,
                }
            },
        ]

        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )

        return end_index + 1

    def write_image_to_doc(self, start_index: int, image_url: str, doc_id: str) -> int:
        """
        Inserts an image into the document at the specified index.

        Args:
            start_index (int): The index at which to insert the image.
            image_url (str): The URL of the image to insert.
            doc_id (str): The ID of the document to update.

        Returns:
            int: The index after the inserted image.
        """
        end_index = start_index

        requests: List[Dict[str, Any]] = [
            {
                "insertInlineImage": {
                    "location": {
                        "index": start_index,
                    },
                    "uri": image_url,
                }
            }
        ]

        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )

        return end_index + 1
