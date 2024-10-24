from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with simple addition questions for the Adding Fractions Game'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the game with the name "Adding Fractions Game"
            game = Game.objects.get(name="Adding Fractions Game")

            # Predefined list of simple fraction pairs to add, excluding answers that simplify to 1
            fraction_pairs = [
                ((1, 2), (1, 4)),  # 1/2 + 1/4 = 3/4
                ((1, 3), (1, 6)),  # 1/3 + 1/6 = 1/2
                ((1, 5), (2, 5)),  # 1/5 + 2/5 = 3/5
                ((2, 3), (1, 6)),  # 2/3 + 1/6 = 5/6
                ((1, 7), (2, 7)),  # 1/7 + 2/7 = 3/7
                ((3, 8), (1, 8)),  # 3/8 + 1/8 = 1/2
                ((2, 5), (1, 10)), # 2/5 + 1/10 = 1/2
                ((1, 6), (2, 6)),  # 1/6 + 2/6 = 1/2
                ((3, 9), (2, 9)),  # 3/9 + 2/9 = 5/9
                ((5, 8), (1, 8)),  # 5/8 + 1/8 = 3/4
                ((1, 10), (3, 10)),# 1/10 + 3/10 = 4/10 = 2/5
                ((2, 7), (3, 7)),  # 2/7 + 3/7 = 5/7
                ((1, 2), (1, 6)),  # 1/2 + 1/6 = 2/3
                ((3, 10), (2, 10)),# 3/10 + 2/10 = 5/10 = 1/2
                ((1, 4), (2, 8)),  # 1/4 + 2/8 = 1/2
                ((2, 9), (4, 9)),  # 2/9 + 4/9 = 6/9 = 2/3
                ((1, 5), (3, 10)), # 1/5 + 3/10 = 1/2
                ((2, 6), (1, 3)),  # 2/6 + 1/3 = 1/2
                ((3, 7), (2, 7)),  # 3/7 + 2/7 = 5/7
                ((2, 8), (3, 8))   # 2/8 + 3/8 = 5/8
            ]

            count = 0  # Initialize count of added questions
            for (numerator1, denominator1), (numerator2, denominator2) in fraction_pairs:
                # Calculate the sum of the fractions without complicated simplification
                common_denominator = denominator1 * denominator2
                sum_numerator = (numerator1 * denominator2) + (numerator2 * denominator1)

                # Simplify the result if necessary, but keep it simple
                if sum_numerator % common_denominator == 0:
                    simplified_numerator = sum_numerator // common_denominator
                    simplified_denominator = 1
                else:
                    simplified_numerator = sum_numerator
                    simplified_denominator = common_denominator

                question_text = f"Add the fractions {numerator1}/{denominator1} and {numerator2}/{denominator2}."

                # Create a new FractionGameQuestion with correct numerator and denominator
                FractionGameQuestion.objects.create(
                    text=question_text,
                    game=game,
                    correct_numerator=simplified_numerator,
                    correct_denominator=simplified_denominator
                )

                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text} (Answer: {simplified_numerator}/{simplified_denominator})'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} FractionGameQuestions for the "Adding Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Adding Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
