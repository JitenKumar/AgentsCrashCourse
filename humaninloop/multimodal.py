from crewai import Crew, Agent, Task, LLM

llm = LLM(model="ollama/phi3:latest", temperature=0.7,
          base_url="http://localhost:11434")

quality_inspector = Agent(
    role="Product Quality Inspector",
    goal="Analyze and assess the quality of product images",
    backstory="""An experienced manufacturing quality control
                 expert who specializes in detecting defects
                 and ensuring compliance.""",
    multimodal=True,
    verbose=True,
    llm=llm
)
# Define a Task for Product Image Inspection
inspection_task = Task(
    description="""Inspect the product image at {image_url}.
                   Identify any visible defects such as scratches,
                   dents, misalignment, or color inconsistencies.
                   Provide a structured quality assessment report.""",
    expected_output="""A detailed report highlighting detected
                       issues and overall quality score.""",
    agent=quality_inspector
)

# Create a Crew with the Multimodal Agent
quality_inspection_crew = Crew(
    agents=[quality_inspector], 
    tasks=[inspection_task], 
    verbose=True
)

image_url = "https://s.marketwatch.com/public/resources/images/MW-HT101_nerd_d_ZG_20191010165334.jpg"

# Run the workflow
result = quality_inspection_crew.kickoff(inputs={"image_url": image_url})

# Display the final inspection report
print("\n=== Final Product Quality Report ===")
print(result.raw)