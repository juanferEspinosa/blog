from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('<slug:slug>/', detail_post, name='detail_post'),
    path('ecommerce/products/', ecommerce_products, name='ecommerce_products'),
    path('ecommerce/products/red-shirt/', ecommerce_product_detail, name='ecommerce_product_detail'),
    #path('blog/langchain-chat/', llmChatbot, name='llm-chatbot'),
]