
import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="CEO BUSINESS TYCOON",
    page_icon="🏙️",
    layout="wide"
)

# ==========================
# 게임 디자인
# ==========================

st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #0b1020;
    color: #ffffff !important;
}

/* 기본 글자 */
html, body, p, span, label,
.stMarkdown, .stText, li {
    color: #f1f5f9 !important;
}

/* 제목 */
h1, h2, h3, h4, h5 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* 설명 글자 */
.stCaption, small {
    color: #cbd5e1 !important;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background-color: #111a2e;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* 입력창 */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #64748b !important;
}

/* 선택 메뉴 */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* 드롭다운 목록 */
[data-baseweb="popover"] {
    background-color: #1e293b !important;
}

[data-baseweb="menu"] * {
    color: #ffffff !important;
}

/* 버튼 */
div.stButton > button {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    min-height: 45px;
    font-weight: bold;
    width: 100%;
}

div.stButton > button:hover {
    background: #3b82f6;
    color: #ffffff !important;
    border: 1px solid #60a5fa;
}

/* 탭 */
button[data-baseweb="tab"] {
    color: #cbd5e1 !important;
    font-weight: bold;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38bdf8 !important;
}

/* 카드 */
.game-card {
    background: linear-gradient(135deg,#182640,#111827);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-bottom: 12px;
    color: #ffffff !important;
}

.game-card * {
    color: #ffffff !important;
}

/* 뉴스 */
.news-card {
    background: #17243a;
    border-left: 4px solid #38bdf8;
    padding: 15px;
    border-radius: 8px;
    margin: 8px 0;
    color: #ffffff !important;
}

/* 지표 */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg,#182640,#111a2e);
    border: 1px solid #30415e;
    border-radius: 14px;
    padding: 16px;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
}

div[data-testid="stMetricLabel"] {
    color: #ffffff !important;
}

/* 안내 상자 */
.stAlert {
    background-color: #1e293b !important;
}

.stAlert * {
    color: #ffffff !important;
}

/* 체크박스 */
.stCheckbox label {
    color: #ffffff !important;
}

/* 라디오 버튼 */
.stRadio label {
    color: #ffffff !important;
}

/* 슬라이더 */
.stSlider label {
    color: #ffffff !important;
}

/* 구분선 */
hr {
    border-color: #334155 !important;
}

/* 데이터프레임 */
[data-testid="stDataFrame"] {
    background-color: #17243a;
}

/* 표 */
table {
    color: #ffffff !important;
}

th {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

td {
    color: #f1f5f9 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================
# 게임 데이터 생성
# ==========================

def init_game(company, product, category, price, cost, quality):

    st.session_state.g = {
        "company": company,
        "product": product,
        "category": category,

        "day": 1,

        "money": 100_000_000,
        "debt": 0,

        "price": price,
        "cost": cost,

        "quality": quality,
        "marketing": 10,
        "brand": 10,
        "reputation": 30,
        "satisfaction": 50,

        "workers": 3,
        "capacity": 100,
        "production": 50,
        "inventory": 50,

        "stores": 1,
        "technology": 1,

        "market_share": 5.0,

        "competitor_price": int(price * 1.1),
        "competitor_strength": 30,

        "sales": 0,
        "expenses": 0,
        "profit": 0,
        "total_sold": 0,

        "history": [],
        "logs": [],
        "events": [],

        "finished": False,

        "last_revenue": 0,
        "last_profit": 0,
        "last_sold": 0,

        "last_event": "새로운 기업이 탄생했습니다!"
    }

    st.session_state.started = True


# ==========================
# 경영 기록
# ==========================

def log(msg):

    g = st.session_state.g

    g["logs"].append(
        f"{g['day']}일차 | {msg}"
    )

    g["logs"] = g["logs"][-50:]


# ==========================
# 공통 함수
# ==========================

def money(n):
    return f"{int(n):,}원"


def clamp(v):
    return max(0, min(100, v))


def spend(amount):

    g = st.session_state.g

    if g["money"] < amount:
        st.error("자금이 부족합니다!")
        return False

    g["money"] -= amount
    g["expenses"] += amount

    return True


# ==========================
# 게임 초기화
# ==========================

if "started" not in st.session_state:
    st.session_state.started = False


# ==========================
# 창업 화면
# ==========================

if not st.session_state.started:

    st.markdown(
        "<h1 style='text-align:center;color:#38bdf8'>🏙️ BUSINESS TYCOON</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center'>YOUR COMPANY. YOUR RULES.</h3>",
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        "당신은 이제 한 기업의 CEO입니다. "
        "작은 스타트업을 세계적인 기업으로 성장시키세요."
    )

    with st.container(border=True):

        st.subheader("🏢 나만의 기업 만들기")

        company = st.text_input(
            "기업 이름",
            "NEXUS GROUP"
        )

        product = st.text_input(
            "판매할 상품",
            "스마트 텀블러"
        )

        category = st.selectbox(
            "사업 분야",
            [
                "전자제품",
                "식품",
                "패션",
                "화장품",
                "게임",
                "IT",
                "인공지능",
                "생활용품",
                "자동차",
                "기타"
            ]
        )

        a, b = st.columns(2)

        with a:

            price = st.number_input(
                "상품 판매 가격",
                min_value=100,
                max_value=10000000,
                value=20000,
                step=1000
            )

        with b:

            cost = st.number_input(
                "상품 생산 원가",
                min_value=100,
                max_value=10000000,
                value=8000,
                step=500
            )

        quality = st.slider(
            "초기 제품 품질",
            10,
            100,
            50
        )

        st.divider()

        st.write("💰 초기 자본금: 1억 원")
        st.write("📢 초기 마케팅 효과: 10점")
        st.write("🏭 초기 생산 능력: 100개")
        st.write("📅 경영 기간: 30일")

        if st.button(
            "🚀 기업 창업 시작",
            type="primary"
        ):

            if not company.strip() or not product.strip():

                st.error("회사 이름과 상품명을 입력하세요.")

            elif price <= cost:

                st.error("판매 가격은 생산 원가보다 높아야 합니다.")

            else:

                init_game(
                    company,
                    product,
                    category,
                    price,
                    cost,
                    quality
                )

                st.rerun()

    st.stop()


# ==========================
# 게임 데이터 불러오기
# ==========================

g = st.session_state.g


# ==========================
# 게임 종료 화면
# ==========================

if g["finished"]:

    st.title("🏆 BUSINESS TYCOON")
    st.header("최종 경영 결과")

    net = g["money"] - g["debt"]

    if g["money"] <= 0:
        grade = "F - 기업 파산"

    elif net >= 300_000_000 and g["reputation"] >= 80:
        grade = "S - 전설적인 CEO"

    elif net >= 200_000_000:
        grade = "A - 성공한 CEO"

    elif net >= 100_000_000:
        grade = "B - 안정적인 기업"

    elif net > 0:
        grade = "C - 성장 가능성"

    else:
        grade = "F - 경영 실패"

    st.subheader(grade)

    a, b, c = st.columns(3)

    a.metric("최종 현금", money(g["money"]))
    b.metric("순자산", money(net))
    c.metric("누적 매출", money(g["sales"]))

    a, b, c = st.columns(3)

    a.metric("총 판매량", f"{g['total_sold']:,}개")
    b.metric("기업 평판", f"{g['reputation']}/100")
    c.metric("시장 점유율", f"{g['market_share']:.1f}%")

    if g["money"] > 0:
        st.balloons()

    if st.button("새로운 기업 창업"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()

    st.stop()


# ==========================
# 상단 게임 HUD
# ==========================

st.markdown(
    f"""
    <div class="game-card">
        <h1>🏙️ {g['company']}</h1>
        <p>CEO MANAGEMENT SIMULATOR</p>
        <h3>주력 상품: {g['product']}</h3>
        <p>DAY {g['day']} / 30</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(min(g["day"] / 30, 1))

a, b, c, d = st.columns(4)

a.metric("💰 보유 자금", money(g["money"]))
b.metric("📈 누적 매출", money(g["sales"]))
c.metric("💸 누적 지출", money(g["expenses"]))
d.metric("🏦 부채", money(g["debt"]))

a, b, c, d = st.columns(4)

a.metric("📢 마케팅", f"{g['marketing']}/100")
b.metric("⭐ 제품 품질", f"{g['quality']}/100")
c.metric("😊 고객 만족도", f"{g['satisfaction']}/100")
d.metric("🏆 기업 평판", f"{g['reputation']}/100")

st.divider()


# ==========================
# 게임 메뉴
# ==========================

tabs = st.tabs([
    "🏠 본사",
    "📢 마케팅",
    "🏭 생산",
    "🔬 연구개발",
    "👥 인사",
    "🏬 확장",
    "📊 기업 정보"
])


# ==========================
# 본사
# ==========================

with tabs[0]:

    st.header("🏢 CEO 본사")

    a, b, c = st.columns(3)

    a.metric("판매 가격", money(g["price"]))
    b.metric("생산 원가", money(g["cost"]))
    c.metric("개당 마진", money(g["price"] - g["cost"]))

    st.subheader("📦 재고 현황")

    a, b = st.columns(2)

    a.metric("현재 재고", f"{g['inventory']:,}개")
    b.metric("하루 생산 능력", f"{g['capacity']:,}개")

    st.divider()

    st.subheader("💵 상품 가격 결정")

    new_price = st.number_input(
        "상품 판매 가격 변경",
        min_value=100,
        max_value=10000000,
        value=int(g["price"]),
        step=500,
        key="main_price"
    )

    if st.button("가격 변경 적용"):

        g["price"] = new_price

        log(f"판매 가격을 {money(new_price)}으로 변경")

        st.success("가격이 변경되었습니다!")

        st.rerun()

    st.divider()

    st.subheader("⚔️ 경쟁사 정보")

    a, b = st.columns(2)

    a.metric(
        "경쟁사 가격",
        money(g["competitor_price"])
    )

    b.metric(
        "경쟁사 경쟁력",
        f"{g['competitor_strength']}/100"
    )

    st.subheader("📰 최근 시장 뉴스")

    for event in reversed(g["events"][-5:]):

        st.markdown(
            f'<div class="news-card">{event}</div>',
            unsafe_allow_html=True
        )

    if not g["events"]:
        st.info("아직 발생한 시장 사건이 없습니다.")


# ==========================
# 마케팅 시스템
# ==========================

with tabs[1]:

    st.header("📢 마케팅 본부")

    st.write(
        "다양한 광고 전략을 선택하세요. "
        "광고에는 성공과 실패 확률이 있으며 "
        "실패하면 마케팅 효과가 감소할 수 있습니다."
    )

    st.divider()

    a, b = st.columns(2)

    with a:

        st.metric(
            "현재 마케팅 효과",
            f"{g['marketing']}/100"
        )

    with b:

        st.metric(
            "브랜드 인지도",
            f"{g['brand']}/100"
        )

    st.progress(g["marketing"] / 100)

    st.caption(
        "마케팅 효과는 하루가 지날 때 자연스럽게 감소할 수도 있습니다."
    )

    st.divider()

    # 광고 이름:
    # 비용, 성공 확률, 성공 상승 최소, 성공 상승 최대,
    # 실패 하락 최소, 실패 하락 최대

    marketing_methods = {

        "📱 SNS 광고":
        (1000000, 0.80, 5, 12, 3, 10),

        "📺 TV 광고":
        (8000000, 0.55, 8, 20, 5, 15),

        "▶️ 유튜브 광고":
        (4000000, 0.70, 6, 18, 3, 12),

        "🌟 인플루언서 협찬":
        (3000000, 0.65, 5, 20, 5, 15),

        "🔍 검색 광고":
        (1500000, 0.85, 4, 10, 2, 8),

        "🔥 바이럴 마케팅":
        (500000, 0.40, 10, 30, 8, 20),

        "🏷️ 할인 행사":
        (2000000, 0.75, 3, 12, 2, 8),

        "🎤 유명인 모델 계약":
        (12000000, 0.50, 10, 25, 8, 20),

        "⚽ 스포츠 후원":
        (10000000, 0.60, 8, 22, 5, 15),

        "🏙️ 옥외 광고":
        (5000000, 0.60, 5, 15, 4, 12),

        "📧 이메일 마케팅":
        (300000, 0.90, 2, 8, 1, 5),

        "🎪 오프라인 이벤트":
        (2500000, 0.70, 4, 15, 3, 10)
    }

    selected = st.selectbox(
        "마케팅 방법 선택",
        list(marketing_methods.keys())
    )

    data = marketing_methods[selected]

    ad_cost = data[0]
    probability = data[1]
    success_min = data[2]
    success_max = data[3]
    fail_min = data[4]
    fail_max = data[5]

    st.markdown(
        '<div class="game-card">',
        unsafe_allow_html=True
    )

    st.subheader(selected)

    a, b = st.columns(2)

    a.metric("광고 비용", money(ad_cost))
    b.metric("성공 확률", f"{probability * 100:.0f}%")

    st.write(
        f"성공 시 마케팅 상승: +{success_min}~{success_max}점"
    )

    st.write(
        f"실패 시 마케팅 하락: -{fail_min}~-{fail_max}점"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "📣 광고 실행하기",
        type="primary"
    ):

        if spend(ad_cost):

            if random.random() < probability:

                gain = random.randint(
                    success_min,
                    success_max
                )

                g["marketing"] = clamp(
                    g["marketing"] + gain
                )

                g["brand"] = clamp(
                    g["brand"] + random.randint(2, 5)
                )

                g["reputation"] = clamp(
                    g["reputation"] + random.randint(0, 3)
                )

                log(
                    f"{selected} 성공! 마케팅 +{gain}점"
                )

                st.success(
                    f"🎉 광고 대성공! 마케팅 효과가 {gain}점 상승했습니다!"
                )

                st.balloons()

            else:

                loss = random.randint(
                    fail_min,
                    fail_max
                )

                g["marketing"] = clamp(
                    g["marketing"] - loss
                )

                g["reputation"] = clamp(
                    g["reputation"] - random.randint(0, 3)
                )

                log(
                    f"{selected} 실패! 마케팅 -{loss}점"
                )

                st.error(
                    f"💥 광고 실패! 마케팅 효과가 {loss}점 감소했습니다."
                )

            st.rerun()

    st.divider()

    st.subheader("📊 마케팅 상태")

    a, b, c = st.columns(3)

    a.metric(
        "마케팅 효과",
        f"{g['marketing']}/100"
    )

    b.metric(
        "브랜드 인지도",
        f"{g['brand']}/100"
    )

    c.metric(
        "기업 평판",
        f"{g['reputation']}/100"
    )

    st.progress(g["marketing"] / 100)

    st.caption(
        "광고를 무작정 많이 한다고 성공하는 것은 아닙니다. "
        "자금 상황과 광고 성공 확률을 고려하세요."
    )

# ==========================
# 생산 관리
# ==========================

with tabs[2]:

    st.header("🏭 생산 공장")

    st.caption("생산량을 조절하고 재고를 관리하세요.")

    a, b, c = st.columns(3)

    a.metric("현재 재고", f"{g['inventory']:,}개")
    b.metric("생산 능력", f"{g['capacity']:,}개")
    c.metric("하루 생산량", f"{g['production']:,}개")

    st.divider()

    st.subheader("⚙️ 생산 계획")

    production = st.slider(
        "하루 생산량 설정",
        min_value=0,
        max_value=g["capacity"],
        value=min(g["production"], g["capacity"]),
        key="production_slider"
    )

    production_cost = production * g["cost"]

    st.write(f"예상 생산 비용: {money(production_cost)}")

    if st.button("생산 계획 저장"):

        g["production"] = production

        log(f"생산 계획을 {production}개로 변경")

        st.success("생산 계획이 저장되었습니다.")

        st.rerun()

    st.divider()

    st.subheader("📦 재고 관리")

    if g["inventory"] > 200:

        st.warning("재고가 너무 많습니다. 보관 비용이 발생할 수 있습니다.")

    elif g["inventory"] < 20:

        st.warning("재고가 부족합니다. 판매 기회를 놓칠 수 있습니다.")

    else:

        st.success("재고가 안정적인 수준입니다.")

    st.metric(
        "예상 재고 가치",
        money(g["inventory"] * g["cost"])
    )

    st.divider()

    st.subheader("🔧 공장 업그레이드")

    st.write("생산 능력을 50개 증가시킵니다.")

    if st.button("공장 확장 (1,500만 원)"):

        if spend(15000000):

            g["capacity"] += 50

            log("공장 확장! 생산 능력 +50개")

            st.success("공장 확장 완료!")

            st.rerun()

    st.divider()

    st.subheader("⚔️ 경쟁사 분석")

    a, b = st.columns(2)

    a.metric(
        "경쟁사 판매 가격",
        money(g["competitor_price"])
    )

    b.metric(
        "경쟁사 경쟁력",
        f"{g['competitor_strength']}/100"
    )

    if st.button("경쟁사 시장 조사 (50만 원)"):

        if spend(500000):

            log("경쟁사 시장 조사 완료")

            st.success(
                f"경쟁사 판매 가격은 {money(g['competitor_price'])}입니다."
            )

            st.rerun()


# ==========================
# 연구개발
# ==========================

with tabs[3]:

    st.header("🔬 연구개발 센터")

    st.caption("기술력을 높이고 제품 경쟁력을 확보하세요.")

    a, b, c = st.columns(3)

    a.metric(
        "제품 품질",
        f"{g['quality']}/100"
    )

    b.metric(
        "기술 단계",
        f"{g['technology']}단계"
    )

    c.metric(
        "브랜드 인지도",
        f"{g['brand']}/100"
    )

    st.progress(g["quality"] / 100)

    st.divider()

    research_options = {

        "⭐ 제품 품질 개선": {
            "cost": 5000000,
            "description": "제품 품질을 무작위로 4~10점 높입니다."
        },

        "🏭 생산 기술 연구": {
            "cost": 7000000,
            "description": "기술 단계와 생산 능력을 높입니다."
        },

        "💡 신제품 연구": {
            "cost": 10000000,
            "description": "브랜드와 기술력을 발전시킵니다."
        },

        "🧪 고급 소재 연구": {
            "cost": 15000000,
            "description": "제품 품질을 크게 개선할 기회를 얻습니다."
        }
    }

    selected_research = st.selectbox(
        "연구개발 분야 선택",
        list(research_options.keys())
    )

    research = research_options[selected_research]

    st.markdown(
        '<div class="game-card">',
        unsafe_allow_html=True
    )

    st.subheader(selected_research)

    st.write(research["description"])

    st.write(
        f"투자 비용: {money(research['cost'])}"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔬 연구개발 시작"):

        if spend(research["cost"]):

            if selected_research == "⭐ 제품 품질 개선":

                gain = random.randint(4, 10)

                g["quality"] = clamp(
                    g["quality"] + gain
                )

                log(f"제품 품질 개선 성공! +{gain}점")

                st.success(
                    f"제품 품질이 {gain}점 상승했습니다!"
                )

            elif selected_research == "🏭 생산 기술 연구":

                g["technology"] += 1

                g["capacity"] += 15

                log(
                    "생산 기술 발전! 생산 능력 +15개"
                )

                st.success(
                    "기술 단계와 생산 능력이 상승했습니다!"
                )

            elif selected_research == "💡 신제품 연구":

                gain = random.randint(2, 8)

                g["brand"] = clamp(
                    g["brand"] + gain
                )

                g["technology"] += 1

                log(
                    f"신제품 연구 성공! 브랜드 +{gain}"
                )

                st.success("신제품 연구에 성공했습니다!")

            else:

                if random.random() < 0.65:

                    gain = random.randint(10, 20)

                    g["quality"] = clamp(
                        g["quality"] + gain
                    )

                    g["cost"] = max(
                        100,
                        int(g["cost"] * 0.95)
                    )

                    log(
                        f"고급 소재 연구 성공! 품질 +{gain}"
                    )

                    st.success(
                        f"연구 성공! 품질 +{gain}, 생산 원가 5% 감소!"
                    )

                else:

                    loss = random.randint(3, 7)

                    g["quality"] = clamp(
                        g["quality"] - loss
                    )

                    log(
                        f"고급 소재 연구 실패! 품질 -{loss}"
                    )

                    st.error(
                        f"연구 실패! 품질이 {loss}점 하락했습니다."
                    )

            st.rerun()

    st.divider()

    st.subheader("📚 기술 현황")

    st.write(f"현재 기술 단계: {g['technology']}")

    st.write(f"현재 제품 품질: {g['quality']}/100")

    st.write(f"현재 생산 원가: {money(g['cost'])}")


# ==========================
# 인사 관리
# ==========================

with tabs[4]:

    st.header("👥 인사 관리")

    st.caption("직원을 채용하고 기업의 생산 능력을 높이세요.")

    a, b, c = st.columns(3)

    a.metric("직원 수", f"{g['workers']}명")

    b.metric("생산 능력", f"{g['capacity']}개")

    c.metric(
        "하루 급여",
        money(g["workers"] * 200000)
    )

    st.divider()

    st.subheader("👨‍💼 직원 채용")

    st.write("직원 1명을 채용하면 생산 능력이 20개 증가합니다.")

    if st.button("➕ 직원 채용 (200만 원)"):

        if spend(2000000):

            g["workers"] += 1

            g["capacity"] += 20

            log("직원 1명 채용 완료")

            st.success("신규 직원이 입사했습니다!")

            st.rerun()

    st.divider()

    st.subheader("📉 직원 해고")

    if st.button("직원 1명 해고"):

        if g["workers"] > 1:

            g["workers"] -= 1

            g["capacity"] = max(
                20,
                g["capacity"] - 20
            )

            log("직원 1명 해고")

            st.warning("직원 1명을 해고했습니다.")

            st.rerun()

        else:

            st.error("최소 1명의 직원은 유지해야 합니다.")

    st.divider()

    st.subheader("🎁 직원 복지")

    st.write(
        "복지 제도를 도입하면 직원들의 사기를 높일 수 있습니다."
    )

    if st.button("직원 복지 투자 (300만 원)"):

        if spend(3000000):

            g["reputation"] = clamp(
                g["reputation"] + 3
            )

            g["satisfaction"] = clamp(
                g["satisfaction"] + 5
            )

            log("직원 복지 제도 도입")

            st.success(
                "직원 복지 제도를 도입했습니다!"
            )

            st.rerun()


# ==========================
# 사업 확장
# ==========================

with tabs[5]:

    st.header("🏬 사업 확장 본부")

    st.caption(
        "사업 규모를 확대하고 새로운 시장에 진출하세요."
    )

    a, b, c = st.columns(3)

    a.metric("현재 매장 수", f"{g['stores']}개")

    b.metric("보유 자금", money(g["money"]))

    c.metric("현재 부채", money(g["debt"]))

    st.divider()

    st.subheader("🏪 신규 매장 개설")

    st.write(
        "매장을 개설하면 판매 수요가 증가하지만 "
        "매일 임대료가 발생합니다."
    )

    if st.button("신규 매장 개설 (1,000만 원)"):

        if spend(10000000):

            g["stores"] += 1

            log("신규 매장 개설 완료!")

            st.success("새로운 매장이 개설되었습니다!")

            st.rerun()

    st.divider()

    st.subheader("🏦 은행 대출")

    st.write("대출 한도: 총 5,000만 원")

    a, b = st.columns(2)

    a.metric("현재 부채", money(g["debt"]))

    b.metric(
        "대출 가능 금액",
        money(max(0, 50000000 - g["debt"]))
    )

    if st.button("1,000만 원 대출"):

        if g["debt"] + 10000000 <= 50000000:

            g["money"] += 10000000

            g["debt"] += 10000000

            log("은행에서 1,000만 원 대출")

            st.success("대출이 승인되었습니다!")

            st.rerun()

        else:

            st.error("대출 한도를 초과했습니다.")

    st.divider()

    st.subheader("💳 대출 상환")

    repayment = st.number_input(
        "상환할 금액",
        min_value=0,
        max_value=max(0, g["debt"]),
        value=0,
        step=1000000,
        key="repayment_input"
    )

    if st.button("대출 상환"):

        if repayment > 0 and g["money"] >= repayment:

            g["money"] -= repayment

            g["debt"] -= repayment

            log(
                f"은행 대출 {money(repayment)} 상환"
            )

            st.success("대출을 상환했습니다!")

            st.rerun()

        else:

            st.error(
                "상환 금액을 확인하거나 보유 자금을 확인하세요."
            )

    st.divider()

    st.subheader("🌍 해외 시장 진출")

    st.write(
        "해외 시장 진출에 성공하면 브랜드 인지도와 "
        "시장 점유율이 상승합니다."
    )

    if st.button("해외 시장 진출 (2,000만 원)"):

        if spend(20000000):

            if random.random() < 0.65:

                gain = random.randint(5, 15)

                g["brand"] = clamp(
                    g["brand"] + gain
                )

                g["market_share"] = min(
                    100,
                    g["market_share"] + random.uniform(1, 4)
                )

                g["reputation"] = clamp(
                    g["reputation"] + 5
                )

                log(
                    f"해외 진출 성공! 브랜드 +{gain}"
                )

                st.success(
                    "🌍 해외 시장 진출에 성공했습니다!"
                )

                st.balloons()

            else:

                loss = random.randint(3, 8)

                g["reputation"] = clamp(
                    g["reputation"] - loss
                )

                log(
                    f"해외 진출 실패! 평판 -{loss}"
                )

                st.error(
                    f"해외 진출 실패! 평판이 {loss}점 하락했습니다."
                )

            st.rerun()

# ==========================
# 기업 정보 및 통계
# ==========================

with tabs[6]:

    st.header("📊 기업 분석 센터")

    st.caption("기업의 성장과 재무 상태를 분석하세요.")

    a, b, c = st.columns(3)

    a.metric(
        "시장 점유율",
        f"{g['market_share']:.1f}%"
    )

    b.metric(
        "브랜드 인지도",
        f"{g['brand']}/100"
    )

    c.metric(
        "기업 평판",
        f"{g['reputation']}/100"
    )

    a, b, c = st.columns(3)

    a.metric(
        "누적 판매량",
        f"{g['total_sold']:,}개"
    )

    b.metric(
        "누적 손익",
        money(g["profit"])
    )

    c.metric(
        "현재 순자산",
        money(g["money"] - g["debt"])
    )

    st.divider()

    st.subheader("📈 매출 및 순이익 그래프")

    if g["history"]:

        df = pd.DataFrame(g["history"])

        st.line_chart(
            df.set_index("day")[["revenue", "profit"]]
        )

    else:

        st.info(
            "아직 데이터가 없습니다. 하루를 진행하면 그래프가 생성됩니다."
        )

    st.divider()

    st.subheader("📜 기업 경영 일지")

    if g["logs"]:

        for item in reversed(g["logs"][-20:]):

            st.write("📌 " + item)

    else:

        st.info("아직 경영 기록이 없습니다.")


# ==========================
# 하루 진행 화면
# ==========================

st.divider()

st.markdown(
    """
    <h2 style='text-align:center;color:#38bdf8'>
    ⏳ CEO TURN SYSTEM
    </h2>
    <p style='text-align:center'>
    오늘의 경영 결정을 마쳤다면 다음 날로 넘어가세요.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="game-card">
        <h3>📅 DAY {g['day']} 경영 상황</h3>
        <p>보유 자금: {money(g['money'])}</p>
        <p>예정 생산량: {g['production']}개</p>
        <p>현재 재고: {g['inventory']}개</p>
        <p>판매 가격: {money(g['price'])}</p>
        <p>마케팅 효과: {g['marketing']}/100</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================
# 하루 진행
# ==========================

if st.button(
    "▶ 다음 날 진행하기",
    type="primary",
    use_container_width=True
):

    produced = g["production"]

    production_cost = produced * g["cost"]

    # 생산비 확인

    if g["money"] < production_cost:

        st.error(
            "생산 비용이 부족합니다. 생산량을 줄이거나 대출을 받으세요."
        )

        st.stop()

    # 생산 비용 지출

    g["money"] -= production_cost

    g["expenses"] += production_cost

    g["inventory"] += produced

    # ======================
    # 경쟁사 변화
    # ======================

    if random.random() < 0.25:

        change = random.uniform(0.90, 1.10)

        g["competitor_price"] = max(
            100,
            int(g["competitor_price"] * change)
        )

    # ======================
    # 시장 수요 계산
    # ======================

    price_ratio = (
        g["price"] /
        max(1, g["competitor_price"])
    )

    price_factor = max(
        0.2,
        min(1.7, 1.5 - price_ratio)
    )

    quality_factor = (
        0.5 + g["quality"] / 100
    )

    marketing_factor = (
        0.5 + g["marketing"] / 100
    )

    satisfaction_factor = (
        0.5 + g["satisfaction"] / 100
    )

    brand_factor = (
        0.7 + g["brand"] / 200
    )

    technology_factor = (
        1 + g["technology"] * 0.05
    )

    store_factor = (
        1 + g["stores"] * 0.2
    )

    competitor_factor = (
        1 - g["competitor_strength"] / 200
    )

    random_factor = random.uniform(0.7, 1.5)

    demand = int(
        40
        * price_factor
        * quality_factor
        * marketing_factor
        * satisfaction_factor
        * brand_factor
        * technology_factor
        * store_factor
        * competitor_factor
        * random_factor
    )

    demand = max(0, demand)

    # 실제 판매량은 재고를 초과할 수 없음

    sold = min(
        demand,
        g["inventory"]
    )

    # ======================
    # 매출 계산
    # ======================

    revenue = sold * g["price"]

    # ======================
    # 고정 지출
    # ======================

    salary = g["workers"] * 200000

    rent = g["stores"] * 300000

    interest = int(
        g["debt"] * 0.001
    )

    daily_expenses = (
        salary + rent + interest
    )

    # ======================
    # 하루 손익
    # ======================

    daily_profit = (
        revenue
        - production_cost
        - daily_expenses
    )

    g["money"] += (
        revenue - daily_expenses
    )

    g["sales"] += revenue

    g["expenses"] += daily_expenses

    g["profit"] += daily_profit

    g["inventory"] -= sold

    g["total_sold"] += sold

    g["last_revenue"] = revenue

    g["last_profit"] = daily_profit

    g["last_sold"] = sold

    # ======================
    # 고객 만족도 변화
    # ======================

    if price_ratio > 1.3:

        g["satisfaction"] -= random.randint(2, 6)

    elif g["quality"] >= 75:

        g["satisfaction"] += random.randint(1, 4)

    else:

        g["satisfaction"] += random.randint(-2, 3)

    g["satisfaction"] = clamp(
        g["satisfaction"]
    )

    # ======================
    # 기업 평판 변화
    # ======================

    if g["satisfaction"] >= 80:

        g["reputation"] += random.randint(1, 3)

    elif g["satisfaction"] < 30:

        g["reputation"] -= random.randint(2, 5)

    g["reputation"] = clamp(
        g["reputation"]
    )

    # ======================
    # 시장 점유율
    # ======================

    g["market_share"] = max(
        0,
        min(
            100,
            g["market_share"]
            + random.uniform(-1, 1)
            + (g["marketing"] - 20) / 100
        )
    )

    # ======================
    # 마케팅 자연 감소
    # ======================

    marketing_loss = random.randint(0, 3)

    g["marketing"] = clamp(
        g["marketing"] - marketing_loss
    )

    # ======================
    # 재고 보관 비용
    # ======================

    if g["inventory"] > 100:

        storage_cost = (
            g["inventory"] - 100
        ) * 100

        g["money"] -= storage_cost

        g["expenses"] += storage_cost

        g["profit"] -= storage_cost

    # ======================
    # 랜덤 사건 18가지
    # ======================

    event = random.randint(1, 18)

    if event == 1:

        bonus = 5000000

        g["money"] += bonus

        g["profit"] += bonus

        g["last_event"] = (
            "🎉 제품 대박! 특별 수익 500만 원!"
        )

    elif event == 2:

        loss = 3000000

        g["money"] -= loss

        g["expenses"] += loss

        g["profit"] -= loss

        g["last_event"] = (
            "📉 경기 침체! 300만 원 손실!"
        )

    elif event == 3:

        g["reputation"] = clamp(
            g["reputation"] + 10
        )

        g["last_event"] = (
            "🏆 우수 기업 선정! 기업 평판 상승!"
        )

    elif event == 4:

        loss = 2000000

        g["money"] -= loss

        g["expenses"] += loss

        g["profit"] -= loss

        g["last_event"] = (
            "⚠️ 설비 고장! 수리비 200만 원!"
        )

    elif event == 5:

        g["quality"] = clamp(
            g["quality"] - 10
        )

        g["last_event"] = (
            "😡 품질 논란! 제품 품질 하락!"
        )

    elif event == 6:

        loss = random.randint(5, 15)

        g["marketing"] = clamp(
            g["marketing"] - loss
        )

        g["last_event"] = (
            f"📢 광고 피로도 증가! 마케팅 -{loss}점!"
        )

    elif event == 7:

        g["quality"] = clamp(
            g["quality"] + 5
        )

        g["last_event"] = (
            "💡 기술 혁신! 제품 품질 상승!"
        )

    elif event == 8:

        g["competitor_strength"] = min(
            90,
            g["competitor_strength"] + 10
        )

        g["last_event"] = (
            "⚔️ 강력한 경쟁사 등장!"
        )

    elif event == 9:

        g["satisfaction"] = clamp(
            g["satisfaction"] + 10
        )

        g["last_event"] = (
            "😊 고객 만족도 상승!"
        )

    elif event == 10:

        g["cost"] = int(
            g["cost"] * 1.10
        )

        g["last_event"] = (
            "📦 원자재 가격 상승! 생산 원가 10% 증가!"
        )

    elif event == 11:

        g["market_share"] = min(
            100,
            g["market_share"] + 5
        )

        g["last_event"] = (
            "🚀 시장 점유율 상승!"
        )

    elif event == 12:

        g["satisfaction"] = clamp(
            g["satisfaction"] - 15
        )

        g["last_event"] = (
            "🔥 제품 불량 논란! 고객 만족도 급락!"
        )

    elif event == 13:

        g["competitor_price"] = max(
            100,
            int(g["competitor_price"] * 0.85)
        )

        g["last_event"] = (
            "💥 경쟁사 가격 인하! 가격 경쟁 심화!"
        )

    elif event == 14:

        bonus = 2000000

        g["money"] += bonus

        g["last_event"] = (
            "🤝 투자자 유치 성공! 현금 200만 원 확보!"
        )

    elif event == 15:

        g["workers"] = max(
            1,
            g["workers"] - 1
        )

        g["capacity"] = max(
            20,
            g["capacity"] - 20
        )

        g["last_event"] = (
            "👷 직원 퇴사! 생산 능력 감소!"
        )

    elif event == 16:

        g["satisfaction"] = clamp(
            g["satisfaction"] - 10
        )

        g["reputation"] = clamp(
            g["reputation"] - 8
        )

        g["last_event"] = (
            "📰 부정적인 언론 보도! 기업 평판 하락!"
        )

    elif event == 17:

        g["brand"] = clamp(
            g["brand"] + 10
        )

        g["last_event"] = (
            "✨ 브랜드 인지도 상승!"
        )

    else:

        g["last_event"] = (
            "☀️ 특별한 사건 없이 하루가 지나갔습니다."
        )

    # ======================
    # 경영 기록 저장
    # ======================

    g["history"].append({
        "day": g["day"],
        "revenue": revenue,
        "profit": daily_profit
    })

    g["events"].append(
        g["last_event"]
    )

    g["events"] = g["events"][-20:]

    log(
        f"매출 {money(revenue)} | "
        f"판매량 {sold}개 | "
        f"당일 손익 {money(daily_profit)}"
    )

    # ======================
    # 날짜 증가
    # ======================

    g["day"] += 1

    # ======================
    # 파산 및 엔딩 조건
    # ======================

    if g["money"] <= 0:

        g["finished"] = True

        log("💥 자금 고갈로 기업 파산!")

    elif g["satisfaction"] <= 0:

        g["finished"] = True

        log("💥 고객 만족도 붕괴!")

    elif g["day"] > 30:

        g["finished"] = True

        log("🎉 30일 경영 완료!")

    st.rerun()


# ==========================
# 사이드바 CEO 프로필
# ==========================

st.sidebar.markdown("# 🏙️ CEO MENU")

st.sidebar.caption(
    "BUSINESS TYCOON"
)

st.sidebar.divider()

st.sidebar.subheader("👤 CEO PROFILE")

st.sidebar.write(
    f"🏢 {g['company']}"
)

st.sidebar.write(
    f"📦 {g['product']}"
)

st.sidebar.write(
    f"📅 DAY {min(g['day'], 30)}/30"
)

st.sidebar.divider()

st.sidebar.subheader("💰 재무 현황")

st.sidebar.metric(
    "현금",
    money(g["money"])
)

st.sidebar.metric(
    "부채",
    money(g["debt"])
)

st.sidebar.metric(
    "순자산",
    money(g["money"] - g["debt"])
)

st.sidebar.divider()

st.sidebar.subheader("📊 기업 능력")

st.sidebar.write("마케팅")

st.sidebar.progress(
    g["marketing"] / 100
)

st.sidebar.write("제품 품질")

st.sidebar.progress(
    g["quality"] / 100
)

st.sidebar.write("고객 만족도")

st.sidebar.progress(
    g["satisfaction"] / 100
)

st.sidebar.write("기업 평판")

st.sidebar.progress(
    g["reputation"] / 100
)

st.sidebar.divider()

st.sidebar.subheader("💡 CEO 경영 팁")

st.sidebar.write(
    "1. 현금이 부족하면 파산할 수 있습니다."
)

st.sidebar.write(
    "2. 마케팅은 시간이 지나면 감소할 수 있습니다."
)

st.sidebar.write(
    "3. 경쟁사의 가격도 계속 변합니다."
)

st.sidebar.write(
    "4. 재고가 너무 많으면 보관 비용이 발생합니다."
)

st.sidebar.write(
    "5. 연구개발로 기업 경쟁력을 높이세요."
)

st.sidebar.divider()

if st.sidebar.button("🔄 게임 초기화"):

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()
