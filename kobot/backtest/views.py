from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import StaticHTMLRenderer

from backtest.CandleRepository import *
from backtest.BacktestService import *

def home(request):
    return render(request, 'home.html')

# @api_view(['GET'])
class Backtest(APIView):

    # renderer_classes = [StaticHTMLRenderer]

    def get(self, request):
        try :
            market = request.GET['market']
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
            upperMovingAverage = int(request.GET['upperMovingAverage'])
            lowerMovingAverage = int(request.GET['lowerMovingAverage'])
            upperK = float(request.GET['upperK'])
            lowerK = float(request.GET['lowerK'])
            riskRate = float(request.GET['riskRate'])
            timeFrame = request.GET['timeFrame']

            response = getBody(market, startDate, endDate, upperMovingAverage, lowerMovingAverage, upperK, lowerK, riskRate, timeFrame)
            response["Access-Control-Allow-Origin"] = "*"
            return response
        except Exception as e:
            print(e)
            return Response(status=400)
