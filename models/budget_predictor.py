# Author: Muhammad Farrel Haidar
# Project: AI PR & KOL Specialist DSS
# Date: 2026-09-22

import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

class KOLBudgetPredictor:
    """
    Model Regresi berbasis XGBoost untuk memprediksi estimasi budget KOL (Key Opinion Leader)
    berdasarkan historis interaksi dan performa KOL.
    """
    def __init__(self, model_path: str = "data/budget_model.joblib"):
        self.model_path = model_path
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=150,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )
        self.is_trained = False
        
        # Load model jika sudah ada
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True

    def train_dummy_model(self):
        """
        Fungsi untuk melatih model dengan dummy dataset.
        Features yang digunakan: [followers, engagement_rate, target_reach]
        Target: estimated_budget (IDR)
        """
        print("Membangkitkan data sintetik untuk pelatihan model...")
        np.random.seed(42)
        n_samples = 500
        
        # Feature 1: Followers (10,000 to 5,000,000)
        followers = np.random.randint(10000, 5000000, n_samples)
        # Feature 2: Engagement Rate Percentage (0.5% to 15.0%)
        engagement_rate = np.random.uniform(0.5, 15.0, n_samples)
        # Feature 3: Target Reach (Estimasi impresi dari audiens yang disasar, biasanya 10-30% follower)
        target_reach = followers * np.random.uniform(0.1, 0.3, n_samples)
        
        X = np.column_stack((followers, engagement_rate, target_reach))
        
        # Logic dummy untuk budget: kombinasi berbobot dari metrik performa ditambah sedikit noise/variasi
        # Base fee (contoh: 50 per follower + bonus tinggi untuk engagement rate + rate tambahan dari reach)
        budget = (followers * 50) + (followers * engagement_rate * 500) + (target_reach * 100)
        noise = np.random.normal(0, 1000000, n_samples) # Add some variance
        y = np.clip(budget + noise, a_min=500000, a_max=None) # Minimum budget 500k IDR
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Melatih XGBoost Regressor...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Menyimpan model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        
        preds = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        return {"status": "trained", "mae": mae, "r2_score": r2}

    def predict_budget(self, followers: int, engagement_rate: float, target_reach: int) -> float:
        """
        Melakukan prediksi harga KOL berdasarkan metrics saat ini.
        """
        if not self.is_trained:
            print("Model belum dilatih. Memulai auto-training dengan dummy data...")
            self.train_dummy_model()
            
        features = np.array([[followers, engagement_rate, target_reach]])
        predicted_budget = self.model.predict(features)[0]
        
        # Memastikan tidak ada angka negatif
        return max(float(predicted_budget), 0.0)

if __name__ == "__main__":
    predictor = KOLBudgetPredictor()
    metrics = predictor.train_dummy_model()
    print(f"Model Metrics -> MAE: {metrics['mae']:,.2f}, R2: {metrics['r2_score']:.4f}")
    
    # Test Inference
    est = predictor.predict_budget(followers=150000, engagement_rate=3.5, target_reach=30000)
    print(f"\nEstimasi Budget untuk Nano/Micro KOL (150K followers, 3.5% ER): Rp {est:,.2f}")
