from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd


class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("query", "").lower()

        # Simulated DataFrame
        data = {
            "id": [1, 2, 3],
            "name": ["Product A", "Product B", "Cool Gadget"],
            "description": ["Basic A", "Advanced B", "Gadget with cool features"],
            "price": [10.99, 20.49, 15.75],
            "in_stock": [True, False, True],
        }
        df = pd.DataFrame(data)

        # If no query is provided, return an empty dictionary
        if not query:
            return Response({})

        # If a query is provided, return the entire DataFrame as is
        result = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "in_stock": row[4],
            }
            for row in df.values.tolist()
        ]

        return Response(result)
