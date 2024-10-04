from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices.'

    def handle(self, *args, **kwargs):
        game = Game.objects.first()  # Get the first game instance (make sure you have at least one game)

        if not game:
            self.stdout.write(self.style.ERROR('No game found. Please create a game first.'))
            return

        questions_data = [
    {
        'text': 'What is 1/2 + 1/4?',
        'choices': [
            {'text': '3/4', 'is_correct': True},
            {'text': '1/2', 'is_correct': False},
            {'text': '1/4', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/4 - 1/8?',
        'choices': [
            {'text': '5/8', 'is_correct': True},
            {'text': '1/2', 'is_correct': False},
            {'text': '1/4', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 2/3 + 1/6?',
        'choices': [
            {'text': '5/6', 'is_correct': False},
            {'text': '4/6', 'is_correct': True},
            {'text': '1/2', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 1/3 - 1/9?',
        'choices': [
            {'text': '2/9', 'is_correct': True},
            {'text': '1/6', 'is_correct': False},
            {'text': '1/3', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 1/4 divided by 2?',
        'choices': [
            {'text': '1/8', 'is_correct': True},
            {'text': '1/4', 'is_correct': False},
            {'text': '2', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/5 + 2/5?',
        'choices': [
            {'text': '1', 'is_correct': True},
            {'text': '1/5', 'is_correct': False},
            {'text': '3/10', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 5/6 - 1/2?',
        'choices': [
            {'text': '1/3', 'is_correct': True},
            {'text': '1/4', 'is_correct': False},
            {'text': '2/6', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 4/5 multiplied by 3/4?',
        'choices': [
            {'text': '3/5', 'is_correct': False},
            {'text': '12/20', 'is_correct': True},
            {'text': '7/10', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 2/7 + 3/7?',
        'choices': [
            {'text': '5/7', 'is_correct': True},
            {'text': '1', 'is_correct': False},
            {'text': '2/7', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 1 - 1/3?',
        'choices': [
            {'text': '2/3', 'is_correct': True},
            {'text': '1/2', 'is_correct': False},
            {'text': '1/4', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/4 divided by 3?',
        'choices': [
            {'text': '1/4', 'is_correct': True},
            {'text': '3/12', 'is_correct': False},
            {'text': '9/4', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 1/2 - 1/6?',
        'choices': [
            {'text': '1/3', 'is_correct': True},
            {'text': '1/4', 'is_correct': False},
            {'text': '1/6', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 2/5 + 3/10?',
        'choices': [
            {'text': '7/10', 'is_correct': True},
            {'text': '5/10', 'is_correct': False},
            {'text': '1/2', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/8 - 1/4?',
        'choices': [
            {'text': '1/2', 'is_correct': False},
            {'text': '1/8', 'is_correct': True},
            {'text': '1/3', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 7/10 + 1/5?',
        'choices': [
            {'text': '9/10', 'is_correct': False},
            {'text': '4/5', 'is_correct': True},
            {'text': '1/2', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 2/3 multiplied by 3/2?',
        'choices': [
            {'text': '1', 'is_correct': True},
            {'text': '1/3', 'is_correct': False},
            {'text': '4/6', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 5/12 - 1/4?',
        'choices': [
            {'text': '1/3', 'is_correct': True},
            {'text': '1/4', 'is_correct': False},
            {'text': '3/12', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/5 + 1/5?',
        'choices': [
            {'text': '4/5', 'is_correct': True},
            {'text': '5/5', 'is_correct': False},
            {'text': '2/5', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 1/2 multiplied by 1/3?',
        'choices': [
            {'text': '1/6', 'is_correct': True},
            {'text': '1/5', 'is_correct': False},
            {'text': '1/4', 'is_correct': False},
        ]
    },
    {
        'text': 'What is 3/4 + 1/8?',
        'choices': [
            {'text': '7/8', 'is_correct': True},
            {'text': '1', 'is_correct': False},
            {'text': '5/8', 'is_correct': False},
        ]
    },
]

# Insert these into the management command


        for question_data in questions_data:
            question = GameQuestion.objects.create(game=game, text=question_data['text'])
            for choice_data in question_data['choices']:
                GameChoice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices.'))
