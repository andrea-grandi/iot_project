import pandas as pd
from prophet import Prophet
import plotly.express as px
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

class Prediction():
    def load_dataset(self, dataset):
        try:
            with open(dataset) as file:
                df = pd.read_csv(file, sep=',')
                df['ds'] = pd.to_datetime(df['Data'])
                df = df[['ds', 'Pericolosita']]  
                df.rename(columns={'Pericolosita': 'y'}, inplace=True) 
        except FileNotFoundError:
            print("File not found")
            return None
        
        return df
    
    def make_prediction(self, df, time_dataset):
        model = Prophet(daily_seasonality=True)
        model.add_country_holidays(country_name='IT')
        model.fit(df)
        
        future = pd.DataFrame({'ds': pd.date_range(start=df['ds'].iloc[0], periods=30)})  
        forecast = model.predict(future)
        forecast[['yhat']] = forecast[['yhat']]#.round(0).astype('int32')
        pred_df = forecast[['ds', 'yhat']].rename(columns={'yhat': 'y'})

        return pred_df

if __name__ == '__main__':
    prediction = Prediction()
    df = prediction.load_dataset("dataset_test.csv")
    
    if df is not None:
        timestamp = dt.now()
        time_dataset = timestamp.strftime('%Y-%m-%d')
        
        pred = prediction.make_prediction(df, time_dataset)
        print(pred)
        fig = px.line(pred, x='ds', y='y')
        fig.show()

