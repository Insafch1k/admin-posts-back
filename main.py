import requests

response = requests.get(
            url="https://habr.com/en/companies/postgrespro/articles/902888/?utm_source=habrahabr&utm_medium=rss&utm_campaign=902888",
            timeout=10
)

print(response.text)