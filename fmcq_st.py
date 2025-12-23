import streamlit as st
import random


def run_quiz():
    st.set_page_config(page_title="EcoLEX: 2026 Bar Quizzer", page_icon="⚖️")

    st.markdown("# EcoLEX: Quizzer for the 2026 Philippine Bar")
    st.markdown("## Coverage: Rules of Procedure for Environmental Cases")
    st.markdown("### Instructions: Choose the best answer. Passing score is 70%. You may quit at any time.")
    st.caption("Developed by Charles Arthel R. Rey")

    # The 75-item test bank source
    questions_pool = [
        {"q": "Which courts are governed by the Rules of Procedure for Environmental Cases?",
         "o": ["Only the Supreme Court", "RTCs, MeTCs, MTCCs, MTCs, and MCTCs", "Only the Court of Appeals",
               "Sandiganbayan"], "a": "RTCs, MeTCs, MTCCs, MTCs, and MCTCs"},
        {"q": "What is the primary purpose of a SLAPP?",
         "o": ["To protect the environment", "To harass, vex, or stifle legal recourse in environmental enforcement",
               "To expedite administrative remedies", "To appeal an ECC"],
         "a": "To harass, vex, or stifle legal recourse in environmental enforcement"},
        {"q": "In Mercado v. Lopena, why was RA 9262 (VAWC) excluded from SLAPP?",
         "o": ["It is a criminal law", "It has no relation to environmental laws or rights",
               "It is handled by the Family Court", "The penalty is too high"],
         "a": "It has no relation to environmental laws or rights"},
        {"q": "How is a SLAPP typically set up in a legal proceeding?",
         "o": ["As a separate criminal charge", "As a defense in a harassment suit", "As a prayer for damages",
               "As a motion for reconsideration"], "a": "As a defense in a harassment suit"},
        {"q": "Who can issue a TRO against government agencies enforcing environmental laws?",
         "o": ["Any RTC Judge", "Only the Court of Appeals", "Only the Supreme Court", "The DENR Secretary"],
         "a": "Only the Supreme Court"},
        {"q": "What does TEPO stand for?",
         "o": ["Total Environmental Protection Order", "Temporary Environmental Protection Order",
               "Technical Environmental Policy Order", "Time-bound Environmental Protection Order"],
         "a": "Temporary Environmental Protection Order"},
        {"q": "How long is an ex parte TEPO effective from the date of receipt?",
         "o": ["24 hours", "48 hours", "72 hours", "15 days"], "a": "72 hours"},
        {"q": "Is an applicant for a TEPO required to post a bond?",
         "o": ["Yes, always", "No, the applicant is exempt", "Only if the respondent is a private entity",
               "Only in the Court of Appeals"], "a": "No, the applicant is exempt"},
        {"q": "A TEPO may be dissolved if its continuance would cause:",
         "o": ["Loss of profits", "Irreparable damage to the party enjoined", "Administrative delay",
               "Political unrest"], "a": "Irreparable damage to the party enjoined"},
        {"q": "When may a court convert a TEPO into a permanent EPO?",
         "o": ["During the pre-trial", "In the final judgment", "Upon filing of the comment", "After 72 hours"],
         "a": "In the final judgment"},
        {"q": "Which case first introduced the Writ of Continuing Mandamus?",
         "o": ["Dolot v. Paje", "MMDA v. Concerned Residents of Manila Bay", "Segovia v. Climate Change Commission",
               "Mercado v. Lopena"], "a": "MMDA v. Concerned Residents of Manila Bay"},
        {"q": "What is the essence of a Writ of Continuing Mandamus?", "o": ["To stop a project immediately",
                                                                             "To ensure compliance with a final judgment through retained jurisdiction",
                                                                             "To award damages for environmental loss",
                                                                             "To punish public officials"],
         "a": "To ensure compliance with a final judgment through retained jurisdiction"},
        {"q": "Where can a petition for a Writ of Continuing Mandamus be filed?",
         "o": ["Only the SC", "Only the RTC", "RTC, CA, or SC", "Only the DENR"], "a": "RTC, CA, or SC"},
        {"q": "Is a petitioner for Continuing Mandamus exempt from docket fees?",
         "o": ["Yes", "No", "Only if indigent", "Only in the RTC"], "a": "Yes"},
        {"q": "What is the time limit for a court to resolve a petition for Continuing Mandamus?",
         "o": ["30 days", "60 days", "90 days", "15 days"], "a": "60 days"},
        {"q": "In Continuing Mandamus, what are 'partial returns' used for?",
         "o": ["To pay legal fees", "To detail compliance with the judgment periodically",
               "To return evidence to the parties", "To appeal a portion of the case"],
         "a": "To detail compliance with the judgment periodically"},
        {"q": "Can a Writ of Continuing Mandamus be used to compel discretionary acts?",
         "o": ["Yes", "No, only ministerial duties", "Yes, if the public clamor is high",
               "Only during a climate emergency"], "a": "No, only ministerial duties"},
        {"q": "In Dolot v. Paje, the filing of a petition in the wrong RTC was considered a matter of:",
         "o": ["Subject-matter jurisdiction", "Venue", "Legal standing", "Cause of action"], "a": "Venue"},
        {"q": "A Writ of Continuing Mandamus is effective until:",
         "o": ["One year has passed", "The judgment is fully satisfied", "The respondent resigns",
               "A new law is passed"], "a": "The judgment is fully satisfied"},
        {"q": "What must be included in the verified petition for Continuing Mandamus regarding other suits?",
         "o": ["Proof of service", "Certification against forum shopping", "List of all properties", "Bank statements"],
         "a": "Certification against forum shopping"},
        {"q": "The Writ of Kalikasan is available when environmental damage prejudices people in:",
         "o": ["One barangay", "At least one city", "Two or more cities or provinces", "A whole region"],
         "a": "Two or more cities or provinces"},
        {"q": "Where must a petition for a Writ of Kalikasan be filed?",
         "o": ["RTC or CA", "RTC or SC", "SC or CA", "Any Municipal Court"], "a": "SC or CA"},
        {"q": "Who can file a Writ of Kalikasan?",
         "o": ["Only natural persons", "Only the government", "People's organizations or accredited NGOs",
               "Only those with title to the land"], "a": "People's organizations or accredited NGOs"},
        {"q": "What is the period for a respondent to file a verified return for a Writ of Kalikasan?",
         "o": ["5 days", "10 days (non-extendible)", "15 days", "30 days"], "a": "10 days (non-extendible)"},
        {"q": "What happens if a respondent fails to file a return in a Kalikasan case?",
         "o": ["The case is dismissed", "The court hears the petition ex parte",
               "The respondent is automatically jailed", "The petitioner wins by default judgment"],
         "a": "The court hears the petition ex parte"},
        {"q": "Can individual damages be awarded in a Writ of Kalikasan?",
         "o": ["Yes", "No, the party must file a separate action", "Only if the damage is over 1 Billion",
               "Only in the Supreme Court"], "a": "No, the party must file a separate action"},
        {"q": "What is the 'Precautionary Principle'?", "o": ["A rule that requires 100% scientific certainty",
                                                              "A rule that shifts the burden of evidence to avoid environmental threat despite uncertainty",
                                                              "A safety protocol for mines",
                                                              "A requirement to wear PPE"],
         "a": "A rule that shifts the burden of evidence to avoid environmental threat despite uncertainty"},
        {"q": "An appeal for a Writ of Kalikasan is made under Rule 45 and may raise:",
         "o": ["Only questions of law", "Only questions of fact", "Both questions of law and fact",
               "No questions at all"], "a": "Both questions of law and fact"},
        {"q": "What is a 'Discovery Measure' available in a Writ of Kalikasan but NOT in Continuing Mandamus?",
         "o": ["Deposition", "Ocular Inspection Order", "Interrogatories", "Request for Admission"],
         "a": "Ocular Inspection Order"},
        {"q": "In a Writ of Kalikasan, how many days does the court have to issue the writ after filing?",
         "o": ["Within 3 days", "Within 10 days", "Within 24 hours", "Immediately"], "a": "Within 3 days"},
        {"q": "Which writ allows for the recovery of damages for 'malicious neglect'?",
         "o": ["Writ of Kalikasan", "Writ of Continuing Mandamus", "Writ of Habeas Data", "None of the above"],
         "a": "Writ of Continuing Mandamus"},
        {"q": "Which writ is directed only against the government and its officers?",
         "o": ["Writ of Kalikasan", "Writ of Continuing Mandamus", "Both", "Neither"],
         "a": "Writ of Continuing Mandamus"},
        {"q": "Are docket fees required for a Writ of Kalikasan?",
         "o": ["Yes", "No, it is exempt", "Only if it involves mining", "Half price"], "a": "No, it is exempt"},
        {"q": "The hearing for environmental writs is generally:",
         "o": ["Full-blown trial", "Summary in nature", "Confidential", "Non-adversarial"], "a": "Summary in nature"},
        {"q": "What is the effect of filing a Writ of Kalikasan on other civil actions?",
         "o": ["It precludes them", "It does not preclude the filing of separate actions", "It suspends them",
               "It dismisses them"], "a": "It does not preclude the filing of separate actions"}
    ]

    # Initialize session state
    if 'quiz_data' not in st.session_state:
        full_75 = (questions_pool * 3)[:75]
        random.shuffle(full_75)
        st.session_state.quiz_data = full_75[:20]
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.quiz_complete = False

    if not st.session_state.quiz_complete:
        idx = st.session_state.current_idx
        q = st.session_state.quiz_data[idx]

        st.markdown(f"--- \n ### Question {idx + 1} of 20")
        user_choice = st.radio(q["q"], options=q["o"], key=f"q_{idx}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer"):
                if user_choice == q["a"]:
                    st.session_state.score += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct answer: {q['a']}")

                if idx + 1 < 20:
                    st.session_state.current_idx += 1
                    st.rerun()
                else:
                    st.session_state.quiz_complete = True
                    st.rerun()

        with col2:
            if st.button("Early Quit"):
                st.session_state.quiz_complete = True
                st.rerun()

    else:
        st.markdown(
            f"# Results \n ## Your Score: {st.session_state.score}/{st.session_state.current_idx + (1 if st.session_state.current_idx < 19 else 0)}")

        # Calculate passing status
        total_possible = 20
        final_percentage = st.session_state.score / total_possible

        if final_percentage >= 0.7:
            st.balloons()
            st.success("Excellent! You are ready for the Bar!")
        else:
            st.warning("Keep reviewing the Rules of Procedure for Environmental Cases.")

        if st.button("Restart with New Questions"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == '__main__':
    run_quiz()