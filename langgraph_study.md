typeError:create_react_agent() got unexpected keyword arguments: {'model_provider': 'ollama'}
报这个错误是因为你用的 langgraph 版本里，create_react_agent 还不支持 model_provider 参数。

在新版本里，create_react_agent 是一个“预构建 Agent 工厂”，它会自动去推断 provider。如果推断不了（比如你用 Ollama 的本地模型），就需要用 ChatOllama 这种显式的模型类去创建。

from langchain_ollama import ChatOllama
# --- 显式定义 Ollama 模型 ---
llm = ChatOllama(
    model="qwen3:0.6b",  # ✅ Ollama 模型名称
    base_url="http://localhost:11434",  # 默认 Ollama 地址
    temperature=0  #温度设定
)

添加提示词：
静态提示：prompt
# --- 创建 agent ---
agent = create_react_agent(
    llm,
    tools=[get_weather],
    prompt=(
        "你是一个天气助手，在用户使用你时，"
        "你只需要调用 get_weather 获取到当地的实时天气，并准确地汇报给用户。"
    )
)
