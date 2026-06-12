from CateMate.models.owner import Owner, GenderType, AllowedGender
from CateMate.utils.hashing import hash_password

# Shared password for all seeded demo accounts. Log in as e.g.
# anna@example.com / password123
SEED_PASSWORD = hash_password("password123")

owners_seed = [
    Owner(name="Anna Müller", gender=GenderType.B, age=28, city_id=1, email="anna@example.com", password=SEED_PASSWORD, bio="Cat lover in Munich.", allow_message_from=AllowedGender.A),
    Owner(name="Max Schmidt", gender=GenderType.A, age=32, city_id=1, email="max@example.com", password=SEED_PASSWORD, bio="Looking for a mate for my cat.", allow_message_from=AllowedGender.A),

    Owner(name="Laura Weber", gender=GenderType.B, age=26, city_id=2, email="laura@example.com", password=SEED_PASSWORD, bio="Cats are life 🐱", allow_message_from=AllowedGender.A),
    Owner(name="Felix Braun", gender=GenderType.A, age=35, city_id=2, email="felix@example.com", password=SEED_PASSWORD, bio="Breeder hobbyist.", allow_message_from=AllowedGender.A),

    Owner(name="Sophia Fischer", gender=GenderType.B, age=29, city_id=3, email="sophia@example.com", password=SEED_PASSWORD, bio="Two lovely cats at home.", allow_message_from=AllowedGender.A),
    Owner(name="Jonas Keller", gender=GenderType.A, age=31, city_id=3, email="jonas@example.com", password=SEED_PASSWORD, bio="New here.", allow_message_from=AllowedGender.A),

    Owner(name="Emma Wagner", gender=GenderType.B, age=27, city_id=4, email="emma@example.com", password=SEED_PASSWORD, bio="Cat enthusiast.", allow_message_from=AllowedGender.A),
    Owner(name="Lukas Hoffmann", gender=GenderType.A, age=33, city_id=4, email="lukas@example.com", password=SEED_PASSWORD, bio="Experienced cat owner.", allow_message_from=AllowedGender.A),

    Owner(name="Mia Becker", gender=GenderType.B, age=24, city_id=5, email="mia@example.com", password=SEED_PASSWORD, bio="First time cat owner.", allow_message_from=AllowedGender.A),
    Owner(name="Noah Schulz", gender=GenderType.A, age=30, city_id=6, email="noah@example.com", password=SEED_PASSWORD, bio="Looking for breeding partner.", allow_message_from=AllowedGender.A),
]