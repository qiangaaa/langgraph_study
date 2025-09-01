from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import requests


# --- 工具函数：调用高德天气 API ---
def get_weather(city_name, extensions='base'):
    """
    获取高德天气信息
    """
    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    params = {
        'key': '30dbb61d137bd88feedaa3e38e376078',  # ✅ 记得换成你自己的高德 Key
        'city': city_name,
        'extensions': extensions,
        'output': 'JSON'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# --- 显式定义 Ollama 模型 ---
llm = ChatOllama(
    model="qwen3:1.7b",  # ✅ Ollama 模型名称
    base_url="http://localhost:11434",  # 默认 Ollama 地址
    temperature=0.7   # 温度设定
)


# --- 创建 agent ---
agent = create_react_agent(
    llm,
    tools=[get_weather],
    prompt=(
        "你是一个天气助手，在用户使用你时，"
        "你只需要调用 get_weather 获取到当地的实时天气，并准确地汇报给用户。"
    )
)

# --- 调用 agent ---
if __name__ == "__main__":
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": "帮我查一下广州的实时天气"}
        ]
    })

    print("Agent 输出：", result)
