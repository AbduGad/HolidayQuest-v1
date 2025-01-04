from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Reset the Users_user table and its auto-increment value"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Truncate table
            cursor.execute("TRUNCATE TABLE Users_user;")
            # Reset auto-increment
            cursor.execute("ALTER TABLE Users_user AUTO_INCREMENT = 1;")
        self.stdout.write(self.style.SUCCESS("Successfully reset users_user table."))
