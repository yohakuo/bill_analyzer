import pandas as pd


def process_and_analyze_data(file_path):
    """
    从给定的文件路径读取账单数据，
    清洗、处理，并提取“特征”以供 AI 分析。
    """

    try:
        # 优先尝试 CSV
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"[analysis.py] 读取 CSV 失败: {e}。 尝试读取 Excel...")
        try:
            # 失败则尝试 Excel
            df = pd.read_excel(file_path)
        except Exception as e2:
            print(f"[analysis.py] 严重错误：无法读取文件 {e2}")
            return None

    try:
        df_expense = df[df["类型"] == "支出"].copy()

        # 核心：转换时间列
        df_expense["时间"] = pd.to_datetime(df_expense["时间"])

    except KeyError:
        print("[analysis.py] 严重错误：文件中未找到 '类型' 或 '时间' 列。")
        return None
    except Exception as e:
        print(f"[analysis.py] 严重错误：解析'时间'列失败。 {e}")
        return None

    df_expense["分类"] = df_expense["分类"].fillna("未分类")
    df_cleaned = df_expense[["时间", "分类", "金额"]]

    start_date = df_cleaned["时间"].min()
    end_date = df_cleaned["时间"].max()
    # 计算总天数，+1 是为了包含当天
    total_days = (end_date - start_date).days + 1

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    df_cleaned_indexed = df_cleaned.set_index("时间")

    if total_days <= 90:
        trend_granularity = "Weekly"
        trend_data = df_cleaned_indexed["金额"].resample("W").sum()
    else:
        trend_granularity = "Monthly"
        trend_data = df_cleaned_indexed["金额"].resample("M").sum()

    total_spending = df_cleaned["金额"].sum()
    category_spending_top5 = (
        df_cleaned.groupby("分类")["金额"].sum().sort_values(ascending=False).head(5)
    )
    top_5_transactions = df_cleaned.nlargest(5, "金额")

    analysis_report = {
        # 时间范围
        "start_date": start_date_str,
        "end_date": end_date_str,
        "total_days": total_days,
        # 趋势分析
        "trend_granularity": trend_granularity,
        "spending_trend_str": trend_data.to_string(),
        # 总体分析
        "total_spending": total_spending,
        "category_spending_top5_str": category_spending_top5.to_string(),
        "top_5_transactions_str": top_5_transactions.to_string(),
    }
    return analysis_report
