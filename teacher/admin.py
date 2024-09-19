from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizAttempt, Class
from .models import UserProfile  # Import UserProfile for permission check

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')  # Display the code in the list view
    readonly_fields = ('code',)  # Make the code field read-only

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new objects
            if not UserProfile.objects.filter(user=request.user, role='teacher').exists():
                raise PermissionError("Only teachers can create classes.")
        super(ClassAdmin, self).save_model(request, obj, form, change)

# Dictionary of models and their respective admin classes
model_admins = {
    Category: admin.ModelAdmin,
    Quiz: admin.ModelAdmin,
    Question: admin.ModelAdmin,
    Choice: admin.ModelAdmin,
    QuizAttempt: admin.ModelAdmin,
    Class: ClassAdmin,
}

# Register each model with its corresponding admin class
for model, admin_class in model_admins.items():
    admin.site.register(model, admin_class)
