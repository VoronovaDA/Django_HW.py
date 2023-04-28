from django.http import HttpResponse
from django.shortcuts import render


DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:


def receipt_view(request, name):
    servings = int(request.GET.get('servings', '1'))
    ingredients = DATA.get(name, None)
    if not ingredients:
        return HttpResponse('Такого блюда нет в списке')
    for ingrid in ingredients:
        ingredients[ingrid] *= servings
    context = {
        'recipe': ingredients,
    }
    return render(request, 'calculator/index.html', context)
