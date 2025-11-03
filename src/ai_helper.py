from click import prompt
from openai import OpenAI

# --- 安全措施：从环境变量读取您的 API Key ---
# (我们稍后会在 .flaskenv 文件中设置它)
# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY")
# )

client = OpenAI(base_url="http://192.168.121.57:11434/v1", api_key="local-qwen3")


def get_ai_suggestion(analysis_report):
    """
    根据账单分析结果，调用 AI 模型生成理财建议。
    """
    print("正在请求 AI 分析...")
    analysis_report["start_date"]
    analysis_report["end_date"]
    analysis_report["total_days"]
    # 趋势粒度
    analysis_report["trend_granularity"]
    analysis_report["spending_trend_str"]
    # 总体数据
    analysis_report["total_spending"]
    analysis_report["category_spending_top5_str"]
    analysis_report["top_5_transactions_str"]

    prompt = """
    你是一个专业的个人理财顾问，任务按照下面的步骤执行：
    1.基于“总体数据”，分析总支出和主要支出项。包含这笔支出的时间范围，支出前五名是哪些分类；
    2.基于“趋势数据”，分析消费波动和关键事件。
    3.最后，请根据这两部分分析，给我 3 条最关键、最具体的省钱建议。
    
    输出格式：
    1.开头使用'你好啊！'
    2.语气必须专业、友善、鼓励，直接对用户说话（用"你"）。
    3.使用标题来组织你的回复，使其清晰易读。

    ---
    [账单特征分析报告]
    ### 1. 总体数据 (用于总体分析)
    账单时间范围: 从 {start_date} 到 {end_date} (共 {total_days} 天)
    期间总支出: {total:.2f} 元
    支出前 5 多的分类:{categories_str}

    ### 2. 趋势数据 (用于趋势分析)
    分析粒度: {granularity} (按{ '周' if granularity == 'Weekly' else '月' }汇总)
    支出趋势:{trend_str}
    期间 Top 5 最大单笔支出:{top_trans_str}
    ---
    
    [你的分析与建议]
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="qwen3:8b",
        )

        chat_completion.choices[0].message.content

        # if "你好呀！" in suggestion:
        #     suggestion = "你好呀！" + suggestion.split("你好呀！", 1)[-1]
        # return suggestion

    except Exception as e:
        print(f"AI 调用失败: {e}")
        return "抱歉，AI 分析服务暂时出了点小问题。"
