import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from bankings.models import DepositBaseList, SavingBaseList


from sklearn.preprocessing import OneHotEncoder

class RecommenderSystem:
    def __init__(self):
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()

    def train(self, survey_data, product_data):
        if "recommended_product" not in survey_data.columns:
            raise ValueError("Missing 'recommended_product' in training data.")

        X = self.encoder.fit_transform(survey_data.drop("recommended_product", axis=1))
        y = self.label_encoder.fit_transform(survey_data["recommended_product"])
        self.model.fit(X, y)

    def predict(self, new_survey, product_data):
        X_new = self.encoder.transform(new_survey)  # handle_unknown="ignore" 덕분에 예외 없음
        predictions = self.model.predict_proba(X_new)

        if predictions.shape[1] == 0:
            raise ValueError("Prediction failed: No matching categories in product data.")

        top_indices = np.argsort(-predictions, axis=1)[:, :5]
        recommended_products = []

        for indices in top_indices:
            recommended_products.append(
                [product_data.iloc[i]["fin_prdt_nm"] for i in indices if i < len(product_data)]
            )

        if not recommended_products[0]:
            raise ValueError("No valid recommendations were found.")

        return recommended_products[0]



def generate_dummy_survey_data(num_samples=100):
    age_groups = ["20대", "30대", "40대", "50대", "60대 이상"]
    income_sources = ["직장", "자영업", "프리랜서", "기타"]
    asset_sizes = ["1000만원 이하", "1000만원 ~ 5000만원", "5000만원 이상"]
    financial_purposes = ["단기 수익", "장기 자산 관리", "리스크 회피", "재산 증식"]
    important_factors = ["이율", "안정성", "유동성", "브랜드 신뢰도"]
    recent_investments = [True, False]
    financial_products = ["예금", "적금", "펀드", "주식", "없음"]
    preferred_banks = ["국민은행", "신한은행", "우리은행", "하나은행", "기타"]

    data = []
    for _ in range(num_samples):
        data.append({
            "age_group": np.random.choice(age_groups),
            "income_source": np.random.choice(income_sources),
            "asset_size": np.random.choice(asset_sizes),
            "financial_purpose": np.random.choice(financial_purposes),
            "important_factor": np.random.choice(important_factors),
            "recent_investment": np.random.choice(recent_investments),
            "financial_products": np.random.choice(financial_products),
            "preferred_bank": np.random.choice(preferred_banks),
        })
    return pd.DataFrame(data)


def generate_training_data(survey_data, product_data):
    """
    설문 데이터를 상품 데이터와 매핑하여 학습 데이터를 생성합니다.
    """
    if "fin_prdt_nm" not in product_data.columns:
        raise ValueError("Missing 'fin_prdt_nm' in product data.")

    product_names = product_data["fin_prdt_nm"].tolist()
    survey_data["recommended_product"] = np.random.choice(product_names, size=len(survey_data))
    return survey_data


def fetch_products():
    """
    Bankings 앱의 예금 및 적금 데이터를 가져옵니다.
    """
    # 예금 상품 가져오기
    deposit_products = DepositBaseList.objects.prefetch_related('deposit_options').all()
    deposit_data = [
        {
            "intr_rate2": max([opt.intr_rate2 or 0 for opt in product.deposit_options.all()]),
            "fin_prdt_nm": product.fin_prdt_nm,
            "kor_co_nm": product.kor_co_nm,
        }
        for product in deposit_products
    ]
    deposit_df = pd.DataFrame(deposit_data)

    # 적금 상품 가져오기
    saving_products = SavingBaseList.objects.prefetch_related('saving_options').all()
    saving_data = [
        {
            "intr_rate2": max([opt.intr_rate2 or 0 for opt in product.saving_options.all()]),
            "fin_prdt_nm": product.fin_prdt_nm,
            "kor_co_nm": product.kor_co_nm,
        }
        for product in saving_products
    ]
    saving_df = pd.DataFrame(saving_data)

    return deposit_df, saving_df
