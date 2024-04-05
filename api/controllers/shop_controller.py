from django.http import JsonResponse

from api.services.shop_service import calculate_highlight_price


def highlight_calculator(request):
    """Controlador que devuelve el precio de destacar una lista"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = calculate_highlight_price(start_date, end_date)

    return JsonResponse({'price': total_price})
