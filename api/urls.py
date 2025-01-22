from django.urls import path
from .import views
 

urlpatterns = [
    path("major/", views.MajorListCreate.as_view(), name="Major-view-create"),
    path("major/<int:pk>/", views.MajorRetreiveUpdateDestroy.as_view(), name="Major-view-retreive-update-delete"),

    path("hour_type/", views.HourTypeListCreate.as_view(), name="HourType-view-create"),
    path("hour_type/<int:pk>/", views.HourTypeRetreiveUpdateDestroy.as_view(), name="HourType-view-retreive-update-delete"),
]