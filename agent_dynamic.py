from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import requests

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


def prompt_dynamic(state: AgentState, config: RunnableConfig)->list[AnyMessage]:
    username=config['configurable'].get("username")
    system_msg=f"你是一个智能体，用来帮助用户解决问题，并尊称用户为：{username}"
    return [{"role": "system", "content": system_msg}] + state["messages"]


llm=ChatOllama(
    model="qwen3:0.6b",  # ✅ Ollama 模型名称
    base_url="http://localhost:11434",  # 默认 Ollama 地址
    temperature=0   #设定温度
)


agent=create_react_agent(
    llm,
    tools=[get_weather],
    prompt=prompt_dynamic,
)

result=agent.invoke(
    {"messages": [{"role": "user", "content": "现在长沙的天气情况"}]},
    config={"configurable": {"user_name": "YZQ"}}
    )

print(result)