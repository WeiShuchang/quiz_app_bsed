from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with questions for converting mixed fractions to improper fractions'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the game with the name "Mixed to Improper Fractions Game"
            game = Game.objects.get(name="Mixed & Improper Fractions Game")

            # List of mixed fractions to convert to improper fractions
            mixed_fractions = [
                (1, 2, 3),  # 1 2/3 = (1*3 + 2)/3 = 5/3
                (2, 3, 4),  # 2 3/4 = (2*4 + 3)/4 = 11/4
                (3, 1, 2),  # 3 1/2 = (3*2 + 1)/2 = 7/2
                (4, 2, 5),  # 4 2/5 = (4*5 + 2)/5 = 22/5
                (5, 3, 4),  # 5 3/4 = (5*4 + 3)/4 = 23/4
                (1, 4, 7),  # 1 4/7 = (1*7 + 4)/7 = 11/7
                (6, 5, 6),  # 6 5/6 = (6*6 + 5)/6 = 41/6
                (4, 7, 9),  # 0 3/8 = (0*8 + 3)/8 = 3/8
                (2, 5, 9),  # 2 5/9 = (2*9 + 5)/9 = 23/9
                (3, 4, 10), # 3 4/10 = (3*10 + 4)/10 = 34/10
                (2, 3, 5),  # 5 0/1 = (5*1 + 0)/1 = 5/1
                (1, 1, 5),  # 1 1/5 = (1*5 + 1)/5 = 6/5
                (2, 4, 6),  # 2 4/6 = (2*6 + 4)/6 = 16/6
                (4, 1, 3),  # 4 1/3 = (4*3 + 1)/3 = 13/3
                (7, 2, 4),  # 7 2/4 = (7*4 + 2)/4 = 30/4
                (8, 3, 8),  # 8 3/8 = (8*8 + 3)/8 = 67/8
                (2, 11, 12),  # 0 5/2 = (0*2 + 5)/2 = 5/2
                (1, 6, 10), # 1 6/10 = (1*10 + 6)/10 = 16/10
                (3, 3, 7),  # 3 3/7 = (3*7 + 3)/7 = 24/7
                (5, 2, 5),  # 5 2/5 = (5*5 + 2)/5 = 27/5
             
            ]

            count = 0  # Initialize count of added questions
            for whole, numerator, denominator in mixed_fractions:
                # Calculate the improper fraction
                improper_numerator = whole * denominator + numerator

                question_text = f"Convert  {whole} {numerator}/{denominator} to an improper fraction."

                # Create a new FractionGameQuestion with the improper fraction
                FractionGameQuestion.objects.create(
                    text=question_text,
                    game=game,
                    correct_numerator=improper_numerator,
                    correct_denominator=denominator
                )

                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text} (Answer: {improper_numerator}/{denominator})'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} FractionGameQuestions for the "Mixed to Improper Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Mixed to Improper Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
