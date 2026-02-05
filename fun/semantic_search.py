"""
Module for storing and searching news articles using text-embedding-ada-002 and ChromaDB.

Classes:
    ArticleEntry: Holds article metadata and content.
Functions:
    add_article_to_db(article): Adds article to the vector DB.
    semantic_search(query, max_results=3, distance_threshold=0.5): Finds N semantically similar articles.
"""

import os
from typing import List
from langchain_openai import OpenAIEmbeddings
import chromadb


from pathlib import Path
import json

with open("data.json") as f:
    api_key = json.load(f)["api-key"]


class ArticleEntry:
    def __init__(
        self, title: str, url: str, summary: str, topics: List[str], distance: float = 0
    ):
        self.title = title
        self.url = url
        self.summary = summary
        self.topics = topics
        self.distance = distance

    def as_str(self):
        return f"Title: {self.title}\nSummary: {self.summary}\nTopics: {self.topics}\nURL: {self.url}\nDistance: {self.distance}"


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)

chroma_path = "./chromadb"
Path(chroma_path).mkdir(exist_ok=True)
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="news-articles")


def add_article_to_db(article: ArticleEntry):
    summary_topics = (
        f"{article.title}. {article.summary}. Topics: {', '.join(article.topics)}"
    )
    emb = embeddings.embed_query(summary_topics)
    print("topics:", ", ".join(article.topics))

    collection.add(
        ids=[article.url],
        embeddings=[emb],
        documents=[summary_topics],
        metadatas=[
            {
                "title": article.title,
                "url": article.url,
                "topics": ", ".join(article.topics),
                "summary": article.summary,
            }
        ],
    )


def semantic_search(
    query: str, max_results: int = 3, distance_threshold: float = 0.5
) -> List[ArticleEntry]:
    query_emb = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=max_results,
        include=["metadatas", "distances"],
    )
    articles = []

    metadata = results["metadatas"][0]
    distance = results["distances"][0]
    for meta, dist in zip(metadata, distance):
        if dist <= distance_threshold:
            articles.append(
                ArticleEntry(
                    title=meta["title"],
                    url=meta["url"],
                    summary=meta["summary"],
                    topics=meta["topics"],
                    distance=dist,
                )
            )
    return articles
