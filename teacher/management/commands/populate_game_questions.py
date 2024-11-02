from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for adding fractions.'

    def handle(self, *args, **kwargs):
        game = Game.objects.first()  # Get the first game instance (make sure you have at least one game)

        if not game:
            self.stdout.write(self.style.ERROR('No game found. Please create a game first.'))
            return

        questions_data = [
            # First 10 questions (already present)
            {
                'text': '1/3 + 3/6?',
                'choices': [
                    {'text': '4/3', 'is_correct': False},
                    {'text': '4/6', 'is_correct': False},
                    {'text': '5/6', 'is_correct': True},
                ]
            },
            {
                'text': '1/4 + 4/12?',
                'choices': [
                    {'text': '7/4', 'is_correct': False},
                    {'text': '5/8', 'is_correct': False},
                    {'text': '7/12', 'is_correct': True},
                ]
            },
             {
                'text': '1/5 + 4/15?',
                'choices': [
                    {'text': '5/10', 'is_correct': False},
                    {'text': '7/15', 'is_correct': True},
                    {'text': '5/20', 'is_correct': False},
                ]
            },
             {
                'text': '1/2 + 3/8?',
                'choices': [
                    {'text': '4/2', 'is_correct': False},
                    {'text': '7/4', 'is_correct': False},
                    {'text': '7/8', 'is_correct': True},
                ]
            },
            {
                'text': '2/7 + 5/14?',
                'choices': [
                    {'text': '9/14', 'is_correct': True},
                    {'text': '10/14', 'is_correct': False},
                    {'text': '11/14', 'is_correct': False},
                ]
            },
              {
                'text': '3/5 + 5/20?',
                'choices': [
                    {'text': '8/10', 'is_correct': False},
                    {'text': '8/15', 'is_correct': False},
                    {'text': '17/20', 'is_correct': True},
                ]
            },
            {
                'text': '3/16 + 1/8?',
                'choices': [
                    {'text': '4/8', 'is_correct': False},
                    {'text': '5/16', 'is_correct': True},
                    {'text': '6/24', 'is_correct': False},
                ]
            },
                {
                'text': '3/25 + 5/25?',
                'choices': [
                    {'text': '5/25', 'is_correct': False},
                    {'text': '6/25', 'is_correct': False},
                    {'text': '8/25', 'is_correct': True},
                ]
            },
            {
                'text': '4/30 + 3/10?',
                'choices': [
                    {'text': '13/30', 'is_correct': True},
                    {'text': '7/40', 'is_correct': False},
                    {'text': '8/50', 'is_correct': False},
                ]
            },
            {
                'text': '6/28 + 3/4?',
                'choices': [
                    {'text': '9/4', 'is_correct': False},
                    {'text': '18/16', 'is_correct': False},
                    {'text': '27/28', 'is_correct': True},
                ]
            },
            {
                'text': '2/5 + 8/25?',
                'choices': [
                    {'text': '10/25', 'is_correct': False},
                    {'text': '18/25', 'is_correct': True},
                    {'text': '26/25', 'is_correct': False},
                ]
            },
            {
                'text': '1/4 + 5/16?',
                'choices': [
                    {'text': '9/16', 'is_correct': True},
                    {'text': '10/16', 'is_correct': False},
                    {'text': '11/16', 'is_correct': False},
                ]
            },
            {
                'text': '1/9 + 3/18?',
                'choices': [
                    {'text': '5/9', 'is_correct': False},
                    {'text': '4/18', 'is_correct': False},
                    {'text': '5/18', 'is_correct': True},
                ]
            },
            {
                'text': '1/18 + 2/3?',
                'choices': [
                    {'text': '3/18', 'is_correct': False},
                    {'text': '8/18', 'is_correct': False},
                    {'text': '13/18', 'is_correct': True},
                ]
            },
            {
                'text': '8/21 + 3/7?',
                'choices': [
                    {'text': '11/7', 'is_correct': False},
                    {'text': '17/21', 'is_correct': True},
                    {'text': '23/35', 'is_correct': False},
                ]
            },
            {
                'text': '7/36 + 4/9?',
                'choices': [
                    {'text': '23/36', 'is_correct': True},
                    {'text': '28/36', 'is_correct': False},
                    {'text': '33/36', 'is_correct': False},
                ]
            },
            {
                'text': '12/35 + 4/7?',
                'choices': [
                    {'text': '16/7', 'is_correct': False},
                    {'text': '32/35', 'is_correct': True},
                    {'text': '48/42', 'is_correct': False},
                ]
            },
            {
                'text': '7/24 + 2/3?',
                'choices': [
                    {'text': '9/18', 'is_correct': False},
                    {'text': '16/21', 'is_correct': False},
                    {'text': '23/24', 'is_correct': True},
                ]
            },
            {
                'text': '2/9 + 5/9?',
                'choices': [
                    {'text': '4/9', 'is_correct': True},
                    {'text': '5/9', 'is_correct': False},
                    {'text': '6/9', 'is_correct': False},
                ]
            },
            {
                'text': '11/20 + 6/20?',
                'choices': [
                    {'text': '17/20', 'is_correct': True},
                    {'text': '18/20', 'is_correct': False},
                    {'text': '19/20', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for adding fractions.'))
