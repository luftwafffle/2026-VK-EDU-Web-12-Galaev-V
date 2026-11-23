from django.shortcuts import render
from django.http import HttpResponse, Http404
from .utils import paginate


# Create your views here.

TAGS_LIST = {
    'GruzinskayaKuhnya': {'slug': 'GruzinskayaKuhnya', 'name': 'Грузинская кухня'},
    'python': {'slug': 'python', 'name': 'Python'},
    'sql': {'slug': 'sql', 'name': 'SQL'},
    'kotiki': {'slug': 'kotiki', 'name': 'Котики'},
    'java': {'slug': 'java', 'name': 'Java'},
    'perl': {'slug': 'perl', 'name': 'Perl'}
}

ANSWERS_LIST = [
    {
        'id': i,
        'text': f'Хммм... Может быть {i}?'
    }
    for i in range(1, 15)
]

QUESTIONS_LIST = [
    {
        'id': i,
        'title': f'Это мой {i}й вопрос, и я не собираюсь останавливаться.',
        'text': f'сколько будет {i}*{i}*{i}*{i}*{i}*{i} ?',
        'tags': (
            [TAGS_LIST['GruzinskayaKuhnya'], TAGS_LIST['python'],TAGS_LIST['sql']]
            if i % 2 == 1
            else [TAGS_LIST['kotiki'], TAGS_LIST['java'],TAGS_LIST['perl']]
        )
    } for i in range(1,301)
]



def index(request):
    page_obj = paginate(QUESTIONS_LIST, request)
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list,'page_obj': page_obj})

def hot(request):
    page_obj = paginate(QUESTIONS_LIST[::-1], request)
    return render(request, 'questions/hot-questions.html', context={'questions': page_obj.object_list,'page_obj': page_obj})

def tag_questions(request, tag_name):
    filtered_questions = [
        question
        for question in QUESTIONS_LIST
        if any(tag['slug'] == tag_name for tag in question['tags'])
    ]
    page_obj = paginate(filtered_questions, request)
    tag_title = TAGS_LIST.get(tag_name, {}).get('name', tag_name)
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})

# def question(request, id):
#     return render(request,'questions/question_details.html', context={'question': {'title': 'tvoi ochi', 'text': 'lihtariki'}})

def question_details(request, question_id):
    question = next((question for question in QUESTIONS_LIST if question['id'] == question_id),None)
    if question is None:
        raise Http404()
    answers_page = paginate(ANSWERS_LIST, request)
    return render(request, 'questions/question_details.html', {'question': question, 'answers': answers_page, 'user': {'is_authenticated': True}})

def login(request):
    return render(request, 'questions/login.html')

def register(request):
    return render(request, 'questions/register.html')

def settings(request):
    return render(request, 'questions/settings.html')

def ask(request):
    return render(request, 'questions/ask.html')


def secretView(request):
    return HttpResponse('<h1>Вы попали в самый секретный уголок интернета!</h1> <p><a href=\'/\'>назад</a></p>')

