from crewai import Crew,Process
from EMS.agent import *
from EMS.tasks import *

ems = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    process=Process.sequential,
)

def runEMS():
    ems.kickoff()