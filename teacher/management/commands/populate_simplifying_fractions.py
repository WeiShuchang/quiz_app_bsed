from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for simplifying fractions.'

    def handle(self, *args, **kwargs):
        # Get the 'Simplifying Fractions Game' instance
        game = Game.objects.filter(name='Simplifying Fractions Game').first()

        if not game:
            self.stdout.write(self.style.ERROR('No game found named "Simplifying Fractions Game". Please create the game first.'))
            return

        questions_data = [
            {
                'text': 'Simplify 12/16',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '3/4', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 18/24',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '5/6', 'is_correct': False},
                    {'text': '3/1', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 21/28',
                'choices': [
                    {'text': '5/7', 'is_correct':  False},
                    {'text': '3/4', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 45/60',
                'choices': [
                    {'text': '3/4', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '5/8', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 14/18',
                'choices': [
                    {'text': '7/9', 'is_correct': True},
                    {'text': '5/7', 'is_correct': False},
                    {'text': '7/8', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 16/24',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '2/3', 'is_correct': True},
                ]
            },
            {
                'text': 'Simplify 24/36',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '2/3', 'is_correct': True},
                    {'text': '4/9', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 30/45',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '3/5', 'is_correct': False},
                    {'text': '4/7', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 10/25',
                'choices': [
                    {'text': '3/5', 'is_correct': False},
                    {'text': '2/5', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 8/12',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '2/3', 'is_correct': True},
                ]
            },
            {
                'text': 'Simplify 24/30',
                'choices': [
                    {'text': '2/3', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                    {'text': '4/5', 'is_correct': True},
                ]
            },
            {
                'text': 'Simplify 35/50',
                'choices': [
                    {'text': '2/5', 'is_correct': False},
                    {'text': '5/7', 'is_correct': False},
                    {'text': '7/10', 'is_correct': True},
                ]
            },
          
            {
                'text': 'Simplify 40/56',
                'choices': [
                    {'text': '4/7', 'is_correct': True},
                    {'text': '5/7', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 27/36',
                'choices': [
                    {'text': '3/4', 'is_correct': True},
                    {'text': '4/9', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 22/44',
                'choices': [
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': True},
                ]
            },
            {
                'text': 'Simplify 50/75',
                'choices': [
                    {'text': '5/6', 'is_correct': False},
                    {'text': '2/3', 'is_correct': True},
                    {'text': '4/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 28/32',
                'choices': [
                    {'text': '2/3', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '7/8', 'is_correct': True},
                ]
            },
            {
                'text': 'Simplify 90/98',
                'choices': [
                    {'text': '20/33', 'is_correct': False},
                    {'text': '45/49', 'is_correct': True},
                    {'text': '25/34', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 30/42',
                'choices': [
                    {'text': '5/7', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '5/6', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 9/15',
                'choices': [
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '3/5', 'is_correct': True},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for simplifying fractions.'))
