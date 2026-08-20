from faker import Faker
import random
from db.database import init_db
from db.queries import add_application, get_all_applications
from datetime import timedelta


fake = Faker()


SOURCES = ["LinkedIn", "Referral", "Company site", "Indeed", "Xing", "Stepstone"]
STATUSES = ["Applied", "Screening", "Interview", "Offer", "Rejected", "Ghosted"]
WEIGHTS = [60, 15, 10, 5 , 20, 10]
LOCATIONS = ['Munich', 'Augsburg', 'Berlin', 'Cologne', 'Dusseldorf', 'Hamburg']
WORKFORM = ['Onsite', 'Remote', 'Hybrid']
N_ROWS = 100

def seed():
    init_db()
    if len(get_all_applications()) > 0:
        print("Already seeded, skipping.")
        return

    for _ in range(N_ROWS):
        status = random.choices(STATUSES, weights=WEIGHTS, k=1)[0]
        applied_on = fake.date_between(start_date="-6M", end_date="today")

        response_date = None
        if status != "Applied":
            random_dates = random.randint(3,21)
            response_date = applied_on + timedelta(days=random_dates)

        add_application(
            company=fake.company(),
            role=fake.job(),
            date_applied=applied_on,
            status=status,
            work_form=random.choice(WORKFORM),
            source=random.choice(SOURCES),
            location=random.choice(LOCATIONS),
            salary_range=None,
        )

    print(f"Seeded {N_ROWS} applications.")

if __name__ == "__main__":
    seed()
