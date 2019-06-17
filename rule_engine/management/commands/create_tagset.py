import argparse
import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from rule_engine.models import TagSet, Tag, Query


class Command(BaseCommand):

    help = 'Create TagSet from JSON files.'

    def add_arguments(self, parser):
        parser.add_argument('tagset_name', type=str)
        parser.add_argument('tagset_dir', type=str)

    def handle(self, *args, **options):
        user = User.objects.get(username='sch459')
        
        tagset_name = options['tagset_name']
        tagset, created = TagSet.objects.get_or_create(name=tagset_name, created_by=user)

        tagset_dir = Path(options['tagset_dir'])
        if not tagset_dir.is_dir():
            self.stderr.write(f'{tagset_dir} is not a directory.')
            return

        for tagset_file in tagset_dir.glob('*.json'):
            main_topic = tagset_file.stem

            for minor_topic, queries in json.load(tagset_file.open(mode='r')).items():
                tag, created = Tag.objects.get_or_create(name=f'{main_topic}-{minor_topic}', tagset=tagset, created_by=user)

                for query_string in queries:
                    query, created = Query.objects.get_or_create(query=query_string, tag=tag, read_only=True, created_by=user)

