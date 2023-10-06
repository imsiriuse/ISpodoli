from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from podres.models import Booker
import json
import csv

class Command(BaseCommand):
    help = 'Load users from csv file name;surname;room;email'

    # TODO
    # zabezpecit ze tam nebudu duplicitne username

    @staticmethod
    def remove_diacritic(word):
        translation_table = str.maketrans(
            'öűőüłżńćęśŕáäĺčéěíďňóôřůúšťžľýŔÁÄĹČÉĚÍĎŇÓÔŘŮÚŠŤŽĽÝÄ',
            'ououlzncesraalceeidnooruustzlyRAALCEEIDNOORUUSTZLYA'
        )

        return word.translate(translation_table)

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs["filename"][0], 'r', encoding='utf8') as f:
            for person in csv.DictReader(f, delimiter=';'):
                username = self.remove_diacritic(person['surname']).lower()[0:4]
                username += self.remove_diacritic(person['name']).lower()[0:3]

                User.objects.create_user(
                    username=username,
                    email=person['email'],
                    password='zmenimsiheslo',
                    first_name=person['name'],
                    last_name=person['surname'],
                )

                user = User.objects.get(username=username)
                user.is_staff = True
                user.save()

                Booker.objects.create(
                    user=user,
                    room=person['room']
                )


        self.stdout.write(self.style.SUCCESS('Users successfully loaded'))
