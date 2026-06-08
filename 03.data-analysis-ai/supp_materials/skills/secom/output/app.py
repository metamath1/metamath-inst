"""Streamlit Inference App — RandomForestClassifier | classification | target: inspection_result
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import pickle, json, os
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="ML 추론 앱", page_icon="🤖", layout="wide")

@st.cache_resource
def load_artifacts():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(base, "metadata.json")) as f:
        meta = json.load(f)
    return model, meta

model, meta = load_artifacts()
label_encoders = {}

st.title("🤖 ML 추론 앱")
st.markdown(f"**모델:** `RandomForestClassifier` &nbsp;|&nbsp; **타겟:** `inspection_result` &nbsp;|&nbsp; **태스크:** classification")
st.divider()

st.sidebar.header("📥 입력값")
inp = {}
inp["etch_chamber_temp_avg"] = st.sidebar.slider("etch_chamber_temp_avg", -28.9882, 66.49767910870291, 4.874430605260174)
inp["cmp_endpoint_thickness"] = st.sidebar.slider("cmp_endpoint_thickness", 6.4482, 48.9882, 20.543227147766324)
inp["thermal_anneal_temp_max"] = st.sidebar.slider("thermal_anneal_temp_max", 4.4981, 65.1651, 12.237384536082475)
inp["etch_endpoint_signal"] = st.sidebar.slider("etch_endpoint_signal", 59.4, 77.2222, 69.07573556701031)
inp["wafer_edge_exclusion"] = st.sidebar.slider("wafer_edge_exclusion", 0.0, 996.7213, 228.49361271477665)
inp["etch_pressure_peak"] = st.sidebar.slider("etch_pressure_peak", -7150.25, 0.0, -5593.20618556701)
inp["cmp_pad_temp"] = st.sidebar.slider("cmp_pad_temp", 0.0, 400.0, 18.947304295532646)
inp["deposition_uniformity_index"] = st.sidebar.slider("deposition_uniformity_index", 0.0, 0.5255, 0.06519536082474227)
inp["deposition_thickness_var"] = st.sidebar.slider("deposition_thickness_var", 8.0787, 23.3453, 8.959238316151204)
inp["cleaning_dhf_concentration"] = st.sidebar.slider("cleaning_dhf_concentration", 0.7217, 8.237, 3.931505670103093)
inp["deposition_rate_mean"] = st.sidebar.slider("deposition_rate_mean", 0.5013, 0.8884, 0.7456312714776633)
inp["implant_dose_total"] = st.sidebar.slider("implant_dose_total", 15.46, 16.07, 15.79922680412371)
inp["litho_overlay_y"] = st.sidebar.slider("litho_overlay_y", 0.0, 108.754, 9.330870103092783)
inp["etch_chamber_temp_std"] = st.sidebar.slider("etch_chamber_temp_std", 14.1113, 253.7931, 55.846123711340205)
inp["deposition_gas_flow_avg"] = st.sidebar.slider("deposition_gas_flow_avg", 1.2391, 400.0, 23.776881099656357)
inp["litho_overlay_x"] = st.sidebar.slider("litho_overlay_x", 0.0, 400.0, 15.715671821305843)
inp["metrology_cd_mean"] = st.sidebar.slider("metrology_cd_mean", 0.0, 1000.0, 6.714621993127148)
inp["cmp_slurry_flow_rate"] = st.sidebar.slider("cmp_slurry_flow_rate", 0.0, 400.0, 8.027637628865978)
inp["implant_beam_current"] = st.sidebar.slider("implant_beam_current", 2.68, 150.87, 9.242096219931272)
inp["metrology_cd_uniformity"] = st.sidebar.slider("metrology_cd_uniformity", 0.0106, 0.2390146191746591, 0.027376236312667918)
inp["etch_rf_power_mean"] = st.sidebar.slider("etch_rf_power_mean", -3.779, 2.458, -0.41623402061855674)
inp["cmp_polish_time"] = st.sidebar.slider("cmp_polish_time", 0.0, 400.0, 8.629452405498283)
inp["litho_exposure_time"] = st.sidebar.slider("litho_exposure_time", 0.0, 0.95, 0.1404948453608247)
inp["deposition_chamber_pressure"] = st.sidebar.slider("deposition_chamber_pressure", 0.0319, 0.4892, 0.08735515463917526)
inp["litho_dose_avg"] = st.sidebar.slider("litho_dose_avg", 0.0, 0.4914, 0.04318556701030928)
inp["implant_tilt_angle"] = st.sidebar.slider("implant_tilt_angle", 3.8922, 13.0958, 5.930315807560137)
inp["implant_energy_mean"] = st.sidebar.slider("implant_energy_mean", 0.3122, 2.211, 1.1711807560137457)
inp["cmp_pressure_avg"] = st.sidebar.slider("cmp_pressure_avg", 15.47, 16.09, 15.80049828178694)
inp["particle_count_post"] = st.sidebar.slider("particle_count_post", 0.0, 989.4737, 201.11068986254296)
inp["litho_focus_offset"] = st.sidebar.slider("litho_focus_offset", -0.017, 0.0106490381808576, -0.009010185407818774)

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("입력 데이터")
    st.dataframe(pd.DataFrame([inp]), use_container_width=True)
with col2:
    st.subheader("🎯 예측")
    try:
        X = pd.DataFrame([inp])[meta["features"]]
        pred = model.predict(X)[0]
        if meta["task_type"] == "classification":
            st.metric("예측 클래스", str(pred))
            try:
                proba = model.predict_proba(X)[0]
                classes = [str(c) for c in model.classes_]
                st.bar_chart(pd.DataFrame({"클래스": classes, "확률": proba}).set_index("클래스"))
            except Exception:
                pass
        else:
            st.metric("예측값", f"{pred:,.4f}")
    except Exception as e:
        st.error(f"오류: {e}")

st.divider()
st.subheader("📂 배치 예측 (X_test CSV 업로드)")
st.caption("타겟 컬럼이 없는 피처 파일을 업로드하세요. 타겟 컬럼이 있어도 자동으로 제외하고 예측합니다.")

tab1, tab2 = st.tabs(["🔮 배치 예측", "📊 성능 평가 (y_test 업로드)"])

with tab1:
    up_x = st.file_uploader("X_test CSV 업로드", type=["csv"], key="x_upload")
    if up_x:
        batch = pd.read_csv(up_x)
        # 타겟 컬럼이 있으면 자동 제외
        feat_cols = meta["features"]
        missing_cols = [c for c in feat_cols if c not in batch.columns]
        if missing_cols:
            st.error(f"필요한 피처 컬럼이 없습니다: {missing_cols}")
        else:
            try:
                X_batch = batch[feat_cols]
                preds = model.predict(X_batch)
                res = batch.copy()
                res["prediction"] = preds
                if meta["task_type"] == "classification":
                    try:
                        proba = model.predict_proba(X_batch)
                        for i, cls in enumerate(model.classes_):
                            res[f"proba_{cls}"] = proba[:, i]
                    except Exception:
                        pass
                st.success(f"✅ {len(res):,}건 예측 완료")
                st.dataframe(res, use_container_width=True)
                csv_bytes = res.to_csv(index=False).encode("utf-8")
                st.download_button("💾 결과 다운로드", csv_bytes, "predictions.csv", "text/csv")
            except Exception as e:
                st.error(f"예측 오류: {e}")

with tab2:
    st.markdown("X_test 예측 결과와 실제 정답(y_test)을 비교해 모델 성능을 평가합니다.")
    col_a, col_b = st.columns(2)
    with col_a:
        up_x2 = st.file_uploader("X_test CSV", type=["csv"], key="x2_upload")
    with col_b:
        up_y = st.file_uploader("y_test CSV (타겟 컬럼만)", type=["csv"], key="y_upload")

    if up_x2 and up_y:
        try:
            X_eval = pd.read_csv(up_x2)
            y_eval = pd.read_csv(up_y)

            feat_cols = meta["features"]
            missing_cols = [c for c in feat_cols if c not in X_eval.columns]
            if missing_cols:
                st.error(f"X_test에 필요한 컬럼 없음: {missing_cols}")
            elif len(X_eval) != len(y_eval):
                st.error(f"행 수 불일치: X_test={len(X_eval)}행, y_test={len(y_eval)}행")
            else:
                preds = model.predict(X_eval[feat_cols])
                y_true = y_eval.iloc[:, 0].values

                if meta["task_type"] == "classification":
                    from sklearn.metrics import (classification_report, confusion_matrix,
                                                 accuracy_score, f1_score, roc_auc_score)
                    acc = accuracy_score(y_true, preds)
                    f1  = f1_score(y_true, preds, average="macro", zero_division=0)

                    st.success(f"✅ 평가 완료 — Accuracy: **{acc:.4f}** | F1 (macro): **{f1:.4f}**")

                    # Metrics 카드
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Accuracy",   f"{acc:.4f}")
                    m2.metric("F1 (macro)", f"{f1:.4f}")
                    try:
                        auc = roc_auc_score(y_true, model.predict_proba(X_eval[feat_cols])[:, 1])
                        m3.metric("ROC-AUC", f"{auc:.4f}")
                    except Exception:
                        m3.metric("ROC-AUC", "N/A")

                    # Classification report 테이블
                    st.subheader("Classification Report")
                    report = classification_report(y_true, preds, output_dict=True, zero_division=0)
                    report_df = pd.DataFrame(report).T.round(4)
                    st.dataframe(report_df, use_container_width=True)

                    # Confusion matrix
                    st.subheader("Confusion Matrix")
                    cm = confusion_matrix(y_true, preds)
                    cm_df = pd.DataFrame(cm,
                        index=[f"실제 {c}" for c in sorted(set(y_true))],
                        columns=[f"예측 {c}" for c in sorted(set(y_true))])
                    st.dataframe(cm_df, use_container_width=True)

                else:
                    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
                    mae  = mean_absolute_error(y_true, preds)
                    rmse = mean_squared_error(y_true, preds) ** 0.5
                    r2   = r2_score(y_true, preds)

                    st.success(f"✅ 평가 완료")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("MAE",  f"{mae:,.4f}")
                    m2.metric("RMSE", f"{rmse:,.4f}")
                    m3.metric("R²",   f"{r2:.4f}")

                    result_df = pd.DataFrame({"실제값": y_true, "예측값": preds, "잔차": y_true - preds})
                    st.subheader("예측 vs 실제")
                    st.dataframe(result_df, use_container_width=True)

                # 결과 다운로드
                result_full = X_eval.copy()
                result_full["y_true"] = y_true
                result_full["y_pred"] = preds
                st.download_button("💾 평가 결과 다운로드",
                    result_full.to_csv(index=False).encode("utf-8"),
                    "eval_result.csv", "text/csv")

        except Exception as e:
            st.error(f"평가 오류: {e}")
            import traceback; st.code(traceback.format_exc())
