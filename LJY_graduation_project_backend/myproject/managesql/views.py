from django.conf import settings
import pymysql
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TrainingInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 使用settings中的数据库配置信息
        connection = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                                     user=settings.DATABASES['default']['USER'],
                                     password=settings.DATABASES['default']['PASSWORD'],
                                     database=settings.DATABASES['default']['NAME'],
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # 获取所有training_info信息
                sql = "SELECT * FROM training_info"
                cursor.execute(sql)
                result = cursor.fetchall()
                return Response(result)
        finally:
            connection.close()