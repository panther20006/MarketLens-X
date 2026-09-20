import serpapi

from config import SERPAPI_KEY


client = serpapi.Client(
    api_key=SERPAPI_KEY
)


def search_products(
    query,
    location="Ahmedabad, Gujarat, India"
):

    results = client.search({

        "engine": "google_shopping",

        "q": query,

        "location": location,

        "gl": "in",

        "hl": "en",

        "device": "desktop"

    })

    return results