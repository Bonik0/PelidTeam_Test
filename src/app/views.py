from django.views import View
from django.http import JsonResponse, HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import Place
from typing import Any


class MapView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["geojson"] = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.longitude, place.latitude],
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": f"place_{place.id}",
                        "detailsUrl": f"/places/{place.id}",
                    },
                }
                for place in Place.objects.all()
            ],
        }
        return context


class PlaceDetailsView(View):

    def get(self, request: HttpRequest, place_id: int) -> JsonResponse:
        place = get_object_or_404(Place, id=place_id)

        details = {
            "title": place.title,
            "imgs": [image.image.url for image in place.images.all().order_by("position")],
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": str(place.longitude),
                "lat": str(place.latitude),
            },
        }

        return JsonResponse(details)
