from core.serializers import *
from rest_framework.views import APIView, Response
from core.models import *



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            seriz = LoginSerializer(user)
            return Response({'result': '1', 'data': seriz.data, 'message': '登录成功'})
        return Response({'result': '0', 'message': '用户名或密码错误'})
