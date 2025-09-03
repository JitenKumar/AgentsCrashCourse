from crewai.flow.flow import Flow, listen , router, start
import random
from pydantic import BaseModel

class CounterState(BaseModel):
    count: int = 0

class StructureStateFlow(Flow):

    @start
    def initialize(self):
        print(f"initial count: {self.state.count}")
        self.state.count = 1

    @listen(initialize)
    def increment_count(self):
        self.state.count += 1
        print(f"incremented count: {self.state.count}")


class RouterFlow(Flow):

    @start
    def classify_request(self):
        request_type = random.choice(["urgent","normal"])
        print(f"Request Classified as: {request_type}")
        return request_type
    @router
    def route_request(self,classification):
        if classification == "urgent":
            return "handle_urgent"
        else:
            return "handle_normal"
        
    @listen("handle_urgent")
    def handle_urgent(self):
        print("Handling urgent request...")

    @listen("handle_normal")
    def handle_normal(self):
        print("Handling normal request...")


flow = RouterFlow()
await flow.kickoff_async()