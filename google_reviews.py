import googlemaps
import pandas as pd
from datetime import datetime
import time


gmaps = googlemaps.Client(key="XXXXXX")

search_queries = [
    "law firms in Glasgow",
    "solicitors in Glasgow",
    "legal services in Glasgow",
    "attorneys in Glasgow",
    "law firms in Edinburgh",
    "solicitors in Edinburgh",
    "legal services in Edinburgh",
    "attorneys in Edinburgh",
]


def fetch_reviews(search_query):
    reviews_data = []

    places_result = gmaps.places(query=search_query)

    while True:
        for place in places_result["results"]:
            place_details = gmaps.place(
                place_id=place["place_id"], fields=["name", "review"]
            )

            if "reviews" in place_details["result"]:
                for review in place_details["result"]["reviews"]:
                    review_data = {
                        "Place Name": place_details["result"]["name"],
                        "Author Name": review.get("author_name"),
                        "Rating": review.get("rating"),
                        "Review Text": review.get("text").replace("\n", " "),
                        "Time": review.get("time"),
                    }
                    reviews_data.append(review_data)

        if "next_page_token" in places_result:
            time.sleep(
                2
            )
            places_result = gmaps.places(
                query=search_query, page_token=places_result["next_page_token"]
            )
        else:
            break

    return reviews_data