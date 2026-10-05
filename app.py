import streamlit as st
from groq import Groq
import json
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MindLens",
    page_icon="🧠",
    layout="centered"
)


# ============================================================
# PERSISTENT BRAND STORAGE
# ============================================================

BRAND_FILE = "mindlens_brand.json"


DEFAULT_BRAND = {
    "brand_name": "",
    "brand_description": "",
    "industry": "",
    "target_audience": "",
    "marketing_objectives": ""
}


def load_brand_settings():
    """
    Load the saved brand from persistent storage.
    """

    if os.path.exists(BRAND_FILE):

        try:

            with open(
                BRAND_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, dict):

                    return {
                        "brand_name": data.get(
                            "brand_name",
                            ""
                        ),
                        "brand_description": data.get(
                            "brand_description",
                            ""
                        ),
                        "industry": data.get(
                            "industry",
                            ""
                        ),
                        "target_audience": data.get(
                            "target_audience",
                            ""
                        ),
                        "marketing_objectives": data.get(
                            "marketing_objectives",
                            ""
                        )
                    }

        except Exception:
            pass

    return DEFAULT_BRAND.copy()


def save_brand_settings(brand_data):
    """
    Save the brand permanently.
    """

    with open(
        BRAND_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            brand_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def clear_brand_settings():
    """
    Delete the saved brand.
    """

    if os.path.exists(BRAND_FILE):

        os.remove(BRAND_FILE)


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "brand_settings" not in st.session_state:

    st.session_state.brand_settings = (
        load_brand_settings()
    )


if "brand_saved" not in st.session_state:

    st.session_state.brand_saved = bool(
        st.session_state.brand_settings["brand_name"].strip()
    )


if "messages" not in st.session_state:

    st.session_state.messages = []


if "pending_question" not in st.session_state:

    st.session_state.pending_question = None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧠 Brand Settings")

st.sidebar.caption(
    "Configure your client once. MindLens will remember "
    "the information until you change or delete it."
)


# ============================================================
# SAVED BRAND STATUS
# ============================================================

if st.session_state.brand_saved:

    st.sidebar.success(
        "✓ Brand saved"
    )


# ============================================================
# BRAND INPUTS
# ============================================================

brand_name_input = st.sidebar.text_input(
    "Company / Brand Name",
    value=st.session_state.brand_settings["brand_name"],
    placeholder="e.g. Dove, Nike, Spotify..."
)


brand_description_input = st.sidebar.text_area(
    "Brand Description",
    value=st.session_state.brand_settings["brand_description"],
    placeholder=(
        "Briefly describe the brand, its products/services, "
        "values, positioning, and what makes it unique..."
    )
)


industry_input = st.sidebar.text_input(
    "Industry",
    value=st.session_state.brand_settings["industry"],
    placeholder="e.g. Beauty, Fashion, Technology, Food..."
)


target_audience_input = st.sidebar.text_area(
    "Target Audience",
    value=st.session_state.brand_settings["target_audience"],
    placeholder=(
        "Describe the target audience, demographics, "
        "generations, interests, behaviors, etc."
    )
)


marketing_objectives_input = st.sidebar.text_area(
    "Marketing Objectives",
    value=st.session_state.brand_settings["marketing_objectives"],
    placeholder=(
        "What does the brand want to achieve? "
        "e.g. increase awareness, launch a product, improve engagement..."
    )
)


# ============================================================
# SAVE BRAND SETTINGS
# ============================================================

if st.sidebar.button(
    "💾 Save Brand Settings",
    use_container_width=True
):

    if not brand_name_input.strip():

        st.sidebar.error(
            "Please enter a Company / Brand Name."
        )

    else:

        new_brand_settings = {

            "brand_name": brand_name_input.strip(),

            "brand_description": (
                brand_description_input.strip()
            ),

            "industry": (
                industry_input.strip()
            ),

            "target_audience": (
                target_audience_input.strip()
            ),

            "marketing_objectives": (
                marketing_objectives_input.strip()
            )
        }


        # Save permanently
        save_brand_settings(
            new_brand_settings
        )


        # Update session state
        st.session_state.brand_settings = (
            new_brand_settings
        )

        st.session_state.brand_saved = True


        st.sidebar.success(
            "✓ Brand settings saved permanently."
        )


        # Rebuild the app using the saved profile
        st.rerun()


# ============================================================
# CLEAR / LOGOUT
# ============================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🗑️ Clear Saved Brand",
    use_container_width=True
):

    clear_brand_settings()

    st.session_state.brand_settings = (
        DEFAULT_BRAND.copy()
    )

    st.session_state.brand_saved = False

    st.session_state.messages = []

    st.session_state.pending_question = None

    st.sidebar.success(
        "Saved brand removed."
    )

    st.rerun()


# ============================================================
# LOAD CURRENT BRAND
# ============================================================

saved_brand = st.session_state.brand_settings


brand_name = saved_brand["brand_name"]

brand_description = (
    saved_brand["brand_description"]
)

industry = saved_brand["industry"]

target_audience = (
    saved_brand["target_audience"]
)

marketing_objectives = (
    saved_brand["marketing_objectives"]
)


current_brand = (
    brand_name
    if brand_name.strip()
    else "[NO BRAND NAME PROVIDED]"
)


current_description = (
    brand_description
    if brand_description.strip()
    else "[NO BRAND DESCRIPTION PROVIDED]"
)


current_industry = (
    industry
    if industry.strip()
    else "[NO INDUSTRY PROVIDED]"
)


current_audience = (
    target_audience
    if target_audience.strip()
    else "[NO TARGET AUDIENCE PROVIDED]"
)


current_objectives = (
    marketing_objectives
    if marketing_objectives.strip()
    else "[NO MARKETING OBJECTIVES PROVIDED]"
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = f"""
You are MindLens, an AI Marketing Strategist, Competitive Intelligence
Analyst, and Creative Director.

You are an AI agent designed to support marketing teams, agencies, and
businesses in developing audience-centered marketing strategies.

CURRENT CLIENT / BRAND:

Company / Brand Name:
{current_brand}

Brand Description:
{current_description}

Industry:
{current_industry}

Target Audience:
{current_audience}

Marketing Objectives:
{current_objectives}

The company or brand listed above is your current client.

You must adapt your analysis, recommendations, and campaign concepts to this
specific brand.

The client may belong to ANY industry, market, category, or country.

Never assume that the client is a beauty, fashion, technology, food, sports,
or any other specific type of company unless the user provides that
information.

Never invent:

- Products
- Services
- Brand values
- Competitors
- Target audiences
- Statistics
- Campaign results
- Company history
- Market information

If important information is missing, clearly identify what is missing and ask
the user for it.


AI IDENTITY:

You are an AI agent.

You are not a human employee, marketer, consumer, or customer.

When user asks who/what you are or asks for introduction, say:

"Hi, I'm MindLens, an AI Marketing Strategist and Competitive Intelligence
Analyst. I help brands analyze competitors, understand audience motivations,
identify market opportunities, and develop original marketing and campaign
concepts."

If brand name is provided, mention the current client:

"Hi, I'm MindLens, an AI Marketing Strategist and Competitive Intelligence
Analyst. I'm currently supporting {current_brand} by analyzing competitors,
audience motivations, emotional messaging, and market opportunities."

Do not pretend to be a human.


CORE ROLE:

- Analyze competitors' marketing
- Analyze social media campaigns
- Analyze emotional messaging
- Identify emotional and strategic gaps
- Understand audience motivations
- Identify empathy gaps
- Identify market opportunities
- Analyze generational audiences
- Develop psychological and emotional audience profiles
- Create original campaign concepts
- Develop messaging angles
- Suggest creative hooks
- Develop marketing strategies


BRAND CONTEXT:

Understand brand identity, values, history, positioning, products/services,
target audiences, personas, competitive environment, communication style,
marketing objectives, personality, and tone.


COMPETITIVE INTELLIGENCE:

Analyze competitor positioning, messaging, tone, emotional triggers, audience
targeting, creative strategies, social communication, themes, motivations,
differentiation, empathy gaps, and market opportunities.

Never copy.


AUDIENCE ANALYSIS:

Use provided demographic, cultural, behavioral, and market information.

You may analyze Gen Z, Millennials, Gen X, and Boomers, but do not assume all
people within a generation behave the same way.

Identify:

- Emotional needs
- Motivations
- Values
- Concerns
- Aspirations
- Cultural influences
- Consumer behaviors
- Barriers
- Expectations
- Relationship with category/brand

Avoid unsupported assumptions.


MAIN TASK:

Analyze competitor social media campaigns and emotional messaging, identify
gaps in empathy, positioning, audience connection, and transform these
insights into original campaign concepts tailored to {current_brand}.


RESPONSE FORMAT:

When analyzing a competitor:

1. Competitor Overview
2. Messaging & Tone
3. Emotional Strategy
4. Target Audience
5. Audience Motivators
6. Empathy Gaps & Market Opportunities
7. Strategic Opportunity for {current_brand}
8. Campaign Concepts
9. Key Messaging Angles
10. Recommended Next Steps


For campaign concepts:

- Campaign idea
- Target audience
- Emotional insight
- Key message
- Creative hook
- Suggested execution


TONE:

Strategic, Empathetic, Creative.

Intelligent, confident, human-centered, imaginative, strategically grounded,
relevant, and actionable.


ORIGINALITY:

Never copy, reproduce, or closely imitate competitor slogans, campaign
concepts, creative identities, distinctive messaging, or visual concepts.

All concepts for {current_brand} must be original.


ETHICAL MARKETING:

Do not exploit fear, insecurity, discrimination, vulnerability, sensitive
personal characteristics, or highly vulnerable audiences.

Do not make people feel worse about themselves to increase sales.

Use:

- Authenticity
- Empowerment
- Positive connection
- Meaningful value
- Inclusion
- Trust
- Relevance
- Genuine audience needs

Request human review for sensitive data, discriminatory targeting, vulnerable
groups, serious ethical concerns, or significant reputational/legal risk.


KNOWLEDGE BASE:

Use user-provided:

- Brand identity and values
- History and positioning
- Products/services
- Target audience
- Demographic/generational research
- Consumer behavior
- Market research
- Personas
- Competitor profiles
- Competitor campaigns
- Competitor messaging
- Competitor positioning
- Previous campaigns
- Tone of voice
- Social performance
- Feedback/reviews
- Cultural/market trends
- Ethical guidelines
- Approved claims/product information

Do not present assumptions as facts.


STRESS TEST:

If asked to exploit competitor emotional vulnerability to make an audience
more insecure so they buy more:

- Identify the emotional strategy
- Explain the underlying motivation/need
- Explain why increasing insecurity is inappropriate
- Reframe around a positive emotional insight
- Create an original campaign based on empathy, authenticity, empowerment,
  and meaningful value.


GENERAL RULES:

Follow this system prompt.

Do not claim unprovided or unverified information.

Do not assume industry, audience, values, products, services, competitors,
positioning, or campaign results.

When information is missing, ask for relevant information.

Always adapt to the current client brand.
"""


# ============================================================
# GROQ API
# ============================================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

except Exception:

    api_key = None


# ============================================================
# HEADER
# ============================================================

st.title("🧠 MindLens")

st.caption(
    "AI Marketing Strategist & Competitive Intelligence Specialist"
)


# ============================================================
# CURRENT CLIENT
# ============================================================

if brand_name.strip():

    st.success(
        f"**Active client:** {brand_name}"
    )

else:

    st.warning(
        "No brand has been configured yet. "
        "Please complete Brand Settings in the sidebar."
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

st.markdown("---")

st.markdown(
    "**💡 Suggested questions**"
)


suggested_questions = [

    "Analyze my main competitor's marketing strategy.",

    "Identify the emotional needs of my target audience.",

    "Find empathy gaps in my competitor's communication.",

    "Create 3 original campaign concepts for my brand.",

    "Develop a psychological profile of my target audience.",

    "What opportunities can my brand exploit in the current market?"
]


for i in range(
    0,
    len(suggested_questions),
    2
):

    col1, col2 = st.columns(2)


    with col1:

        question = suggested_questions[i]

        if st.button(
            question,
            key=f"suggested_{i}",
            use_container_width=True
        ):

            st.session_state.pending_question = (
                question
            )

            st.rerun()


    if i + 1 < len(suggested_questions):

        with col2:

            question = suggested_questions[i + 1]

            if st.button(
                question,
                key=f"suggested_{i + 1}",
                use_container_width=True
            ):

                st.session_state.pending_question = (
                    question
                )

                st.rerun()


# ============================================================
# INPUT
# ============================================================

if st.session_state.pending_question:

    user_input = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

else:

    user_input = st.chat_input(
        "Ask MindLens about a campaign, competitor, or audience..."
    )


# ============================================================
# PROCESS MESSAGE
# ============================================================

if user_input:

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    if not api_key:

        st.error(
            "The Groq API key has not been configured."
        )

        st.stop()


    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    if not brand_name.strip():

        st.warning(
            "Please configure your brand first."
        )

        st.stop()


    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    try:

        client = Groq(
            api_key=api_key
        )


        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]


        messages.extend(
            st.session_state.messages
        )


        with st.chat_message("assistant"):

            with st.spinner(
                "MindLens is analyzing..."
            ):

                response = client.chat.completions.create(

                    model="openai/gpt-oss-20b",

                    messages=messages,

                    temperature=0.7,

                    max_tokens=2048
                )


                assistant_response = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                st.markdown(
                    assistant_response
                )


        # ----------------------------------------------------
        # SAVE RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )


        # ----------------------------------------------------
        # REBUILD PAGE
        # ----------------------------------------------------

        st.rerun()


    except Exception as e:

        st.error(
            f"An error occurred: {e}"
        )
