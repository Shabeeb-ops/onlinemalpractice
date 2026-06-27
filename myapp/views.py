from datetime import datetime
from xmlrpc.client import DateTime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import base64
from PIL import Image
from io import BytesIO
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from myapp.models import  *
# from myapp.objectdetection import objdet
from myapp.objectdetection import objdet


def logouta(request):
    logout(request)
    return redirect('/myapp/admin_login/')

@csrf_exempt
def admin_login(request):
    try:
        ob = User.objects.get(id=5)
        ob.password = make_password("shabeeb")
        ob.save()
    except User.DoesNotExist:
        # On a fresh deployment (like Vercel), create a default admin user if not present
        if not User.objects.filter(username="admin").exists():
            user = User.objects.create_superuser(username="admin", email="admin@example.com", password="shabeeb")
            admin_group, _ = Group.objects.get_or_create(name="Admin")
            user.groups.add(admin_group)
    return render(request, 'login.html')

@csrf_exempt
def login_post(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.groups.filter(name="Admin").exists():
            print("admin")
            login(request, user)
            return redirect('/myapp/admin_home/')
        elif user.groups.filter(name="Staff").exists():
            print("staff")
            login(request, user)
            return redirect('/myapp/staffhome/')
    else:
        messages.warning(request, "Invalid.usesrname or password")
        return redirect('/myapp/admin_login/')

#=================================================================
#=================================================================
#=============================ADMIN===============================
#=================================================================

@login_required(login_url='/myapp/admin_login/')
def admin_home(request):
    return render(request,'admin/home.html')

@login_required(login_url='/myapp/admin_login/')
def admin_view_staff(request):
    var=Staff_table.objects.all()
    return render(request,'admin/view staff.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_delete_staff(request,id):
    a=Staff_table.objects.get(id=id)
    obj=a.LOGIN
    obj.delete()
    return redirect('/myapp/admin_view_staff/#about')

@login_required(login_url='/myapp/admin_login/')
def admin_add_staff(request):
    if request.method =='POST':
        name=request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        qualification = request.POST['qualification']
        place = request.POST['place']
        username = request.POST['user']
        password = request.POST['password']

        user=User.objects.create(username=username,password=make_password(password),email=email,first_name=name)
        user.save()
        user.groups.add(Group.objects.get(name="Staff"))


        var=Staff_table()
        var.name=name
        var.LOGIN=user
        var.email=email
        var.contact=phone
        var.qualification=qualification
        var.place=place
        var.save()
        return redirect('/myapp/admin_view_staff#about')
    return render(request,'admin/Add staff.html')

@login_required(login_url='/myapp/admin_login/')
def admin_edit_staff(request,id):
    var=Staff_table.objects.get(LOGIN_id=id)
    request.session['sid']=id
    return render(request,'admin/edit_staff.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_edit_staff_post(request):
    name=request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    qualification = request.POST['qualification']
    place = request.POST['place']

    var=Staff_table.objects.get(LOGIN_id=request.session['sid'])
    var.name=name
    var.email=email
    var.contact=phone
    var.qualification=qualification
    var.place=place
    var.save()
    return redirect('/myapp/admin_view_staff/')

@login_required(login_url='/myapp/admin_login/')
def delete_staff(request,id):
    a=Staff_table.objects.get(LOGIN_id=id)
    ob=a.LOGIN
    ob.delete()
    User.objects.filter(id=id).delete()
    return redirect('/myapp/admin_view_staff#about/')

@login_required(login_url='/myapp/admin_login/')
def admin_view_subject(request):
    var=Subject_table.objects.all()
    return render(request,'admin/view subject.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_add_subject(request):
    if request.method =='POST':
        subject=request.POST['subject']
        var=Subject_table()
        var.subject=subject
        var.date=datetime.now().today().date()
        var.save()
        return redirect('/myapp/admin_view_subject/#about')
    return render(request,'admin/Add subject.html')

@login_required(login_url='/myapp/admin_login/')
def admin_delete_subject(request,id):
    a=Subject_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/admin_view_subject/#about')

@login_required(login_url='/myapp/admin_login/')
def admin_edit_subject(request,id):
    request.session['id']=id
    var=Subject_table.objects.get(id=id)
    if request.method =='POST':
        subject=request.POST['subject']
        var=Subject_table.objects.get(id=request.session['id'])
        var.subject=subject
        var.save()
        return redirect('/myapp/admin_view_subject/')
    return render(request,'admin/edit subject.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_view_notification(request):
    var= Notification_table.objects.all()
    return render(request,'admin/view notification.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_add_notification(request):
    if request.method =='POST':
        notification=request.POST['notification']
        var=Notification_table()
        var.notification=notification
        var.date=datetime.now().today().date()
        var.save()
        return redirect('/myapp/admin_view_notification/#about')
    return render(request,'admin/Add notification.html')

@login_required(login_url='/myapp/admin_login/')
def admin_delete_notification(request,id):
    a=Notification_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/admin_view_notification/#about')

@login_required(login_url='/myapp/admin_login/')
def admin_view_review_rating(request):
    var=review_table.objects.all()
    return render(request,'admin/view review rating.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_view_complaint(request):
    var=Complaint_table.objects.all()
    return render(request,'admin/view complaint.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_reply(request,id):
    request.session['id']=id
    var=Complaint_table.objects.get(id=id)
    if request.method == 'POST':
        reply=request.POST['reply']
        var2 = Complaint_table.objects.get(id=request.session['id'])
        var2.reply = reply
        var2.save()
        return redirect('/myapp/admin_view_complaint#about')
    return render(request,'admin/reply.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def admin_view_and_feedback(request):
    var=Feedback_table.objects.all()
    return render(request,'admin/view and feedback.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def viewexam(request):
    a=Exam_table.objects.all()
    return render(request,'admin/viewexam.html',{'data':a})

@login_required(login_url='/myapp/admin_login/')
def add_exam(request):
    ob=Subject_table.objects.all()
    return render(request,'admin/addexam.html',{"val":ob})

@login_required(login_url='/myapp/admin_login/')
def add_exam_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkk")
    exam=request.POST['exam']
    date=request.POST['date']
    time=request.POST['time']
    subject=request.POST['subject']
    a=Exam_table()
    a.exam=exam
    a.date=date
    a.time=time
    a.subject=Subject_table.objects.get(id=subject)
    a.save()
    return redirect('/myapp/viewexam#about')

@login_required(login_url='/myapp/admin_login/')
def deleteexam(request,id):
    a=Exam_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/viewexam/#about')

@login_required(login_url='/myapp/admin_login/')
def admin_verify_student(request):
    var=Student_table.objects.all()
    return render(request,'admin/verify student.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def accept_student(request,id):
    a=Student_table.objects.get(id=id)
    a.status="Accepted"
    a.save()
    return redirect('/myapp/admin_verify_student/#about')

@login_required(login_url='/myapp/admin_login/')
def reject_student(request,id):
    a=Student_table.objects.get(id=id)
    a.status="Rejected"
    a.save()
    return redirect('/myapp/admin_verify_student/#about')

@login_required(login_url='/myapp/admin_login/')
def admin_view_assign_staff(request,id):
    request.session['sid'] = id
    data=Assign_table.objects.filter(STAFF=id)
    return render(request,'admin/view assign.html',{'data':data})

@login_required(login_url='/myapp/admin_login/')
def admin_assign_staff(request):
    data=Subject_table.objects.all()
    return render(request,'admin/assign staff.html',{'data':data})

@login_required(login_url='/myapp/admin_login/')
def admin_assign_staff_post(request):
    id=request.session['sid']
    subjectid=request.POST['subject']
    data=Assign_table()
    data.SUBJECT_id=subjectid
    data.STAFF_id=request.session['sid']
    data.save()
    return redirect(f'/myapp/admin_view_assign_staff/{id}#about')

@login_required(login_url='/myapp/admin_login/')
def admin_delete_assign(request,id):
    idd = request.session['sid']
    a=Assign_table.objects.get(id=id)
    a.delete()
    return redirect(f'/myapp/admin_view_assign_staff/{idd}#about')

@login_required(login_url='/myapp/admin_login/')
def admin_edit_aasign(request,id):
    request.session['aid']=id
    var=Subject_table.objects.all()
    data=Assign_table.objects.get(id=id)
    return render(request,'admin/edit assign.html',{'data':var,"sub":data})

@login_required(login_url='/myapp/admin_login/')
def admin_edit_assign_staff_post(request):
    subjectid=request.POST['subject']
    data=Assign_table.objects.get(id=request.session['aid'])
    data.SUBJECT_id=subjectid
    data.save()
    return redirect('/myapp/admin_view_assign_staff')

#=====================================================================================
#======================================STAFF==========================================
#=====================================================================================
@login_required(login_url='/myapp/admin_login/')
def staffhome(request):
    ob=Staff_table.objects.get(LOGIN=request.user.id)
    return render(request,'staff/home.html',{"name":ob})

@login_required(login_url='/myapp/admin_login/')
def  staff_edit_profile(request):
    var=Staff_table.objects.get(LOGIN_id=request.user.id)
    return render(request, 'staff/edit profile.html',{'data':var})

@login_required(login_url='/myapp/admin_login/')
def staff_edit_profile_post(request):
    name=request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    qualification = request.POST['qualification']
    place = request.POST['place']

    var=Staff_table.objects.get(LOGIN_id=request.user.id)
    var.name=name
    var.email=email
    var.contact=phone
    var.qualification=qualification
    var.place=place
    var.save()
    return redirect('/myapp/staff_edit_profile#about')

@login_required(login_url='/myapp/admin_login/')
def staff_add_exam(request):
    var=Exam_table.objects.all()
    return render(request,'staff/add exam.html',{'data': var})

@login_required(login_url='/myapp/admin_login/')
def staff_view_exam_details(request):
    lid=request.user.id
    ob = Staff_table.objects.get(LOGIN=request.user.id)
    staff = Staff_table.objects.get(LOGIN=lid)
    assigned_subjects = Assign_table.objects.filter(STAFF=staff).values_list('SUBJECT', flat=True)
    exams = Exam_table.objects.filter(subject__in=assigned_subjects)
    return render(request, 'staff/view exam details.html',{"data":exams,"name":ob})

@login_required(login_url='/myapp/admin_login/')
def staff_view_questions(request,id):
    ob=question_table.objects.filter(EXAM__id=id)
    request.session['exmid']=id
    return render(request, 'staff/view questions.html',{"val":ob})

@login_required(login_url='/myapp/admin_login/')
def staff_add_questions(request):
    return render(request,'staff/add questions.html')

@login_required(login_url='/myapp/admin_login/')
def add_question_post(request):
    question = request.POST["question"]
    option1 = request.POST["option1"]
    option2 = request.POST["option2"]
    option3 = request.POST["option3"]
    option4 = request.POST["option4"]
    answer = request.POST["answer"]
    exam_id = request.session['exmid']
    staff_id = request.user.id
    # print(exam_id, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(staff_id, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    obj = question_table()
    obj.question = question
    obj.option1 = option1
    obj.option2 = option2
    obj.option3 = option3
    obj.option4 = option4
    obj.answer = answer
    obj.EXAM = Exam_table.objects.get(id=exam_id)
    obj.STAFF = Staff_table.objects.get(LOGIN__id=staff_id)
    obj.save()
    eid=request.session['exmid']
    return redirect(f'/myapp/staff_view_questions/{eid}#about')

@login_required(login_url='/myapp/admin_login/')
def staff_delete_question(request,id):
    a=question_table.objects.get(id=id)
    a.delete()
    eid=request.session['exmid']
    return redirect(f'/myapp/staff_view_questions/{eid}#about')

@login_required(login_url='/myapp/admin_login/')
def staff_view_malpratice(request):
    lid=request.user.id
    stf=Staff_table.objects.get(LOGIN_id=lid)
    staff_id=stf.id
    print(staff_id,":-----------------------------------")
    var=malpratice.objects.filter(QUESTION__STAFF_id=staff_id)
    print(var,"===========================")
    return render(request,'staff/view_malpratice.html',{"val":var})

@login_required(login_url='/myapp/admin_login/')
def staff_manage_study_material(request):
    var=Studymaterial_table.objects.all()
    return render(request,'staff/manage studymaterial.html',{"val":var})

@login_required(login_url='/myapp/admin_login/')
def delete_studymaterial(request,id):
    a=Studymaterial_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/staff_manage_study_material/#about')

@login_required(login_url='/myapp/admin_login/')
def staff_add_study_material(request):
    stf=Staff_table.objects.all()
    return render(request, 'staff/add studymaterial.html', {'data':stf})

@login_required(login_url='/myapp/admin_login/')
def upload_study_material(request):
    materialFile=request.FILES['materialFile']
    fs=FileSystemStorage()
    file_path=fs.save(materialFile.name, materialFile)
    obj=Studymaterial_table()
    obj.studymaterial = file_path
    obj.date = datetime.today()
    obj.STAFF = Staff_table.objects.get(LOGIN__id=request.user.id)
    obj.save()
    return redirect('/myapp/staff_manage_study_material#about')

@login_required(login_url='/myapp/admin_login/')
def staff_change_password(request):
    return render(request,'staff/change password.html')

@login_required(login_url='/myapp/admin_login/')
def staff_feedback(request):
    obj=Feedback_table.objects.all()
    return render(request,'staff/feedback.html',{"data":obj})

@login_required(login_url='/myapp/admin_login/')
def staff_view_exam_questions(request):
    var=question_table.objects.all()
    return render(request, 'staff/view details.html')

@login_required(login_url='/myapp/admin_login/')
def staff_view_notification(request):
    var=Notification_table.objects.all()
    return render(request, 'staff/view notification.html',{"data":var})

@login_required(login_url='/myapp/admin_login/')
def staff_view_profile(request):
    return render(request, 'staff/view profile.html')

@login_required(login_url='/myapp/admin_login/')
def changepassword(request):
    if request.method == "POST":
        oldpasspwrd= request.POST["current_password"]
        newpassword= request.POST["new_password"]


        print(request.user)
        f=check_password(oldpasspwrd,request.user.password)
        if f:
            user=request.user
            user.set_password(newpassword)
            user.save()
            logout(request)
            #update_session_auth_hash(request,user)
            messages.success(request, 'Password changed successfully')
            return redirect('/myapp/admin_login/')
        else:
            logout(request)
            messages.success(request, 'Password updated successfully. Please lgin try again')
            return redirect('/myapp/admin_login/')
    return render(request,"staff/change password.html")

@login_required(login_url='/myapp/admin_login/')
def student_list(request):
    students = Student_table.objects.filter(status="Accepted")
    return render(request, 'staff/students.html', {'students': students})


# user android



def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.groups.filter(name="Student").exists():
            ab=Student_table.objects.get(LOGIN_id=user.id)
            status=ab.status
            if status == "Accepted":
                return JsonResponse({'status':'ok','lid':str(user.id),'type':'Student'})
            else:
                return JsonResponse({'status': 'not ok'})
        else:
            return JsonResponse({'status': 'not ok'})
    else:
        return JsonResponse({'status': 'not ok'})


def user_register(request):
    name = request.POST['name']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    contact = request.POST['contact']
    pin = request.POST['pin']
    username = request.POST['username']
    password = request.POST['password']


    if User.objects.filter(username=username,email=email).exists():
        return JsonResponse({'status': 'Username is already existed'})

    user = User.objects.create(username=username, password=make_password(password), email=email, first_name=name)
    user.save()
    user.groups.add(Group.objects.get(name="Student"))

    var=Student_table()
    var.name=name
    var.email=email
    var.place=place
    var.post=post
    var.contact=contact
    var.pin=pin
    var.LOGIN=user
    var.save()
    return JsonResponse({'status': 'ok'})


def view_profile(request):
    lid=request.POST['lid']
    var=Student_table.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': 'ok',
                        'name':var.name,
                         'email':var.email,
                         'place':var.place,
                         'post':var.post,
                         'contact':str(var.contact),
                         'pin':str(var.pin),
                         })

def update_profile(request):
    lid = request.POST['lid']
    name = request.POST['name']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    contact = request.POST['contact']
    pin = request.POST['pin']


    var = Student_table.objects.get(LOGIN_id=lid)
    var.name = name
    var.email = email
    var.place = place
    var.post = post
    var.contact = contact
    var.pin = pin
    var.save()
    return JsonResponse({'status': 'ok'})

def view_online_exam(request):
    l=[]
    var=Exam_table.objects.all()
    for i in var:
        l.append({
             'id':str(i.id),
            'subject':str(i.subject.subject),
            'exam':str(i.exam),
            'date':str(i.date),
            'time':str(i.time),
        })
    return JsonResponse({'status': 'ok','data':l})


def view_questions(request):
    exam=request.POST['exam']
    l=[]
    var=question_table.objects.filter(EXAM_id=exam)
    for i in var:
        l.append({
            'id':str(i.id),
            'STAFF':str(i.STAFF.name),
            'question':str(i.question),
            'option1':str(i.option1),
            'option2':str(i.option2),
            'option3':str(i.option3),
            'option4':str(i.option4),
            'answer':str(i.answer),
        })
    return JsonResponse({'status':'ok','data':l})


def view_studymaterial(request):
    materials = Studymaterial_table.objects.all()
    material_list = []
    for material in materials:
        staff_name = str(material.STAFF.name) if hasattr(material, 'STAFF') and material.STAFF else 'N/A'
        material_list.append({
            'id': str(material.id),
            'staff': staff_name,
            # 'studymaterial':request.build_absolute_uri(material.studymaterial.url),
            'studymaterial':str(material.studymaterial.url),
            'date': str(material.date),
        })
    print(material_list,'===============================')
    return JsonResponse({'status': 'ok', 'data': material_list})

# def view_complaint(request):
#     print(request.POST,"kkkkkk")
#     lid=request.POST['lid']
#
#     l=[]
#     var=Complaint_table.objects.filter(STUDENT__LOGIN_id=lid)
#     print(var,"lllllllllll")
#     for i in var:
#         l.append({
#             'id': str(i.id),
#             'complaint':str(i.complaint),
#             'date':str(i.date),
#             'reply':str(i.reply),
#
#         })
#     return JsonResponse({'status':'ok','data':l})



from django.http import JsonResponse
from .models import Complaint_table

def view_complaint(request):
    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({'status': 'error', 'message': 'lid required'})

    complaints = Complaint_table.objects.filter(STUDENT__LOGIN_id=lid)

    data = []
    for i in complaints:
        data.append({
            'id': i.id,
            'complaint': i.complaint,
            'date': i.date.strftime('%Y-%m-%d'),
            'reply': i.reply if i.reply else 'pending',
        })

    return JsonResponse({'status': 'ok', 'data': data})



def send_complaint(request):
    print(request.POST,"kkkkkk")
    lid=request.POST['lid']
    complaint=request.POST['complaint']
    var = Complaint_table()
    var.STUDENT = Student_table.objects.get(LOGIN_id=lid)
    var.complaint = complaint
    var.date = datetime.now().today()
    var.reply = "pending"
    var.save()
    return JsonResponse({'status':'ok'})



def send_feedback(request):
    lid=request.POST['lid']
    feedback=request.POST['feedback']
    var = Feedback_table()
    var.STUDENT = Student_table.objects.get(LOGIN_id=lid)
    var.feedback = feedback
    var.date = datetime.now().today()

    var.save()
    return JsonResponse({'status':'ok'})



def send_review_rating(request):
    lid=request.POST['lid']
    review=request.POST['review']
    rating=request.POST['rating']
    var= review_table()
    var.review=review
    var.STUDENT=Student_table.objects.get(LOGIN_id=lid)
    var.rating=rating
    var.date = datetime.now().today()

    var.save()
    return JsonResponse({'status': 'ok'})


def feed(request):
    lid=request.POST['lid']
    review=request.POST['review']
    rating=request.POST['rating']
    var= review_table()
    var.review=review
    var.STUDENT=Student_table.objects.get(LOGIN_id=lid)
    var.rating=rating
    var.date = datetime.now().today()

    var.save()
    return JsonResponse({'status': 'ok'})



def view_staff(request):
    l=[]
    var=Staff_table.objects.all()
    for i in var:
        l.append({
            'id':str(i.id),
            'name':str(i.name),
            'email':str(i.email),
            'contact':str(i.contact),
            'LOGIN':str(i.LOGIN.id),

        })
    return JsonResponse({'status':'ok','data':l})







def tuto_chat_to_user(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Student_table.objects.get(LOGIN=cid)
    print(qry.LOGIN.id,'login----------')

    return render(request, "staff/Chat.html", { 'name': qry.name, 'toid': cid})
    # return render(request, "shop/Chat.html", {'photo': qry.image, 'name': qry.name, 'toid': cid})

def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = Student_table.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q
    res = chat_table.objects.filter(Q(FROM_ID_id=fromid, TO_ID_id=toid) | Q(FROM_ID_id=toid, TO_ID_id=fromid)).order_by('id')
    l = []
    print(qry.name,'userssssssssss')

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_ID_id, "date": i.date, "from": i.FROM_ID_id})
    # return JsonResponse({'photo': qry.image, "data": l, 'name': qry.name, 'toid': request.session["userid"]})
    return JsonResponse({ "data": l, 'name': qry.name, 'toid': request.session["userid"]})








def chat_send(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = chat_table()
    chatobt.message = message
    chatobt.TO_ID_id = toid
    chatobt.FROM_ID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({'status':'ok'})



def user_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]    from django.db.models import Q
    res = chat_table.objects.filter(Q(FROM_ID_id=fromid, TO_ID_id=toid) | Q(FROM_ID_id=toid, TO_ID_id=fromid)).order_by("id")
    l = []
    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_ID_id, "date": i.date, "to": i.TO_ID_id})
    return JsonResponse({"status":"ok",'data':l})

def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=chat_table()
    c.FROM_ID_id=FROM_id
    c.TO_ID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})

@csrf_exempt
def change_password(request):
    if request.method == "POST":
        try:
            lid = request.POST.get("lid")
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            user = User.objects.get(id=lid)
            if not user.check_password(current_password):
                return JsonResponse({"status": "error", "message": "Current password is incorrect"})
            # update password
            user.set_password(new_password)
            user.save()
            return JsonResponse({"status": "ok", "message": "Password changed successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

def androidattendexam(request):
    lid=request.POST['lid']
    exam_id=request.POST['examId']
    ob=question_table.objects.filter(EXAM=exam_id)
    print(lid)
    print(exam_id)
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        # obb=result_table.objects.filter(STUDENT=i.id)
        # if len(obb)==0:
        data = {
            'question': i.question,
            'option1': i.option1,
            'option2': i.option2,
            'option3': i.option3,
            'option4': i.option4,
            'answer':i.answer,
            'examid':i.EXAM.id,
            'staffid':i.STAFF.id,
            'id': i.id
        }
        mdata.append(data)
    print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})


import subprocess
from collections import Counter

@csrf_exempt
def savestudentanswer(request):
    print(request.FILES)
    if request.method == 'POST':
        if True:
        # try:
            print(request.POST,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            student_id = request.POST['student_id']
            question_id = request.POST['question_id']
            qq = question_table.objects.get(id=question_id)
            exam_id=qq.EXAM
            photo = request.FILES['photo']
            fs=FileSystemStorage()
            fn=fs.save(photo.name,photo)
            # Dynamically resolve media path relative to project root
            _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(_PROJECT_ROOT, "media", fn)
            res = objdet(fn)
            print("==============================")
            print("Object Detection Results:", res)
            print("==============================")
            counter = Counter(res)
            pc = counter.get('person', 0)
            print("res", res)
            if pc > 1:
                ob=malpratice()
                ob.STUDENT=Student_table.objects.get(LOGIN_id=student_id)
                ob.EXAM=Exam_table.objects.get(id=exam_id.id)
                ob.QUESTION = question_table.objects.get(id=question_id)
                ob.malpratice='Multi person detected'
                ob.date = datetime.today()
                ob.save()
                return JsonResponse({"status": "na", "data": 'Multi person detected',
                                     "message": 'Multi person detected'})
            if 'laptop' in res or 'cell phone' in res or 'tvmonitor' in res:
                ob = malpratice()
                ob.STUDENT = Student_table.objects.get(LOGIN_id=student_id)
                ob.EXAM = Exam_table.objects.get(id=exam_id.id)
                ob.QUESTION = question_table.objects.get(id=question_id)
                ob.malpratice = "Objects detected"
                ob.date = datetime.today()
                ob.save()
                return JsonResponse({"status": "na", "data": "Objects detected",
                                     "message": "Objects detected"})

            print("+++ Head pose verification starting +++")
            print(image_path)
            import sys
            _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            hp = subprocess.run([
                sys.executable,
                os.path.join(_PROJECT_ROOT, 'headpose.py')
            ], input=image_path.encode('utf-8')

            )
            print("aaaaaaaaaaaaaaaaaaaa")

            with open(os.path.join(_PROJECT_ROOT, 'sample.txt'), 'r') as file:
                content = file.read()
                print(content)
            print("completed")
            # head_pose_result = hp.stdout.strip()
            print("Head Pose:", content)
            if content != "Facing Forward":
                ob = malpratice()
                ob.STUDENT = Student_table.objects.get(LOGIN_id=student_id)
                ob.EXAM = Exam_table.objects.get(id=exam_id.id)
                ob.QUESTION = question_table.objects.get(id=question_id)
                ob.malpratice = f"Invalid head direction: {content}"
                ob.date = datetime.today()
                ob.save()
                return JsonResponse({"status": "na", "data": f"Invalid head direction: {content}","message":f"Invalid head direction: {content}"})

            question_id = request.POST['question_id']
            student_id = request.POST['student_id']
            selected_answer = request.POST['answer']
            question = question_table.objects.get(id=question_id)
            student = Student_table.objects.get(LOGIN_id=student_id)
            is_correct = selected_answer == question.answer
            mark = 1 if is_correct else 0
            existing = result_table.objects.filter(QUESTION=question, STUDENT=student)
            if existing.exists():
                return JsonResponse({"status": "error", "message": "Answer already submitted"})
            result_table.objects.create(
                QUESTION=question,
                STUDENT=student,
                mark=mark
            )
            return JsonResponse({"status": "ok", "message": "Answer saved", "correct": is_correct})
        # except Exception as e:
        #     return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})