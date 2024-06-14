import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from object.models import City, Country, Location, Category, Contact, Realty


class Command(BaseCommand):
    help = 'Uploading objects from csv-file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='The CSV file to upload',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not file_path:
            raise CommandError('Please provide the path to the CSV file using --file')

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                country, created = Country.objects.get_or_create(title='Россия')

                with transaction.atomic():
                    for row in reader:
                        city, created = City.objects.get_or_create(
                            name=row.get('location_city'),
                            country=country,
                            district=row.get('district')
                        )
                        location, created = Location.objects.get_or_create(
                            city=city,
                            post_index=row.get('location_post_index'),
                            street=row.get('location_street'),
                            building=row.get('location_building'),
                            floor=row.get('location_floor')
                        )

                        category, created = Category.objects.get_or_create(name=row.get('category'))
                        contact, created = Contact.objects.get_or_create(
                            name=row.get('contact_name'),
                            email=row.get('contact_email'),
                            phone_number=list(row.get('contact_phone_number').split(','))
                        )
                        Realty.objects.get_or_create(
                            title=row.get('title'),
                            site=row.get('site'),
                            area=row.get('area') if isinstance(row.get('area'), int) else None,
                            price=row.get('price') if isinstance(row.get('price'), int) else None,
                            category=category,
                            contact=contact,
                            location=location
                        )
        except FileNotFoundError:
            raise CommandError(f'File "{file_path}" does not exist')
        except Exception as e:
            raise CommandError(f'Error reading file "{file_path}": {e}')

        self.stdout.write(self.style.SUCCESS('Successfully uploaded objects from CSV file'))
