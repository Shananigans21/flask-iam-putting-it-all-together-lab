#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    # Use session.query(...).delete() for proper delete in SQLAlchemy ORM
    db.session.query(Recipe).delete()
    db.session.query(User).delete()
    db.session.commit()

    print("Creating users...")

    users = []
    usernames = set()

    for _ in range(20):
        username = fake.unique.first_name()
        # Alternatively, if you want to manually check:
        # while username in usernames:
        #     username = fake.first_name()
        usernames.add(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.image_url(),  # faker has image_url() method
        )
        # Set password using your model's setter (password, not password_hash)
        user.password = username + 'password'

        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating recipes...")

    recipes = []
    for _ in range(100):
        instructions = fake.paragraph(nb_sentences=8)

        recipe = Recipe(
            title=fake.sentence(nb_words=4),
            instructions=instructions,
            minutes_to_complete=randint(15, 90),
            user=rc(users)
        )

        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()

    print("Complete.")
