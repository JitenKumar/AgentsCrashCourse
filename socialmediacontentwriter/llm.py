from crewai import LLM
llm = LLM(model="gpt-4", temperature=0)
local_llm = LLM(model="ollama/llama-3.3", base_url="http://localhost:11434")