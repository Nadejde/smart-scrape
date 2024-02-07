from typing import Type
from pydantic import BaseModel, Field
from langchain_community.utilities.serpapi import SerpAPIWrapper
from template.tools.base import ToolEnvKeyException, BaseTool
import os


SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise Exception("No SERPAPI_API_KEY key found")


class SerpGoogleSearchSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query for Google search.",
    )


class SerpGoogleSearchTool(BaseTool):
    name = "Serp Google Search"

    slug = "serp_google_seach"

    description = (
        "This tool performs Google searches and extracts relevant snippets and webpages. "
        "It's particularly useful for staying updated with current events and finding quick answers to your queries."
    )

    args_schema: Type[SerpGoogleSearchSchema] = SerpGoogleSearchSchema

    tool_id = "a66b3b20-d0a2-4b53-a775-197bc492e816"

    def _run(
        self,
        query: str,
    ) -> str:
        """Search Google and return the results."""

        search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

        try:
            return search.run(query)
        except Exception as err:
            if "Invalid API key" in str(err):
                raise ToolEnvKeyException(
                    f"Serp API Key is not valid. Please check in the [Google SERP Search Toolkit](/toolkits/{self.toolkit_slug})"
                )

            return "Could not search Google. Please try again later."
