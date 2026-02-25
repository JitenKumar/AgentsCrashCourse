from crewai import Agent, LLM , Task, Crew

llm = LLM(model="ollama/phi3:latest", temperature=0.7,
          base_url="http://localhost:11434")


researcher_agent = Agent(
    role="Senior AI Researcher",
    goal="""Discover and summarize the latest
            trends in AI and technology.""",
    backstory="""An expert in AI research who tracks
                 emerging trends and their real-world applications.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

content_strategist_agent = Agent(
    role="Tech Content Strategist",
    goal="""Transform AI research insights
            into compelling blog content.""",
    backstory="""An experienced tech writer who makes
                 AI advancements accessible to a broad audience.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

ai_research_task = Task(
    description=(
            "Conduct a deep analysis of AI trends in 2025. "
            "Identify key innovations, breakthroughs, and market shifts. "
            "Before finalizing, ask a human reviewer "
            "for feedback to refine the report."
    ),
    expected_output="""A structured research summary
                       covering AI advancements in 2025.""",
    agent=researcher_agent,
    human_input=True
)

blog_post_task = Task(
    description=(
        "Using insights from the AI Researcher, create an "
        " engaging blog post summarizing key AI advancements. "
        "Ensure the post is informative and accessible. Before "
        "finalizing, ask a human reviewer for approval."
    ),
    expected_output="A well-structured blog post on AI trends in 2025.",
    agent=content_strategist_agent,
    human_input=True
)
ai_research_crew = Crew(
    agents=[researcher_agent, content_strategist_agent],
    tasks=[ai_research_task, blog_post_task],
    verbose=True
)
result = ai_research_crew.kickoff()