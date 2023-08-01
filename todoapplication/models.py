from django.db import models

class Todo(models.Model) : # model 클래스로부터 상속 받도록
    id=models.AutoField(primary_key=True) # Auto_increment
    userID=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    done=models.BooleanField()
    regdate=models.DateTimeField(auto_now_add=True)# 작성 날짜 자동
    moddate=models.DateTimeField()
    #계정을 delete = 1 이렇게 해서 휴면계정을 설정할 수 있다.