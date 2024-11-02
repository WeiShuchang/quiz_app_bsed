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
          
            {
                'text': '1/2 ÷ 1/3?',
                'choices': [
                    {'text': '1/6', 'is_correct': False},
                    {'text': '3/2', 'is_correct': True},
                    {'text': '2/3', 'is_correct': False},
                ]
            },
             {
                'text': '1/4 ÷ 1/5?',
                'choices': [
                    {'text': '1/20', 'is_correct': False},
                    {'text': '4/5', 'is_correct': False},
                    {'text': '5/4', 'is_correct': True},
                ]
            },
            {
                'text': '1/6 ÷ 1/7?',
                'choices': [
                    {'text': '1/42', 'is_correct': False},
                    {'text': '7/6', 'is_correct': True},
                    {'text': '6/7', 'is_correct': False},
                ]
            },
             {
                'text': '1/9 ÷ 1/10?',
                'choices': [
                    {'text': '1/19', 'is_correct': False},
                    {'text': '9/10', 'is_correct': False},
                    {'text': '10/9', 'is_correct': True},
                ]
            },
            {
                'text': '2/4 ÷ 2/5?',
                'choices': [
                    {'text': '5/4', 'is_correct': True},
                    {'text': '4/5', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                ]
            },
             {
                'text': '2/6 ÷ 2/7?',
                'choices': [
                    {'text': '7/6', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '6/7', 'is_correct': False},
                ]
            },
             {
                'text': '2/8 ÷ 2/9?',
                'choices': [
                    {'text': '1/18', 'is_correct': False},
                    {'text': '9/8', 'is_correct': True},
                    {'text': '4/9', 'is_correct': False},
                ]
            },
             {
                'text': '3/4 ÷ 3/5?',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '5/4', 'is_correct': True},
                    {'text': '9/20', 'is_correct': False},
                ]
            },
             {
                'text': '3/7 ÷ 3/8?',
                'choices': [
                    {'text': '8/7', 'is_correct': True},
                    {'text': '24/21', 'is_correct': False},
                    {'text': '7/8', 'is_correct': False},
                ]
            },
             {
                'text': '4/5 ÷ 4/6?',
                'choices': [
                    {'text': '6/5', 'is_correct': True},
                    {'text': '12/10', 'is_correct': False},
                    {'text': '5/6', 'is_correct': False},
                ]
            },
            {
                'text': '4/9 ÷ 4/10?',
                'choices': [
                    {'text': '5/4', 'is_correct': False},
                    {'text': '10/9', 'is_correct': True},
                    {'text': '5/6', 'is_correct': False},
                ]
            },
             {
                'text': '5/8 ÷ 5/9?',
                'choices': [
                    {'text': '9/8', 'is_correct': True},
                    {'text': '8/9', 'is_correct': False},
                    {'text': '1/9', 'is_correct': False},
                ]
            },
            {
                'text': '6/7 ÷ 6/8?',
                'choices': [
                    {'text': '4/5', 'is_correct': False},
                    {'text': '8/7', 'is_correct': True},
                    {'text': '7/8', 'is_correct': False},
                ]
            },
            {
                'text': '7/8 ÷ 7/9?',
                'choices': [
                    {'text': '9/8', 'is_correct': True},
                    {'text': '7/9', 'is_correct': False},
                    {'text': '8/9', 'is_correct': False},
                ]
            },
              {
                'text': '8/9 ÷ 8/10?',
                'choices': [
                    {'text': '10/9', 'is_correct': True},
                    {'text': '8/10', 'is_correct': False},
                    {'text': '9/8', 'is_correct': False},
                ]
            },
             {
                'text': '10/14 ÷ 10/15?',
                'choices': [
                    {'text': '10/15', 'is_correct': False},
                    {'text': '15/14', 'is_correct': True},
                    {'text': '10/14', 'is_correct': False},
                ]
            },
            {
                'text': '10/16 ÷ 8/7?',
                'choices': [
                    {'text': '35/64', 'is_correct': True},
                    {'text': '8/5', 'is_correct': False},
                    {'text': '7/8', 'is_correct': False},
                ]
            },
              {
                'text': '10/3 ÷ 12/26?',
                'choices': [
                    {'text': '10/39', 'is_correct': False},
                    {'text': '13/6', 'is_correct': False},
                    {'text': '65/36', 'is_correct': True},
                ]
            },
               {
                'text': '1/2 ÷ 11/27?',
                'choices': [
                    {'text': '27/11', 'is_correct': False},
                    {'text': '12/11', 'is_correct': False},
                    {'text': '27/22', 'is_correct': True},
                ]
            },
              {
                'text': '2/4 ÷ 2/3?',
                'choices': [
                    {'text': '23/24', 'is_correct': False},
                    {'text': '3/4', 'is_correct': True},
                    {'text': '34/25', 'is_correct': False},
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
