from crewai import Crew, Task, Process
from mem0 import MemoryClient

os.environ["MEM0_API_KEY"] = "<your-api-key>"

user_memory = {"provider": "mem0",
               "config": {"user_id": "Paul"},
               "user_memory" : {}}
crew = Crew(
    agents=[],
    tasks=[],
    memory=True,
    process=Process.sequential,
    memory_config=user_memory
)

#Reset the crew memories

crew.reset_memories(command_type = 'all') 

crew.reset_memories(command_type='short')
crew.reset_memories(command_type='long')
crew.reset_memories(command_type='kickoff_outputs')