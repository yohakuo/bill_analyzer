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

    # --- 设计"提示词 (Prompt)" ---
    prompt = f"""你是一个专业的个人理财顾问。请根据下面的账单数据，直接给出友善的理财建议。

重要要求：
- 你的回复必须直接以"你好呀！"开头，不能有任何其他文字
- 绝对不要展示分析过程、思考步骤或任何解释性文字
- 不要说"我来分析一下"、"根据数据"等话语
- 直接给出建议，就像朋友聊天一样自然
- 不要包含任何元标签或格式标记

账单数据：
本月总支出：{total_spending:.2f} 元
各分类支出：
{categories_text}

请直接给出建议："你好呀！"""

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