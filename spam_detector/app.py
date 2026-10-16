"""Spam Message Detector - a minimal Streamlit app.

Run with:  streamlit run app.py
"""

import streamlit as st

from detector import check_message
from storage import block_number, load_numbers, report_number, validate_number

st.set_page_config(page_title="Spam Message Detector", page_icon="🛡️")

st.title("🛡️ Spam Message Detector")
st.caption(
    "A simple warning aid. Results can be incorrect. Never share passwords, "
    "codes, or payment details with a suspicious sender."
)

# Show one-time success/error messages saved before a page refresh.
if "flash" in st.session_state:
    kind, text = st.session_state.pop("flash")
    (st.success if kind == "success" else st.error)(text)

tab_check, tab_log = st.tabs(["Check a message", "Spam call log"])

# ---------------------------------------------------------------------------
# Tab 1: message checker
# ---------------------------------------------------------------------------
with tab_check:
    message = st.text_area("Paste or type a message", height=160)

    if st.button("Check message", type="primary"):
        if not message.strip():
            st.error("Please enter a message to check.")
        else:
            result = check_message(message)
            if result["label"] == "Spam":
                st.error(f"🚨 Result: **{result['label']}** (suspicion score {result['score']})")
            else:
                st.success(f"✅ Result: **{result['label']}** (suspicion score {result['score']})")

            if result["reasons"]:
                st.warning("**Why this looks suspicious:**")
                for reason in result["reasons"]:
                    st.write(f"- {reason}")

            st.info(
                "This tool only reads the text. It never opens or follows links. "
                "It can be wrong, so stay cautious either way."
            )

# ---------------------------------------------------------------------------
# Tab 2: spam call log
# ---------------------------------------------------------------------------
with tab_log:
    st.subheader("Report a number")
    number_input = st.text_input("Phone number", placeholder="+1 555 123 4567")

    if st.button("Mark as spam"):
        clean, error = validate_number(number_input)
        if error:
            st.error(error)
        elif report_number(clean):
            st.session_state["flash"] = ("success", f"{clean} was reported as spam.")
            st.rerun()
        else:
            st.error(f"{clean} is already in your list.")

    st.divider()
    st.subheader("Reported numbers")
    st.caption(
        "ℹ️ 'Block' only records the number as blocked inside this app (in a local file). "
        "It does not block calls through your phone carrier or operating system."
    )

    numbers = load_numbers()
    if not numbers:
        st.write("No numbers reported yet.")
    else:
        for number, info in numbers.items():
            col_num, col_date, col_action = st.columns([3, 3, 2])
            col_num.write(f"**{number}**")
            col_date.write(info["reported_at"])
            if info["blocked"]:
                col_action.write("🚫 Blocked")
            elif col_action.button("Block", key=f"block_{number}"):
                block_number(number)
                st.session_state["flash"] = ("success", f"{number} was marked as blocked in this app.")
                st.rerun()
