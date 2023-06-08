from __future__ import annotations

from typing import Union

from langchain.agents import AgentOutputParser
from langchain.output_parsers.json import parse_json_markdown
from langchain.schema import AgentAction, AgentFinish, OutputParserException


from .prompt import FORMAT_INSTRUCTIONS


def check_is_valid_markdown(markdown_string: str) -> bool:
    """Check if a string is valid markdown."""
    return markdown_string.startswith("```") and markdown_string.endswith("```")


def get_markdown_tag(markdown_string: str) -> str:
    """Get the markdown tag from a string."""
    return markdown_string.split("\n")[0][3:]


class TestCaseGenOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        stripped_text = text.strip()
        if not check_is_valid_markdown(stripped_text):
            raise OutputParserException(
                f"Output is not valid markdown: {stripped_text}")
        markdown_tag = get_markdown_tag(stripped_text)
        if markdown_tag == "json":
            try:
                response = parse_json_markdown(stripped_text)
                action, action_input = response["action"], response["action_input"]
                return AgentAction(action, action_input, stripped_text)
            except Exception as e:
                raise OutputParserException(
                    f"Could not parse LLM output: {stripped_text}") from e
        else:
            return AgentFinish({"output": stripped_text}, stripped_text)

    @property
    def _type(self) -> str:
        return "conversational_chat"
