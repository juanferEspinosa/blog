from django.shortcuts import render
from .models import Post
from django.http import JsonResponse, HttpResponse
from .llm_logic import build_database, answer_query, database_exists
import threading





def detail_post(request, slug):
    detail_post = Post.objects.get(slug=slug)
    
    return render(request, 'blog-details.html', {'detail_post':detail_post})

def ecommerce_products(request):
    return render(request, 'ecommerce/products.html')

def ecommerce_product_detail(request):
    return render(request, 'ecommerce/product-details.html')


def llmChatbot(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        result = answer_query(query)  # Embeddings
         
         
        return JsonResponse(result)
    return render(request, 'langchain-chat.html')

def db_status(request):
    status = {
        'exists': database_exists(),
        'message': 'Database exists' if database_exists() else 'Database is being built',
    }
    return JsonResponse(status)

def buildDB(request):
    # build the database asynchronously
    thread = threading.Thread(target=build_database)
    thread.start()
    return JsonResponse({'status': 'Building database'})

