import streamlit as st
import random
import requests

# Configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3-vl:235b-cloud"

# Database of Questions
QUESTIONS = [
    {
        "id": 1,
        "question": "A law was passed declaring Mt. Karbungko as a protected area since it was a major watershed. The protected area covered a portion located in Municipality A of the Province I and a portion located in the City of Z of Province II. Maingat is the leader of Samahan ng Tagapag-ingat ng Karbungko (STK), a people’s organization. He learned that a portion of the mountain located in the City of Z of Province II was extremely damaged when it was bulldozed and leveled to the ground, and several trees and plants were cut down and burned by workers of World Pleasure Resorts, Inc. (WPRI) for the construction of a hotel and golf course. Upon inquiry with the project site engineer if they had a permit for the project, Maingat was shown a copy of the Environmental Compliance Certificate (ECC) issued by the DENR-EMB, Regional Director (RD-DENR-EMB). Immediately, Maingat and STK filed a petition for the issuance of a writ of continuing mandamus against RD-DENR-EMB and WPRI with the RTC of Province I, a designated environmental court, as the RD-DENR-EMB negligently issued the ECC to WPRI. On scrutiny of the petition, the court determined that the area where the alleged actionable neglect or omission subject of the petition took place in the City of Z of Province II, and therefore cognizable by the RTC of Province II. Thus, the court dismissed outright the petition for lack of jurisdiction. Assuming that the court did not dismiss the petition, the RD-DENR-EMB in his Comment moved to dismiss the petition on the ground that petitioners failed to appeal the issuance of the ECC and to exhaust administrative remedies provided in the DENR Rules and Regulations. Should the court dismiss the petition? (2015 BAR)",
        "suggested_answer": "YES. The court should dismiss the petition because the proper procedure to question defect in an ECC is to follow the DENR administrative appeal process in accordance with the doctrine of exhaustion of administrative remedies. (Dolot v. Hon. Paje, G.R. No. 199199, 27 Aug. 2013; Paje v. Casiño, G.R. No. 207257, 03 Feb. 2015)"
    },
    {
        "id": 2,
        "question": "What do you understand about the “precautionary principle” under the Rules of Procedure for Environmental Cases? (2018, 2012 BAR)",
        "suggested_answer": "Precautionary principle states that when human activities may lead to threats of serious and irreversible damage to the environment that is scientifically plausible but uncertain, actions shall be taken to avoid or diminish that threat. In its essence, the precautionary principle calls for the exercise of caution in the face of risk and uncertainty (Sec. 4, Rule 1, Rules of Procedure for Environmental Cases) (Divina, 2024)."
    },
    {
        "id": 3,
        "question": "Distinguish between a writ of kalikasan and writ of continuing mandamus (2019 BAR)",
        "suggested_answer": "1. As to the subject matter, a writ of kalikasan should pertain to an unlawful act or omission which involves environmental damage that prejudices the life, health, or property of the inhabitants in two or more cities or provinces. (Sec. 1, Rule 7, Rules of Procedure for Environmental Cases) A writ of continuing mandamus, on the other hand, pertains to an unlawful neglect of the performance of an act which the law specifically enjoins as a duty in connection with the enforcement or violation of an environmental law, rule, or regulation or a right therein, or an unlawful exclusion from the use or enjoyment of such right. (Sec. 1, Rule 8, Rules of Procedure for Environmental Cases)\n2. As to the respondents, the respondents in a writ of kalikasan petition may either be a public or private individual or entity. (Sec. 1, Rule 7, Rules of Procedure for Environmental Cases) The respondents in a writ of mandamus may only be public officials, or a government agency or instrumentality. (Sec. 1, Rule 8, Rules of Procedure for Environmental Cases)\n3. As to the venue, a writ of kalikasan petition may only be filed before the Supreme Court or Court of Appeals. (Sec. 3, Rule 7, Rules of Procedure for Environmental Cases) On the other hand, a writ of continuing mandamus petition may be filed before the Supreme Court, the Court of Appeals, or the Regional Trial Court. (Sec. 2, Rule 8, Rules of Procedure for Environmental Cases)\n4. As to damages, damages may not be recovered in a writ of kalikasan petition. (Sec. 15(e), Rule 7, Rules of Procedure for Environmental Cases) On the other hand, damages may be recovered in a writ of continuing mandamus. (Sec. 1, Rule 8, Rules of Procedure for Environmental Cases)\n5. As to discovery measures, ocular inspection and production of documents are available discovery measures in a writ of kalikasan petition. (Sec. 12, Rule 7, Rules of Procedure for Environmental Cases) No discovery measures are enumerated for a writ of continuing mandamus petition. (Rule 8, Rules of Procedure for Environmental Cases) (Divina, 2024)"
    },
    {
        "id": 4,
        "question": "The officers of “Ang Kapaligiran ay Alagaan, Inc.” engaged your services to file an action against ABC Mining Corporation which is engaged in mining operations in Sta. Cruz, Marinduque. ABC used highly toxic chemicals in extracting gold. ABC’s toxic mine tailings were accidentally released from its storage dams and were discharged into the rivers of said town. The mine tailings found their way to Calancan Bay, allegedly to the waters of nearby Romblon and Quezon. The damage to the crops and loss of earnings were estimated at ₱1 Billion. Damage to the environment is estimated at ₱1 Billion. As a lawyer for the organization, you are requested to explain the advantages derived from a petition for writ of kalikasan before the Supreme Court over a complaint for damages before the RTC of Marinduque or vice versa. What action will you recommend? Explain. (2018)",
        "suggested_answer": "I will recommend the filing of a petition for the writ of kalikasan. The following are the advantages of a writ of kalikasan petition: 1. The petitioner in a writ of kalikasan petition is exempt from the payment of docket fees. (Sec. 4, Rule 7, Rules of Procedure for Environmental Cases) 2. The writ is immediately issued within three (3) days from the filing of the petition, if the petition is sufficient in form and substance. (Sec. 5, Rule 7, Rules of Procedure for Environmental Cases) 3. The proceedings therein are abbreviated, as the respondents are given a non-extendible period of ten (10) days after service of the writ to them. (Sec. 8, Rule 7, Rules of Procedure for Environmental Cases) 4. Judgment in environmental cases shall be immediately executory pending appeal, unless restrained by an appellate court. (Sec. 2, Rule 5, Rules of Procedure for Environmental Cases) 5. Even if damages cannot be awarded in a writ of kalikasan case, the Rules of Procedure for Environmental Cases do not preclude the filing of a separate civil action for damages. (Sec. 17, Rule 7, Rules of Procedure for Environmental Cases) (Divina, 2024)"
    },
    {
        "id": 5,
        "question": "Hannibal, Donna, Florence and Joel, concerned residents of Laguna de Bay, filed a complaint of mandamus against the Laguna Lake Development Authority, the Department of Environment and Natural Resources, the Department of Public Works and Highways, Department of Interior and Local Government, Department of Agriculture, Department of Budget and Philippine National Police before the RTC of Laguna alleging that the continued neglect of defendants in performing their duties has resulted in serious deterioration of the water quality of the lake and the degradation of the marine life in the lake. The plaintiffs prayed that said government agencies be ordered to clean up Laguna de Bay and restore its water quality to Class C waters as prescribed by Presidential Decree 1151, otherwise known as the Philippine Environment Code. Defendants raise the defense that the clean up of the lake is not a ministerial function and they cannot be compelled by mandamus to perform the same. The RTC of Laguna rendered a decision declaring that it is the duty of the agency to clean up Laguna de Bay and issued a permanent writ of mandamus ordering said agencies to perform their duties prescribed by law relating to the cleanup of Laguna de Bay. (2016 BAR) (a) Is the RTC correct in issuing the writ of mandamus? Explain.",
        "suggested_answer": "YES, the RTC is correct in issuing the writ of mandamus. Generally, the writ of mandamus lies to require the execution of a ministerial duty. While the implementation of the government agencies mandated tasks may entail a decision-making process, the enforcement of the law or the very act of doing what the law exacts to be done is ministerial in nature and may be compelled by mandamus. Here, the duty to clean up Laguna Lake and restore its water quality to Class C is required not only by Presidential Decree No. 1152, otherwise known as the Philippine Environment Code, but also in its charter. It is, thus, ministerial in nature and can be compelled by mandamus. Accordingly, the RTC may issue a writ of continuing mandamus directing any agency or instrumentality of the government or officer thereof to perform an act or series of acts decreed by final judgment which shall remain effective until the judgement is fully satisfied. (Metropolitan Manila Development Authority v. Concerned Residents of Manila Bay, G.R. Nos. 171947-48, 18 Dec. 2008)."
    },
    {
        "id": 6,
        "question": "What is the writ of continuing mandamus?",
        "suggested_answer": "A writ of continuing mandamus is a writ issued when any agency or instrumentality of the government, or officer thereof, unlawfully neglects the performance of an act which the law specifically enjoins as a duty resulting from an office, trust, or station in connection with the enforcement or violation of an environmental law, rule, or regulation or a right therein, or unlawfully excludes another from the use or enjoyment of such right, and there is no other plain, speedy, and adequate remedy in the ordinary course of law. The person aggrieved thereby may file a verified petition in the proper court, alleging the facts with certainty, attaching thereto supporting evidence, specifying that the petition concerns an environmental law, rule, or regulation, and praying that judgment be rendered commanding the respondent to do an act or series of acts until the judgment is fully satisfied, and to pay damages sustained by the petitioner by reason of malicious neglect to perform the duties of the respondent under the law, rules, or regulations. The petition shall also contain a sworn certification of non-forum shopping. (Sec. 1, Part III, Rule 8, A.M. No. 09-6-8-SC)"
    }
]


def grade_essay(user_essay, suggested_answer):
    prompt = f"""
    You are a Bar Exam Grader. Compare the User's Answer against the Suggested Answer.

    Suggested Answer: {suggested_answer}
    User's Answer: {user_essay}

    Provide your response using Markdown:
    - Use ## for headlines.
    - Use **bold** for key legal terms and the final verdict.
    - Provide a score from 0 to 100%.
    - Brief feedback.
    - A final verdict (Passed/Failed).
    """
    try:
        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=data)
        return response.json()["message"]["content"]
    except Exception as e:
        return f"# ⚠️ The Free Ollama Language Model is only available for local deployment. The local installation is capable of giving a score."


def main():
    st.set_page_config(page_title="EcoLEX: Bar Exam Practice", page_icon="⚖️")

    st.markdown("# ⚖️ **EcoLEX: Bar Exam Practice**")
    st.markdown("### Philippine Environmental Law Reviewer")
    st.divider()

    # Session state initialization
    if 'current_question' not in st.session_state:
        st.session_state.current_question = random.choice(QUESTIONS)
        st.session_state.grading_result = None
        st.session_state.user_essay = ""

    q_data = st.session_state.current_question

    st.markdown(f"## **Question:**")
    st.markdown(q_data['question'])

    user_essay = st.text_area("Your Essay Answer:", placeholder="Type your legal basis here...", height=300,
                              key="essay_input")

    col1, col2 = st.columns([1, 4])

    if col1.button("Submit Answer"):
        if user_essay.strip() == "":
            st.warning("Please type an answer before submitting.")
        else:
            with st.spinner("ECOLEX is evaluating your legal arguments..."):
                st.session_state.grading_result = grade_essay(user_essay, q_data['suggested_answer'])
                st.session_state.user_essay = user_essay

    if st.session_state.grading_result:
        st.divider()
        st.markdown("## 📝 **Grading & Feedback**")

        st.subheader("Suggested Answer")
        st.info(q_data['suggested_answer'])

        st.subheader("EcoLEX Evaluation")
        st.markdown(st.session_state.grading_result)

        if st.button("Try Another Question"):
            st.session_state.current_question = random.choice(QUESTIONS)
            st.session_state.grading_result = None
            st.rerun()

        if st.button("Exit"):
            st.balloons()
            st.markdown("# 🏛️ Good luck with the Bar, future Atenean lawyer!")
            st.stop()


if __name__ == '__main__':
    main()
