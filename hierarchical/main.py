from crewai import Crew, Agent,Task, LLM, Process

llm = LLM(
    model="ollama/phi3:latest",      # or "ollama/llama3", "ollama/mistral"
    base_url="http://localhost:11434",
    temperature=0.7,
)

#manager agent
manager_agent = Agent(
    role="Project Research Manager",
    goal="Oversee the project research",
    backstory="""Your are an experienced project manager responsible
                 for ensuring project research.""",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

market_demand_agent = Agent(
    role="Market Demand Analyst",
    goal="Analyze market demand for new projects.",
    backstory="""A skilled market analyst with expertise
                 in evaluating product-market fit.""",
    allow_delegation=False,  
    verbose=True,
    llm=llm
)

# Risk associated with a project
risk_analysis_agent = Agent(
    role="Risk Analysis Analyst",
    goal="Assess potential risks associated with the project.",
    backstory="""A financial and strategic expert
                 focused on identifying business risks.""",
    allow_delegation=False,  
    verbose=True,
    llm=llm
)
# ROI investment agent
return_on_investment_agent = Agent(
    role="Return on Investment Analyst",
    goal="Estimate the financial return on investment.",
    backstory="""You are an expert in financial modeling
                 and investment analysis.""",
    allow_delegation=False,  
    verbose=True,
    llm=llm
)

manager_task = Task(
    description="""Oversee the project research on {project_title}
                   and ensure timely, high-quality responses.""",
    expected_output="""A manager-approved response ready to be
                       sent as an article on {project_title}.""",
    agent=manager_agent,  
)

market_demand_task = Task(
    description="Analyze the demand for the project '{project_title}'.",

    expected_output="A structured summary of market demand trends.",

    agent=market_demand_agent,  
)

risk_analysis_task = Task(
    description="Assess the risks associated with the project '{project_title}'.",

    expected_output="A comprehensive risk assessment report.",

    agent=risk_analysis_agent,  
)

return_on_investment_task = Task(
    description="Estimate the return on investment for the project '{project_title}'.",

    expected_output="A detailed ROI analysis report.",

    agent=return_on_investment_agent,  

)
final_report_task = Task(
    description="""Review the final responses from the market demand,
                   risk analysis, and ROI agents and create a final report.""",
    expected_output="""A comprehensive report on the project '{project_title}'
                       containing the market demand, risk analysis,
                       and return on investment.""",
    agent=manager_agent,
)

project_research_crew = Crew(
    name="Project Research Crew",
    agents=[
        market_demand_agent,
        risk_analysis_agent,
        return_on_investment_agent,
    ],
    tasks=[
        market_demand_task,
        risk_analysis_task,
        return_on_investment_task,
        final_report_task,
    ],
    manager_agent=manager_agent,
    process=Process.hierarchical,
    verbose=True
)

inputs = {
    "project_title": "Multi-Agent Systems"
}

result = project_research_crew.kickoff(inputs=inputs)
