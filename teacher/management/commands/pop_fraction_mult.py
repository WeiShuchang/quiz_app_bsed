from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name
import math

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with simple multiplication questions for the Multiplying Fractions Game'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the game with the name "Multiplying Fractions Game"
            game = Game.objects.get(name="Multiplying Fractions Game")

            # Extended list of fraction pairs to multiply (20 in total)
            fraction_pairs = [
                ((1, 2), (1, 3)),    # 1/2 * 1/3 = 1/6
                ((3, 4), (2, 5)),    # 3/4 * 2/5 = 6/20 = 3/10
                ((7, 8), (3, 7)),    # 7/8 * 3/7 = 21/56 = 3/8
                ((5, 6), (4, 9)),    # 5/6 * 4/9 = 20/54 = 10/27
                ((2, 3), (3, 4)),    # 2/3 * 3/4 = 6/12 = 1/2
                ((5, 7), (3, 5)),    # 5/7 * 3/5 = 15/35 = 3/7
                ((4, 9), (2, 3)),    # 4/9 * 2/3 = 8/27
                ((7, 10), (5, 7)),   # 7/10 * 5/7 = 35/70 = 1/2
                ((9, 11), (3, 4)),   # 9/11 * 3/4 = 27/44
                ((6, 8), (2, 9)),    # 6/8 * 2/9 = 12/72 = 1/6
                ((8, 10), (5, 6)),   # 8/10 * 5/6 = 40/60 = 2/3
                ((9, 10), (7, 9)),   # 9/10 * 7/9 = 63/90 = 7/10
                ((4, 5), (3, 8)),    # 4/5 * 3/8 = 12/40 = 3/10
                ((7, 9), (2, 3)),    # 7/9 * 2/3 = 14/27
                ((5, 6), (6, 7)),    # 5/6 * 6/7 = 30/42 = 5/7
                ((3, 5), (4, 7)),    # 3/5 * 4/7 = 12/35
                ((9, 13), (5, 9)),   # 9/13 * 5/9 = 45/117 = 5/13
                ((2, 5), (7, 8)),    # 2/5 * 7/8 = 14/40 = 7/20
                ((7, 10), (3, 8)),   # 7/10 * 3/8 = 21/80
                ((11, 12), (3, 4))   # 11/12 * 3/4 = 33/48 = 11/16
            ]

            count = 0  # Initialize count of added questions
            for (numerator1, denominator1), (numerator2, denominator2) in fraction_pairs:
                # Calculate the product of the fractions
                product_numerator = numerator1 * numerator2
                product_denominator = denominator1 * denominator2

                # Simplify the result using the greatest common divisor (GCD)
                gcd = math.gcd(product_numerator, product_denominator)
                simplified_numerator = product_numerator // gcd
                simplified_denominator = product_denominator // gcd

                question_text = f"Multiply the fractions {numerator1}/{denominator1} and {numerator2}/{denominator2}."

                # Create a new FractionGameQuestion with the simplified numerator and denominator
                FractionGameQuestion.objects.create(
                    text=question_text,
                    game=game,
                    correct_numerator=simplified_numerator,
                    correct_denominator=simplified_denominator
                )

                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text} (Answer: {simplified_numerator}/{simplified_denominator})'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} FractionGameQuestions for the "Multiplying Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Multiplying Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
