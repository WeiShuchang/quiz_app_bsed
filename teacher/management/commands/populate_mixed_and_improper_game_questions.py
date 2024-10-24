from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for converting improper fractions to mixed fractions.'

    def handle(self, *args, **kwargs):
        # Fetch the game named "Mixed and Improper Fractions Game"
        game = Game.objects.filter(name="Mixed and Improper Fractions Game").first()

        if not game:
            self.stdout.write(self.style.ERROR('No game found with the name "Mixed and Improper Fractions Game". Please create the game first.'))
            return

        questions_data = [
            # 20 sample questions for converting improper fractions to mixed fractions
            {
                'text': 'Convert 9/4 to a mixed fraction.',
                'choices': [
                    {'text': '2 1/4', 'is_correct': True},
                    {'text': '3 1/4', 'is_correct': False},
                    {'text': '1 1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 7/3 to a mixed fraction.',
                'choices': [
                    {'text': '2 1/3', 'is_correct': True},
                    {'text': '3 1/3', 'is_correct': False},
                    {'text': '1 2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 5/2 to a mixed fraction.',
                'choices': [
                    {'text': '2 1/2', 'is_correct': True},
                    {'text': '2 3/2', 'is_correct': False},
                    {'text': '3 1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 11/5 to a mixed fraction.',
                'choices': [
                    {'text': '2 1/5', 'is_correct': True},
                    {'text': '3 1/5', 'is_correct': False},
                    {'text': '1 2/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 8/3 to a mixed fraction.',
                'choices': [
                    {'text': '2 2/3', 'is_correct': True},
                    {'text': '3 1/3', 'is_correct': False},
                    {'text': '1 1/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 13/4 to a mixed fraction.',
                'choices': [
                    {'text': '3 1/4', 'is_correct': True},
                    {'text': '2 1/4', 'is_correct': False},
                    {'text': '4 1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 10/3 to a mixed fraction.',
                'choices': [
                    {'text': '3 1/3', 'is_correct': True},
                    {'text': '2 1/3', 'is_correct': False},
                    {'text': '4 2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 14/5 to a mixed fraction.',
                'choices': [
                    {'text': '2 4/5', 'is_correct': True},
                    {'text': '3 4/5', 'is_correct': False},
                    {'text': '1 4/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 15/8 to a mixed fraction.',
                'choices': [
                    {'text': '1 7/8', 'is_correct': True},
                    {'text': '2 7/8', 'is_correct': False},
                    {'text': '1 1/8', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 17/6 to a mixed fraction.',
                'choices': [
                    {'text': '2 5/6', 'is_correct': True},
                    {'text': '3 5/6', 'is_correct': False},
                    {'text': '1 5/6', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 20/7 to a mixed fraction.',
                'choices': [
                    {'text': '2 6/7', 'is_correct': True},
                    {'text': '3 6/7', 'is_correct': False},
                    {'text': '1 6/7', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 19/5 to a mixed fraction.',
                'choices': [
                    {'text': '3 4/5', 'is_correct': True},
                    {'text': '2 4/5', 'is_correct': False},
                    {'text': '4 4/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 12/5 to a mixed fraction.',
                'choices': [
                    {'text': '2 2/5', 'is_correct': True},
                    {'text': '3 2/5', 'is_correct': False},
                    {'text': '1 2/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 22/9 to a mixed fraction.',
                'choices': [
                    {'text': '2 4/9', 'is_correct': True},
                    {'text': '3 4/9', 'is_correct': False},
                    {'text': '1 4/9', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 23/4 to a mixed fraction.',
                'choices': [
                    {'text': '5 3/4', 'is_correct': True},
                    {'text': '6 3/4', 'is_correct': False},
                    {'text': '4 3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 27/10 to a mixed fraction.',
                'choices': [
                    {'text': '2 7/10', 'is_correct': True},
                    {'text': '3 7/10', 'is_correct': False},
                    {'text': '1 7/10', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 16/7 to a mixed fraction.',
                'choices': [
                    {'text': '2 2/7', 'is_correct': True},
                    {'text': '3 2/7', 'is_correct': False},
                    {'text': '1 2/7', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 18/4 to a mixed fraction.',
                'choices': [
                    {'text': '4 1/2', 'is_correct': True},
                    {'text': '5 1/2', 'is_correct': False},
                    {'text': '3 1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 25/6 to a mixed fraction.',
                'choices': [
                    {'text': '4 1/6', 'is_correct': True},
                    {'text': '5 1/6', 'is_correct': False},
                    {'text': '3 1/6', 'is_correct': False},
                ]
            },
            {
                'text': 'Convert 30/11 to a mixed fraction.',
                'choices': [
                    {'text': '2 8/11', 'is_correct': True},
                    {'text': '3 8/11', 'is_correct': False},
                    {'text': '1 8/11', 'is_correct': False},
                ]
            },
            
        ]

        for question_data in questions_data:
            question = GameQuestion.objects.create(game=game, text=question_data['text'])
            for choice_data in question_data['choices']:
                GameChoice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )

            # Optionally print the question and choices for confirmation
            self.stdout.write(self.style.SUCCESS(f'Question: {question_data["text"]}'))
            for choice in question_data['choices']:
                self.stdout.write(f' - Choice: {choice["text"]} (Correct: {choice["is_correct"]})')

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for converting improper fractions to mixed fractions.'))
