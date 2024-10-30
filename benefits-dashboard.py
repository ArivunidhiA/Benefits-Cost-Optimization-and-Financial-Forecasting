import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv('data/insurance.csv')
    # Add date column for time series analysis
    dates = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    df['date'] = dates
    return df

def calculate_metrics(df):
    metrics = {
        'avg_cost': df['charges'].mean(),
        'total_cost': df['charges'].sum(),
        'cost_per_smoker': df[df['smoker'] == 'yes']['charges'].mean(),
        'cost_per_non_smoker': df[df['smoker'] == 'no']['charges'].mean(),
        'avg_age': df['age'].mean(),
        'total_beneficiaries': len(df)
    }
    return metrics

def forecast_costs(df, periods=12):
    # Prepare data for Prophet
    forecast_df = df.groupby('date')['charges'].sum().reset_index()
    forecast_df.columns = ['ds', 'y']
    
    model = Prophet(yearly_seasonality=True)
    model.fit(forecast_df)
    
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)
    return forecast

def main():
    st.set_page_config(page_title="Benefits Cost Optimization Dashboard", layout="wide")
    st.title("Benefits Cost Optimization and Financial Forecasting Dashboard")
    
    # Load data
    df = load_data()
    metrics = calculate_metrics(df)
    
    # Sidebar for filters and controls
    st.sidebar.header("Controls")
    age_range = st.sidebar.slider("Age Range", min_value=int(df['age'].min()), 
                                max_value=int(df['age'].max()), 
                                value=(25, 60))
    
    deductible_impact = st.sidebar.slider("Simulate Deductible Change (%)", 
                                        min_value=-50, max_value=50, value=0)
    
    # Filter data based on selections
    filtered_df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Cost per Employee", f"${metrics['avg_cost']:,.2f}")
    with col2:
        st.metric("Total Benefits Cost", f"${metrics['total_cost']:,.2f}")
    with col3:
        st.metric("Total Beneficiaries", f"{metrics['total_beneficiaries']:,}")
    with col4:
        st.metric("Average Age", f"{metrics['avg_age']:.1f}")
    
    # Cost Distribution
    st.subheader("Cost Distribution Analysis")
    fig_dist = px.histogram(filtered_df, x='charges', 
                          title='Distribution of Benefits Costs',
                          labels={'charges': 'Cost ($)', 'count': 'Frequency'})
    st.plotly_chart(fig_dist)
    
    # Cost Forecast
    st.subheader("Cost Forecast")
    forecast = forecast_costs(filtered_df)
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
                                    name='Forecast',
                                    line=dict(color='blue')))
    fig_forecast.add_trace(go.Scatter(x=forecast['ds'], 
                                    y=forecast['yhat_upper'],
                                    fill=None,
                                    mode='lines',
                                    line=dict(color='rgba(0,0,255,0)'),
                                    showlegend=False))
    fig_forecast.add_trace(go.Scatter(x=forecast['ds'], 
                                    y=forecast['yhat_lower'],
                                    fill='tonexty',
                                    mode='lines',
                                    line=dict(color='rgba(0,0,255,0)'),
                                    name='Confidence Interval'))
    st.plotly_chart(fig_forecast)
    
    # Cost Drivers Analysis
    st.subheader("Cost Drivers Analysis")
    col1, col2 = st.columns(2)
    with col1:
        fig_age = px.scatter(filtered_df, x='age', y='charges',
                           title='Cost vs Age',
                           labels={'charges': 'Cost ($)', 'age': 'Age'})
        st.plotly_chart(fig_age)
    
    with col2:
        avg_cost_by_smoker = filtered_df.groupby('smoker')['charges'].mean()
        fig_smoker = px.bar(avg_cost_by_smoker,
                           title='Average Cost by Smoking Status',
                           labels={'value': 'Average Cost ($)', 
                                 'smoker': 'Smoking Status'})
        st.plotly_chart(fig_smoker)
    
    # ROI Analysis
    st.subheader("ROI Analysis")
    st.write("""
    Return on Investment (ROI) is calculated by comparing the cost savings from 
    preventive care programs against the program implementation costs.
    """)
    
    # Simulated cost impact
    if deductible_impact != 0:
        original_cost = filtered_df['charges'].mean()
        new_cost = original_cost * (1 + deductible_impact/100)
        cost_difference = new_cost - original_cost
        st.metric("Impact of Deductible Change", 
                 f"${cost_difference:,.2f}",
                 delta=f"{deductible_impact}%")

if __name__ == "__main__":
    main()
