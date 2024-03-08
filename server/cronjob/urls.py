from django.urls import path, re_path
from cronjob import views

urlpatterns = [
    path("api/ess/cronjob/add_cronjob/", views.add_cronjob),
    path("api/ess/cronjob/get_cronjob/", views.get_cronjob),
    path("api/ess/cronjob/get_cronjob_log/", views.get_cronjob_log),
    path("api/ess/cronjob/del_cronjob/", views.del_cronjob),
    # re_path(r"report_img/(.*)$",views.ReportImage.as_view()),
]
