from django.urls import path
from .import views
 

urlpatterns = [
    path("major/", views.MajorListCreate.as_view(), name="Major-view-create"),
    path("major/<int:pk>/", views.MajorRetreiveUpdateDestroy.as_view(), name="Major-view-retreive-update-delete"),
    path("complementary_activity/", views.ComplementaryActivitySerializer.as_view(), name = "ComplementaryActivity-view-create"),
    path("activity_type/", views.ActivityTypeListCreate.as_view(), name="ActivityType-view-create"),
    path("activity_type/<int:pk>/", views.ActivityTypeRetreiveUpdateDestroy.as_view(), name="ActivityType-view-retreive-update-delete"),
]