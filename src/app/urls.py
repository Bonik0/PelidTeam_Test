from django.urls import path
from .views import MapView, PlaceDetailsView


urlpatterns = [
    path("", MapView.as_view(), name="map_page"),
    path(
        "places/<int:place_id>",
        PlaceDetailsView.as_view(),
        name="place_details",
    ),
]
