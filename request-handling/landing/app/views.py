from collections import Counter

from django.http import Http404
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_lending = request.GET.get('from-landing')
    if from_lending == 'original':
        counter_click['original'] += 1
    elif from_lending == 'test':
        counter_click['test'] += 1
    else:
        raise Http404
    return render(request,
                  'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test = request.GET.get('ab-test-arg')
    if ab_test == 'original':
        counter_show['original'] += 1
        template = 'landing.html'
    elif ab_test == 'test':
        counter_show['test'] += 1
        template = 'landing_alternate.html'
    else:
        template = 'landing_choice.html'
    return render(request,
                  template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_show['original'] or counter_click['original']:
        original_conversion = counter_click['original'] / counter_show['original']
    else:
        original_conversion = 0
    if counter_show['test'] or counter_click['test']:
        test_conversion = counter_click['test'] / counter_show['test']
    else:
        test_conversion = 0
    return render(request,
                  'stats.html',
                  context={
                      'test_conversion': round(test_conversion, 2),
                      'original_conversion': round(original_conversion, 2),
                  })
