from django.core.management.base import BaseCommand
from teacher.models import FractionGameQuestion, Game  # Adjust 'teacher' to your app's name

class Command(BaseCommand):
    help = 'Populate FractionGameQuestion with 20 predefined simplifiable questions for the Simplifying Fractions Game'

    def handle(self, *args, **kwargs):
        # Get the specific game instance you want to associate the questions with
        try:
            # Fetch the game with the name "Simplifying Fractions Game"
            game = Game.objects.get(name="Simplifying Fractions Game")
            
            # Predefined list of simplifiable fractions
            fractions = [
                (2, 4),   # Simplifies to 1/2
                (3, 6),   # Simplifies to 1/2
                (4, 8),   # Simplifies to 1/2
                (10, 20), # Simplifies to 1/2
                (12, 16), # Simplifies to 3/4
                (6, 9),   # Simplifies to 2/3
                (15, 25), # Simplifies to 3/5
                (18, 24), # Simplifies to 3/4
                (8, 12),  # Simplifies to 2/3
                (9, 27),  # Simplifies to 1/3
                (10, 15), # Simplifies to 2/3
                (14, 21), # Simplifies to 2/3
                (16, 24), # Simplifies to 2/3
                (4, 10),  # Simplifies to 2/5
                (2, 6),   # Simplifies to 1/3
                (8, 32),  # Simplifies to 1/4
                (12, 36), # Simplifies to 1/3
                (9, 18),  # Simplifies to 1/2
                (6, 18),  # Simplifies to 1/3
                (8, 20),  # Simplifies to 2/5
                (10, 30)  # Simplifies to 1/3
            ]

            count = 0  # Initialize count of added questions
            for numerator, denominator in fractions:
                question_text = f"Simplify the fraction {numerator}/{denominator}."
                FractionGameQuestion.objects.create(
                    numerator=numerator,
                    denominator=denominator,
                    text=question_text,  # Assuming there is a 'text' field in your GameQuestion
                    game=game  # Associate with the "Simplifying Fractions Game"
                )
                self.stdout.write(self.style.SUCCESS(f'Added question: {question_text}'))
                count += 1  # Increment count of added questions

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} simplifiable FractionGameQuestions for the "Simplifying Fractions Game".'))
        except Game.DoesNotExist:
            self.stdout.write(self.style.ERROR('Game "Simplifying Fractions Game" not found. Please create the game first.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
