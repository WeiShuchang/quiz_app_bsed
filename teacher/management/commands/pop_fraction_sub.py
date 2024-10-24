from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with simple subtraction questions for the Subtracting Fractions Game'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the game with the name "Subtracting Fractions Game"
            game = Game.objects.get(name="Subtracting Fractions Game")

            # Predefined list of simple fraction pairs to subtract, excluding answers that simplify to 0
            fraction_pairs = [
                ((9, 12), (2, 12)), # 9/12 - 2/12 = 7/12
                ((5, 9), (1, 9)),   # 5/9 - 1/9 = 4/9
                ((7, 8), (2, 8)),   # 7/8 - 2/8 = 5/8
                ((11, 12), (3, 12)),# 11/12 - 3/12 = 8/12 = 2/3
                ((4, 7), (1, 7))    # 4/7 - 1/7 = 3/7
            ]

            count = 0  # Initialize count of added questions
            for (numerator1, denominator1), (numerator2, denominator2) in fraction_pairs:
                # Calculate the difference of the fractions
                common_denominator = denominator1 * denominator2
                diff_numerator = (numerator1 * denominator2) - (numerator2 * denominator1)

                # Simplify the result if necessary
                if diff_numerator % common_denominator == 0:
                    simplified_numerator = diff_numerator // common_denominator
                    simplified_denominator = 1
                else:
                    simplified_numerator = diff_numerator
                    simplified_denominator = common_denominator

                question_text = f"Subtract the fractions {numerator1}/{denominator1} and {numerator2}/{denominator2}."

                # Create a new FractionGameQuestion with the correct numerator and denominator
                FractionGameQuestion.objects.create(
                    text=question_text,
                    game=game,
                    correct_numerator=simplified_numerator,
                    correct_denominator=simplified_denominator
                )

                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text} (Answer: {simplified_numerator}/{simplified_denominator})'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} FractionGameQuestions for the "Subtracting Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Subtracting Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
