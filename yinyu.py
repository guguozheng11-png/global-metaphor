import json
import os
import requests
import streamlit as st

# ================= 页面基础配置 =================
st.set_page_config(page_title="跨文化广告隐喻分析库", page_icon="🌍", layout="wide")

# 注入自定义 CSS 美化界面
st.markdown("""
    <style>
    .custom-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #4CAF50; }
    .risk-card { background-color: #ffebee; padding: 15px; border-radius: 8px; border-left: 5px solid #f44336; margin-top: 10px; }
    .culture-card { background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 5px solid #2196F3; margin-bottom: 20px;}
    h1, h2, h3 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)


# ================= 读取数据 =================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "data.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("countries", []), data.get("products", [])
    except Exception as e:
        st.error(f"数据读取失败，请检查 data.json 格式：{e}")
        return [], []


countries_data, products_data = load_data()
country_names = [c["name"] for c in countries_data]

# ================= 侧边栏 =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209421.png", width=80)
    st.title("🌍 设置中心")
    st.markdown("---")

    st.markdown("### 1. 选择目标国家")
    selected_country_name = st.selectbox("请选择要出海的国家/地区：", country_names)
    current_country = next((c for c in countries_data if c["name"] == selected_country_name), None)

    st.markdown("### 2. AI 顾问配置")
    api_key = st.text_input("输入 DeepSeek API Key：", type="password")
    if st.button("🗑️ 清空 AI 会话记录"):
        st.session_state.messages = []
        st.rerun()

# ================= 主界面 =================
st.title("跨文化广告隐喻分析库")
st.markdown("> 基于认知语言学与跨文化营销理论，辅助中国出海企业进行文案本地化适配。")

tab1, tab2, tab3, tab4 = st.tabs(["🌍 国家文化档案", "🧩 产品隐喻匹配", "📚 全球案例库", "🤖 AI 隐喻顾问"])

# --- Tab1: 国家文化档案 ---
with tab1:
    if current_country:
        st.header(f"📍 【{current_country['name']}】文化透视与禁忌雷达")

        st.markdown(f"""
        <div class="culture-card">
            <h3>🏛️ 文化底色</h3>
            <p>{current_country['culture']}</p>
            <h3>🔥 热门隐喻源域</h3>
            <p>{'、'.join(current_country['hot_metaphors'])}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚠️ 文化禁忌与风险预警")
        for taboo in current_country['taboos']:
            st.error(taboo)

# --- Tab2: 产品隐喻匹配器 ---
with tab2:
    st.header("🧩 产品隐喻匹配器")
    st.markdown("选择你的产品类别，系统将为你推荐合适的隐喻方向。你可以点击“一键发给AI”获取创意。")

    for prod in products_data:
        with st.expander(f"📦 {prod['category']}", expanded=True):
            st.markdown(f"**💡 适合的隐喻模板**：{', '.join(prod['suitable_metaphors'])}")
            st.markdown(f"**📝 创作建议**：{prod['tips']}")

            if st.button(f"✨ 用这些隐喻为【{selected_country_name}】设计广告语", key=prod['category']):
                if not api_key:
                    st.error("请先在左侧填写 API Key！")
                else:
                    quick_prompt = f"请结合【{selected_country_name}】的文化和禁忌，针对【{prod['category']}】产品，使用以下隐喻方向：{', '.join(prod['suitable_metaphors'])}，设计3句广告语。\n要求：给出目标语言原版、中文释义，并说明如何契合当地文化。"
                    st.session_state.quick_prompt = quick_prompt
                    st.success("指令已生成！请切换到最右侧的【🤖 AI 隐喻顾问】标签页，它会自动填入！")

# --- Tab3: 全球案例库（新增国家分类筛选） ---
with tab3:
    st.header("📚 全球案例速查与搜索")

    # 新增：先做国家分类，再做关键词搜索
    col_search1, col_search2 = st.columns([1, 2])
    with col_search1:
        filter_country = st.selectbox("按国家筛选：", ["全部国家"] + country_names)
    with col_search2:
        search_query = st.text_input("🔍 按关键词搜索（隐喻类型、案例名等）：", "")

    # 把所有国家的 cases 摊平
    all_cases = []
    for c in countries_data:
        for case in c.get("cases", []):
            case_copy = case.copy()
            case_copy["country"] = c["name"]
            all_cases.append(case_copy)

    # 过滤逻辑：先看国家，再看关键词
    filtered_data = all_cases
    if filter_country != "全部国家":
        filtered_data = [item for item in filtered_data if item['country'] == filter_country]

    if search_query:
        filtered_data = [item for item in filtered_data
                         if search_query.lower() in item['metaphor'].lower()
                         or search_query.lower() in item['success_case'].lower()
                         or search_query.lower() in item['success_desc'].lower()]

    st.markdown(f"共找到 **{len(filtered_data)}** 条相关案例：")

    for item in filtered_data:
        with st.expander(f"🌍 {item['country']} | {item['success_case']}（{item['metaphor']}）"):
            st.markdown(f"**🗣️ 表达方式**：{item['expression']}")
            st.markdown(f"**📝 案例描述**：{item['success_desc']}")
            if item.get('risk_warning', '无') != "无":
                st.error(f"**⚠️ 风险预警**：{item['risk_warning']}")

# --- Tab4: AI 顾问（恢复了高级模板） ---
with tab4:
    st.header("🤖 AI 跨文化隐喻顾问")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    model_choice = st.radio("选择模型：", ["deepseek-reasoner (深度)", "deepseek-chat (快速)"], horizontal=True)
    model_id = "deepseek-reasoner" if "reasoner" in model_choice else "deepseek-chat"

    # 快捷指令提示
    if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
        st.info(f"已接收到来自【产品匹配器】的指令：\n\n{st.session_state.quick_prompt}")
        if st.button("🚀 发送此快捷指令给 AI"):
            st.session_state.messages.append({"role": "user", "content": st.session_state.quick_prompt})
            del st.session_state.quick_prompt
            st.rerun()

    # 模式切换
    st.markdown("### 1. 填写产品信息")
    mode = st.radio("请选择填写模式：", ["📝 表单快速填写", "💻 高级模板编辑（适合微调指令）"], horizontal=True)

    # 获取当前国家的禁忌，方便自动填入
    taboo_str = '、'.join(current_country['taboos']) if current_country else '无'
    metaphor_str = '、'.join(current_country['hot_metaphors']) if current_country else '无'

    if mode == "📝 表单快速填写":
        with st.form("product_info_form"):
            col1, col2 = st.columns(2)
            with col1:
                input_product = st.text_input("产品类型", "扫地机器人")
                input_audience = st.text_input("目标人群", "城市中产家庭")
            with col2:
                input_skills = st.text_area("已知卖点", "安静、省心")

            submitted = st.form_submit_button("生成方案")
            if submitted and api_key:
                final_prompt = f"请作为跨文化广告专家，为【{input_product}】在【{selected_country_name}】市场设计隐喻方案。目标人群：{input_audience}。卖点：{input_skills}。请严格遵守当地禁忌：{taboo_str}。输出表格和自检表。"
                st.session_state.messages.append({"role": "user", "content": final_prompt})
                st.rerun()
    else:
        # 恢复高级模板
        default_template = f"""【角色】
你是跨文化广告隐喻顾问，同时懂目标市场广告法规中的“明显夸张（puffery）”边界。你的理论依据是概念隐喻：目标域 IS 源域，源域必须具体可感、文化可及、无情感创伤。

【任务】
为目标市场产品设计广告隐喻方向，输出要同时保留创意张力和风险可见性，并给出可入库的法务收口版。

【产品事实卡】（请在下方修改你的真实产品信息，必须严格遵守）
- 国家/市场：{selected_country_name}
- 产品：扫地机器人
- 隐私硬件情况：有摄像头
- 价格带：中端
- 目标人群：城市中产家庭
- 已知卖点：定时出粮、远程视频互动、不漏电安全设计

【当地文化约束与禁忌】
- 热门隐喻：{metaphor_str}
- 禁忌提醒：{taboo_str}

【硬约束】
1. 不要“科技是魔法”作为主方向。
2. 不要“从不休假/不知疲倦/无偿服务/off duty”等劳工表达。
3. 不要主仆压迫、帝国庄园、精英化视觉。
4. 不要暗示产品替代人际陪伴。
5. 不要涉及敏感人群的绝对承诺。
6. 每条广告语必须能对应事实卡中的至少一项；对应不上的，不得输出。
7. 每条广告语必须标：这是“明显夸张”还是“可能被当成事实宣称”。

【输出格式要求（极重要，必须严格遵守）】
第一部分：方向 + 广告语表
标准 Markdown 表格表头：
| 目标语言广告语 | 中文释义 | 英文释义 | 对应隐喻 | 类型 | 风险等级 | 风险点 | 法务收口版 |
（必须使用目标国家当地官方语言或通用商业语言。每个方向最后给一句“推荐投放版”。）

第二部分：需规避隐喻清单（表格）

第三部分：跨方向投放建议

第四部分：入库字段（JSON格式）

【交卷前自检】
必须另起一节“自检表”，逐条回答以下 8 项，不得写“已检查无问题”：
1. 隐喻标签：目标域 IS 源域是否成立？
2. 绝对词扫描：列出所有 never/always 等并说明类型。
3. 事实宣称对卡：逐项对应情况。
4. 敏感人群：涉及情况与改写。
5. 三类风险：阶级/劳工/隐私擦边说明。
6. 目标语言可用性：自然度与重写建议。
7. 夸张与宣称是否分离。
8. 必须找出问题：至少列出 3 处不够稳的表达并修订。

【总评】
最后给一句总评：本稿是“可内部讨论 / 可入库草稿 / 可直接投放”中的哪一档。"""

        user_prompt_template = st.text_area("直接编辑最终 Prompt（修改上方【产品事实卡】即可）：", default_template,
                                            height=450)

        if st.button("🚀 发送高级指令"):
            if not api_key:
                st.error("请先在左侧填写 API Key！")
            else:
                st.session_state.messages.append({"role": "user", "content": user_prompt_template})
                st.rerun()

    st.markdown("---")
    st.markdown("### 对话与结果")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("或者直接在这里输入你的问题..."):
        if not api_key:
            st.error("请先在左侧填写 API Key！")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    # 核心调用逻辑
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and api_key:
        with st.chat_message("assistant"):
            with st.spinner("AI 正在思考..."):
                try:
                    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                    payload = {"model": model_id, "messages": st.session_state.messages[-6:], "stream": False}
                    res = requests.post("https://api.deepseek.com/chat/completions", json=payload, headers=headers,
                                        timeout=180)
                    res.raise_for_status()
                    reply = res.json()["choices"][0]["message"].get("content", "")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"API 错误: {e}")