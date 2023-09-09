from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import myUsers

class Command(BaseCommand):
  def handle(self, *args, **options):
    if not myUsers.objects.filter(username="admin").exists():
        myUsers.objects.create_superuser("admin", "admin@gmail.com", "admin")