import requests
import pandas as pd
import streamlit as st
from app.core.config import settings

class APIClient:
    def __init__(self):
        self.base_url = f"http://localhost:8000{settings.API_V1_STR}"
        self.token = st.session_state.get('access_token')
        self.headers = {"X-API-KEY": settings.API_KEY}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def login(self, username, password):
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.access_token = data['access_token']
                self.token = data['access_token']
                self.headers["Authorization"] = f"Bearer {self.token}"
                return True
            return False
        except Exception as e:
            st.error(f"Connection Error: {e}")
            return False

    def get_me(self):
        try:
            response = requests.get(f"{self.base_url}/auth/me", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_stats(self):
        try:
            response = requests.get(f"{self.base_url}/history/stats", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_analytics(self):
        try:
            response = requests.get(f"{self.base_url}/history/analytics", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_history(self, limit=50):
        try:
            response = requests.get(f"{self.base_url}/history/", params={"limit": limit}, headers=self.headers)
            if response.status_code == 200:
                return pd.DataFrame(response.json())
            return pd.DataFrame()
        except:
            return pd.DataFrame()

    def get_seeded_claims(self):
        try:
            response = requests.get(f"{self.base_url}/history/claims", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def predict(self, claim_data, explain=False):
        try:
            response = requests.post(
                f"{self.base_url}/predict/", 
                json=claim_data, 
                params={"explain": explain},
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
