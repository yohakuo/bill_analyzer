import pandas as pd


def analyze_bill_data(file_path):
    """
    从给定的文件路径读取账单数据，
    清洗并分析，返回分析结果。
    """

    df = pd.read_csv(file_path)
    df_expense = df[df["类型"] == "支出"].copy()
    df_expense["分类"] = df_expense["分类"].fillna("未分类")
    df_cleaned = df_expense[["时间", "分类", "金额"]]

    print("[analysis.py] 数据已清洗")

    total_spending = df_cleaned["金额"].sum()
    category_spending = (
        df_cleaned.groupby("分类")["金额"].sum().sort_values(ascending=False)
    )

    return total_spending, category_spending
