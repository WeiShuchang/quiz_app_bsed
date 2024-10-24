from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for subtracting fractions.'

    def handle(self, *args, **kwargs):
        game = Game.objects.first()  # Get the first game instance (make sure you have at least one game)

        if not game:
            self.stdout.write(self.style.ERROR('No game found. Please create a game first.'))
            return

        questions_data = [
            # First 10 questions (already present)
            {
                'text': 'What is 1/2 - 1/4?',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/5 - 1/5?',
                'choices': [
                    {'text': '2/5', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/6 - 1/3?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/8 - 1/8?',
                'choices': [
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/8', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 2/4 - 1/4?',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/2 - 1/6?',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/8 - 3/8?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/8', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 4/5 - 2/5?',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/10 - 1/5?',
                'choices': [
                    {'text': '3/10', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 9/12 - 1/4?',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '5/12', 'is_correct': False},
                ]
            },
            # Additional 10 questions
            {
                'text': 'What is 3/4 - 1/2?',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/6 - 1/2?',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/8 - 1/4?',
                'choices': [
                    {'text': '5/8', 'is_correct': True},
                    {'text': '3/8', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 4/5 - 3/10?',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 2/3 - 1/6?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 8/10 - 2/5?',
                'choices': [
                    {'text': '2/5', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/7 - 2/7?',
                'choices': [
                    {'text': '3/7', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/5 - 1/10?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/10', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 6/8 - 1/4?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '3/8', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/12 - 1/6?',
                'choices': [
                    {'text': '1/4', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for subtracting fractions.'))
