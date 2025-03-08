from django.test import TestCase
from django.urls import reverse

class ProductEvaluationAPITest(TestCase):
    
    def test_product_evaluation(self):
        # Assuming your API endpoint is '/api/evaluate_product/'
        url = reverse('evaluate_product')  # Adjust to your URL pattern name
        data = {
            "order_id": 123,
            "image": "image_path_or_file",  # Add a valid file if needed, or mock the image.
            "text": "Product was damaged.",
        }
        
        response = self.client.post(url, data, format='json')  # Make a POST request
        
        self.assertEqual(response.status_code, 200)  # Check if the status code is 200 (OK)
        self.assertIn('classification', response.json())  # Check if 'classification' is in the response