from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Recipe

class RecipeDetailViewTests(APITestCase):
    def setUp(self):
        # Create two users: Adam and Brian
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        
        # Create two recipes: one for Adam, one for Brian
        Recipe.objects.create(
            owner=adam, 
            title='Recipe 1',
            short_description='Recipe by Adam',
            ingredients='Ingredient1, Ingredient2',
            steps='Step1, Step2'
        )
        Recipe.objects.create(
            owner=brian, 
            title='Recipe 2',
            short_description='Recipe by Brian',
            ingredients='Ingredient3, Ingredient4',
            steps='Step3, Step4'
        )

    def test_can_retrieve_recipe_using_valid_id(self):
        # Test retrieving a recipe with a valid ID (Adam's recipe)
        response = self.client.get('/api/recipes/1/')
        self.assertEqual(response.data['title'], 'Recipe 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_recipe_using_invalid_id(self):
        # Test retrieving a recipe with an invalid ID
        response = self.client.get('/api/recipes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_recipe(self):
        # Adam tries to update his own recipe
        self.client.login(username='adam', password='pass')
        response = self.client.put('/api/recipes/1/', {
            'title': 'Updated Recipe Title',
            'short_description': 'Updated description',
            'ingredients': 'Updated Ingredient1, Updated Ingredient2',
            'steps': 'Updated Step1, Updated Step2'
        })
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.title, 'Updated Recipe Title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_recipe(self):
        # Adam tries to update Brian's recipe (should be forbidden)
        self.client.login(username='adam', password='pass')
        response = self.client.put('/api/recipes/2/', {
            'title': 'Unauthorized Update',
            'short_description': 'Should not update',
            'ingredients': 'Should not update',
            'steps': 'Should not update'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
