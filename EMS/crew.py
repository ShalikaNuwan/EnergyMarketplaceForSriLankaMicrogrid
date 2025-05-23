from crewai import Crew,Process
from agent import *
from tasks import *

ems = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    process=Process.sequential,
)

ems.kickoff()