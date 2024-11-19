import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Loading the data
def load_data():
  # Money Market Funds data
    mmf_data = {
    'Fund': [
        'Cytonn Money Market Fund', 
        'Lofty Corban Money Market Fund', 
        'Etica Money Market Fund', 
        'ArvoCap Money Market Fund', 
        'Kuza Money Market Fund', 
        'GenAfrica Money Market Fund', 
        'Nabo Africa Money Market Fund', 
        'Jubilee Money Market Fund', 
        'Madison Money Market Fund', 
        'Co-op Money Market Fund', 
        'KCB Money Market Fund', 
        'Sanlam Money Market Fund', 
        'ABSA Shilling MMF', 
        'Enwealth Money Market Fund', 
        'Mail Money Market Fund', 
        'Mayfair Money Market Fund', 
        'Faulu Money Market Fund', 
        'Orient Kasha Money Market Fund', 
        'Genghis Money Market Fund', 
        'African Alliance Kenya Money Market Fund', 
        'Dry Associates Money Market Fund', 
        'Old Mutual Money Market Fund', 
        'Apollo Money Market Fund', 
        'CIC Money Market Fund', 
        'ICEA Lion Money Market Fund', 
        'British-American Money Market Fund', 
        'Equity Money Market Fund'
    ],
    'Return': [
        18.07, 17.96, 17.11, 17.09, 16.88, 16.51, 15.66, 15.61, 15.43, 15.36, 15.17, 
        15.13, 15.03, 15.00, 15.01, 15.00, 14.86, 14.81, 14.74, 14.56, 14.39, 13.97, 
        13.91, 13.75, 13.61, 13.29, 13.23
    ]
}

  # SACCO data
    sacco_data = {
    'Name': [
        'MWALIMU NATIONAL', 'STIMA DT', 'KENYA NATIONAL POLICE DT', 'HARAMBEE', 'TOWER',
        'AFYA', 'UNAITAS', 'IMARISHA', 'UNITED NATIONS DT', 'UKULIMA',
        'HAZINA', 'GUSII MWALIMU', 'INVEST AND GROW', 'MENTOR', 'IMARIKA',
        'BANDARI DT', 'TRANSNATION', 'SAFARICOM', 'BORESHA', 'WINAS',
        'NEWFORTIS', 'KIMISITU'
    ],
    'Total_Assets': [
        66.43, 59.15, 54.24, 38.57, 23.23,
        22.79, 22.70, 21.78, 18.21, 15.18,
        14.76, 14.30, 14.06, 13.47, 13.11,
        12.68, 12.02, 11.72, 11.25, 11.28,
        10.67, 11.07
    ]
}

    
    return pd.DataFrame(mmf_data), pd.DataFrame(sacco_data)

def calculate_risk_score(answers):
    score = 0
    
    # Investment duration weight
    duration_weights = {
        'Less than 1 year': 1,
        '1-3 years': 2,
        '3-5 years': 3,
        'More than 5 years': 4
    }
    score += duration_weights.get(answers['investment_duration'], 0)
    
    # Emergency fund consideration
    if answers['emergency_fund'] == 'Yes':
        score -= 2
    
    # Withdrawal frequency weight
    withdrawal_weights = {
        'Very frequently (weekly)': 1,
        'Frequently (monthly)': 2,
        'Occasionally (quarterly)': 3,
        'Rarely (yearly or less)': 4
    }
    score += withdrawal_weights.get(answers['withdrawal_frequency'], 0)
    
    # Risk appetite weight
    risk_weights = {
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'High': 4,
        'Very High': 5
    }
    score += risk_weights.get(answers['risk_appetite'], 0) * 2  # Double weight for risk appetite
    
    return score

def get_investment_recommendations(risk_score, investment_amount):
    recommendations = []
    
    if risk_score <= 5:  # Very Conservative
        recommendations.append({
            'product': 'Money Market Funds',
            'allocation': 70,
            'description': 'Low risk, high liquidity, suitable for emergency funds',
            'recommended_providers': ['Cytonn MMF', 'Lofty Goshan MMF']
        })
        recommendations.append({
            'product': 'Fixed Deposits',
            'allocation': 30,
            'description': 'Low risk, stable returns, limited liquidity',
            'recommended_providers': ['Top tier banks']
        })
    
    elif risk_score <= 8:  # Conservative
        recommendations.append({
            'product': 'Money Market Funds',
            'allocation': 50,
            'description': 'Low risk, high liquidity',
            'recommended_providers': ['Cytonn MMF', 'Etica MMF']
        })
        recommendations.append({
            'product': 'SACCOs',
            'allocation': 30,
            'description': 'Moderate risk, good for loans',
            'recommended_providers': ['Mwalimu National', 'Stima DT']
        })
        recommendations.append({
            'product': 'Government Bonds',
            'allocation': 20,
            'description': 'Low risk, fixed income',
            'recommended_providers': ['Treasury Direct']
        })
    
    elif risk_score <= 12:  # Balanced
        recommendations.append({
            'product': 'Money Market Funds',
            'allocation': 30,
            'description': 'Low risk, emergency fund',
            'recommended_providers': ['Cytonn MMF', 'Kuza MMF']
        })
        recommendations.append({
            'product': 'SACCOs',
            'allocation': 30,
            'description': 'Moderate risk, loan access',
            'recommended_providers': ['Mwalimu National', 'Kenya Police DT']
        })
        recommendations.append({
            'product': 'Equity Funds',
            'allocation': 40,
            'description': 'Higher risk, growth potential',
            'recommended_providers': ['Top performing equity funds']
        })
    
    else:  # Aggressive
        recommendations.append({
            'product': 'Equity Funds',
            'allocation': 60,
            'description': 'High risk, high potential returns',
            'recommended_providers': ['Leading equity funds']
        })
        recommendations.append({
            'product': 'Money Market Funds',
            'allocation': 20,
            'description': 'Liquidity buffer',
            'recommended_providers': ['Cytonn MMF']
        })
        recommendations.append({
            'product': 'Dollar Funds',
            'allocation': 20,
            'description': 'Currency diversification',
            'recommended_providers': ['Top dollar funds']
        })
    
    return recommendations

def main():
    st.set_page_config(page_title="Investment Advisor", layout="wide")
    
    st.title("Investment Advisory System")
    st.write("Let us help you make informed investment decisions based on your profile.")
    
    # Load market data
    mmf_data, sacco_data = load_data()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Investment Profile", "Market Data", "About"])
    
    with tab1:
        st.header("Investment Profile Questionnaire")
        
        with st.form("investment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                investment_amount = st.number_input("How much do you plan to invest? (KES)", 
                                                  min_value=1000, 
                                                  value=10000)
                
                investment_duration = st.selectbox(
                    "How long do you plan to invest?",
                    ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"]
                )
                
                emergency_fund = st.radio(
                    "Is this an emergency fund account?",
                    ["Yes", "No"]
                )
            
            with col2:
                withdrawal_frequency = st.selectbox(
                    "How often do you plan to withdraw?",
                    ["Very frequently (weekly)", "Frequently (monthly)", 
                     "Occasionally (quarterly)", "Rarely (yearly or less)"]
                )
                
                risk_appetite = st.select_slider(
                    "What is your risk appetite?",
                    options=["Very Low", "Low", "Medium", "High", "Very High"]
                )
                
                investment_knowledge = st.select_slider(
                    "How would you rate your investment knowledge?",
                    options=["Beginner", "Intermediate", "Advanced"]
                )
            
            submitted = st.form_submit_button("Get Recommendations")
            
            if submitted:
                answers = {
                    'investment_duration': investment_duration,
                    'emergency_fund': emergency_fund,
                    'withdrawal_frequency': withdrawal_frequency,
                    'risk_appetite': risk_appetite
                }
                
                risk_score = calculate_risk_score(answers)
                recommendations = get_investment_recommendations(risk_score, investment_amount)
                
                st.success("Based on your profile, here are our recommendations:")
                
                # Display recommendations
                cols = st.columns(len(recommendations))
                for idx, (col, rec) in enumerate(zip(cols, recommendations)):
                    with col:
                        st.markdown(f"### {rec['product']}")
                        st.markdown(f"**Allocation: {rec['allocation']}%**")
                        st.markdown(f"Amount: KES {investment_amount * rec['allocation']/100:,.2f}")
                        st.markdown(f"*{rec['description']}*")
                        st.markdown("**Recommended Providers:**")
                        for provider in rec['recommended_providers']:
                            st.markdown(f"- {provider}")
                
                # Create and display allocation pie chart
                allocation_data = pd.DataFrame([
                    {'Product': r['product'], 'Allocation': r['allocation']}
                    for r in recommendations
                ])
                
                fig = px.pie(allocation_data, 
                           values='Allocation', 
                           names='Product',
                           title='Recommended Portfolio Allocation')
                st.plotly_chart(fig)
    
    with tab2:
        st.header("Current Market Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Money Market Funds")
            st.dataframe(mmf_data)
            
            # Create bar chart for MMF returns
            fig = px.bar(mmf_data, 
                        x='Fund', 
                        y='Return',
                        title='Money Market Fund Returns (%)')
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Top SACCOs by Total Assets")
            st.dataframe(sacco_data)
            
            # Create bar chart for SACCO assets
            fig = px.bar(sacco_data, 
                        x='Name', 
                        y='Total_Assets',
                        title='SACCO Total Assets (Billion KES)')
            st.plotly_chart(fig)
    
    with tab3:
        st.header("About the Investment Advisor")
        st.write("""
        This investment advisory system helps you make informed investment decisions based on your:
        - Investment timeline
        - Risk tolerance
        - Liquidity needs
        - Emergency fund requirements
        
        The system provides personalized recommendations across various investment products including:
        - Money Market Funds
        - SACCOs
        - Fixed Deposits
        - Government Bonds
        - Equity Funds
        - Dollar Funds
        
        All recommendations are based on current market data and best practices in financial planning.
        """)

if __name__ == "__main__":
    main()