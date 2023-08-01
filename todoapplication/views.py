import json

from django.shortcuts import render
from django.views import View
#클래스의 get, post, put, delete 메서드가 각 요청 방식을 처리함
from .models import Todo
# JSON 응답을 만들기 위한 import
from django.http import JsonResponse
from rest_framework import status
import datetime # 날짜 사용을 위한 import
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class TodoView(View):
    # get 요청 처리
    def get(self,request):
        # 파라미터 읽어오기
        # userid가 없다면 none
        userID=request.GET.get("userID", None)
        if userID !=None:
            todos=Todo.objects.filter(userID=userID)
        else:
            todos=Todo.objects.all()
        # Json 응답, list라는 키로 검색된 데이터를 list로 전달
        return JsonResponse({'list':list(todos.values())},status=status.HTTP_200_OK)
    # post 요청 처리
    # post는 숨겨서 보내야 하기 때문에, url에서 사용을 못하니, 서버가 동작하는지 확인하고
    # 클라이언트를 만들어서 확인을 하던가 해야 한다.
    def post(self, request):
        # 파라미터 읽기
        params=json.loads(request.body)
        userID=params["userID"]
        title=params["title"]
        #삽입할 객체 생성
        todo=Todo()
        todo.userID=userID
        todo.title=title
        todo.done=False
        #regdate는 auto 현재 날짜이지만, moddate는 없으니 설정
        todo.moddate=datetime.datetime.today()
        #데이터 저장
        todo.save()
        #삽입 후 결과 처리
        #일반 적으로 삽입한 데이터만 리턴하거나, 아니면
        #전체 데이터 리턴 방식이 존재함 이건 프로젝트에 따라 다를 것이다.
        #나는 삽입한 데이터 하나만 리턴할래
        todos = Todo.objects.filter(userID=userID)
        # Json 응답, list라는 키로 검색된 데이터를 list로 전달
        return JsonResponse({'list': list(todos.values())}, status=status.HTTP_200_OK)

    def put(self, request):
        # 1단계 클라이언트의 파라미터 읽기
        params=json.loads(request.body)
        id=params["id"]
        userID=params["userID"]
        done=params["done"]
        # 2단계 서버에서의 처리
        # 여기서 데이터베이스 작업 이외의 작업을 한다면,
        # 별도의 클래스를 만들어서 처리한 후 리턴받아서 다음 작업을 수행
        # id에 해당하는 데이터를 찾아서 done의 값을 수정하는 것이다.
        # get은 하나만, filter는 여러개 return
        todo=Todo.objects.get(id=id)
        todo.done=done
        # 수정한 날짜를 기록하고 싶어.
        todo.moddate=datetime.datetime.today()
        todo.save()
        # 3단계 응답 만들기
        # 1개 줄거야? 아니면 전체 다 줄거야?
        todos = Todo.objects.filter(userID=userID)
        # Json 응답, list라는 키로 검색된 데이터를 list로 전달
        return JsonResponse({'list': list(todos.values())}, status=status.HTTP_200_OK)

    def delete(self, request):
        # 파라미터 읽기
        params = json.loads(request.body)
        id = params["id"]
        # 데이터 가져오기
        todo = Todo.objects.get(id=id)
        # 데이터 삭제하기
        todo.delete()
        # 응답 만들기
        todos = Todo.objects.all()
        # Json 응답, list라는 키로 검색된 데이터를 list로 전달
        return JsonResponse({'list': list(todos.values())}, status=status.HTTP_200_OK)