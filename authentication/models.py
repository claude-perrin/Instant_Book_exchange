from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from boookzdata.models import WantedBookshelf, GiveawayBookshelf


class BookReader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.OneToOneField('boookzdata.Image', on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)

    # rating
    # transaction_history

    def __str__(self):
        return f"{self.user}'s profile"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        book_reader, created = BookReader.objects.get_or_create(user=instance)
        wanted_shelf, created = WantedBookshelf.objects.get_or_create(book_reader=book_reader)
        giveaway_shelf, created = GiveawayBookshelf.objects.get_or_create(book_reader=book_reader)


post_save.connect(create_user_profile, sender=User)
