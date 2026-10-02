import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MindLens",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are MindLens, an AI Marketing Strategist & Competitive Intelligence Specialist.

==================================================
CORE RULES
==================================================

Do not claim to have information that has not been provided or verified.

Do not assume the company's industry, audience, values, products, services,
competitors, or positioning.

When information is missing, clearly state what is missing and ask the user
for the relevant information.

Always adapt your recommendations to the current client brand.

==================================================
CUSTOMER PERSONA
==================================================

Help users understand their target customers by analyzing:

- Demographic context
- Generational context
- Motivations
- Goals
- Expectations
- Frustrations
- Purchasing motivations
- Barriers
- Emotional needs
- Content preferences
- Communication preferences

Do not treat an entire generation or demographic group as psychologically
identical.

Present psychological characteristics as marketing hypotheses rather than
universal facts.

==================================================
COMPETITIVE INTELLIGENCE
==================================================

When the user provides information about competitors, analyze:

- Their messaging
- Emotional appeals
- Communication style
- Customer promises
- Possible gaps
- Possible opportunities for differentiation

Do not claim to have analyzed a competitor unless the user provides the
relevant information or verified data.

Never invent competitor campaigns, statistics, customer reactions, or
company strategies.

==================================================
CAMPAIGN IDEAS
==================================================

Generate original campaign concepts based on the information provided by
the user.

Campaign ideas should include, when relevant:

- Campaign name
- Big idea
- Target audience
- Customer insight
- Emotional direction
- Key message
- Social media execution
- Call to action

Avoid generic marketing suggestions.

==================================================
EMOTIONAL MARKETING
==================================================

Help identify:

- Customer emotions
- Motivations
- Aspirations
- Concerns
- Emotional expectations
- Communication opportunities

Do not encourage deceptive or exploitative psychological manipulation.

==================================================
RESPONSE STYLE
==================================================

Be clear, practical, strategic and concise.

Use headings and bullet points when useful.

If essential brand information is missing, ask for it instead of guessing.

Always distinguish between:
- Information provided by the user
- Verified information
- Marketing hypotheses
- Creative recommendations

==================================================
END SYSTEM PROMPT
==================================================
"""

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8F7FC;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8E3EF;
}

/* Main title */

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #211A2D;
    margin-bottom: 5px;
}

.subtitle {
    color: #756C7D;
    font-size: 17px;
    margin-bottom: 30px;
}

/* Hero */

.hero {
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #F0EBFF
    );
    border: 1px solid #E3DCF2;
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 28px;
    font-weight: 750;
    color: #211A2D;
}

.hero-text {
    color: #706779;
    line-height: 1.6;
    margin-top: 8px;
}

/* Feature cards */

.card {
    background: white;
    border: 1px solid #E8E3EF;
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
}

.card-icon {
    font-size: 28px;
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    margin-top: 8px;
    color: #292131;
}

.card-text {
    color: #777080;
    font-size: 13px;
    line-height: 1.5;
}

/* Buttons */

.stButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 12px;
    border: 1px solid #DDD6E8;
    background: white;
    font-weight: 650;
}

.stButton > button:hover {
    border-color: #7C3AED;
    color: #7C3AED;
    background: #FAF8FF;
}

/* Primary button */

div.stButton > button[kind="primary"] {
    background: #7C3AED;
    color: white;
    border: none;
}

div.stButton > button[kind="primary"]:hover {
    background: #6D28D9;
    color: white;
}

/* Section title */

.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #241D2E;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# API KEY
# =========================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = None

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_action" not in st.session_state:
    st.session_state.selected_action = None

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 Brand Settings")

    st.caption(
        "Enter the information about the brand you are working with."
    )

    brand_name = st.text_input(
        "Company / Brand Name",
        placeholder="e.g. Nike"
    )

    brand_description = st.text_area(
        "Brand Description",
        placeholder="Describe the company, its products/services and positioning.",
        height=100
    )

    industry = st.text_input(
        "Industry",
        placeholder="e.g. Sportswear"
    )

    target_audience = st.text_area(
        "Target Audience",
        placeholder="e.g. Gen Z consumers interested in sustainable fashion.",
        height=90
    )

    marketing_goal = st.text_input(
        "Main Marketing Goal",
        placeholder="e.g. Increase brand awareness"
    )

    st.divider()

    st.markdown("### ⚙️ Settings")

    creativity = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.7,
        0.1
    )

# =========================================================
# BRAND CONTEXT
# =========================================================

def build_brand_context():

    return f"""
CURRENT CLIENT BRAND INFORMATION

Company / Brand:
{brand_name if brand_name.strip() else "NOT PROVIDED"}

Brand Description:
{brand_description if brand_description.strip() else "NOT PROVIDED"}

Industry:
{industry if industry.strip() else "NOT PROVIDED"}

Target Audience:
{target_audience if target_audience.strip() else "NOT PROVIDED"}

Marketing Goal:
{marketing_goal if marketing_goal.strip() else "NOT PROVIDED"}
"""

# =========================================================
# CHECK MISSING BRAND INFORMATION
# =========================================================

def missing_brand_information():

    missing = []

    if not brand_name.strip():
        missing.append("Company / Brand Name")

    if not brand_description.strip():
        missing.append("Brand Description")

    if not industry.strip():
        missing.append("Industry")

    if not target_audience.strip():
        missing.append("Target Audience")

    return missing

# =========================================================
# AI FUNCTION
# =========================================================

def ask_mindlens(user_request):

    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": build_brand_context()
        }
    ]

    messages.extend(st.session_state.messages)

    messages.append(
        {
            "role": "user",
            "content": user_request
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=creativity,
        max_tokens=2048
    )

    return response.choices[0].message.content

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🧠 MindLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Marketing Strategist & Competitive Intelligence Specialist'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
See your market through a different lens.
</div>

<div class="hero-text">
MindLens combines customer persona design, emotional marketing analysis,
competitive intelligence and creative campaign development to help
marketers turn customer insights into strategic ideas.
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURES
# =========================================================

st.markdown(
    '<div class="section-title">What can MindLens do?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="card">

        <div class="card-icon">🔍</div>

        <div class="card-title">
            Competitor Analysis
        </div>

        <div class="card-text">
            Analyze competitor information and identify possible
            messaging and emotional gaps.
        </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">

        <div class="card-icon">👤</div>

        <div class="card-title">
            Customer Persona
        </div>

        <div class="card-text">
            Transform audience information into actionable customer
            profiles and messaging insights.
        </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">

        <div class="card-icon">💡</div>

        <div class="card-title">
            Campaign Ideas
        </div>

        <div class="card-text">
            Turn customer insights into creative campaign concepts
            and communication ideas.
        </div>

    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="card">

        <div class="card-icon">🧠</div>

        <div class="card-title">
            Emotional Insights
        </div>

        <div class="card-text">
            Explore customer motivations, expectations and emotional
            communication opportunities.
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# ACTION BUTTONS
# =========================================================

st.markdown(
    '<div class="section-title">Choose your analysis</div>',
    unsafe_allow_html=True
)

b1, b2, b3, b4 = st.columns(4)

with b1:

    if st.button("🔍 Analyze Competitors"):

        st.session_state.selected_action = """
Analyze the competitor information provided by the user.

Identify:
- competitor messaging
- emotional appeals
- communication patterns
- possible gaps
- opportunities for differentiation

Do not invent competitor information.
If competitor information has not been provided, clearly explain what is
missing and ask the user to provide competitor information.
"""

with b2:

    if st.button("👤 Build Customer Persona"):

        st.session_state.selected_action = """
Create a detailed customer persona using only the brand and audience
information provided.

Include:
- customer profile
- motivations
- goals
- expectations
- frustrations
- emotional needs
- purchasing motivations
- barriers
- content preferences
- messaging opportunities

Clearly distinguish hypotheses from verified information.
"""

with b3:

    if st.button("💡 Generate Campaign Ideas"):

        st.session_state.selected_action = """
Generate five original campaign concepts based on the information
provided about the client brand.

For each concept include:

1. Campaign name
2. Big idea
3. Customer insight
4. Emotional direction
5. Key message
6. Social media execution
7. Call to action

Do not invent facts about the brand.
"""

with b4:

    if st.button("🧠 Emotional Insights"):

        st.session_state.selected_action = """
Analyze the emotional marketing opportunities for this brand.

Discuss:
- customer motivations
- emotional expectations
- aspirations
- concerns
- possible emotional messaging
- communication opportunities
- potential risks of manipulative messaging

Use only the information provided.
"""

# =========================================================
# ANALYZE BUTTON
# =========================================================

st.markdown("")

if st.button(
    "🚀 ANALYZE MY MARKET",
    type="primary"
):

    if not api_key:

        st.error(
            "The Groq API key has not been configured. "
            "Please add GROQ_API_KEY to Streamlit Secrets."
        )

    else:

        missing = missing_brand_information()

        if missing:

            st.warning(
                "Before running a market analysis, please provide: "
                + ", ".join(missing)
                + "."
            )

        else:

            if st.session_state.selected_action:

                prompt = st.session_state.selected_action

            else:

                prompt = """
Create a strategic overview of this client brand.

Analyze:

1. Customer profile
2. Customer motivations
3. Emotional expectations
4. Marketing opportunities
5. Competitive considerations
6. Three campaign opportunities
7. Suggested messaging angles

Only use information provided by the user.
Do not invent missing facts.
"""

            with st.spinner(
                "MindLens is analyzing..."
            ):

                try:

                    result = ask_mindlens(prompt)

                    st.markdown("---")

                    st.markdown(
                        '<div class="section-title">'
                        '🧠 MindLens Analysis'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(result)

                except Exception as e:

                    st.error(
                        f"An error occurred: {e}"
                    )

# =========================================================
# CHAT
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">💬 Ask MindLens</div>',
    unsafe_allow_html=True
)

st.caption(
    "Ask about your campaign, competitors, customers or marketing strategy."
)

# =========================================================
# SHOW CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask MindLens about a campaign, competitor, or audience..."
)

if user_input:

    # -----------------------------------------------------
    # API CHECK
    # -----------------------------------------------------

    if not api_key:

        st.error(
            "The Groq API key has not been configured."
        )

        st.stop()

    # -----------------------------------------------------
    # BRAND CHECK
    # -----------------------------------------------------

    if not brand_name.strip():

        st.warning(
            "Please enter your Company / Brand Name "
            "in the Brand Settings section."
        )

        st.stop()

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)

    # -----------------------------------------------------
    # AI RESPONSE
    # -----------------------------------------------------

    try:

        with st.chat_message("assistant"):

            with st.spinner(
                "MindLens is analyzing..."
            ):

                assistant_response = ask_mindlens(
                    user_input
                )

            st.markdown(
                assistant_response
            )

        # -------------------------------------------------
        # SAVE RESPONSE
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

    except Exception as e:

        st.error(
            f"An error occurred: {e}"
        )

# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">💭 Try asking</div>',
    unsafe_allow_html=True
)

examples = [
    "Create a customer persona for my target audience.",
    "What emotional needs might my customers have?",
    "Help me identify gaps in my competitor's campaign.",
    "Generate five campaign concepts for my brand.",
    "What messaging angles could resonate with my audience?",
    "Help me understand my target customer's motivations."
]

for example in examples:

    st.markdown(
        f"""
        <div style="
            background:white;
            border:1px solid #E8E3EF;
            padding:12px 16px;
            border-radius:10px;
            margin-bottom:8px;
            color:#625A6B;
            font-size:14px;
        ">
        💬 {example}
        </div>
        """,
        unsafe_allow_html=True
    )
