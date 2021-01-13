from django.conf.urls import url
from .views import (
    HelloView,
    RegistrationAPI,
    LoginView,
    LogoutView,
    UserRoleCreate,
    ListOfUserRole,
    product_list,
    PaginationView,
    OrderCreate,
    ListOfOrder,
    OrderPlace,
    AcceptOrder,search_product)
#urls for djnago app
urlpatterns = [
    url(r'^hello/', HelloView.as_view(), name='hello'),
    url(r'^register/', RegistrationAPI.as_view(), name='register'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^user_role_create/', UserRoleCreate.as_view(), name='user_role_create'),
    url(r'^user_role_list/', ListOfUserRole.as_view(), name='user_role_list'),
    url(r'^order_create/', OrderCreate.as_view(), name='order_create'),
    url(r'^order_list/', ListOfOrder.as_view(), name='order_list'),
    url(r'^<str:slug>/', product_list, name='product_detail'),
    url(r'^order_place/', OrderPlace.as_view(), name='order_place'),
    url(r'^order_accept/', AcceptOrder.as_view(), name='order_accept'),
     url(r'^search_product/', product_list, name='search_product'),
    url(r'^pagination_list/$',PaginationView.as_view())
]
