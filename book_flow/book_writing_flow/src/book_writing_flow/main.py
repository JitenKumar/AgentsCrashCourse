#!/usr/bin/env python
import os
import asyncio

from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from book_writing_flow.crews.Writer_crew.writer_crew import ChapterWriterCrew
from book_writing_flow.crews.Outline_crew.outline_crew import OutlineCrew
from dotenv import load_dotenv

load_dotenv()

class Chapter(BaseModel):
    title: str = ""
    content: str = ""

class ChaperState(BaseModel):
    topic: str = "AI in 2025"
    total_chapters: int = 0
    titles: list[str] = []
    chapters: list[Chapter] = []

class ChaperFlow(Flow[ChaperState]):
    print("Chapter flow started")
    @start
    def generate_outline(self):
        outline = OutlineCrew().crew().kickoff(input={"topic": self.state.topic})
        self.state.total_chapters = outline.total_chapters
        self.state.titles = outline.titles

    @listen(generate_outline)
    async def generate_chapters(self):
        print("Generating chapters...")
        tasks = []

        async def write_single_chapter(title: str):
            output = (ChapterWriterCrew().crew().kickoff(input={"title": title,
                                                                "topic": self.state.topic,
                                                                "chapters": [chapter.title for chapter in self.state.chapters]
                                                                }))
            return output.pydantic
        for i in range(self.state.total_chapters):
            task = asyncio.create_task(write_single_chapter(self.state.titles[i]))
            tasks.append(task)
        chapters = await asyncio.gather(*tasks)
        print("Chapters generated.")
        self.state.chapters.extend(chapters)

        @listen(generate_chapters)
        async def save_book(Saving Book):
            print("All chapters have been generated.")
            with open("book.md","w") as f:
                for chapter in self.state.chapters:
                    f.write(f"# {chapter.title}\n\n")
                    f.write(f"{chapter.content}\n\n")
            # You can add any finalization logic here
def kickoff():
    book_flow = BookFlow()
    asyncio.run(book_flow.kickoff_async())

def plot():
    book_flow = BookFlow()
    book_flow.plot()

if __name__ == "__main__":
    kickoff()