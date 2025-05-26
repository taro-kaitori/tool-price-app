
import streamlit as st
import pandas as pd
from io import BytesIO

@st.cache_data
def load_data():
    inventory = pd.read_csv("inventory_data.csv")
    maker_df = pd.read_excel("maker_coefficients.xlsx")
    category_df = pd.read_excel("category_coefficients.xlsx")
    return inventory, maker_df, category_df

def smart_round(val):
    if val <= 99:
        return round(val, -1)
    elif val <= 9999:
        return round(val, -2)
    elif val <= 99999:
        return round(val, -3)
    else:
        return round(val, -4)

def format_yen(val):
    return f"{int(val):,}円"

def estimate(inventory, maker_table, category_table, 商品名キーワード):
    df = inventory[inventory["商品名"].str.contains(商品名キーワード, na=False, case=False)]
    if df.empty:
        return None, None

    row = df.iloc[0]
    maker_rank = row["メーカーランク"]
    category_code = str(row["カテゴリコード"])
    product_name = row["商品名"]
    manufacturer = row["メーカー名"]

    grade_priority = ["未使用", "中古A", "中古B", "中古C", "中古D"]
    actual_grades = df["グレード"].unique().tolist()
    result = []

    base_row = None
    base_grade = None
    for g in grade_priority:
        base = df[df["グレード"] == g]
        if not base.empty:
            base_row = base.iloc[0]
            base_grade = g
            break

    for grade in grade_priority:
        count = df[df["グレード"] == grade].shape[0]
        if grade in actual_grades:
            sub = df[df["グレード"] == grade]
            avg_buy = smart_round(sub["買取原価"].mean())
            avg_sell = smart_round(sub["買取売価"].mean())
            mode_buy = smart_round(sub["買取原価"].mode().iloc[0]) if not sub["買取原価"].mode().empty else avg_buy
            mode_sell = smart_round(sub["買取売価"].mode().iloc[0]) if not sub["買取売価"].mode().empty else avg_sell
            max_buy = smart_round(sub["買取原価"].max())
            max_sell = smart_round(sub["買取売価"].max())
            min_buy = smart_round(sub["買取原価"].min())
            min_sell = smart_round(sub["買取売価"].min())
        elif base_row is not None:
            buy_rate = (
                maker_table[maker_rank]["買取"][grade] / maker_table[maker_rank]["買取"][base_grade]
            ) * (
                category_table[category_code][grade] / category_table[category_code][base_grade]
            )
            sell_rate = (
                maker_table[maker_rank]["売価"][grade] / maker_table[maker_rank]["売価"][base_grade]
            ) * (
                category_table[category_code][grade] / category_table[category_code][base_grade]
            )
            base_buy = base_row["買取原価"]
            base_sell = base_row["買取売価"]
            avg_buy = mode_buy = max_buy = min_buy = smart_round(base_buy * buy_rate)
            avg_sell = mode_sell = max_sell = min_sell = smart_round(base_sell * sell_rate)
        else:
            continue

        result.append({
            "グレード": f"{grade}（実績あり）" if count > 0 else grade,
            "買取点数": f"{count}" if count > 0 else "",
            "平均売価": format_yen(avg_sell),
            "平均原価": format_yen(avg_buy),
            "最頻売価": format_yen(mode_sell),
            "最頻原価": format_yen(mode_buy),
            "最大売価": format_yen(max_sell),
            "最大原価": format_yen(max_buy),
            "最小売価": format_yen(min_sell),
            "最小原価": format_yen(min_buy),
        })

    return product_name, pd.DataFrame(result)

def export_by_maker(inventory, maker_name, maker_table, category_table):
    df = inventory[inventory["メーカー名"] == maker_name]
    if df.empty:
        return None

    export_rows = []
    grouped = df.groupby(["多分型番", "商品名", "カテゴリコード", "カテゴリ名", "メーカーランク"])

    for (型番, 商品名, カテゴリコード, カテゴリ名, メーカーランク), group in grouped:
        base_row = group[group["グレード"] == "未使用"]
        if base_row.empty:
            continue
        base_row = base_row.iloc[0]
        base_buy = base_row["買取原価"]
        base_sell = base_row["買取売価"]
        base_grade = "未使用"

        for grade in ["未使用", "中古A", "中古B", "中古C", "中古D"]:
            sub = group[group["グレード"] == grade]
            count = len(sub)

            if count > 0:
                avg_sell = smart_round(sub["買取売価"].mean())
                avg_cost = smart_round(sub["買取原価"].mean())
                mode_sell = smart_round(sub["買取売価"].mode().iloc[0]) if not sub["買取売価"].mode().empty else avg_sell
                mode_cost = smart_round(sub["買取原価"].mode().iloc[0]) if not sub["買取原価"].mode().empty else avg_cost
                max_sell = smart_round(sub["買取売価"].max())
                max_cost = smart_round(sub["買取原価"].max())
                min_sell = smart_round(sub["買取売価"].min())
                min_cost = smart_round(sub["買取原価"].min())
            else:
                try:
                    buy_rate = (
                        maker_table[メーカーランク]["買取"][grade] / maker_table[メーカーランク]["買取"][base_grade]
                    ) * (
                        category_table[カテゴリコード][grade] / category_table[カテゴリコード][base_grade]
                    )
                    sell_rate = (
                        maker_table[メーカーランク]["売価"][grade] / maker_table[メーカーランク]["売価"][base_grade]
                    ) * (
                        category_table[カテゴリコード][grade] / category_table[カテゴリコード][base_grade]
                    )
                    avg_cost = mode_cost = max_cost = min_cost = smart_round(base_buy * buy_rate)
                    avg_sell = mode_sell = max_sell = min_sell = smart_round(base_sell * sell_rate)
                except Exception:
                    continue

            export_rows.append({
                "メーカー": maker_name,
                "型番": 型番,
                "商品名称": 商品名,
                "カテゴリ名": カテゴリ名,
                "カテゴリコード": カテゴリコード,
                "グレード": grade,
                "メーカーランク": メーカーランク,
                "買取点数": count,
                "平均売価": avg_sell,
                "平均原価": avg_cost,
                "最頻売価": mode_sell,
                "最頻原価": mode_cost,
                "最大売価": max_sell,
                "最大原価": max_cost,
                "最小売価": min_sell,
                "最小原価": min_cost
            })
    return pd.DataFrame(export_rows)
    df = inventory[inventory["メーカー名"] == maker_name]
    if df.empty:
        return None

    export_rows = []
    group = df.groupby(["多分型番", "商品名", "グレード", "メーカーランク", "カテゴリコード"])
    for (型番, 商品名, グレード, メーカーランク, カテゴリコード), g in group:
        export_rows.append({
            "メーカー": maker_name,
            "型番": 型番,
            "商品名称": 商品名,
            "グレード": グレード,
            "メーカーランク": メーカーランク,
            "カテゴリコード": カテゴリコード,
            "買取点数": g.shape[0],
            "平均売価": smart_round(g["買取売価"].mean()),
            "平均原価": smart_round(g["買取原価"].mean()),
            "最頻売価": smart_round(g["買取売価"].mode().iloc[0]) if not g["買取売価"].mode().empty else "",
            "最頻原価": smart_round(g["買取原価"].mode().iloc[0]) if not g["買取原価"].mode().empty else "",
            "最大売価": smart_round(g["買取売価"].max()),
            "最大原価": smart_round(g["買取原価"].max()),
            "最小売価": smart_round(g["買取売価"].min()),
            "最小原価": smart_round(g["買取原価"].min()),
        })
    return pd.DataFrame(export_rows)

# UI部
st.title("🔧 工具価格査定フォーム")

inventory, maker_df, category_df = load_data()

# メーカー名のプルダウン
メーカー候補 = sorted(inventory["メーカー名"].dropna().unique())
selected_maker = st.selectbox("メーカー名を選んでください", options=メーカー候補)

# 商品名キーワード検索
商品キーワード = st.text_input("商品名または型番の一部を入力してください", value="TD173")

if 商品キーワード:
    with st.spinner("検索中..."):
        maker_table, category_table = {}, {}
        for _, row in maker_df.iterrows():
            maker_table[row["メーカーランク"]] = {
                "買取": {g: row[f"{g}_買取"] for g in ["未使用", "中古A", "中古B", "中古C", "中古D"]},
                "売価": {g: row[f"{g}_売価"] for g in ["未使用", "中古A", "中古B", "中古C", "中古D"]}
            }
        for _, row in category_df.iterrows():
            category_table[row["カテゴリコード"]] = {
                g: row[g] for g in ["未使用", "中古A", "中古B", "中古C", "中古D"]
            }

        product_name, results_df = estimate(
            inventory[
                inventory["メーカー名"] == selected_maker
            ], maker_table, category_table, 商品キーワード
        )

        if results_df is not None:
            st.write(f"📋 メーカー: {selected_maker}　商品名候補: {product_name}")
            st.dataframe(results_df)
        else:
            st.warning("該当するデータが見つかりませんでした。")

# メーカー別出力
if st.button("メーカー別データを出力する"):
    output_df = export_by_maker(inventory, selected_maker, maker_table, category_table)
    if output_df is not None:
        buffer = BytesIO()
        output_df.to_csv(buffer, index=False, encoding="utf-8-sig")
        st.download_button(
            label="CSVをダウンロード",
            data=buffer.getvalue(),
            file_name=f"{selected_maker}_価格リスト.csv",
            mime="text/csv"
        )
    else:
        st.warning("このメーカーのデータは見つかりませんでした。")
