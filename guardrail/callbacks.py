from crewai import Agent, Task, Crew

# AI Researcher Agent
research_agent = Agent(
    role="AI News Researcher",
    goal="Find and summarize the latest AI news from trusted sources",
    backstory="""You are an AI journalist who follows the
                 latest advancements in artificial intelligence.""",
    verbose=False,
)

def notify_team(output):

    print(f"""Task Completed!
              Task: {output.description}
              Output Summary: {output.summary}""")

    with open("latest_ai_news.txt", "w") as f:
        f.write(f"Task: {output.description}\n")
        f.write(f"Output Summary: {output.summary}\n")
        f.write(f"Full Output: {output.raw}\n")
    
    print("News summary saved to latest_ai_news.txt")

research_news_task = Task(
    description="Find and summarize the latest AI news",
    agent=research_agent,
    callable=notify_team
)
ai_news_crew = Crew(
    agents=[research_agent],
    tasks=[research_news_task],
    verbose=False
)

result = ai_news_crew.kickoff()

