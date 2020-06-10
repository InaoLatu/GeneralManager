from django.urls import path
from general_manager import views as general_manager_views



urlpatterns = [
    path('identification_telegram/<str:username>/<str:id>', general_manager_views.identification_telegram, name='identification_telegram'),
    path('check_user/<str:type>/<str:id>', general_manager_views.check_user_exists, name='check_user_exists'),
    path('get_units/', general_manager_views.get_units, name='get_units'),
    path('units/<str:unit>/<str:id>', general_manager_views.get_unit_microcontent, name='get_unit_microcontent'),
    path('microcontent', general_manager_views.get_microcontent, name='get_microcontent'),
    # path('store_mark/<str:student_id>/<str:unit_name>/<int:microcontent_id>/<str:mark>', general_manager_views.store_mark, name='store_mark'),
    path('store_mark', general_manager_views.store_mark, name='store_mark'),
]