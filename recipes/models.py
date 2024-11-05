from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta


class Recipe(models.Model):
    DIFFICULTY_CHOICES=[('easy','Easy'),
                    ('moderate','Moderate'),
                    ('difficult','Difficult')
                    ]
    
    FOOD_TYPE_CHOICE=[('veg','Vegetarian'),
                      ('vegan','Vegan'),
                      ('non_veg','Non_Vegetarian'),
                      ]
    
    CUISINE_CHOICES = [('italian', 'Italian'),
                       ('indian', 'Indian'),
                       ('mexican', 'Mexican'),
                       ('chinese', 'Chinese'),
                       ('japanese', 'Japanese'),
                       ]
    
    title=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='recipes')
    cuisine=models.CharField(max_length=20,choices=CUISINE_CHOICES)
    food_type=models.CharField(max_length=20,choices=FOOD_TYPE_CHOICE)
    difficulty_level=models.CharField(max_length=10,choices=DIFFICULTY_CHOICES)
    instructions=models.TextField()
    servings=models.PositiveIntegerField(help_text="Number of servings")
    preparation_time=models.DurationField(help_text="Preparation time in hours, minutes, and seconds (hh:mm:ss)")
    total_time=models.DurationField(help_text="Total cooking time in hours, minutes, and seconds (hh:mm:ss)")
    calories=models.PositiveIntegerField(help_text="Total calories in kcal")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    featured=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.preparation_time is None or self.total_time is None:
            raise ValidationError("Preparation time and total time must be set.")
        
        if self.preparation_time < timedelta(seconds=0) or self.total_time < timedelta(seconds=0):
            raise ValidationError("Preparation time and total time must be greater than zero.")
        
        if self.total_time < self.preparation_time:
            raise ValidationError("Total time cannot be less than preparation time.")
    
    
class Collection(models.Model):
    title=models.CharField(max_length=200)
    recipes=models.ManyToManyField(Recipe,related_name='collection')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='collection')
    
    def __str__(self):
        return self.title
    
    
class Ingredient(models.Model):
    UNIT_CHOICES=[('gms','Grams'),
              ('numbers','Numbers'),
              ('teaspoon','Teaspoon'),
              ('tablespoon','Tablespoon'),
              ('litres','Litres')
              ]
    
    name=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField()
    unit=models.CharField(max_length=20,choices=UNIT_CHOICES)
    is_optional=models.BooleanField(default=False)
    recipe=models.ForeignKey(Recipe,related_name='ingredients',on_delete=models.CASCADE)
    
    def clean(self):
        if self.quantity<=0:
            raise ValidationError('Quantity must be greater than Zero')
    
    def __str__(self):
        return f'{self.quantity} {self.get_unit_display()} {self.name}'
    

class Image(models.Model):
    image=models.ImageField(upload_to='images/')
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='images')
    
    def __str__(self):
        return f"{self.recipe.title}-Image"