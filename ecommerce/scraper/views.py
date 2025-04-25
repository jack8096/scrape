from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .amazon import AmazonScraper
from .flipkart import FlipkartScraper
from .myntra import MyntraScraper


class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return Response(
                {"error": "Please provide a search query (?q=red dress)"}, status=400
            )

        amazon_results = AmazonScraper(query).get_results()
        flipkart_results = FlipkartScraper(query).get_results()
        myntra_results = MyntraScraper(query).get_results()

        all_results = pd.DataFrame(amazon_results + flipkart_results + myntra_results)
        all_results_sorted = all_results.sort_values(
            by="rating", ascending=False, na_position="last"
        ).fillna("")

        return Response(all_results_sorted.to_dict(orient="records"))
