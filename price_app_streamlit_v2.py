
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

@st.cache_data
def load_data():
    inventory = pd.read_csv("inventory_data.csv")
    maker_df = pd.read_excel("maker_coefficients.xlsx", engine="openpyxl")
    category_df = pd.read_excel("category_coefficients.xlsx", engine="openpyxl")
    return inventory, maker_df, category_df

def round_price(value):
    if pd.isna(value):
        return ""
    value = int(value)
    if value <= 99:
        return f"{round(value, -1):,}円"
    elif value <= 9999:
        return f"{round(value, -2):,}円"
    elif value <= 99999:
        return f"{round(value, -3):,}円"
    else:
        return f"{round(value, -4):,}円"

def estimate(inventory, maker_df, category_df, maker_name, keyword):
    df = inventory[inventory["メーカー名"] == maker_name]
    df = df[df["多分型番"].astype(str).str.contains(keyword, case=False, na=False)]

    if df.empty:
        return "該当データがありません", None, None, None

    first_row = df.iloc[0]
    product_name = first_row["商品名"]
    maker_rank = first_row["メーカーランク"]
    category_code = first_row["カテゴリコード"]

    try:
        maker_rate = maker_df.set_index("メーカーコード").loc[maker_rank].to_dict()
        category_rate = category_df.set_index("カテゴリコード").loc[category_code].to_dict()
    except:
        maker_rate = category_rate = {}

    base_grade = "未使用"
    base_data = df[df["グレード"] == base_grade]
    results = []

    for grade in ["未使用", "中古A", "中古B", "中古C", "中古D"]:
        target = df[df["グレード"] == grade]
        count = len(target)

        if count > 0:
            row = {
                "グレード": f"{grade}（実績あり）",
                "買取点数": count,
                "平均売価": round_price(target["買取売価"].mean()),
                "平均原価": round_price(target["買取原価"].mean()),
                "最頻売価": round_price(target["買取売価"].mode().values[0]) if not target["買取売価"].mode().empty else "",
                "最頻原価": round_price(target["買取原価"].mode().values[0]) if not target["買取原価"].mode().empty else "",
                "最大売価": round_price(target["買取売価"].max()),
                "最大原価": round_price(target["買取原価"].max()),
                "最小売価": round_price(target["買取売価"].min()),
                "最小原価": round_price(target["買取原価"].min()),
            }
        else:
            if base_data.empty or maker_rank not in maker_rate or category_code not in category_rate:
                continue
            base_sell = base_data["買取売価"].mean()
            base_cost = base_data["買取原価"].mean()
            sell = base_sell * maker_rate.get(grade, 100) / maker_rate[base_grade] * category_rate.get(grade, 100) / 100
            cost = base_cost * maker_rate.get(grade, 100) / maker_rate[base_grade] * category_rate.get(grade, 100) / 100
            row = {
                "グレード": grade,
                "買取点数": 0,
                "平均売価": round_price(sell),
                "平均原価": round_price(cost),
                "最頻売価": round_price(sell),
                "最頻原価": round_price(cost),
                "最大売価": round_price(sell),
                "最大原価": round_price(cost),
                "最小売価": round_price(sell),
                "最小原価": round_price(cost),
            }
        results.append(row)

    return product_name, maker_rank, category_code, pd.DataFrame(results)

# メーカー別全データ出力
def export_by_maker(inventory, maker_name, maker_df, category_df):
    df = inventory[inventory["メーカー名"] == maker_name].copy()
    if df.empty:
        return pd.DataFrame()

    result_list = []
    for model in df["多分型番"].dropna().unique():
        _, mr, cat_code, result = estimate(df, maker_df, category_df, maker_name, model)
        if isinstance(result, pd.DataFrame):
            result["メーカー"] = maker_name
            result["型番"] = model
            result["メーカーランク"] = mr
            result["カテゴリコード"] = cat_code
            result["商品名"] = df[df["多分型番"] == model]["商品名"].values[0]
            result_list.append(result)
    return pd.concat(result_list, ignore_index=True) if result_list else pd.DataFrame()

# アプリUI
st.title("🔧 工具価格査定フォーム")

inventory, maker_table, category_table = load_data()
メーカー一覧 = inventory["メーカー名"].dropna().unique().tolist()
メーカー一覧.sort()

selected_maker = st.selectbox("メーカー名を選んでください", メーカー一覧)
keyword = st.text_input("商品名または型番の一部を入力してください")

if selected_maker and keyword:
    product_name, maker_rank, category_code, results_df = estimate(
        inventory, maker_table, category_table, selected_maker, keyword
    )

    if isinstance(results_df, pd.DataFrame):
        st.markdown(f"**📦 商品名**：{product_name}")
        st.markdown(f"**🏭 メーカーランク**：{maker_rank}")
        st.markdown(f"**🧩 カテゴリコード**：{category_code}")
        st.dataframe(results_df, use_container_width=True)

        csv = results_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 この結果をCSVでダウンロード",
            csv,
            f"{selected_maker}_{keyword}_査定結果.csv",
            "text/csv",
            key="download-csv"
        )
    else:
        st.warning("該当するデータが見つかりませんでした。")

# メーカー別CSV出力
if selected_maker:
    if st.button("📦 このメーカーの査定データをCSVで出力"):
        output_df = export_by_maker(inventory, selected_maker, maker_table, category_table)
        if not output_df.empty:
            csv = output_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "📥 メーカー全体の査定データをダウンロード",
                csv,
                f"{selected_maker}_全体査定データ.csv",
                "text/csv",
                key="download-maker-csv"
            )
        else:
            st.warning("出力可能なデータがありませんでした。")
