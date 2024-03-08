from django.urls import path
from service import views

urlpatterns = [
    path("api/ess/auth/login/", views.login),
    # path("api/ess/auth/regist/", views.regist),
    path("api/ess/auth/changepwd/", views.changepwd),
    path("api/ess/auth/changeuserimg/", views.changeuserimg),
    path("api/ess/auth/get_user_info/", views.get_user_info),


    path("api/ess/admin/admin_get_user_info_list/", views.admin_get_user_info_list),
    path("api/ess/admin/admin_get_user_info/", views.admin_get_user_info),
    path("api/ess/admin/admin_update_user_info/", views.admin_update_user_info),
    path("api/ess/admin/admin_update_user_pwd/", views.admin_update_user_pwd),

    path("api/ess/admin/admin_get_project_info_list/", views.admin_get_project_info_list),
    path("api/ess/admin/admin_add_project/", views.admin_add_project),
    path("api/ess/admin/admin_get_project_info/", views.admin_get_project_info),
    path("api/ess/admin/admin_update_project_info/", views.admin_update_project_info),
    path("api/ess/admin/admin_delete_project/", views.admin_delete_project),

    path("api/ess/admin/admin_get_supplier_info_list/", views.admin_get_supplier_info_list),
    path("api/ess/admin/admin_add_supplier/", views.admin_add_supplier),
    path("api/ess/admin/admin_get_supplier_info/", views.admin_get_supplier_info),
    path("api/ess/admin/admin_update_supplier_info/", views.admin_update_supplier_info),
    path("api/ess/admin/admin_delete_supplier/", views.admin_delete_supplier),

    path("api/ess/admin/admin_get_ybudget_data/", views.admin_get_ybudget_data),
    path("api/ess/admin/admin_add_ybudget_data/", views.admin_add_ybudget_data),
    path("api/ess/admin/admin_get_ybudget_data_one/", views.admin_get_ybudget_data_one),
    path("api/ess/admin/admin_update_ybudget_data/", views.admin_update_ybudget_data),
    path("api/ess/admin/admin_delete_ybudget_data/", views.admin_delete_ybudget_data),

    path("api/ess/admin/admin_get_slesspn/", views.admin_get_slesspn),
    path("api/ess/admin/admin_add_slesspn/", views.admin_add_slesspn),
    path("api/ess/admin/admin_get_slesspn_one/", views.admin_get_slesspn_one),
    path("api/ess/admin/admin_update_slesspn/", views.admin_update_slesspn),
    path("api/ess/admin/admin_delete_slesspn/", views.admin_delete_slesspn),
    path("api/ess/admin/admin_get_slessvd/", views.admin_get_slessvd),
    path("api/ess/admin/admin_add_slessvd/", views.admin_add_slessvd),
    path("api/ess/admin/admin_get_slessvd_one/", views.admin_get_slessvd_one),
    path("api/ess/admin/admin_update_slessvd/", views.admin_update_slessvd),
    path("api/ess/admin/admin_delete_slessvd/", views.admin_delete_slessvd),

    path("api/ess/admin/admin_get_task_kind_info_list/", views.admin_get_task_kind_info_list),
    path("api/ess/admin/admin_add_task_kind/", views.admin_add_task_kind),
    path("api/ess/admin/admin_get_task_kind_info/", views.admin_get_task_kind_info),
    path("api/ess/admin/admin_update_task_kind_info/", views.admin_update_task_kind_info),
    path("api/ess/admin/admin_delete_task_kind/", views.admin_delete_task_kind),


    path("api/ess/pubcli/get_user_list/", views.get_user_list),
    path("api/ess/pubcli/get_project_list/", views.get_project_list),
    path("api/ess/pubcli/get_supplier_list/", views.get_supplier_list),
    path("api/ess/pubcli/get_anno_task_kind_list/", views.get_anno_task_kind_list),


    path("api/ess/annoteam/search_anno_team_data/", views.search_anno_team_data),
    path("api/ess/annoteam/add_anno_task_data/", views.add_anno_task_data),
    path("api/ess/annoteam/get_anno_task_data_one/", views.get_anno_task_data_one),
    path("api/ess/annoteam/get_all_anno_team_data/", views.get_all_anno_team_data),
    path("api/ess/annoteam/update_anno_task_data/", views.update_anno_task_data),
    path("api/ess/annoteam/delete_anno_task_data/", views.delete_anno_task_data),
    path("api/ess/annoteam/get_anno_team_efficiency/", views.get_anno_team_efficiency),
    path("api/ess/annoteam/get_anno_team_person/", views.get_anno_team_person),
    path("api/ess/annoteam/get_anno_team_task_count/", views.get_anno_team_task_count),


    path("api/ess/supplier/get_supplier_task_data/", views.get_supplier_task_data),
    path("api/ess/supplier/get_all_supplier_task_data/", views.get_all_supplier_task_data),
    path("api/ess/supplier/get_supplier_task_data_one/", views.get_supplier_task_data_one),
    path("api/ess/supplier/add_supplier_task_data/", views.add_supplier_task_data),
    path("api/ess/supplier/get_supplier_data_jsfs/", views.get_supplier_data_jsfs),
    path("api/ess/supplier/update_supplier_task_data/", views.update_supplier_task_data),
    path("api/ess/supplier/delete_supplier_task_data/", views.delete_supplier_task_data),
    path("api/ess/supplier/get_supplier_task_count/", views.get_supplier_task_count),

    
    path("api/ess/budget/add_budget_data/", views.add_budget_data),
    path("api/ess/budget/get_budget_all_data/", views.get_budget_all_data),
    path("api/ess/budget/get_budget_one_data/", views.get_budget_one_data),
    path("api/ess/budget/update_budget_data/", views.update_budget_data),
    path("api/ess/budget/delete_budget_data/", views.delete_budget_data),
]
