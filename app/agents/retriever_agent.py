import os
import logging
import yaml
from langchain_core.agents import AgentFinish
from typing import Dict,Any
from crewai import Agent, Task
from crewai.tasks.conditional_task import ConditionalTask
from app.db.db_retriever import search_document
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

def custom_operation_tool(user_query: str,top_k:int=5) -> str:
            """ Search Document from the vector database based on the provided User query."""    
            try:
                logger.info("Initializing Strategic Retriever Agent configurations...")
                docs = search_document(user_query)
                print(f"Docs is {docs}")
                if  docs:  
                    retrieved_context=[doc for doc,score in docs]
                    print(f"Retrieved Context is {retrieved_context[0].page_content}")
                    if user_query.lower() in retrieved_context[0].page_content.lower():
                        print("Substring found!")
                        context = user_query
                        return context
                    else:
                        print("Substring not found.")
                        print("NO_DATA_FOUND") 
                        return "NO_DATA_FOUND"    
                else:
                    print("NO_DATA_FOUND") 
                    return "NO_DATA_FOUND"
            except Exception as e:
                logger.exception(f"Retriever error: {str(e)}")

def my_step_callback(step_output):
        print(f"\n--- [STEP CALLBACK] ---")    
        if isinstance(step_output, AgentFinish):
            print(f"Retriever Agent Finish: {step_output.return_values['output']}")
        else:
            print(f"Retriever Agent Thought: {step_output.thought}")
            print(f"Retriever Agent Action: {step_output.tool}")
print(f"------------------------\n")

def task_callback(task_output:TaskOutput):
    print(f"--- Task Completed ---")
    print(f"Retriever Task Description: {task_output.description}")
    print(f"Retriever Task Result: {task_output.raw}")
print("----------------------")

def pipeline_conditional_router(last_task_output:TaskOutput) -> bool:
        """
        Evaluates Retriever Agent results. 
        Returns False to halt execution if nothing is found in the DB.
        """
        output_data = str(last_task_output.raw).strip()
        if "NO_DATA_FOUND" in output_data:
            print("🛑 [Pipeline Halting] Vector database returned empty strings. Terminating Crew sequence early.")
            return False # Drop the execution chain right here
        return True # Safe to hand data to the Reasoner Agent


class RetrieverClass:
    
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
        config = self.agents_config["retriever"]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose= True,
            allow_delegation= False,
            llm=self.llm,
            step_callback=my_step_callback

        )

    def get_task(self, agent_instance: Agent, user_query: str) -> Task:
        config = self.tasks_config["retriever_task"]
        db_context = custom_operation_tool(user_query)
        print("Retrieved Context is ",db_context)
        formatted_description=""
        format_output=""
        if db_context == "NO_DATA_FOUND":
            formatted_description="Retrived Context is NO_DATA_FOUND"
            format_output="NO_DATA_FOUND"
        
        elif db_context is None or not db_context.strip():
            formatted_description="Retrived Context is NO_DATA_FOUND"
            format_output="NO_DATA_FOUND"
        
        else :    
            formatted_description = config["description"].format(
                 retrieved_context=db_context
            )
            format_output=config["expected_output"]
        
        return ConditionalTask(
                description=formatted_description,
                expected_output=format_output,
                agent=agent_instance,
                callback=task_callback,
                condition=pipeline_conditional_router
        )