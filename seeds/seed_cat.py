from CateMate.models.cat import Cat, CatGender

cats_seed = [
    Cat(owner_id=1, name="Luna", age=3, breed_id=1, gender=CatGender.FEMALE, color="White", notes="Vaccinated and friendly."),
    Cat(owner_id=2, name="Simba", age=4, breed_id=2, gender=CatGender.MALE, color="Orange Tabby", notes="Very social."),
    Cat(owner_id=3, name="Milo", age=2, breed_id=3, gender=CatGender.MALE, color="Gray", notes="Indoor cat."),
    Cat(owner_id=4, name="Bella", age=5, breed_id=4, gender=CatGender.FEMALE, color="Cream", notes="Calm temperament."),
    Cat(owner_id=5, name="Oliver", age=3, breed_id=5, gender=CatGender.MALE, color="Brown", notes="Pedigree line."),

    Cat(owner_id=6, name="Nala", age=2, breed_id=1, gender=CatGender.FEMALE, color="Black", notes="Very playful."),
    Cat(owner_id=7, name="Leo", age=4, breed_id=2, gender=CatGender.MALE, color="Golden", notes="Healthy and active."),
    Cat(owner_id=8, name="Coco", age=1, breed_id=6, gender=CatGender.FEMALE, color="Chocolate", notes="Still a kitten."),
    Cat(owner_id=9, name="Charlie", age=3, breed_id=3, gender=CatGender.MALE, color="Blue Gray", notes="Gentle personality."),
    Cat(owner_id=10, name="Daisy", age=4, breed_id=4, gender=CatGender.FEMALE, color="White and Gray", notes="Vaccinated."),

    Cat(owner_id=1, name="Rocky", age=6, breed_id=5, gender=CatGender.MALE, color="Black", notes="Strong and healthy."),
    Cat(owner_id=2, name="Lucy", age=2, breed_id=6, gender=CatGender.FEMALE, color="Silver", notes="Curious."),
    Cat(owner_id=3, name="Max", age=5, breed_id=2, gender=CatGender.MALE, color="Orange", notes="Friendly."),
    Cat(owner_id=4, name="Lily", age=3, breed_id=1, gender=CatGender.FEMALE, color="Snow White", notes="Well cared for."),
    Cat(owner_id=5, name="Toby", age=2, breed_id=4, gender=CatGender.MALE, color="Cream Brown", notes="Very active."),
]