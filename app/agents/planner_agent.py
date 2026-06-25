import os
import logging
import yaml
import re
from app.utils.util import clean_text
from langchain_core.agents import AgentFinish
from typing import Dict,Any
from crewai import Agent, Task
from crewai.tasks.task_output import TaskOutput
from crewai.project import CrewBase
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

def my_step_callback(step_output):
        print(f"\n--- [STEP CALLBACK] ---")    
        if isinstance(step_output, AgentFinish):
            print(f"Planner Agent Finish: {step_output.return_values['output']}")
        else:
            print(f"Planner Agent Thought: {step_output.thought}")
            print(f"Planner Agent Action: {step_output.tool}")
print(f"------------------------\n")

def task_callback(task_output:TaskOutput):
    print(f"--- Task Completed ---")
    print(f"Planner Task Description: {task_output.description}")
    print(f"Planner Task Result: {task_output.raw}")
print("----------------------")



class PlannerClass:
   
    def __init__(self, llm: str):
        self.llm = llm
        self.agents_config = self.load_config("app/agents/config/agents.yaml")
        self.tasks_config = self.load_config("app/agents/config/tasks.yaml")     

    def load_config(self, file_path: str) -> Dict[str, Any]:
        """
        Configuration Utility Function: Safely opens and maps system 
        YAML configurations into Python dictionaries.
        """            
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
            if not config_data:
                raise ValueError(f"Configuration file at {file_path} is completely empty.")
            return config_data

    def get_agent(self) -> Agent:
        """Extracts settings from the configuration function map to initialize the Agent."""
        config = self.agents_config["planner"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self.llm,
            step_callback=my_step_callback,
            verbose=True
        )

    def get_task(self, agent_instance: Agent, user_query: str) -> Task:
        """Extracts details from the task configuration map and passes dynamic data."""
        config = self.tasks_config["planner_task"]
        clean_query = user_query.lower().strip()
        extracted_search_terms=clean_text(clean_query)
        formatted_description = config["description"].format(
            user_query=user_query,
            extracted_search_terms=extracted_search_terms
        )
        formatted_output=config["expected_output"].format(
            user_query=user_query,
            extracted_search_terms=extracted_search_terms
        )

        return Task(
            description=formatted_description,
            expected_output=formatted_output,
            agent=agent_instance,
            callback=task_callback
        )