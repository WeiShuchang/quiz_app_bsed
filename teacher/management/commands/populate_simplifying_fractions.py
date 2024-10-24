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
            # First 10 questions
            {
                'text': 'Simplify 4/8',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/8', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 6/9',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '3/9', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 10/20',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/5', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 9/12',
                'choices': [
                    {'text': '3/4', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 15/45',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 8/16',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '3/8', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 12/24',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 14/28',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '3/5', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 20/30',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 5/25',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            # Additional 10 questions
            {
                'text': 'Simplify 3/12',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 7/14',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 6/18',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/6', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 18/36',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 10/50',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 25/50',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 9/18',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 16/64',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 12/16',
                'choices': [
                    {'text': '3/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'Simplify 8/24',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
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
