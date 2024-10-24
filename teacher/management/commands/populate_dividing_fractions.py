from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for dividing fractions.'

    def handle(self, *args, **kwargs):
        # Get the 'Dividing Fractions Game' instance
        game = Game.objects.filter(name='Dividing Fractions Game').first()

        if not game:
            self.stdout.write(self.style.ERROR('No game found named "Dividing Fractions Game". Please create the game first.'))
            return

        questions_data = [
            # First 10 questions
            {
                'text': 'What is 1/2 ÷ 1/4?',
                'choices': [
                    {'text': '2', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/4 ÷ 1/2?',
                'choices': [
                    {'text': '3/2', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/6 ÷ 1/3?',
                'choices': [
                    {'text': '5/2', 'is_correct': True},
                    {'text': '5/9', 'is_correct': False},
                    {'text': '3/6', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/8 ÷ 1/2?',
                'choices': [
                    {'text': '7/4', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '14/8', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 9/10 ÷ 3/5?',
                'choices': [
                    {'text': '3/2', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 4/5 ÷ 2/3?',
                'choices': [
                    {'text': '6/5', 'is_correct': True},
                    {'text': '5/6', 'is_correct': False},
                    {'text': '2/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 8/9 ÷ 2/3?',
                'choices': [
                    {'text': '4/3', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '8/6', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/7 ÷ 3/5?',
                'choices': [
                    {'text': '5/7', 'is_correct': True},
                    {'text': '7/5', 'is_correct': False},
                    {'text': '1', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 6/8 ÷ 2/4?',
                'choices': [
                    {'text': '3', 'is_correct': True},
                    {'text': '4/3', 'is_correct': False},
                    {'text': '6/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/9 ÷ 1/3?',
                'choices': [
                    {'text': '7/3', 'is_correct': True},
                    {'text': '3/7', 'is_correct': False},
                    {'text': '9/7', 'is_correct': False},
                ]
            },
            # Additional 10 questions
            {
                'text': 'What is 5/8 ÷ 1/4?',
                'choices': [
                    {'text': '5/2', 'is_correct': True},
                    {'text': '5/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 10/11 ÷ 2/3?',
                'choices': [
                    {'text': '15/11', 'is_correct': True},
                    {'text': '5/11', 'is_correct': False},
                    {'text': '10/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 12/15 ÷ 4/5?',
                'choices': [
                    {'text': '1', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '5/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/5 ÷ 2/5?',
                'choices': [
                    {'text': '3/2', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '5/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 4/7 ÷ 1/2?',
                'choices': [
                    {'text': '8/7', 'is_correct': True},
                    {'text': '4/14', 'is_correct': False},
                    {'text': '1/7', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 2/9 ÷ 1/3?',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '3/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 9/16 ÷ 3/8?',
                'choices': [
                    {'text': '3/2', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/12 ÷ 5/6?',
                'choices': [
                    {'text': '7/10', 'is_correct': True},
                    {'text': '5/6', 'is_correct': False},
                    {'text': '10/7', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 2/3 ÷ 4/5?',
                'choices': [
                    {'text': '5/6', 'is_correct': True},
                    {'text': '6/5', 'is_correct': False},
                    {'text': '2/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/4 ÷ 3/8?',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '3/2', 'is_correct': False},
                    {'text': '4/3', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for dividing fractions.'))
