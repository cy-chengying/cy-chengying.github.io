# from django.shortcuts import render,redirect
# from django.http import JsonResponse
# from . import models
# # Create your views here.
#
# def cart(request):
#     uid = request.session.get('uid')
#     carts = Cart.objects.filter(user_id=uid)
#
#     context = {'title': '购物车',
#                'name': 1,
#                'carts': carts}
#     return render(request, 'cart/cart.html', context)