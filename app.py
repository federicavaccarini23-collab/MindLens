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
