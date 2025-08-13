from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from rest_framework import status
from rest_framework.response import Response
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error,r2_score


# Create your views here.

class StockPredictionAPIView(APIView):
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            #fetch the data from yfinance
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            if df.empty:
                return Response({"error": "No data found for the given ticker", "status": status.HTTP_404_NOT_FOUND})
            df = df.reset_index()
            print(df)

            #generate basic plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5));
            plt.plot(df.Close, label='Closing Price');
            plt.title(f'Closing price of {ticker}');
            plt.xlabel('Days');
            plt.ylabel('Close Price');
            plt.legend()
            
            #SAVE THE PLOT TO A FILE
            plot_img_path = f'{ticker}_plot.png'
            plot_img = save_plot(plot_img_path)

            # 100 days moving avg.
            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5));
            plt.plot(df.Close, label='Closing Price');
            plt.plot(ma100, 'r', label='100Days moving avg.')
            plt.title(f'100 days moving avg. of {ticker}');
            plt.xlabel('Days');
            plt.ylabel('Price');
            plt.legend()
            plot_img_path = f'{ticker}_100_dma.png'
            plot_100_dma = save_plot(plot_img_path)


            # 200 days moving avg.
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5)); 
            plt.plot(df.Close, label='Closing Price');
            plt.plot(ma100, 'r', label='100Days moving avg.')
            plt.plot(ma200, 'g', label='200Days moving avg.')
            plt.title(f'200 days moving avg. of {ticker}');
            plt.xlabel('Days');
            plt.ylabel('Price');
            plt.legend()
            plot_img_path = f'{ticker}_200_dma.png'
            plot_200_dma = save_plot(plot_img_path)


            # spliting data into training and testing 70% & 30%
            dataTraining = pd.DataFrame(df.Close[0:int(len(df)*0.7)]) 
            dataTesting = pd.DataFrame(df.Close[int(len(df)*0.7) : int(len(df))])

            # scaling down the data B/W 0 and 1.
            scaler = MinMaxScaler(feature_range = (0,1))

            #Load the model using keras
            model = load_model('stock_prediction_model.keras')
            
            #preparing test data
            pastHunderedDays = dataTraining.tail(100)
            final_df = pd.concat([pastHunderedDays, dataTesting], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100 : i])
                y_test.append(input_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            #making prediction
            y_predicted = model.predict(x_test)

            #Revert the scaled prices to original prices
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1,1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1,1)).flatten() 
            print('y_predicted=>', y_predicted)
            print('y_test=>', y_test)

            #plot the final prediction
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5)); 
            plt.plot(y_test, 'b', label='Original Price');
            plt.plot(y_predicted, 'r', label='Predicted price')
            plt.title(f'final prediction for {ticker}');
            plt.xlabel('Days');
            plt.ylabel('Price');
            plt.legend()
            plot_img_path = f'{ticker}_Final_prediction.png'
            plot_prediction= save_plot(plot_img_path)

            #Model Evaluation
            #Mean Square Error(MSE)
            mse = mean_squared_error(y_test, y_predicted)
            # root mean squared error RMSE: lower is good
            rmse = np.sqrt(mse)
            # R-Squared: it must be b/w 0&1
            r2 = r2_score(y_test, y_predicted)


            return Response({'status' : 'success',
                             'plot_img' : plot_img,
                             'plot_100_dma' : plot_100_dma,
                             'plot_200_dma' : plot_200_dma,
                             'plot_prediction' : plot_prediction,
                             'mse' : mse,
                             'rmse' : rmse,
                             'r2' : r2,
                             })

