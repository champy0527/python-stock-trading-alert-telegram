import requests
from datetime import datetime, timedelta


def get_today_date():
    today = datetime.now()
    return today.strftime("%Y-%m-%d")


def get_two_days_ago():
    today = datetime.now()
    yesterday = today - timedelta(days= 2)
    return yesterday.strftime("%Y-%m-%d")


TODAY = get_today_date()
TWO_DAYS_AGO = get_two_days_ago()


class News:
    NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything?"

    def __init__(self, keyword, apiKey, date_from=TWO_DAYS_AGO, searchIn="title", sortBy="publishedAt"):
        self.apiKey = apiKey
        self.keyword = keyword
        self.date_from = date_from
        self.searchIn = searchIn
        self.sortBy = sortBy
        self.headline_articles = self.get_news_headlines()["articles"]

    def get_news_headlines(self):
        new_parameters = {
            "q": self.keyword,
            "from": self.date_from,
            "language": "en",
            # "to": self.date_to,
            "searchIn": self.searchIn,
            "sortBy": self.sortBy,
            "pageSize": 3,
            "apiKey": self.apiKey
        }

        response = requests.get(url=self.NEWS_API_ENDPOINT, params=new_parameters)
        response.raise_for_status()
        return response.json()

    def get_article_headline(self):
        return [article["title"] for article in self.headline_articles]

    def get_article_brief(self):
        return [article["description"].replace("\n", "") for article in self.headline_articles]

    def zip_article_dict(self):
        article_keys = self.get_article_headline()
        article_values = self.get_article_brief()
        return dict(zip(article_keys, article_values))
