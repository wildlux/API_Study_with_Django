from django.contrib import admin
from django.urls import path
from learning.views import home, theory, practice, exercises, methods, test_get_request, test_post_request, quiz_home, quiz_results, check_answer, check_all_answers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('theory/', theory, name='theory'),
    path('practice/', practice, name='practice'),
    path('exercises/', exercises, name='exercises'),
    path('methods/', methods, name='methods'),
    path('test-get/', test_get_request, name='test_get_request'),
    path('test-post/', test_post_request, name='test_post_request'),
    path('quiz/', quiz_home, name='quiz_home'),
    path('quiz/results/', quiz_results, name='quiz_results'),
    path('check-answer/', check_answer, name='check_answer'),
    path('check-all-answers/', check_all_answers, name='check_all_answers'),
]