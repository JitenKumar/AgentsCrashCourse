from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


class Outline(BaseModel):
    total_chapters: int
    titles: list[str]

@CrewBase
class OutlineCrew:
    """Outline Crew"""

    agents_configs = "configs/agents.yaml"
    tasks_configs = "configs/tasks.yaml"
    
    @agent
    def research_agent(self):
            return Agent(config=self.agents_configs["research_agent"], tools=[SerperDevTool()])
    
    @task
    def research_task(self):
        return Task(config=self.tasks_configs["research_task"])
    
    @agent
    def outline_writer(self):
         return Agent(config=self.agents_configs["outline_writer"])
    
    @task
    def write_outline(self):
        return Task(config=self.tasks_configs["write_outline"], output_pydantic=Outline)
    
    @crew
    def crew(self):
         return Crew(agents=self.agents,tasks=self.tasks,
                     Process=Process.SEQUENTIAL,
                     verbose=True,)