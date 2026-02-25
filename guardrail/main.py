from crewai import Agent, Task, Crew
from pydantic import BaseModel

summary_agent = Agent(role="Summary agent",
                      description="Summarizes the content",
                      tools=["text-summarizer"],
                      goal="Summarise the research paper " \
                      ' Conventional Neural Networks in 200 words"',
                      backstory="Specialize in summarising research papers",
                      verbose=True)
 
 
def validate_summary_length(task_output):
    try:
        print("Validating summary length")
        task_str_output = str(task_output)
        total_words = len(task_str_output.split())

        print(f"Word count: {total_words}")

        if total_words > 150:
            print("Summary exceeds 150 words")
            return (False, f"""Summary exceeds 150 words.
                               Current Word count: {total_words}""")

        if total_words == 0:
            print("Summary is empty")
            return (False, "Generated summary is empty.")

        print("Summary is valid")
        return (True, task_output)

    except Exception as e:
        print("Validation system error")
        return (False, f"Validation system error: {str(e)}")


summary_task = Task(

    description="Summarizes the content of the research paper",
    agent=summary_agent,
    expected_output="A concise summary of the research paper in 200 words",
    guardrail=validate_summary_length,
    max_retry_limit=3
)

#Pydantic Model for strict json format
class ResearchReport(BaseModel):
    """Represent a structured research report"""
    title: str
    summary: str
    key_finding: list[str]

class ResearchFindings(BaseModel):
    """Structured research report output"""
    title: str
    key_findings: list[str]

class AnalysisSummary(BaseModel):
    """Structured summary of research findings"""
    insights: list[str]
    key_takeaways: str


import json
from typing import Tuple, Any

def validate_json_report(task_output):
    """"""
    try:
        # Parse JSON output
        data = json.loads(task_output.pydantic.model_dump_json())

        # Check required fields
        if "title" not in data or "summary" not in data or "key_findings" not in data:
            return (False, "Missing required fields: title, summary, or key_findings.")

        return (True, task_output)
        
    except json.JSONDecodeError:
        return (False, "Invalid JSON format. Please ensure correct syntax.")

research_report_agent = Agent(
    role="Research Analyst",
    goal="Generate structured JSON reports for research papers",
    backstory="You are an expert in structured reporting.",
    verbose=False)

research_report_task = Task(
    description="Generate a structured JSON research report",
    expected_output="A JSON with 'title', 'summary', and 'key_findings'.",
    agent=research_report_agent,
    output_pydantic=ResearchReport,
    guardrail=validate_json_report,
    max_retries=3
)

summary_crew = Crew(
    agents=[summary_agent],
    tasks=[summary_task],
    verbose=True
)

result = summary_crew.kickoff()