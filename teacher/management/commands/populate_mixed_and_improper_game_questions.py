from django.core.management.base import BaseCommand
from teacher.models import Game, GameQuestion, GameChoice

class Command(BaseCommand):
    help = 'Populate the database with sample game questions and choices for converting mixed fractions to improper fractions.'

    def handle(self, *args, **kwargs):
        # Fetch the game named "Mixed and Improper Fractions Game"
        game = Game.objects.filter(name="Mixed & Improper Fractions Game").first()

        if not game:
            self.stdout.write(self.style.ERROR('No game found with the name "Mixed and Improper Fractions Game". Please create the game first.'))
            return

        questions_data = [
            {
                'text': '22/7 to mixed fraction.',
                'choices': [
                    {'text': '1 1/7', 'is_correct': False},
                    {'text': '2 1/7', 'is_correct': False},
                    {'text': '4 1/7', 'is_correct': True},
                ]
            },
             {
                'text': '43/6 to mixed fraction.',
                'choices': [
                    {'text': '7 1/6', 'is_correct': True},
                    {'text': '7 2/6', 'is_correct': False},
                    {'text': '7 3/6', 'is_correct': False},
                ]
            },
            {
                'text': '30/8 to mixed fraction.',
                'choices': [
                    {'text': '3 2/8', 'is_correct': False},
                    {'text': '3 4/8', 'is_correct': False},
                    {'text': '3 6/8', 'is_correct': True},
                ]
            },
            {
                'text': '29/4 to mixed fraction.',
                'choices': [
                    {'text': '6 1/4', 'is_correct': False},
                    {'text': '7 1/4', 'is_correct': True},
                    {'text': '8 1/4', 'is_correct': False},
                ]
            },
            {
                'text': '54/7 to mixed fraction.',
                'choices': [
                    {'text': '7 1/7', 'is_correct': False},
                    {'text': '7 3/7', 'is_correct': False},
                    {'text': '7 5/7', 'is_correct': True},
                ]
            },
            {
                'text': '100/11 to mixed fraction.',
                'choices': [
                    {'text': '3 1/11', 'is_correct': False},
                    {'text': '5 1/11', 'is_correct': False},
                    {'text': '9 1/11', 'is_correct': True},
                ]
            },
            {
                'text': '71/12 to mixed fraction.',
                'choices': [
                    {'text': '5 11/12', 'is_correct': True},
                    {'text': '6 11/12', 'is_correct': False},
                    {'text': '7 11/12', 'is_correct': False},
                ]
            },
            {
                'text': '44/5 to mixed fraction.',
                'choices': [
                    {'text': '8 2/5', 'is_correct': False},
                    {'text': '8 4/5', 'is_correct': True},
                    {'text': '8 6/5', 'is_correct': False},
                ]
            },
            {
                'text': '27/4 to mixed fraction.',
                'choices': [
                    {'text': '6 1/4', 'is_correct': False},
                    {'text': '6 2/4', 'is_correct': False},
                    {'text': '6 3/4', 'is_correct': True},
                ]
            },
            {
                'text': '83/9 to mixed fraction.',
                'choices': [
                    {'text': '9 1/9', 'is_correct': False},
                    {'text': '9 2/9', 'is_correct': True},
                    {'text': '9 3/9', 'is_correct': False},
                ]
            },
            {
                'text': '48/7 to mixed fraction.',
                'choices': [
                    {'text': '6 2/7', 'is_correct': False},
                    {'text': '6 4/7', 'is_correct': False},
                    {'text': '6 6/7', 'is_correct': True},
                ]
            },
            {
                'text': '62/8 to mixed fraction.',
                'choices': [
                    {'text': '7 1/8', 'is_correct': False},
                    {'text': '7 3/8', 'is_correct': False},
                    {'text': '7 6/8', 'is_correct': True},
                ]
            },
            {
                'text': '29/5 to mixed fraction.',
                'choices': [
                    {'text': '5 4/5', 'is_correct': True},
                    {'text': '5 5/5', 'is_correct': False},
                    {'text': '5 6/5', 'is_correct': False},
                ]
            },
            {
                'text': '91/6 to mixed fraction.',
                'choices': [
                    {'text': '15 1/6', 'is_correct': True},
                    {'text': '15 2/6', 'is_correct': False},
                    {'text': '15 3/6', 'is_correct': False},
                ]
            },
            {
                'text': '35/4 to mixed fraction.',
                'choices': [
                    {'text': '8 2/4', 'is_correct': False},
                    {'text': '8 3/4', 'is_correct': True},
                    {'text': '8 4/4', 'is_correct': False},
                ]
            },
             {
                'text': '93/7 to mixed fraction.',
                'choices': [
                    {'text': '13 1/7', 'is_correct': False},
                    {'text': '13 2/7', 'is_correct': True},
                    {'text': '13 3/7', 'is_correct': False},
                ]
            },
              {
                'text': '59/9 to mixed fraction.',
                'choices': [
                    {'text': '6 2/9', 'is_correct': False},
                    {'text': '6 3/9', 'is_correct': False},
                    {'text': '6 5/9', 'is_correct': True},
                ]
            },
              {
                'text': '84/11 to mixed fraction.',
                'choices': [
                    {'text': '5 7/11', 'is_correct': False},
                    {'text': '6 7/11', 'is_correct': False},
                    {'text': '7 7/11', 'is_correct': True},
                ]
            },

             {
                'text': '38/5 to mixed fraction.',
                'choices': [
                    {'text': '7 2/5', 'is_correct': False},
                    {'text': '7 3/5', 'is_correct': True},
                    {'text': '7 4/5', 'is_correct': False},
                ]
            },
               {
                'text': '26/4 to mixed fraction.',
                'choices': [
                    {'text': '6 2/4', 'is_correct': True},
                    {'text': '6 3/4', 'is_correct': False},
                    {'text': '6 4/4', 'is_correct': False},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated game questions and choices for converting mixed fractions to improper fractions.'))
