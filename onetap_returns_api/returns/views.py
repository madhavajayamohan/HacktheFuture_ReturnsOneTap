from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import OrderHistory, Products, Customer, ReturnRequest
from .serializers import ProductSerializer, OrderHistorySerializer, ProductEvaluationSerializer, ReturnSerializer
import google.generativeai as genai
from google.cloud import vision
from django.conf import settings

class CustomerOrderHistoryViewSet(viewsets.ViewSet):
    def list(self, request, customer_id=None):
        try:
            customer = Customer.objects.get(cust_id=customer_id)
            order_history = OrderHistory.objects.filter(cust_id=customer)
            serializer = OrderHistorySerializer(order_history, many = True)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

class ProductEvaluationViewSet(viewsets.ViewSet):
    def gemini_evaluate(self, name, category, company, date, price, image_desc, reason):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        prompt = "You are a Product Returns Specialist for an eCommerce company. Your task is to classify a product submitted for return using the following criteria: Product Name, Product Category, Company Name, Purchase Date, Price Sold At, an Analysis of an Image of the Product with Google Cloud Vision, Customer's Written Reason for Return. Based on this information, you must classify the product into one of these six conditions: \n"
        prompt += "Unused: The product has not been used at all. It is in its original condition. \n"
        prompt += "Lightly Used: The product has been used, but it is in good enough condition to be resold at full price. \n"
        prompt += "Moderately Used: The product has signs of usage and may require minor repairs or maintenance to be resold. \n"
        prompt += "Heavily Used: The product shows significant signs of usage, and can only be resold at a deep discount or donated. \n"
        prompt += "Damaged by User: The product has visible damage caused by the user due to improper or excessive use. \n"
        prompt += "Manufacturing Defect: The product is faulty due to a manufacturing error and does not work as intended. \n \n"

        prompt += "After classifying the product, you should also suggest the amount of money to refund to the user, based on the condition of the product. A Full Refund should only be given if the product is classified as Unused, Lightly Used, or Manufacturing Defect. \n"

        prompt += "Finally, give a 50-word reasoning as for why you classified the product this way. \n"

        prompt += "Please return the product classification and refund suggestion as a list of strings, where each string is one item in the list like: \n"
        prompt += "[\"Condition\", \"Refund Amount\", \"Explanation of condition\"]"

        prompt += "Please find below information on the product: \n"

        prompt += f"Product Name: {name} \n Product Category: {category} \n Company: {company} \n Purchase Date: {date} \n Price Sold At: {price} \n Customer Reason for Returning: {reason} \n Image: Attached with list"

        response = model.generate_content(
            contents=[prompt, image_desc])
        return response
     
    def evaluate_product(self, request, order_id=None):
        serializer = ProductEvaluationSerializer(data=request.data)
        
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            prod_image = serializer.validated_data['image']
            desc = serializer.validated_data['text']
        
        try:
            order = OrderHistory.get(id=order_id)
            product = order.prod_id
        except OrderHistory.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        
        prod_name = product.name
        product_cat = product.product_type
        product_company = product.company
        purchase_date = order.purchase_date
        product_price = product.price

        answer = self.gemini_evaluate(prod_name, product_cat, product_company, purchase_date, product_price, prod_image, desc)

        try:
            # This assumes the response is something like: '["Product Condition: Lightly Used", "Refund Suggestion: $50.00"]'
            answer_list = eval(answer.text)  # This converts the string representation of a list into an actual list
        except Exception as e:
            # Handle any parsing errors
            return {"error": str(e)}

        if answer_list[0] in ["Unused", "Lightly Used"]:
            return Response("Restock", answer_list[1], answer_list[2])
        elif answer_list[0] in ["Moderately Used", "Heavily Used"]:
            return Response("Resale", answer_list[1], answer_list[2])
        elif answer_list[0] == "Damaged by User":
            return Response("Recycle", answer_list[1], answer_list[2])
        else:
            return Response("Recall", answer_list[1], answer_list[2])

class ReturnRequestViewSet(viewsets.ViewSet):

    def request_return(self, request, order_id=None):
        serializer = ReturnSerializer(data=request.data)

        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            prod_image = serializer.validated_data['image']
            desc = serializer.validated_data['text']
            refund_value = serializer.validated_data['refund_value']
            return_option = serializer.validated_data['return_option']
            condition = serializer.validated_data['condition']
        
        try:
            order = OrderHistory.objects.get(id=order_id)
            product = order.prod_id
            customer = order.cust_id
        except OrderHistory.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        
        return_request = ReturnRequest.objects.create(
                prod_id=product,
                cust_id=customer,
                order_id=order,
                condition=condition,
                ret_option=return_option,
                refund_value=refund_value,
                image=prod_image,
                ret_reason=desc,
                request_status=ReturnRequest.ReturnStatus.IN_PROGRESS)
        
        return Response(serializer.data, status=201)
        
        










        




