"""
Module for extracting news articles and their titles from URLs.

Supports multiple languages specified by their ISO 639-1 codes.

Classes:
    News: Data structure to hold the full text and title of a news article.

Functions:
    get_news(url: str, lang: str) -> News | None:
        Downloads and parses a news article from the given URL if the language is supported.News extracto

"""

from typing import Dict
from newspaper import Article
from dataclasses import dataclass
from langchain.tools import tool


SUPPORTED_LANG = [
    "ar",
    "ru",
    "nl",
    "de",
    "en",
    "es",
    "fr",
    "he",
    "it",
    "ko",
    "no",
    "fa",
    "pl",
    "pt",
    "sv",
    "hu",
    "fi",
    "da",
    "zh",
    "id",
    "vi",
    "sw",
    "tr",
    "el",
    "uk",
]


@dataclass
class News:
    fulltext: str = ""
    title: str = ""

    def __init__(self, fulltext: str, title: str):
        self.fulltext = fulltext
        self.title = title


def get_news(url: str) -> Dict[str, str]:
    """grab news article + title
    Extracts news article and title from a given URL.
    Returns news title and full text. Use for URLs containing news articles.
    Args:
        url (str)
    """
    print(f"Start parcing url: {url}")
    article = Article(url)
    article.download()
    article.parse()
    return {"fulltext": article.text, "title": article.title}
