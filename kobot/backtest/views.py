from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import StaticHTMLRenderer
from .bolidngerband import BackTestBollingerBand
import os

from backtest.models import Candle
# Create your views here.
def home(request):
    return render(request, 'home.html')

# mtv
# 

# market, riskRate, std, from, to
# @api_view(['GET'])
class Backtest(APIView):

    renderer_classes = [StaticHTMLRenderer]

    def get(self, request):
        try :
            print("##########")
            movingAverage = int(request.GET['movingAverage'])
            market = request.GET['market']
            riskRate = float(request.GET['riskRate'])
            std = float(request.GET['std'])
            
            filePath = BackTestBollingerBand(movingAverage, std, riskRate)
            f = open(filePath)
            body = f.read()
            os.remove(filePath)
            
            print("##########")
            dic = { 'date_time_kst' : [], 'trade_price' : []}
            Candle.objects.all()
            for c in Candle.objects.raw(
                """
                Select id, trade_price, date_time_kst
                    From candle 
                    Where market = %s and time_unit='DAY'
                    order by date_time_kst
                """, [market]):
                dic['trade_price'].append(float(c.trade_price))
                dic['date_time_kst'].append(c.date_time_kst.strftime("%Y-%m-%d %H:%M:%S"))
            response = Response(body)
            response["Access-Control-Allow-Origin"] = "*"
            return response # 파일명 반환 -> 다시 요청
        except Exception as e:
            print(e)
            return Response(status=400)
