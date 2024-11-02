from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for subtracting fractions.'

    def handle(self, *args, **kwargs):
        game = Game.objects.get(name="Subtracting Fractions Game")  # Get the first game instance (make sure you have at least one game)

        if not game:
            self.stdout.write(self.style.ERROR('No game found. Please create a game first.'))
            return

        questions_data = [
            # First 10 questions (already present)
            {
                'text': '5/6 - 2/6?',
                'choices': [
                    {'text': '1/6', 'is_correct': False},
                    {'text': '3/6', 'is_correct': False},
                    {'text': '1/3', 'is_correct': True},
                ]
            },
             {
                'text': '7/8 - 5/8?',
                'choices': [
                    {'text': '1/8', 'is_correct': False},
                    {'text': '2/8', 'is_correct': False},
                    {'text': '1/4', 'is_correct': True},
                ]
            },
             {
                'text': '9/10 - 4/10?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '5/2', 'is_correct': False},
                    {'text': '1/10', 'is_correct': False},
                ]
            },
            {
                'text': '6/9 - 2/9?',
                'choices': [
                    {'text': '3/9', 'is_correct': False},
                    {'text': '4/9', 'is_correct': True},
                    {'text': '5/9', 'is_correct': False},
                ]
            },
            {
                'text': '8/12 - 5/12?',
                'choices': [
                    {'text': '3/12', 'is_correct': False},
                    {'text': '1/12', 'is_correct': False},
                    {'text': '1/4', 'is_correct': True},
                ]
            },
            {
                'text': '11/15 - 7/15?',
                'choices': [
                    {'text': '3/15', 'is_correct': False},
                    {'text': '4/15', 'is_correct': True},
                    {'text': '5/15', 'is_correct': False},
                ]
            },
            {
                'text': '3/7 - 2/7?',
                'choices': [
                    {'text': '1/7', 'is_correct': True},
                    {'text': '2/7', 'is_correct': False},
                    {'text': '3/7', 'is_correct': False},
                ]
            },
             {
                'text': '5/9 - 1/9?',
                'choices': [
                    {'text': '1/9', 'is_correct': False},
                    {'text': '2/9', 'is_correct': False},
                    {'text': '4/9', 'is_correct': True},
                ]
            },
            {
                'text': '10/11 - 6/11?',
                'choices': [
                    {'text': '2/11', 'is_correct': False},
                    {'text': '3/11', 'is_correct': False},
                    {'text': '4/11', 'is_correct': True},
                ]
            },
            {
                'text': '4/5 - 3/5?',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                ]
            },
            {
                'text': '13/20 - 8/20?',
                'choices': [
                    {'text': '5/20', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                    {'text': '1/4', 'is_correct': True},
                ]
            },
             {
                'text': '7/10 - 4/10?',
                'choices': [
                    {'text': '2/10', 'is_correct': False},
                    {'text': '3/10', 'is_correct': True},
                    {'text': '4/10', 'is_correct': False},
                ]
            },
            {
                'text': '14/21 - 9/21?',
                'choices': [
                    {'text': '5/21', 'is_correct': True},
                    {'text': '6/21', 'is_correct': False},
                    {'text': '7/21', 'is_correct': False},
                ]
            },
            {
                'text': '6/8 - 3/8?',
                'choices': [
                    {'text': '1/8', 'is_correct': False},
                    {'text': '2/8', 'is_correct': False},
                    {'text': '3/8', 'is_correct': True},
                ]
            },
            {
                'text': '9/14 - 5/14?',
                'choices': [
                    {'text': '1/7', 'is_correct': False},
                    {'text': '2/7', 'is_correct': True},
                    {'text': '3/7', 'is_correct': False},
                ]
            },
            {
                'text': '5/6 - 1/4?',
                'choices': [
                    {'text': '7/6', 'is_correct': False},
                    {'text': '4/12', 'is_correct': False},
                    {'text': '7/12', 'is_correct': True},
                ]
            },
            {
                'text': '7/8 - 2/5?',
                'choices': [
                    {'text': '5/40', 'is_correct': False},
                    {'text': '9/40', 'is_correct': False},
                    {'text': '19/40', 'is_correct': True},
                ]
            },
            {
                'text': '9/10 - 1/3?',
                'choices': [
                    {'text': '8/30', 'is_correct': False},
                    {'text': '17/30', 'is_correct': True},
                    {'text': '26/30', 'is_correct': False},
                ]
            },
            {
                'text': '4/9 - 1/5?',
                'choices': [
                    {'text': '11/15', 'is_correct': False},
                    {'text': '11/30', 'is_correct': False},
                    {'text': '11/45', 'is_correct': True},
                ]
            },
            {
                'text': '6/7 - 1/4?',
                'choices': [
                    {'text': '17/28', 'is_correct': True },
                    {'text': '18/28', 'is_correct': False},
                    {'text': '19/28', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for subtracting fractions.'))
