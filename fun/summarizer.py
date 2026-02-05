from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from fun.news_extractor import News, get_news
from fun.semantic_search import add_article_to_db, ArticleEntry
from langchain_core.runnables import RunnableLambda, RunnableMap
import json


class NewsAnalysis(BaseModel):
    summary: str = Field(description="Concise summary of the article")
    topics: List[str] = Field(
        description="Main topics disscussed in the article. Minimum of 15"
    )
    title: str = Field(
        description="Actual article title (MUST be exactly as extracted from the tool, do not change it!!!)"
    )


def summarize(url: str):
    chain = build_chain()
    result = chain.invoke({"url": url})
    return result


def build_chain():
    with open("data.json") as f:
        api_key = json.load(f)["api-key"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

    news_extraction = RunnableLambda(
        lambda inp: (
            lambda news: {
                "title": news["title"],
                "fulltext": news["fulltext"],
                "url": inp["url"],
            }
        )(get_news(inp["url"]))
    )

    prompt = ChatPromptTemplate.from_template(
        """
    You are an AI that analizes news article.
    
    Provide:
        - A concise summary of the article's content.
        - A list of the main topics.

    Title: {title}
    Text: {fulltext}
        """
    )
    summarizer = prompt | llm.with_structured_output(NewsAnalysis)

    db_writer = RunnableLambda(
        lambda inp: add_article_to_db(
            ArticleEntry(
                title=inp["title"],
                url=inp["url"],
                summary=inp["summary"],
                topics=inp["topics"],
            )
        )
    )

    chain = (
        news_extraction
        | RunnableMap({"llm_result": summarizer, "url": lambda inp: inp["url"]})
        | RunnableLambda(
            lambda out: {
                **out["llm_result"].dict(),
                "db_status": db_writer.invoke(
                    {
                        "title": out["llm_result"].title,
                        "url": out["url"],
                        "summary": out["llm_result"].summary,
                        "topics": out["llm_result"].topics,
                    }
                ),
            }
        )
    )

    return chain
