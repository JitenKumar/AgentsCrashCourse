
Business Rules JSON -> chroma db will provided these
Tables = config file DDL, DML Data - Neo4j will provide these details


Main LLM -> Orchestrator -> Tasks Segregation
Planning Agent/ReactPattern
validate plan 123 in all system

IntentAgent: query -> validate plan 123 in all system
{
"intent": {
    "name": "check_plan_validity",
    "confidence_score": 0.92,
    "description": "User wants to verify whether a telecom plan is currently active and valid."
  },
  "entities": [
    {
      "name": "plan_id",
      "value": "PK123",
      "type": "string",
      "confidence_score": 0.95
    },
    {
      "name": "system",
      "value": "EPC, Siebel , ATOM, FX",
      "type": "system_reference",
      "confidence_score": 0.88
    }
  ],
}

PlanningAgent : intent :

{
  "name": "check_plan_validity",
  "confidence_score": 0.92,
  "description": "User wants to verify whether a telecom plan is currently active and valid."
}



Tools :
actual function that can be used for calling like DB, API, Web search
runADBQuery(<query>,system)
    system : connection get and fire the query
    structured output : <output>

callWebAPI(<api_details>,<params>,system)
    system : connection get and fire the query
    JSON FormatOut : <output>,ObjectTType