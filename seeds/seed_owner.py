from CateMate.models.owner import Owner, GenderType, AllowedGender

owners_seed = [
    Owner(name="Anna Müller", gender=GenderType.B, age=28, city_id=1, email="anna@example.com", password="hashed_pw", bio="Cat lover in Munich.", allow_message_from=AllowedGender.A),
    Owner(name="Max Schmidt", gender=GenderType.A, age=32, city_id=1, email="max@example.com", password="hashed_pw", bio="Looking for a mate for my cat.", allow_message_from=AllowedGender.A),

    Owner(name="Laura Weber", gender=GenderType.B, age=26, city_id=2, email="laura@example.com", password="hashed_pw", bio="Cats are life 🐱", allow_message_from=AllowedGender.A),
    Owner(name="Felix Braun", gender=GenderType.A, age=35, city_id=2, email="felix@example.com", password="hashed_pw", bio="Breeder hobbyist.", allow_message_from=AllowedGender.A),

    Owner(name="Sophia Fischer", gender=GenderType.B, age=29, city_id=3, email="sophia@example.com", password="hashed_pw", bio="Two lovely cats at home.", allow_message_from=AllowedGender.A),
    Owner(name="Jonas Keller", gender=GenderType.A, age=31, city_id=3, email="jonas@example.com", password="hashed_pw", bio="New here.", allow_message_from=AllowedGender.A),

    Owner(name="Emma Wagner", gender=GenderType.B, age=27, city_id=4, email="emma@example.com", password="hashed_pw", bio="Cat enthusiast.", allow_message_from=AllowedGender.A),
    Owner(name="Lukas Hoffmann", gender=GenderType.A, age=33, city_id=4, email="lukas@example.com", password="hashed_pw", bio="Experienced cat owner.", allow_message_from=AllowedGender.A),

    Owner(name="Mia Becker", gender=GenderType.B, age=24, city_id=5, email="mia@example.com", password="hashed_pw", bio="First time cat owner.", allow_message_from=AllowedGender.A),
    Owner(name="Noah Schulz", gender=GenderType.A, age=30, city_id=6, email="noah@example.com", password="hashed_pw", bio="Looking for breeding partner.", allow_message_from=AllowedGender.A),
]