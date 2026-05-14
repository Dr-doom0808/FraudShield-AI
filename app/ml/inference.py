import joblib
import pandas as pd
import numpy as np
import shap
import os
import time
from app.core.config import settings
from app.utils.logger import logger

class ModelManager:
    """
    Singleton class for managing ML model loading and inference.
    Includes performance tracking and data validation.
    """
    _instance = None
    _model = None
    _explainer = None
    _metadata = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """Loads the model if not already loaded with metadata tracking."""
        if self._model is None:
            try:
                start_time = time.time()
                model_path = settings.MODEL_PATH
                if not os.path.exists(model_path):
                    logger.error(f"Model file not found at {model_path}")
                    raise FileNotFoundError(f"Model file not found at {model_path}")
                
                self._model = joblib.load(model_path)
                
                # Extract metadata if available or set defaults
                self._metadata = {
                    "path": model_path,
                    "loaded_at": time.time(),
                    "size_mb": os.path.getsize(model_path) / (1024 * 1024),
                    "algorithm": str(type(self._model.named_steps['classifier']).__name__)
                }
                
                # Pre-initialize SHAP explainer
                classifier = self._model.named_steps['classifier']
                self._explainer = shap.TreeExplainer(classifier)
                
                logger.info(f"ML Model ({self._metadata['algorithm']}) loaded in {time.time() - start_time:.2f}s")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise

    def validate_input(self, data: pd.DataFrame):
        """Checks for basic data drift or out-of-bounds values."""
        # Example: Check if claim amounts are extreme
        if (data['InscClaimAmtReimbursed'] > 100000).any():
            logger.warning("Extreme claim amount detected (>100k). Model might be less accurate.")
        return True

    def predict(self, data: pd.DataFrame):
        """Runs inference on input dataframe with timing."""
        if self._model is None:
            self.load_model()
        
        self.validate_input(data)
        
        start_time = time.time()
        scaler = self._model.named_steps['scaler']
        classifier = self._model.named_steps['classifier']
        
        scaled_data = scaler.transform(data)
        prediction = classifier.predict(scaled_data)
        probabilities = classifier.predict_proba(scaled_data)[:, 1]
        
        inference_time = time.time() - start_time
        logger.debug(f"Inference completed in {inference_time:.4f}s")
        
        return prediction, probabilities

    def explain(self, data: pd.DataFrame):
        """Generates SHAP values for explanation."""
        if self._explainer is None:
            self.load_model()
            
        scaler = self._model.named_steps['scaler']
        scaled_data = scaler.transform(data)
        
        shap_values = self._explainer.shap_values(scaled_data)
        
        if isinstance(shap_values, list):
            return shap_values[1][0]
        return shap_values[0]

    def get_metadata(self):
        return self._metadata

model_manager = ModelManager()
