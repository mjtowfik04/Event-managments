import os
import django
from faker import Faker
import random
from events.models import Project, Event, EventDetail, Participant

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_managements.settings')
django.setup()

def populate_db():
    fake = Faker()

    # Create Projects
    projects = [Project.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph(),
        start_date=fake.date_this_year()
    ) for _ in range(5)]
    print(f"Created {len(projects)} projects.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.unique.email()
    ) for _ in range(10)]
    print(f"Created {len(participants)} participants.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED'])
        )

        # Assign participants (ManyToMany)
        event.assigned_to.set(random.sample(participants, random.randint(1, 3)))
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Event Details
    for event in events:
        EventDetail.objects.create(
            task=event,
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )
    print("Populated EventDetails for all events.")
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
