from crewai import Agent,Task,Crew,LLM
import os## operating system



## make func of llms that u export
llm=LLM(
    model="gemini/gemini-2.5-flash",## this is free
    api_key=os.getenv("GEMINI_API_KEY")
)
## every agent needs a task
research_agent=Agent(
    role="research agent",
    goal="research the latest news on stock market",
    backstory="You are a research agent with expertise in  stock market and will fetch me the latest.",
    llm=llm
    
)
research_task=Task(
    description="research the latest news on stock market and provide a summary.",
    agent=research_agent,
    expected_output="A detailed report on the latest news in the stock market."
)
analysis_agent=Agent(
    role="analysis agent",
    goal="determine how news affects stocks",
    backstory="You are an analysis agent with expertise in stock market and will analyze how news affects stocks .",
    llm=llm
)
analy_task=Task(
    description="analyze recent news affect on stock market.",
    agent=analysis_agent,
    expected_output="A detailed analysis of effect of how recent news have affected on stock market."
)
opinion_agent=Agent(
    role="public opinion agent",
    goal="tell public opinion on recent trends",
    backstory="you are a public opinion agent who will tell public opinion(from twitter,instagram) on recent stock trends",
    llm=llm
)
opinion_task=Task(
    description="tell public opinion on recent stock trends.",
    agent=opinion_agent,
    expected_output="A detailed report on public opinion on recent stock trends."
)
crew=Crew(
    agent=[research_agent,analysis_agent,opinion_agent],
    tasks=[research_task,analy_task,opinion_task],
    verbose=True, ##if u do true shows agents reasoning thinking etc ..by default its true if u want to save token do false
    llm=llm
)
result=crew.kickoff()
print(result)




 



   
