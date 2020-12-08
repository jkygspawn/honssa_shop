import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator

from .models import *

def admin_login(request):
    if request.method == 'POST':
        if request.POST["id"] == "" or request.POST["password"] == "":
            return render(request, 'admin/login.html', {})

        id = request.POST["id"]
        password = request.POST["password"]
        print(id, password)
        if User.objects.get(username=id).is_superuser is True:
            user = auth.authenticate(request, username=id, password=password)
            if user is not None:
                print('로그인')
                login(request, user)
                return redirect("admin:admin_main")

    return render(request, 'admin/login.html', {})

def admin_logout(request):
    logout(request)
    return redirect("admin:admin_login")

def admin_index(request):
    m2m = m2mfaq_tbl.objects.order_by('comment_write_date')
    day = []
    pay = 0
    cnt = 0
    now = datetime.datetime.now()
    nowdate = now.strftime('%Y-%m-%d')

    for a in order_tbl.objects.all():
        day.append(a.order_date.strftime('%Y-%m-%d'))
        if a.order_date.strftime('%Y-%m-%d') == nowdate:
            pay += a.order_price
            cnt += 1

    pay_fin = order_tbl.objects.filter(order_pay_status = 6)
    # for i in day:
    #     if i == nowdate:
    #         cnt += 1

    content = {'day': day, 'now': nowdate, 'cnt': cnt, 'pay': pay, 'fin': pay_fin, 'm2m_list': m2m}

    return render(request, 'admin/index.html', content)

@login_required
def member_manage(request):

    # member_tbl 테이블의 모든 레코드를 불러온다
    search_list = member_tbl.objects.all()

    # search_option 을 option 에 저장
    option = request.GET.get('search_option')

    # search_key 를 search_key 에 저장
    search_key = request.GET.get('search_key')

    if option == 'rank':
        search_list = search_list.filter(member_rank__icontains=search_key)
    elif option == 'name':
        search_list = search_list.filter(member_name__icontains=search_key)
    elif option == 'userid':
        search_list = search_list.filter(member_id__icontains=search_key)
    elif option == 'email':
        search_list = search_list.filter(member_email__icontains=search_key)
    elif option == 'phone_number':
        search_list = search_list.filter(member_contact_number__icontains=search_key)
    elif option == 'reg_date':
        search_list = search_list.filter(member_join_date__icontains=search_key)
    else:
        search_list

    paginator = Paginator(search_list, 10)  # member_tbl 테이블의 모든 레코드를 페이지네이터에서 10개씩 저장한다.
    page = request.GET.get('page')  # request된 page를 저장한다
    search_list = paginator.get_page(page)  # request된 page의 레코드를 저장한다

    # search_list 에 member_join_date 날짜를 '%Y/%m/%d' 형식으로 출력
    for a in search_list:
        a.member_join_date = a.member_join_date.strftime('%Y-%m-%d')

    return render(request, 'admin/member_manage.html',
                  {'search_list':search_list})
#
@login_required
def member_update(request, id):
    # member_tbl 에 있는 데어터를 해당 id 를 통해서 info 에 저장
    info = member_tbl.objects.get(id=id)

    # member_rank 는 비어있으면 안돼기 때문에 'POST' 로 이용한다.
    # 'GET' 은 처음부터 비어있는 상태로 적용을 시키려 하기 때문에 오류가 난다.
    # 반면 'POST' 는 그렇지 않기 때문에 오류가 나지 않는다.
    if request.method == 'POST':
        info.member_rank = request.POST['rank_edit']
        info.save()

    info.member_join_date = info.member_join_date.strftime('%Y/%m/%d')
    return render(request, 'admin/member_update.html', {'info':info})

@login_required
def faq_manage(request):

    # m2mfaq_tbl 테이블의 모든 레코드를 불러온다
    faqs = m2mfaq_tbl.objects.all()

    # 비어있는 리스트를 생성
    names = []

    # 비어있는 리스트에 추가
    for i in faqs:
        names.append(member_tbl.objects.get(id=i.member_number_id).member_name)
    print(names)

    # m2mfaq_tbl 테이블의 모든 레코드를 페이지네이터에서 10개씩 저장한다.
    paginator = Paginator(faqs, 10)
    # request된 page를 저장한다
    page = request.GET.get('page')
    # request된 page의 레코드를 저장한다
    faqlists = paginator.get_page(page)

    # 문의목록에 있는 작성 날짜의 형식을 '%Y-%m-%d' 으로 바꾼다
    for a in faqs:
        a.comment_write_date = a.comment_write_date.strftime('%Y-%m-%d')

    return render(request, 'admin/faq_manage.html',
                  {'faqs':faqs, 'faqlists':faqlists})
#

@login_required
def answer_window(request, id): # answer_window 함수

    # m2mfaq_tbl 에 있는 데어터를 id 를 통해서 question 에 저장
    question = m2mfaq_tbl.objects.get(id=id)

    # member_tbl 에 있는 데어터를 question 안에 있는
    #  member_number_id 를 통해서 user 에 저장
    user = member_tbl.objects.get(id=question.member_number_id)

    # request 의 method 가 POST 라면
    if request.method == 'POST':

        # reply_box 를 POST 로 reply 에 저장
        reply = request.POST['reply_box']

        try:
            # faq_answer_tbl 에 있는 question 이 저장된 comment_number 를
            # data 에 저장
            data = faq_answer_tbl.objects.get(comment_number=question)

            # reply 를 data 안에 있는 answer_description 에 저장
            data.answer_description = reply
            data.save() # reply 에 입력한 값을 data 에 저장

        except:
            # faq_answer_tbl 에 있는;
            # reply 를 answer_description 에 저장,
            # '관리자' 라는 이름으로 answer_writer 에 저장
            # question 을 comment_number 에 저장
            new_data = faq_answer_tbl(
                answer_description = reply,
                answer_writer = '관리자',
                comment_number = question
            )
            new_data.save() # 입력한 값을 new_data에 저장

            # 문의에 답변을 했을 경우
            # 답변 상태의 값을 0 에서 1 로 변경
            question.comment_status = 1
            question.save()

    try:
        answer = faq_answer_tbl.objects.get(comment_number=question)
    except:
        return render(request, 'admin/answer_window.html',
                      {'question': question, 'user': user})

    return render(request, 'admin/answer_window.html',
                  {'question': question, 'user': user, 'answer': answer})
# Create your views here.
