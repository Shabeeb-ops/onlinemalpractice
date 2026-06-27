
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('admin_home/',views.admin_home),
    path('admin_add_staff/',views.admin_add_staff),
    path('admin_add_subject/',views.admin_add_subject),
    path('admin_assign_staff',views.admin_assign_staff),
    path('admin_assign_staff_post/',views.admin_assign_staff_post),
    path('admin_view_assign_staff/<id>',views.admin_view_assign_staff),
    path('admin_edit_aasign/<id>',views.admin_edit_aasign),
    path('admin_delete_assign/<id>',views.admin_delete_assign),
    path('admin_edit_assign_staff_post/',views.admin_edit_assign_staff_post),
    path('viewexam/',views.viewexam),
    path('add_exam_post/',views.add_exam_post),
    path('add_exam/',views.add_exam),
    path('deleteexam/<id>/',views.deleteexam),

    path('admin_login/',views.admin_login),
    path('logouta/',views.logouta),
    path('login_post/',views.login_post),
    path('admin_add_notification/',views.admin_add_notification),
    path('admin_delete_notification/<id>',views.admin_delete_notification),

    path('admin_reply/<id>',views.admin_reply),
    path('accept_student/<id>',views.accept_student),
    path('reject_student/<id>',views.reject_student),
    path('admin_verify_student/',views.admin_verify_student),
    path('admin_view_and_feedback/',views.admin_view_and_feedback),
    path('admin_view_complaint/',views.admin_view_complaint),
    path('admin_view_notification/',views.admin_view_notification),
    path('admin_view_review_rating/',views.admin_view_review_rating),
    path('admin_view_staff/',views.admin_view_staff),
    path('admin_delete_staff/<id>',views.admin_delete_staff),
    path('admin_view_subject/',views.admin_view_subject),
    path('admin_delete_staff/<id>',views.delete_staff),
    path('admin_edit_staff/<id>',views.admin_edit_staff),
    path('admin_edit_staff_post/',views.admin_edit_staff_post),
    path('admin_edit_subject/<id>',views.admin_edit_subject),
    path('admin_delete_subject/<id>',views.admin_delete_subject),


    path('staffhome/',views.staffhome),
    path('staff_add_exam/',views.staff_add_exam),
    path('staff_add_questions/',views.staff_add_questions),
    path('add_question_post/',views.add_question_post),
    path('staff_add_study_material/',views.staff_add_study_material),
    path('staff_change_password/',views.staff_change_password),
    path('staff_edit_profile/',views.staff_edit_profile),
    path('staff_edit_profile_post',views.staff_edit_profile_post),
    path('staff_feedback/',views.staff_feedback),
    path('staff_manage_study_material/',views.staff_manage_study_material),
    path('staff_view_exam_questions/',views.staff_view_exam_questions),
    path('staff_view_exam_details/',views.staff_view_exam_details),
    path('staff_view_notification/',views.staff_view_notification),
    path('staff_view_profile/',views.staff_view_profile),
    path('staff_view_questions/<id>',views.staff_view_questions),
    path('staff_delete_question/<id>',views.staff_delete_question),
    path('delete_studymaterial/<id>/',views.delete_studymaterial),
    path('upload_study_material/',views.upload_study_material),
    path('staff_view_malpratice/',views.staff_view_malpratice),
    path('changepassword/',views.changepassword),



    path('user_login',views.user_login),
    path('user_register',views.user_register),
    path('view_profile',views.view_profile),
    path('view_online_exam/',views.view_online_exam),
    path('send_complaint',views.send_complaint),
    path('view_complaint',views.view_complaint),
    path('view_studymaterial',views.view_studymaterial),
    path('send_feedback',views.send_feedback),
    path('view_questions',views.view_questions),
    path('send_review_rating',views.send_review_rating),
    path('view_staff/',views.view_staff),

    path('student_list/',views.student_list),
    path('tuto_chat_to_user/<id>',views.tuto_chat_to_user),
    path('chat_send/<msg>',views.chat_send),
    path('chat_view',views.chat_view),


    path('user_viewchat',views.user_viewchat),
    path('user_sendchat',views.user_sendchat),

    path('change_password/',views.change_password),
    path('androidattendexam/',views.androidattendexam),
    path('savestudentanswer/',views.savestudentanswer),









]