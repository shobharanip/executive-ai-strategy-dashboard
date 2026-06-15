"""
Churn Predictor Model - XGBoost-based account churn prediction
CEO-Track Portfolio | Executive AI Strategy Dashboard
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import xgboost as xgb
import shap
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChurnPredictor:
      """XGBoost-based churn prediction model with SHAP explainability."""

    FEATURES = [
              'days_since_login', 'feature_adoption_score', 'support_tickets_90d',
              'nps_score', 'contract_months_remaining', 'arr', 'user_count',
              'api_calls_30d', 'dashboard_views_30d', 'export_count_30d',
              'account_age_days', 'expansion_count', 'payment_failures_90d'
    ]

    def __init__(self, model_params=None):
              self.params = model_params or {
                            'n_estimators': 300,
                            'max_depth': 6,
                            'learning_rate': 0.05,
                            'subsample': 0.8,
                            'colsample_bytree': 0.8,
                            'min_child_weight': 3,
                            'scale_pos_weight': 4,
                            'eval_metric': 'auc',
                            'use_label_encoder': False,
                            'random_state': 42
              }
              self.model = xgb.XGBClassifier(**self.params)
              self.scaler = StandardScaler()
              self.explainer = None
              self.feature_importance = None

    def preprocess(self, df: pd.DataFrame) -> np.ndarray:
              """Preprocess features for model input."""
              X = df[self.FEATURES].copy()
              X = X.fillna(X.median())
              X['login_velocity'] = X['days_since_login'] / (X['account_age_days'] + 1)
              X['support_per_user'] = X['support_tickets_90d'] / (X['user_count'] + 1)
              X['api_engagement'] = np.log1p(X['api_calls_30d'])
              return X

    def train(self, df: pd.DataFrame, target_col: str = 'churned_90d'):
              """Train the churn prediction model."""
              logger.info(f"Training on {len(df)} accounts...")
              X = self.preprocess(df)
              y = df[target_col]
              X_train, X_test, y_train, y_test = train_test_split(
                  X, y, test_size=0.2, random_state=42, stratify=y
              )
              self.model.fit(
                  X_train, y_train,
                  eval_set=[(X_test, y_test)],
                  early_stopping_rounds=50,
                  verbose=False
              )
              preds = self.model.predict_proba(X_test)[:, 1]
              auc = roc_auc_score(y_test, preds)
              logger.info(f"Model AUC: {auc:.4f}")
              self.explainer = shap.TreeExplainer(self.model)
              self.feature_importance = pd.DataFrame({
                  'feature': X.columns,
                  'importance': self.model.feature_importances_
              }).sort_values('importance', ascending=False)
              return {'auc': auc, 'feature_importance': self.feature_importance}

    def predict_churn_scores(self, df: pd.DataFrame) -> pd.DataFrame:
              """Generate churn probability scores for all accounts."""
              X = self.preprocess(df)
              scores = self.model.predict_proba(X)[:, 1]
              result = df[['account_id', 'account_name', 'arr']].copy()
              result['churn_score'] = scores
              result['risk_tier'] = pd.cut(
                  scores,
                  bins=[0, 0.3, 0.6, 1.0],
                  labels=['Low Risk', 'Medium Risk', 'High Risk']
              )
              shap_values = self.explainer.shap_values(X)
              result['top_churn_driver'] = [
                  X.columns[np.argmax(np.abs(shap_values[i]))]
                  for i in range(len(X))
              ]
              return result.sort_values('churn_score', ascending=False)

    def get_at_risk_accounts(self, df: pd.DataFrame, threshold: float = 0.6) -> pd.DataFrame:
              """Return accounts above churn risk threshold."""
              scores = self.predict_churn_scores(df)
              at_risk = scores[scores['churn_score'] >= threshold].copy()
              at_risk['at_risk_arr'] = at_risk['arr'] * at_risk['churn_score']
              logger.info(f"Found {len(at_risk)} at-risk accounts with ${at_risk['at_risk_arr'].sum():,.0f} ARR at risk")
              return at_risk

    def save(self, path: str):
              """Serialize model to disk."""
              with open(path, 'wb') as f:
                            pickle.dump({'model': self.model, 'scaler': self.scaler,
                                                                 'explainer': self.explainer}, f)
                        logger.info(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str) -> 'ChurnPredictor':
              """Load serialized model from disk."""
        predictor = cls()
        with open(path, 'rb') as f:
                      data = pickle.load(f)
                  predictor.model = data['model']
        predictor.scaler = data['scaler']
        predictor.explainer = data['explainer']
        return predictor


if __name__ == '__main__':
      # Demo training run
      np.random.seed(42)
    n = 5000
    df_demo = pd.DataFrame({
              col: np.random.rand(n) * 100 for col in ChurnPredictor.FEATURES
    })
    df_demo['account_id'] = [f'ACC_{i:05d}' for i in range(n)]
    df_demo['account_name'] = [f'Company {i}' for i in range(n)]
    df_demo['churned_90d'] = (df_demo['days_since_login'] > 60).astype(int)
    predictor = ChurnPredictor()
    results = predictor.train(df_demo)
    print(f"Training AUC: {results['auc']:.4f}")
    print(results['feature_importance'].head(5))
    at_risk = predictor.get_at_risk_accounts(df_demo)
    print(f"At-risk accounts: {len(at_risk)}")
