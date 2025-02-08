import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv
from crewai_tools import PDFSearchTool
from pydantic import BaseModel

load_dotenv()


@CrewBase
class FaqChatBot:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    anthropic_llm = LLM(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        max_tokens=1024,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    rag_tool = PDFSearchTool(
        config=dict(
            llm=dict(
                provider="anthropic",
                config=dict(
                    model="claude-3-5-sonnet-20241022",
                    
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model="text-embedding-ada-002",
                ),
            ),
        ),
        pdf="resources/cal_user_guide.pdf"
    )
    

    @agent
    def retriever(self) -> Agent:
        return Agent(
            llm=self.anthropic_llm,
            config=self.agents_config['retriever'],
            tools=[self.rag_tool],
            verbose=True,
            max_iter=2,
        )

    @agent
    def quality_checker(self) -> Agent:
        return Agent(
            llm=self.anthropic_llm,
            config=self.agents_config['quality_checker'],
            tools=[self.rag_tool],
            verbose=True,
            max_iter=2,
        )

    @task
    def extraction_data(self) -> Task:
        return Task(
            config=self.tasks_config['extraction_data'],
            output_file="outputs/first_draft.md",

        )

    @task
    def quality_checking(self) -> Task:
        return Task(
            config=self.tasks_config["quality_checking"],
            output_file="outputs/final_answer.txt",
            context=[self.extraction_data()]
        )

    @crew
    def faqChatBotCrew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )
