from research_assist.researcher.AgentNodes import AgentNodes, AgentState
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os
from typing import Dict, Any, List


def load_secrets(env_path: str = ".env") -> Dict[str, str]:
    """
    Load API keys from the specified environment file.

    This function loads environment variables from the default `.env` file
    and the specified `env_path`. It retrieves the OpenAI and Tavily API keys.

    Args:
        env_path (str): The path to the environment file. Defaults to ".env".

    Returns:
        Dict[str, str]: A dictionary containing the loaded API keys.
    """
    # both calls are needed here
    load_dotenv()
    load_dotenv(dotenv_path=env_path)

    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
    }


class ResearchAgent:
    """
    A class representing a research agent that manages the workflow of research tasks.

    This agent utilizes a state graph to navigate through various stages of research,
    including planning, writing, reviewing, and revising reports.

    Attributes:
        nodes (AgentNodes): An instance of AgentNodes containing the nodes for the state graph.
        agent (StateGraph): The state graph that manages the research workflow.
    """

    def __init__(self, model: Any, searcher: Any) -> None:
        """
        Initialize the ResearchAgent with a model and a searcher.

        Args:
            model (Any): The model used for generating research content.
            searcher (Any): The searcher used for retrieving relevant information.
        """
        self.nodes = AgentNodes(model, searcher)
        self.agent = self._setup()

    def _setup(self) -> StateGraph:
        """
        Set up the state graph for the research agent.

        This method initializes the state graph, adds nodes, and defines the edges
        that represent the workflow of the research process.

        Returns:
            StateGraph: The configured state graph for the research agent.
        """
        agent = StateGraph(AgentState)
        agent.add_node("initial_plan", self.nodes.plan_node)
        agent.add_node("write", self.nodes.generation_node)
        agent.add_node("review", self.nodes.review_node)
        agent.add_node("research_plan", self.nodes.research_plan_node)
        agent.add_node("research_revise", self.nodes.research_critique_node)
        agent.add_node("reject", self.nodes.reject_node)
        agent.add_node("accept", self.nodes.accept_node)
        agent.set_entry_point("initial_plan")
        agent.add_conditional_edges(
            "write",
            self.nodes.should_continue,
            {"accepted": "accept", "to_review": "review", "rejected": "reject"},
        )

        agent.add_edge("initial_plan", "research_plan")
        agent.add_edge("research_plan", "write")
        agent.add_edge("review", "research_revise")
        agent.add_edge("research_revise", "write")
        agent.add_edge("reject", END)
        agent.add_edge("accept", END)

        return agent

    def run_task(self, task_description: str, max_revisions: int = 1) -> List[Any]:
        """
        Execute a research task based on the provided description.

        This method compiles the state graph and streams the task through the agent,
        collecting results along the way.

        Args:
            task_description (str): A description of the task to be executed.
            max_revisions (int): The maximum number of revisions allowed. Defaults to 1.

        Returns:
            List[Any]: A list of results generated during the task execution.
        """
        with SqliteSaver.from_conn_string(":memory:") as checkpointer:
            graph = self.agent.compile(checkpointer=checkpointer)
            results = []
            thread = {"configurable": {"thread_id": "1"}}
            for s in graph.stream(
                {
                    "task": task_description,
                    "max_revisions": max_revisions,
                    "revision_number": 1,
                },
                thread,
            ):
                print("#" * 20)
                print(s)
                results.append(s)

        return results
