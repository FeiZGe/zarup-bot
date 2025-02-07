from statsmodels.tsa.arima.model import ARIMA

def predict_future_complaints(data, province):
    """พยากรณ์จำนวนเรื่องร้องทุกข์ในอนาคต"""
    filtered_data = data[data['province'] == province]
    model = ARIMA(filtered_data['Total'], order=(5, 1, 0))
    model_fit = model.fit()
    prediction = model_fit.forecast(steps=1)
    return prediction[0]