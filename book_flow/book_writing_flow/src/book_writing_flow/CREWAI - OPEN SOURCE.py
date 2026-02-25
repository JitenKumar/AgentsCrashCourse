CREWAI - OPEN SOURCE
    
AUTOGEN -> MICROSOFT framworl
LANGRAPH -> OPENSOURCE framewokr

EPC AGENT -> LANGRAPH USE -> 
FLOW BASED -> EPC SARE EXECUTE


from crewai.knowledge.source.string_knowledge_source
 import StringKnowledgeSource


policy_text = """
Our return policy allows customers to return
any product within 30 days of purchase. Refunds
will be issued only if the item is unused and in original packaging.
Customers must provide proof of purchase when requesting a return.
"""

# Create a StringKnowledgeSource object
return_policy_knowledge = StringKnowledgeSource(content=policy_text)



from crewai import Crew, Process

crew = Crew(
    agents=[returns_agent],
    tasks=[returns_task],
    process=Process.sequential,
    knowledge_sources=[return_policy_knowledge],
    verbose=True
)