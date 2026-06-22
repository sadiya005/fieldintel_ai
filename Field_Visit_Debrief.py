import streamlit as st
import os

from database import init_db, save_visit
from ai import generate_debrief
from speech import transcribe_audio

# --------------------------
# INITIAL SETUP
# --------------------------

init_db()

os.makedirs("uploads/audio", exist_ok=True)

st.set_page_config(
    page_title="FieldIntel AI",
    page_icon="📋",
    layout="wide"
)

# --------------------------
# HEADER
# --------------------------

st.title("FieldIntel AI")
st.caption("AI-Powered Field Visit Intelligence System")

st.markdown("---")

# --------------------------
# FORM
# --------------------------

st.subheader("Field Visit Debrief Form")

col1, col2 = st.columns(2)

with col1:
    location = st.text_input("Location *")

with col2:
    visit_date = st.date_input("Visit Date *")

program_area = st.selectbox(
    "Program Area * ",
    [
        "Agriculture",
        "Livelihood",
        "Women Empowerment",
        "Skilling",
        "Health"
    ]
)

stakeholders = st.text_input(
    "Stakeholders Met * "
)

notes = st.text_area(
    "Observations / Notes (or upload voice memo) ",
    height=250
)


audio = st.file_uploader(
    "Upload Voice Memo",
    type=["mp3", "wav", "m4a"]
)

# --------------------------
# GENERATE DEBRIEF
# --------------------------

if st.button("Generate AI Debrief", use_container_width=True):

    if not location.strip():
        st.error("Please enter location.")
        st.stop()

    if not stakeholders.strip():
        st.error("Please enter stakeholders met.")
        st.stop()

    if not notes.strip() and not audio:
        st.error("Please enter observations or upload a voice memo.")
        st.stop()


    # --------------------------
    # SAVE AUDIO
    # --------------------------

    audio_path = ""

    if audio:

        audio_path = f"uploads/audio/{audio.name}"

        with open(audio_path, "wb") as f:
            f.write(audio.getbuffer())


    # --------------------------
    # AI GENERATION
    # --------------------------

    with st.spinner("Generating AI Debrief..."):

        transcript = ""

        if audio_path:

            transcript = transcribe_audio(audio_path)

        combined_notes = ""

        if notes.strip():

            combined_notes += "WRITTEN NOTES:\n"
            combined_notes += notes

        if transcript:

            combined_notes += "\n\nVOICE MEMO TRANSCRIPT:\n"
            combined_notes += transcript

    # --------------------------
    # SAVE TO DATABASE
    # --------------------------

    tags = ai_result.get("tags", [])

    if isinstance(tags, list):
        tags = ",".join(tags)

    save_visit(
        (
            location,
            str(visit_date),
            program_area,
            stakeholders,
            combined_notes,
            "", #photo
            audio_path,
            ai_result.get("key_findings", ""),
            ai_result.get("blockers", ""),
            ai_result.get("sentiment", ""),
            ai_result.get("followups", ""),
            tags
        )
    )

    # --------------------------
    # DISPLAY RESULTS
    # --------------------------

    st.success("Visit Saved Successfully")

    if transcript:

        st.subheader("Voice Memo Transcript")

        st.info(transcript)

    st.markdown("---")

    st.subheader("AI Debrief Summary")

    c1, c2 = st.columns(2)

    with c1:
        st.info("Key Findings")
        st.write(ai_result.get("key_findings", ""))

    with c2:
        st.warning("Blockers Observed")
        st.write(ai_result.get("blockers", ""))

    c3, c4 = st.columns(2)

    with c3:
        st.success("Community Sentiment")
        st.write(ai_result.get("sentiment", ""))

    with c4:
        st.info("Suggested Follow-Ups")
        st.write(ai_result.get("followups", ""))

    st.subheader("Issue Tags")

    tags = ai_result.get("tags", [])

    if isinstance(tags, str):
        tag_list = [tag.strip() for tag in tags.split(",")]
    else:
        tag_list = tags

    for tag in tag_list:

        if str(tag).strip():
            st.badge(tag)
