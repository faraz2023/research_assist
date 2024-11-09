from research_assist.gsuite.base.GSuiteService import GSuiteService
from googleapiclient.discovery import build
from typing import Any


class GoogleDocsService(GSuiteService):
    """
    A service class for interacting with Google Docs API.

    Inherits from GSuiteService and implements the methods to retrieve
    the required scopes and create the Google Docs service.

    Methods:
        get_scopes: Returns the scopes required for Google Docs API.
        get_service: Creates and returns the Google Docs service object.
    """

    def get_scopes(self) -> list[str]:
        """
        Retrieves the scopes required for the Google Docs service.

        Returns:
            list[str]: A list containing the required scopes for Google Docs API.
        """
        SCOPES = ["https://www.googleapis.com/auth/documents"]
        return SCOPES

    def get_service(self, creds: Any) -> Any:
        """
        Creates and returns the Google Docs service object.

        Args:
            creds (Any): The credentials to use for the Google Docs service.

        Returns:
            Any: The Google Docs service object.
        """
        return build("docs", "v1", credentials=creds, cache_discovery=False)
