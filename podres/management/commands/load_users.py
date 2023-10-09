from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from podres.models import Booker
import json
import csv
import random
import pandas as pd

class Command(BaseCommand):
    help = 'Load users from csv file name;surname;room;email'
    usernames = []

    @staticmethod
    def remove_diacritic(word):
        translation_table = str.maketrans(
            'öűőüłżńćęśŕáäĺčéěíďňóôřůúšťžľýŔÁÄĹČÉĚÍĎŇÓÔŘŮÚŠŤŽĽÝÄ',
            'ououlzncesraalceeidnooruustzlyRAALCEEIDNOORUUSTZLYA'
        )

        return word.translate(translation_table)

    def generate_username(self, name, surname):
        username = self.remove_diacritic(surname).lower()[0:4]
        username += self.remove_diacritic(name).lower()[0:3]

        while True:
            if username in self.usernames:
                username += str(random.randint(0, 9))
            else:
                self.usernames.append(username)
                break

        return username

    def generate_password(self, name, surname):
        character_pool = "!@#$%^&*()_+{}[]:;<>?/.,"
        password = self.remove_diacritic(surname).upper()[:3]
        password += self.remove_diacritic(name).lower()[:3]
        password += str(character_pool[random.randint(0, len(character_pool) - 1)])
        password += str(random.randint(0, 50))
        return password

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **kwargs):

        df = pd.read_csv(kwargs["filename"][0], sep=';')

        df['username'] = df.apply(lambda r: self.generate_username(r['name'], r['surname']), axis=1)
        df['password'] = df.apply(lambda r: self.generate_password(r['name'], r['surname']), axis=1)

        df.to_csv(kwargs["filename"][0], sep=';', index=False)

        for index, row in df.iterrows():
            user = User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email'],
                first_name=row['name'],
                last_name=row['surname'],
                is_staff=True,
            )

            Booker.objects.create(
                user=user,
                room=row['room']
            )

        self.stdout.write(self.style.SUCCESS('Users successfully loaded'))
