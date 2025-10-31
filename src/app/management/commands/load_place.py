import json
import requests
from typing import Any
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandParser
from django.core.files.base import ContentFile
from app.models import Place, PlaceImage


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("json_file", type=str, help="Путь к json файлу")

    def get_image_file_by_url(self, image_url: str) -> ContentFile:
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            if not response.headers["content-type"].startswith("image"):
                raise ValueError("URL не ведет на изображение")

            return ContentFile(response.content, name=image_url.split("/")[-1])

        except requests.exceptions.RequestException as error:
            self.stdout.write(self.style.WARNING(f"{image_url}: oшибка сети ({error})"))
        except ValueError as error:
            self.stdout.write(self.style.WARNING(f"{image_url}: ошибка данных ({error})"))

    def handle(self, *args: Any, **options: Any) -> None:
        new_place: dict[str, Any] = {}

        with open(options["json_file"], "r") as file:
            new_place = json.load(file)

        place, created = Place.objects.get_or_create(
            title=new_place["title"],
            defaults={
                "description_short": new_place["description_short"],
                "description_long": new_place["description_long"],
                "longitude": Decimal(new_place["coordinates"]["lng"]),
                "latitude": Decimal(new_place["coordinates"]["lat"]),
            },
        )

        if not created:
            self.stdout.write(
                self.style.WARNING(f"Место с таким названием уже существует: {place.title}")
            )
            return

        for i, image_url in enumerate(new_place["imgs"], start=1):
            PlaceImage.objects.create(
                place=place,
                image=self.get_image_file_by_url(image_url),
                position=i,
            )

        self.stdout.write(self.style.SUCCESS(f"Место сохранено: {place.title}"))
