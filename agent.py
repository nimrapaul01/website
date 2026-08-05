from crewai import Agent,Task,Crew,LLM,Process
import os
from dotenv import load_dotenv

load_dotenv()
llm=LLM(
     model="gemini/gemini-2.5-flash",## this is free
     api_key=os.getenv("GEMINI_API_KEY")
)
# -> we r trying to build a web development agent
# ->requirment analyst agent
# ->ui/ux development AGENT
# ->front end agent
# ->gui BASED MODEL
# ->streemlit add
# ->gui BASED
requirement_agent=Agent(
 role="you are a requirment agent  ",
 goal="that will gather the information for the website project",## task executions and constraints,
 backstory="you are an expert in requirement analysis and will gather information for the website project",
 llm=llm,
 verbose=True
)
requirement_agent_task=Task(
    description="gather the information for the website project",
    agent=requirement_agent,
    expected_output="A detailed report on the information gathered for the website project.",
    output_file="requirement.html"
)
ui_ux_agent=Agent(
    role="you are a ui/ux agent",
    goal="that will  and give me the code for ui/ux of website ",## task executions and constraints,
    backstory="you are an expert in ui/ux development and will give me working code the ui/ux of the website",
    llm=llm
)
ui_ux_agent_task=Task(
    description="give code the ui/ux of the website",
    agent=ui_ux_agent,
    expected_output="A detailed report on the ui/ux of the website.",
    output_file="ui_ux.html"
)
frontend_agent=Agent(
    role="you are a front end agent",
    goal="that will give me the complete front end code of this website also you will give the whole code of the webiste CSS,HTML,Javascript also this agent will decide what will be the best tech stack to build this website",## task executions and constraints,
    backstory="i want to build a website called webdevelopment and want complete front end code for it for now",
    llm=llm

)
frontend_agent_task=Task(
    description="give codde for the front end of the website",
    agent=frontend_agent,
    expected_output="A detailed report on the front end of the website.",
    output_file="frontend.html"
)
crew=Crew(
   agents=[requirement_agent,ui_ux_agent,frontend_agent],
   tasks=[requirement_agent_task,ui_ux_agent_task,frontend_agent_task],
   verbose=True
    
)
result=crew.kickoff()
print(result)
 


