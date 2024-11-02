from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for multiplying fractions.'

    def handle(self, *args, **kwargs):
        # Fetch the game named "Multiplying Fractions Game"
        game = Game.objects.filter(name="Multiplying Fractions Game").first()

        if not game:
            self.stdout.write(self.style.ERROR('No game found with the name "Multiplying Fractions Game". Please create the game first.'))
            return

        questions_data = [
            # 20 sample questions for multiplying fractions
            {
                'text': 'What is 1/2 × 1/4?',
                'choices': [
                    {'text': '1/8', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/40 × 35/12?',
                'choices': [
                    {'text': '21/4', 'is_correct': False},
                    {'text': '19/26', 'is_correct': False},
                    {'text': '7/32', 'is_correct': True},
                ]
            },
            {
                'text': 'What is 5/6 × 2/3?',
                'choices': [
                    {'text': '5/9', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/3 × 3/5?',
                'choices': [
                    {'text': '1/5', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '1/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 10/17 × 3/2?',
                'choices': [
                    {'text': '15/7', 'is_correct': True},
                    {'text': '7/15', 'is_correct': False},
                    {'text': '30/19', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/8 × 3/4?',
                'choices': [
                    {'text': '21/32', 'is_correct': True},
                    {'text': '7/12', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/2 × 1/3?',
                'choices': [
                    {'text': '1/6', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/10 × 1/5?',
                'choices': [
                    {'text': '1/10', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/4 × 8/30?',
                'choices': [
                    {'text': '1/3', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/5', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 9/12 × 1/4?',
                'choices': [
                    {'text': '3/16', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/7 × 2/3?',
                'choices': [
                    {'text': '2/7', 'is_correct': True},
                    {'text': '6/7', 'is_correct': False},
                    {'text': '3/6', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/5 × 4/5?',
                'choices': [
                    {'text': '4/25', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 1/2 × 3/8?',
                'choices': [
                    {'text': '3/16', 'is_correct': True},
                    {'text': '1/4', 'is_correct': False},
                    {'text': '1/8', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/20 × 4/20?',
                'choices': [
                    {'text': '7/20', 'is_correct': False},
                    {'text': '3/100', 'is_correct': True},
                    {'text': '1/200', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 4/9 × 2/3?',
                'choices': [
                    {'text': '8/27', 'is_correct': True},
                    {'text': '6/27', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 5/7 × 1/2?',
                'choices': [
                    {'text': '5/14', 'is_correct': True},
                    {'text': '7/14', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 6/8 × 3/4?',
                'choices': [
                    {'text': '9/16', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '3/8', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 7/12 × 2/3?',
                'choices': [
                    {'text': '7/18', 'is_correct': True},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 3/5 × 7/10?',
                'choices': [
                    {'text': '21/50', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/7', 'is_correct': False},
                ]
            },
            {
                'text': 'What is 2/3 × 5/9?',
                'choices': [
                    {'text': '10/27', 'is_correct': True},
                    {'text': '2/9', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for multiplying fractions.'))
