from django.db import models
from ckeditor.fields import RichTextField


class Place(models.Model):

    title = models.CharField(max_length=200, verbose_name="Название", unique=True)
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = RichTextField(verbose_name="Полное описание")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class PlaceImage(models.Model):

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место",
    )
    image = models.ImageField(upload_to="places/", verbose_name="Изображение")
    position = models.PositiveIntegerField(default=0, verbose_name="Позиция")

    class Meta:
        verbose_name = "Изображение места"
        verbose_name_plural = "Изображения мест"
        ordering = ["position", "id"]

    def __str__(self) -> str:
        return f"Изображение {self.position} для {self.place.title}"
