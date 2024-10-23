from django.test import TestCase
from django.contrib.auth.models import User
from .models import ReviewRating

class ReviewRatingTest(TestCase):

    def setUp(self):
        # Set up a user and a review for testing
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')

        self.review = ReviewRating.objects.create(
            review="Great car!",
            rating=5,
            reviewer=self.user1,
            reviewee=self.user2
        )

    def test_review_creation(self):
        # Test if the review was created correctly
        review = ReviewRating.objects.get(id=self.review.id)
        self.assertEqual(review.review, "Great car!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.reviewer, self.user1)
        self.assertEqual(review.reviewee, self.user2)

    def test_review_rating_range(self):
        # Test if rating is within the correct range
        self.assertGreaterEqual(self.review.rating, 1)
        self.assertLessEqual(self.review.rating, 5)

    def test_string_representation(self):
        # Optionally, you might want to test the string representation of the model
        self.assertEqual(str(self.review), "Great car!")
