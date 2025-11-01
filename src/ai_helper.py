from click import prompt
from openai import OpenAI

# --- 安全措施：从环境变量读取您的 API Key ---
# (我们稍后会在 .flaskenv 文件中设置它)
# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY")
# )

client = OpenAI(base_url="http://192.168.121.57:11434/v1", api_key="local-qwen3")


def get_ai_suggestion(total_spending, categories_text):
    """
    根据账单分析结果，调用 AI 模型生成理财建议。
    """
    print("正在请求 AI 分析...")

    # --- 设计“提示词 (Prompt)” ---
    prompt = f"""
[角色]
你是一个专业的个人理财顾问。

[任务]
根据我提供的账单内容，对其进行长期的总结，并对短期的消费进行趋势分析，根据总结和分析提出合理的意见。

[规则]
1.  语气必须友善、鼓励，直接对用户说话（用"你"）。
2.  **绝对不要**展示你的分析过程、思考步骤、或任何“好的，我来分析一下...”之类的内心独白。
3.  **你的回复必须直接以"你好呀！"或类似的友善问候语开头。**
4.  你的回复中**禁止**包含任何"[角色]"、"[任务]"或"[规则]"这样的元标签。
5.  请直接开始你的回复，就好像你在给一个朋友发消息。

[账单数据]
1.  本月总支出：{total_spending:.2f} 元
2.  各分类支出详情（仅展示主要分类）：
{categories_text}

[你的回复]
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

        suggestion = chat_completion.choices[0].message.content

        if "你好呀！" in suggestion:
            suggestion = "你好呀！" + suggestion.split("你好呀！", 1)[-1]
        return suggestion

    except Exception as e:
        print(f"AI 调用失败: {e}")
        return "抱歉，AI 分析服务暂时出了点小问题。"
