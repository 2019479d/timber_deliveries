from django.urls import path
from . import views

# URL configuration of the stc app
urlpatterns = [
    # Add QR
    path('<str:username>/addQR/<str:visible_material_no>/<int:region_id>/<str:depot_id>', views.add_qr),
    # Modify QR
    path('<str:username>/modifyQR/<str:visible_material_no>/<int:region_id>/<str:depot_id>', views.modify_qr),
    # Working Sheet (Search: Visual Material Number)
    path('<str:username>/workingSheet/<str:visible_material_nos>/<int:region_id>/<str:depot_id>', views.logs_from_visible_material_no),
    # Working Sheet (Search: QR ID)
    path('<str:username>/workingSheet/<str:qr_ids>', views.logs_from_qr_id),
    # Search log by qr
    path('<str:username>/workingSheet/search/<str:qr_ids>', views.search_log_by_qr),
    # To create a working sheet and save on the database , searched by QR
    path('<str:username>/saveWSQR/<str:qr_ids>/<str:depot_id>', views.save_working_sheet_qr),
    # To create a working sheet and save on the database , searched by visible materila number
    path('<str:username>/saveWSvmn/<str:visible_material_nos>/<str:depot_id>', views.save_working_sheet_vmn),

    #stc_db_t1
]
