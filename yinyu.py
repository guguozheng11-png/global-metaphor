import json
import os
import requests
import streamlit as st

# ================= 页面基础配置 =================
st.set_page_config(page_title="跨文化广告隐喻助手", page_icon="🌍", layout="wide")

# ================= 读取数据 =================
@st.cache_data
def load_data():
    # 获取当前 app.py 所在的绝对文件夹路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接出 data.json 的绝对路径
    json_path = os.path.join(current_dir, "data.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
data = load_data()
# 提取所有国家（去重）
countries = list(set([item["country"] for item in data]))

# ================= 侧边栏 =================
with st.sidebar:
    st.title("🌍 设置中心")
    st.markdown("### 1. 选择目标国家")
    selected_country = st.selectbox("请选择要出海的国家/地区：", countries)
    
    st.markdown("### 2. AI 顾问配置")
    api_key = st.text_input("输入 DeepSeek API Key：", type="password", help="用于与 AI 顾问对话")
    if st.button("清空会话记录"):
        st.session_state.messages = []
        st.rerun()

st.title("跨文化广告隐喻分析库")
st.markdown("基于认知语言学与跨文化营销理论，辅助中国出海企业进行文案本地化适配。")

# ================= 主界面分页 =================
tab1, tab2, tab3 = st.tabs(["📍 目标国家隐喻库", "📚 全球成功案例库", "🤖 AI 隐喻顾问"])

# --- 标签页 1：根据国家显示 ---
with tab1:
    st.header(f"📍 【{selected_country}】的隐喻表达习惯")
    
    # 筛选当前国家的数据
    country_data = [item for item in data if item["country"] == selected_country]
    
    if not country_data:
        st.info("该国家暂无数据，快去 data.json 里补充吧！")
    
    for item in country_data:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader(f"核心隐喻：{item['metaphor']}")
                st.info(f"**目标文化表达**：\n{item['expression']}")
            with col2:
                st.markdown(f"**✅ 成功案例**：{item['success_case']}")
                st.write(item['success_desc'])
                if item['risk_warning'] != "无":
                    st.error(f"⚠️ **风险预警**：{item['risk_warning']}")
            st.divider()

# --- 标签页 2：全球案例库 ---
with tab2:
    st.header("📚 全球案例速查")
    for item in data:
        with st.expander(f"{item['country']} | {item['success_case']}（{item['metaphor']}）"):
            st.markdown(f"- **表达方式**：{item['expression']}")
            st.markdown(f"- **案例描述**：{item['success_desc']}")
            if item['risk_warning'] != "无":
                st.error(f"**风险预警**：{item['risk_warning']}")

# --- 标签页 3：AI 顾问 ---
# --- 标签页 3：AI 顾问 ---
# --- 标签页 3：AI 顾问 ---
with tab3:
    st.header("🤖 AI 跨文化隐喻顾问")

    # 1. 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. 模型选择
    model_choice = st.radio(
        "选择 AI 模型：",
        ["deepseek-reasoner (深度思考，严谨但较慢)", "deepseek-chat (快速响应，适合日常对话)"],
        horizontal=True
    )
    model_id = "deepseek-reasoner" if "reasoner" in model_choice else "deepseek-chat"

    # 3. 提供超级提示词模板
    with st.expander("📝 点击展开：专业的【广告隐喻提问模板】（可编辑后发送）", expanded=False):
        default_template = """【角色】
你是跨文化广告隐喻顾问，同时懂目标市场广告法规中的“明显夸张（puffery）”边界。你的理论依据是概念隐喻：目标域 IS 源域，源域必须具体可感、文化可及、无情感创伤。

【任务】
为目标市场产品设计广告隐喻方向，输出要同时保留创意张力和风险可见性，并给出可入库的法务收口版。

【产品事实卡】（必须严格遵守，不得假设、不得外推）
- 国家/市场：英国
- 产品：扫地机器人
- 是否有摄像头：无
- 是否有麦克风：无
- 地图是否本地处理：是
- 导航能力：基础激光导航，不支持“学习户型/记忆户型”宣传
- 是否支持每日定时：是
- 价格带：中端
- 目标人群：城市中产家庭，含养宠家庭与小户型租房者
- 已知卖点：安静、省心、不打扰

【硬约束】
1. 不要“科技是魔法”作为主方向。
2. 不要“从不休假/不知疲倦/无偿服务/off duty”等劳工表达。
3. 不要主仆压迫、帝国庄园、精英化视觉。
4. 不要暗示产品替代人际陪伴。
5. 不要涉及婴儿、宠物健康、老人、健康安全的绝对承诺。
6. 每条广告语必须能对应事实卡中的至少一项；对应不上的，不得输出。
7. 管家/butler 只能作创意符号，不得每句直呼。
8. 每条广告语必须标：这是“明显夸张”还是“可能被当成事实宣称”。

【输出格式要求（极重要，必须严格遵守）】
第一部分：方向 + 广告语表
每个方向必须使用标准 Markdown 表格，表头如下：
| 广告语（英文） | 中文释义 | 对应隐喻 | 类型（夸张/事实宣称/情感表达） | 风险等级（低/中/高） | 风险点 | 法务收口版 |
|---|---|---|---|---|---|---|
（填写要求：夸张句保留需注明“靠明显夸张成立，不能配具体数据背书”。事实宣称类必须逐项对应事实卡。每个方向最后给一句“推荐投放版”，必须从收口版里选。中文只作内部释义，最终投放以英文收口版为准。）

第二部分：需规避隐喻清单
| 隐喻 | 为什么不适用 | 可能触发的风险 |
|---|---|---|

第三部分：跨方向投放建议
（主投方向、辅助方向、隐私事实锚点如何组合。）

第四部分：入库字段（JSON）
请输出一个结构化的 JSON 代码块（不要有任何多余的解释），字段名必须使用中文，结构如下：
{
  "国家": "填写国家/市场",
  "核心隐喻": "填写目标域 IS 源域",
  "表达方式": "填写源域的具体表达",
  "成功案例": "填写成功案例企业或产品",
  "案例描述": "一段话说明这个隐喻如何起作用",
  "风险预警": "用一段话覆盖所有中高风险点"
}

【交卷前自检】
在输出正文后，必须另起一节“自检表”，逐条回答以下 8 项，不得写“已检查无问题”：
1. 隐喻标签：每个方向的“目标域 IS 源域”是否成立？源域是否具体可感？有没有硬套理论标签？
2. 绝对词扫描：列出所有 never / always / everything / only / 100% / 从不 / 只 / 完全 / just，逐句说明是“明显夸张”还是“事实宣称”。
3. 事实宣称对卡：每条事实宣称是否逐项对应产品事实卡？对不上的标“高”，并给收口版。
4. 敏感人群：有没有涉及婴儿、宠物健康、老人、健康安全的承诺？有则标“高”并改写。
5. 三类风险：阶级/劳工/隐私，逐方向说明有没有擦边，擦边在哪。
6. 英文可用性：推荐投放版是否为自然英文？有没有中文直译痕迹？给一句英文重写建议。
7. 夸张与宣称是否分离：夸张句有没有挂数据或认证？事实句有没有混入拟人夸张？
8. 必须找出问题：至少列出 3 处你认为仍不够稳的表达，并给出修订版。如果确实找不到，说明你判断“稳”的依据。

【强制修订条款】
自检表第 8 项列出的“仍不够稳的表达”，必须在最终收口版中彻底替换，不得保留原风险词只做修饰。例如：
- 不得把“quiet enough”改成“designed to be quiet enough”；
- 不得保留“less”比较级却不给对比对象；
- 不得保留抽象词“baseline”却只说“可测试”。
若无法彻底替换，必须说明原因并标“高”风险。

【总评】
最后给一句总评：本稿是“可内部讨论 / 可入库草稿 / 可直接投放”中的哪一档，并说明还差什么。"""

        user_prompt_template = st.text_area("在这里修改产品信息后，点击下方按钮发送给 AI：", default_template, height=400)

        if st.button("🚀 使用此模板提问"):
            if not api_key:
                st.error("请先在左侧侧边栏输入你的 API Key！")
            else:
                st.session_state.messages.append({"role": "user", "content": user_prompt_template})
                st.rerun()

    # 4. 显示历史对话
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. 接收常规聊天输入
    if prompt := st.chat_input("或者直接在这里输入你的问题，按回车发送..."):
        if not api_key:
            st.error("请先在左侧侧边栏输入你的 API Key！")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    # 6. 核心调用逻辑
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and api_key:
        with st.chat_message("assistant"):
            wait_msg = "Reasoner 正在深度推演法务边界与隐喻映射，大概需要 30~60 秒..." if model_id == "deepseek-reasoner" else "AI 正在快速生成..."

            with st.spinner(wait_msg):
                try:
                    system_prompt = "你是一个严格按照用户指令输出内容的 AI。请绝对遵守用户的格式要求，不要遗漏任何表格和自检项。"
                    api_messages = [{"role": "system", "content": system_prompt}]
                    api_messages.extend(st.session_state.messages[-6:])

                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }

                    payload = {
                        "model": model_id,
                        "messages": api_messages,
                        "stream": False
                    }
                    if model_id == "deepseek-chat":
                        payload["temperature"] = 0.3

                    timeout_val = 180 if model_id == "deepseek-reasoner" else 60

                    res = requests.post("https://api.deepseek.com/chat/completions",
                                        json=payload, headers=headers, timeout=timeout_val)
                    res.raise_for_status()
                    reply_data = res.json()["choices"][0]["message"]
                    reply = reply_data.get("content", "")

                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                except Exception as e:
                    st.error(f"调用 API 失败：{e}")

                    #py -m streamlit run yinyu.py