import os
import logging
from crewai import  Crew,Process,Agent,Task
from app.agents.planner_agent import  PlannerClass
from app.agents.reasoning_agent import ReasoningClass
from app.agents.retriever_agent import RetrieverClass
from app.agents.validator_agent import ValidatorClass
from crewai.project import CrewBase, agent, task,crew
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

@CrewBase
class AgentManager:
    def __init__(self,user_query: str):
        self.user_query = user_query
        self.gemini_llm = "gemini/gemini-3.1-flash-lite-preview"
        self.planer_class = PlannerClass(llm=self.gemini_llm)
        self.retriever_class = RetrieverClass(llm=self.gemini_llm)
        self.reasoning_class = ReasoningClass(llm=self.gemini_llm)
        self.validator_class = ValidatorClass(llm=self.gemini_llm)

    @agent
    def planner_agent(self) -> Agent:
        return self.planer_class.get_agent()

    @agent
    def retriever_agent(self) -> Agent:
        return self.retriever_class.get_agent()

    @agent
    def reasoning_agent(self) -> Agent:
        return self.reasoning_class.get_agent()

    @agent
    def validator_agent(self) -> Agent:
        return self.validator_class.get_agent()


    @task
    def planner_task(self) -> Task:
        return self.planer_class.get_task(agent_instance=self.planner_agent(),user_query=self.user_query)

    @task
    def retriever_task(self) -> Task:
        return self.retriever_class.get_task(agent_instance=self.retriever_agent(),user_query=self.user_query)

    @task
    def reasoning_task(self) -> Task:
        return self.reasoning_class.get_task(agent_instance=self.reasoning_agent(),
                                             user_query=self.user_query,context_dependencies=[self.retriever_task()])

    @task
    def validator_task(self) -> Task:
        return self.validator_class.get_task(agent_instance=self.validator_agent(),user_query=self.user_query,context_dependencies=[self.reasoning_task()])




    @crew
    def crew(self) -> Crew:
        p_task=self.planner_task()
        ret_task=self.retriever_task()
        reas_task=self.reasoning_task()
        valid_task=self.validator_task()
        return Crew(   
           agents=[self.planner_agent(),self.retriever_agent(),self.reasoning_agent(),self.validator_agent()],
           tasks=[p_task,ret_task,reas_task,valid_task],
           process=Process.sequential,
           max_rpm=15,
           verbose=True
        )


def execute_agent_manager(user_query:str)->str:
    agentManager=AgentManager(user_query)
    result=agentManager.crew().kickoff()
    final_response_text=str(result)           
    if "NO_DATA_FOUND" in final_response_text:
            return {
                "status": "Empty Vector Storage",
                "user_query": user_query,
                "final_verified_response": "No data found matching your query within the local document ecosystem index."
            }   
    return {
        "status": "Success",
        "user_query": user_query,
        "final_verified_response": final_response_text
    }