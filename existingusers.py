import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Set page configuration
st.set_page_config(
    page_title="Investment Portfolio Recommender",
    page_icon="💰",
    layout="wide"
)

# Custom CSS to improve the appearance
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .recommendation-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .message-card {
        background-color: #e1e5eb;
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the saved models and data
@st.cache_resource
def load_models():
    try:
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        with open('tfidf.pkl', 'rb') as file:
            tfidf = pickle.load(file)
        df = pd.read_csv('investment_member.csv')
        return model, tfidf, df
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None

def get_recommendations_with_messages(member_features, df, member_data, n=5):
    """
    Modified version of get_recommendations_with_messages that works with input data
    instead of looking up from DataFrame
    """
    recommended_products = []
    messages = []
    
    # Extract member details from input data
    member_beneficiery_age = member_data.get('beneficiary_age')
    member_age_group = member_data.get('age_group')
    member_town = member_data.get('town')
    member_gender = member_data.get('gender')
    member_current_products = set(member_data.get('current_products', []))

    # Rule 1: Beneficiary age recommendations
    if member_beneficiery_age is not None:
        if 18 <= member_beneficiery_age <= 25:
            recommended_products.append("Student Account")
            messages.append(
                "Planning for your child's future? Our Student Account is perfect for "
                "young adults aged 18-25. Start securing their educational journey today!"
            )
        elif member_beneficiery_age < 18:
            recommended_products.append("Junior Account")
            messages.append(
                "Give your child a head start with our Junior Account! It's specially designed "
                "for children under 18 to help them develop good financial habits early."
            )

    # Rule 2: Age group recommendations
    age_group_products = (
        df[df['age_group'] == member_age_group]
        .portfolio_map.value_counts()
        .index
        .tolist()
    )
    for product in age_group_products:
        if product not in member_current_products and product not in recommended_products:
            recommended_products.append(product)
            if len(recommended_products) >= n:
                break

    if age_group_products:
        messages.append(
            f"Members in your age group are enjoying these popular products: "
            f"{', '.join(age_group_products[:3])}. Join them in making smart financial choices!"
        )

    # Rule 3: Location-based recommendations
    town_products = (
        df[df['town'] == member_town]
        .portfolio_map.value_counts()
        .index
        .tolist()
    )
    for product in town_products:
        if product not in member_current_products and product not in recommended_products:
            recommended_products.append(product)
            if len(recommended_products) >= n:
                break

    if town_products:
        messages.append(
            f"Trending in {member_town}! Your neighbors are choosing "
            f"{', '.join(town_products[:3])}. Discover why these products are popular in your community!"
        )

    # Final personalized message
    if recommended_products:
        messages.append(
            f"💡 Pro tip: Adding {', '.join(recommended_products[:n])} to your portfolio "
            f"could help you achieve your financial goals faster!"
        )

    return recommended_products[:n], messages

# Main title
st.title("📊 Investment Portfolio Recommender")
st.markdown("---")

# Create the input form
with st.form("recommendation_form"):
    st.subheader("📝 Enter Member Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox(
            "Age Group",
            options=['0-18', '19-30', '31-45', '46-60', '60+']
        )
        
        town = st.selectbox(
            "Town",
            options=['NAIROBI', 'MOMBASA', 'KISUMU', 'ELDORET', 'NAKURU']
        )
        
        gender = st.radio(
            "Gender",
            options=['Male', 'Female']
        )

    with col2:
        has_beneficiary = st.checkbox("Has Beneficiary")
        
        beneficiary_age = None
        if has_beneficiary:
            beneficiary_age = st.number_input(
                "Beneficiary Age",
                min_value=0,
                max_value=100,
                value=18
            )
        
        current_products = st.multiselect(
            "Current Products",
            options=[
                'Money Market',
                'Fixed Income',
                'Equity Fund',
                'Balanced Fund',
                'Dollar Fund',
                'Student Account',
                'Junior Account'
            ]
        )

    n_recommendations = st.slider(
        "Number of Recommendations",
        min_value=1,
        max_value=5,
        value=3
    )
    
    submit_button = st.form_submit_button("Get Recommendations")

# Process form submission
if submit_button:
    model, tfidf, df = load_models()
    
    if model is not None and tfidf is not None and df is not None and not df.empty:
        try:
            # Create member data dictionary
            member_data = {
                'age_group': age_group,
                'beneficiary_age': beneficiary_age if has_beneficiary else None,
                'town': town,
                'gender': gender,
                'current_products': current_products
            }
            
            # Create feature vector
            member_features = pd.DataFrame({
                'member_age': [age_group],
                'beneficiery_age': [beneficiary_age if has_beneficiary else np.nan],
                'age_group': [age_group],
                'gender_mapped': [gender]
            })
            
            # Convert features to string format
            member_features['features'] = member_features.astype(str).sum(axis=1)
            
            # Transform features using TF-IDF
            features_tfidf = tfidf.transform(member_features['features'])
            
            # Get recommendations
            recommendations, messages = get_recommendations_with_messages(
                features_tfidf,
                df,
                member_data,
                n=n_recommendations
            )
            
            # Display results in a nice format
            st.markdown("---")
            st.subheader("🎯 Recommended Products")
            
            # Create two columns for recommendations and messages
            rec_col, msg_col = st.columns([1, 2])
            
            with rec_col:
                for i, product in enumerate(recommendations, 1):
                    st.markdown(
                        f"""
                        <div class="recommendation-card">
                            <h4>{i}. {product}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with msg_col:
                for message in messages:
                    st.markdown(
                        f"""
                        <div class="message-card">
                            <p>{message}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Display current portfolio if any
            if current_products:
                st.markdown("---")
                st.subheader("📂 Current Portfolio")
                st.write(", ".join(current_products))
                
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
    else:
        st.error("Unable to load the required models and data. Please check if all files are present.")

# Add footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ by Your Team</p>
    </div>
    """,
    unsafe_allow_html=True
)