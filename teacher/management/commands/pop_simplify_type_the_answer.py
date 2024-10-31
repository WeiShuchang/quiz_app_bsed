from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with simplifying fractions questions for the Simplifying Fractions Game'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the game with the name "Simplifying Fractions Game"
            game = Game.objects.get(name="Simplifying Fractions Game")

            # List of fractions to simplify along with their simplified answers
            fractions_with_answers = [
                (12, 16, 3, 4),  # 12/16 simplifies to 3/4
                (18, 24, 3, 4),  # 18/24 simplifies to 3/4
                (7, 21, 1, 3),   # 7/21 simplifies to 1/3
                (45, 75, 3, 5),  # 45/75 simplifies to 3/5
                (14, 18, 7, 9),  # 14/18 simplifies to 7/9
                (16, 24, 2, 3),  # 16/24 simplifies to 2/3
                (36, 54, 2, 3),  # 36/54 simplifies to 2/3
                (30, 45, 2, 3),  # 30/45 simplifies to 2/3
                (13, 39, 1, 3),  # 13/39 simplifies to 1/3
                (14, 49, 2, 7),  # 14/49 simplifies to 2/7
                (17, 34, 1, 2),  # 17/34 simplifies to 1/2
                (35, 50, 7, 10), # 35/50 simplifies to 7/10
                (77, 99, 7, 9),  # 77/99 simplifies to 7/9
                (40, 56, 5, 7),  # 40/56 simplifies to 5/7
                (27, 36, 3, 4),  # 27/36 simplifies to 3/4
                (22, 66, 2, 3),  # 22/66 simplifies to 2/3
                (15, 75, 1, 5),  # 15/75 simplifies to 1/5
                (24, 72, 1, 3),  # 24/72 simplifies to 1/3
                (30, 54, 5, 9),  # 30/54 simplifies to 5/9
                (9, 15, 3, 5)    # 9/15 simplifies to 3/5
            ]

            count = 0  # Initialize count of added questions
            for numerator, denominator, simplified_numerator, simplified_denominator in fractions_with_answers:
                question_text = f"Simplify {numerator}/{denominator}."

                # Create a new FractionGameQuestion with the simplified numerator and denominator
                FractionGameQuestion.objects.create(
                    text=question_text,
                    game=game,
                    correct_numerator=simplified_numerator,
                    correct_denominator=simplified_denominator
                )

                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text} (Answer: {simplified_numerator}/{simplified_denominator})'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} FractionGameQuestions for the "Simplifying Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Simplifying Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
