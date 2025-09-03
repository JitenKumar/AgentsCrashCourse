from crewai import Agent,LLM,Task,Crew
from crewai_tools import FileReadTool
localllm = LLM(model="phi3:latest", base_url="http://localhost:8000")
senior_technical_writer = Agent(
    role= "Senior Technical Writer",
    goal="Create comprehensive documentation for AI and machine learning projects.",
    backstory= """You are an experienced technical writer
                 with expertise in simplifying complex
                 concepts, structuring content for readability,
                 and ensuring accuracy in documentation.""",
                 verbose=True,
                 llm=localllm
)

research_analyst = Agent(
    role="Senior Research Analyst",
    goal="""Find, analyze, and summarize information 
            from various sources to support technical 
            and business-related inquiries.""",
    backstory="""You are a skilled research analyst with expertise 
                 in gathering accurate data, identifying key trends, 
                 and presenting insights in a structured manner.""",
    llm=localllm,
    verbose=True
)
legal_reviewer = Agent(
    role="Legal Document Expert Reviewer",
    goal="""Review contracts and legal documents to 
            ensure compliance with applicable laws and 
            highlight potential risks.""",
    backstory="""You are a legal expert with deep knowledge 
                 of contract law, regulatory frameworks, 
                 and risk mitigation strategies.""",
    llm=localllm,
    verbose=True
)

writing_task = Task(
    description="""Write a well-structured, engaging,
                   and technically accurate article
                   on {topic}.""",

    agent=senior_technical_writer,

    expected_output="""A polished, detailed, and easy-to-read
                       article on the given topic.""",
)

summarizer_agent = Agent(
    role="Senior Document Summarizer",
    goal="Extract and summarize key insights from provided files in 20 words or less.",
    backstory="""You are an expert in document analysis, skilled at extracting 
                 key details, summarizing content, and identifying critical 
                 insights from structured and unstructured text.""",
    tools=[file_read_tool],
    verbose=True
)
summarise_task = Task(
    description="""Use the FileReadTool to read the contents of the {file_path} the key points from the article
                   on {topic}.""",

    agent=summarizer_agent,
    tools=[file_read_tool],
    expected_output="""A concise summary highlighting the main
                       ideas and insights from the file.""",
)

senior_technical_writer_crew = Crew(
    agents= [senior_technical_writer, research_analyst, legal_reviewer],
    tasks= [writing_task,research_task, legal_review_task],
    verbose=True,
    process=Process.sequenti
)

summarizer_crew = Crew(
    agents=[summarizer_agent],
    tasks=[summarise_task],
    verbose=True,
)

file_read_tool = FileReadTool()

responses = senior_technical_writer_crew.kickoff(inputs={"topic": "The Future of AI in IT Industry"})
summarizer_crew = summarizer_crew.kickoff(inputs={"file_path": "path/to/your/file.txt"})