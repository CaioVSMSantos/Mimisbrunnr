from django.shortcuts import render
from .src.mimisbrunnr import simple_text_generator
import markdown

def index(request):
    return render(request, 'index.html')


def get_recommendations(request):
    result = None
    prompt = request.POST.get('prompt')
    error_message = None
    if request.method == 'POST' and prompt:
        prompt = request.POST.get('prompt')
        text_result = simple_text_generator(prompt)
        result = markdown.markdown(text_result)
    return render(request, 'index.html', {'prompt': prompt,
                                          'result': result,
                                          'error_message': error_message})
