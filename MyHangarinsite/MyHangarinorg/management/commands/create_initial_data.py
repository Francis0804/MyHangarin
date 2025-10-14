from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from MyHangarinorg.models import Category, Priority, Task, SubTask, Note

fake = Faker()

class Command(BaseCommand):
    help = 'Create initial data for the web application'

    def handle(self, *args, **kwargs):
        self.create_task(10)
        self.create_notes(10)
        self.create_subtask(10)

    def create_task(self, count):
        category = Category.objects.order_by('?').first()
        if not category:
            category = Category.objects.create(name='Default Category')

        priority = Priority.objects.order_by('?').first()
        if not priority:
            priority = Priority.objects.create(name='Default Priority')

        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5)[:50],  # max_length=50
                description=fake.sentence(nb_words=10)[:50],  # max_length=50
                deadline=timezone.make_aware(fake.date_time_between(start_date='-1y', end_date='+1y')),
                status=fake.random_element(elements=['Pending', 'In progress', 'Completed']),
                category=category,
                priority=priority
            )
        self.stdout.write(self.style.SUCCESS('Initial data for task created successfully.'))

    def create_notes(self, count):
        for _ in range(count):
            task = Task.objects.order_by('?').first()
            if task:
                Note.objects.create(
                    task=task,
                    content=fake.sentence(nb_words=10)[:50],  # max_length=50
                )
        self.stdout.write(self.style.SUCCESS('Initial data for note created successfully.'))

    def create_subtask(self, count):
        for _ in range(count):
            parent_task = Task.objects.order_by('?').first()
            if parent_task:
                SubTask.objects.create(
                    parent_task=parent_task,
                    title=fake.sentence(nb_words=5)[:50],  # max_length=50
                    status=fake.random_element(elements=['Pending', 'In progress', 'Completed']),
                )
        self.stdout.write(self.style.SUCCESS('Initial data for subtask created successfully.'))
