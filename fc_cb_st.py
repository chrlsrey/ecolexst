import streamlit as st
import random
import requests
import json
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3-vl:235b-cloud"
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question below based only on the context provided but in your answer do not say that it was based on context.
Context: {context}
Question: {question}
Answer:
"""

# --- DATABASE OF QUESTIONS (ESSAY) ---
ESSAY_QUESTIONS = [
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

# --- MATCHING DATA BANK ---
QUIZ_BANK = [
    {"term": "Writ of Kalikasan",
     "definition": "Issued when environmental damage prejudices life, health, or property in 2 or more cities or provinces."},
    {"term": "Writ of Continuing Mandamus",
     "definition": "A command to any government agency to perform acts until the judgment is fully satisfied."},
    {"term": "SLAPP",
     "definition": "A legal action filed to harass, vex, or stifle legal recourse in environmental enforcement."},
    {"term": "72 Hours", "definition": "The duration of an ex parte TEPO from the date of receipt."},
    {"term": "SC and CA", "definition": "Courts where a petition for a Writ of Kalikasan may be filed."},
    {"term": "SC, CA, and RTC",
     "definition": "Courts where a petition for a Writ of Continuing Mandamus may be filed."},
    {"term": "Mercado v. Lopena",
     "definition": "Case ruling that RA 9262 (VAWC) cases are not covered by SLAPP rules."},
    {"term": "Precautionary Principle",
     "definition": "Shifts the burden of evidence to avoid environmental threat despite scientific uncertainty."},
    {"term": "Exempted",
     "definition": "The status of petitioners regarding the payment of docket fees for Kalikasan/Mandamus."},
    {"term": "Ex parte", "definition": "How a TEPO is issued when there is extreme urgency and irreparable injury."},
    {"term": "10 Days",
     "definition": "Non-extendible period for a respondent to file a verified return for a Writ of Kalikasan."},
    {"term": "60 Days",
     "definition": "Time limit for the court to resolve a petition for Continuing Mandamus from submission."},
    {"term": "Malicious Neglect",
     "definition": "The ground upon which damages may be recovered in a Writ of Continuing Mandamus."},
    {"term": "Ocular Inspection Order",
     "definition": "A discovery measure available in a Writ of Kalikasan but not explicitly in Mandamus."},
    {"term": "Venue",
     "definition": "In Dolot v. Paje, the requirement to file where the omission took place was ruled as this, not jurisdiction."},
    {"term": "Summary", "definition": "The nature of the hearing for a Writ of Continuing Mandamus."},
    {"term": "Non-forum Shopping",
     "definition": "Certification that must be included in a verified petition for environmental writs."},
    {"term": "MMDA v. Concerned Residents",
     "definition": "The case where the Writ of Continuing Mandamus was first introduced (2008)."},
    {"term": "Environmental Protection Order",
     "definition": "An order directing a person to perform or desist from an act to protect the environment."},
    {"term": "Quarterly",
     "definition": "Frequency of progress reports the court may require for monitoring judgment satisfaction."},
    {"term": "70%", "definition": "The passing score for the Philippine Bar (referenced in user context)."},
    {"term": "Rule 45",
     "definition": "The rule under which a party may appeal a Kalikasan judgment to the Supreme Court."},
    {"term": "Question of Fact",
     "definition": "Unlike standard Rule 45 appeals, Kalikasan appeals may raise this type of question."},
    {"term": "Public Officials",
     "definition": "The only types of respondents allowed in a Writ of Continuing Mandamus."},
    {"term": "Separate Action",
     "definition": "The required method for recovering individual damages in a Writ of Kalikasan case."},
    {"term": "Certification",
     "definition": "The document by which a judge reports TEPO action to the SC within 10 days."},
    {"term": "Ministerial Duty",
     "definition": "The type of duty (not discretionary) required to support a Mandamus petition."},
    {"term": "15 Days", "definition": "The period to appeal an adverse judgment in a Writ of Kalikasan."},
    {"term": "Partial Return", "definition": "Periodic reports detailing compliance with the judgment in Mandamus."},
    {"term": "Final Return", "definition": "Made by the respondent upon full satisfaction of the judgment."},
    {"term": "Doctrine of Exhaustion",
     "definition": "Doctrine that remains consistent with the Rules of Procedure for Environmental Cases."},
    {"term": "Indigent",
     "definition": "In standard cases, they are exempt from fees, but in environmental cases, everyone is exempt."},
    {"term": "Jurisdictional",
     "definition": "The nature of the requirement that a petition for a Writ of Kalikasan be verified."},
    {"term": "Corporate Personality",
     "definition": "A hurdle for organizations in civil suits not present in Kalikasan petitions."},
    {"term": "Immediate Execution",
     "definition": "The status of environmental judgments pending appeal unless restrained."}
]

# --- MULTIPLE CHOICE DATA ---
MCQ_POOL = [
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
     "o": ["Loss of profits", "Irreparable damage to the party enjoined", "Administrative delay", "Political unrest"],
     "a": "Irreparable damage to the party enjoined"},
    {"q": "When may a court convert a TEPO into a permanent EPO?",
     "o": ["During the pre-trial", "In the final judgment", "Upon filing of the comment", "After 72 hours"],
     "a": "In the final judgment"},
    {"q": "Which case first introduced the Writ of Continuing Mandamus?",
     "o": ["Dolot v. Paje", "MMDA v. Concerned Residents of Manila Bay", "Segovia v. Climate Change Commission",
           "Mercado v. Lopena"], "a": "MMDA v. Concerned Residents of Manila Bay"},
    {"q": "What is the essence of a Writ of Continuing Mandamus?",
     "o": ["To stop a project immediately", "To ensure compliance with a final judgment through retained jurisdiction",
           "To award damages for environmental loss", "To punish public officials"],
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
     "o": ["One year has passed", "The judgment is fully satisfied", "The respondent resigns", "A new law is passed"],
     "a": "The judgment is fully satisfied"},
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
     "o": ["The case is dismissed", "The court hears the petition ex parte", "The respondent is automatically jailed",
           "The petitioner wins by default judgment"], "a": "The court hears the petition ex parte"},
    {"q": "Can individual damages be awarded in a Writ of Kalikasan?",
     "o": ["Yes", "No, the party must file a separate action", "Only if the damage is over 1 Billion",
           "Only in the Supreme Court"], "a": "No, the party must file a separate action"},
    {"q": "What is the 'Precautionary Principle'?", "o": ["A rule that requires 100% scientific certainty",
                                                          "A rule that shifts the burden of evidence to avoid environmental threat despite uncertainty",
                                                          "A safety protocol for mines", "A requirement to wear PPE"],
     "a": "A rule that shifts the burden of evidence to avoid environmental threat despite uncertainty"},
    {"q": "An appeal for a Writ of Kalikasan is made under Rule 45 and may raise:",
     "o": ["Only questions of law", "Only questions of fact", "Both questions of law and fact", "No questions at all"],
     "a": "Both questions of law and fact"},
    {"q": "What is a 'Discovery Measure' available in a Writ of Kalikasan but NOT in Continuing Mandamus?",
     "o": ["Deposition", "Ocular Inspection Order", "Interrogatories", "Request for Admission"],
     "a": "Ocular Inspection Order"},
    {"q": "In a Writ of Kalikasan, how many days does the court have to issue the writ after filing?",
     "o": ["Within 3 days", "Within 10 days", "Within 24 hours", "Immediately"], "a": "Within 3 days"},
    {"q": "Which writ allows for the recovery of damages for 'malicious neglect'?",
     "o": ["Writ of Kalikasan", "Writ of Continuing Mandamus", "Writ of Habeas Data", "None of the above"],
     "a": "Writ of Continuing Mandamus"},
    {"q": "Which writ is directed only against the government and its officers?",
     "o": ["Writ of Kalikasan", "Writ of Continuing Mandamus", "Both", "Neither"], "a": "Writ of Continuing Mandamus"},
    {"q": "Are docket fees required for a Writ of Kalikasan?",
     "o": ["Yes", "No, it is exempt", "Only if it involves mining", "Half price"], "a": "No, it is exempt"},
    {"q": "The hearing for environmental writs is generally:",
     "o": ["Full-blown trial", "Summary in nature", "Confidential", "Non-adversarial"], "a": "Summary in nature"},
    {"q": "What is the effect of filing a Writ of Kalikasan on other civil actions?",
     "o": ["It precludes them", "It does not preclude the filing of separate actions", "It suspends them",
           "It dismisses them"], "a": "It does not preclude the filing of separate actions"}
]


# --- RAG BOT LOGIC ---
def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def generate_rag_answer(query_text: str) -> str:
    return f"Hello, future Atenean Lawyer! \n\nSadly, your inquiry cannot proceed. \nEcoLEX Chatbot API is available only for local installations."


# --- SHARED FUNCTIONS ---
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
        data = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}], "stream": False}
        response = requests.post(OLLAMA_URL, json=data)
        return response.json()["message"]["content"]
    except Exception as e:
        return f"Hello, future Atenean Lawyer! \n\nManually compare your answer with the suggested answer. \nEcoLEX AI Grader API is available only for local installations."


def reset_matching():
    st.session_state.matching_items = random.sample(QUIZ_BANK, 10)
    st.session_state.matching_answers = {}
    st.session_state.matching_submitted = False


def reset_mcq():
    full_list = (MCQ_POOL * 3)[:75]
    random.shuffle(full_list)
    st.session_state.mcq_data = full_list[:20]
    st.session_state.mcq_idx = 0
    st.session_state.mcq_score = 0
    st.session_state.mcq_complete = False


# --- PATH HANDLERS ---
def essay_path():
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.path = "dashboard"
        st.rerun()

    st.markdown("# ✍️ **EcoLEX Bar Simulator**")
    if 'current_essay_q' not in st.session_state:
        st.session_state.current_essay_q = random.choice(ESSAY_QUESTIONS)
        st.session_state.essay_result = None

    q = st.session_state.current_essay_q
    st.markdown(f"## **Question:**")
    st.markdown(q['question'])
    user_input = st.text_area("Your Essay Answer:", height=300, key="essay_area")

    if st.button("Submit Answer"):
        if user_input.strip() == "":
            st.warning("Please type an answer.")
        else:
            with st.spinner("Evaluating..."):
                st.session_state.essay_result = grade_essay(user_input, q['suggested_answer'])

    if st.session_state.essay_result:
        st.divider()
        st.subheader("Suggested Answer")
        st.info(q['suggested_answer'])
        st.subheader("EcoLEX Evaluation")
        st.markdown(st.session_state.essay_result)
        if st.button("Try Another"):
            st.session_state.current_essay_q = random.choice(ESSAY_QUESTIONS)
            st.session_state.essay_result = None
            st.rerun()


def matching_path():
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.path = "dashboard"
        st.rerun()

    st.markdown("# 🧩 **EcoLEX Match**")
    if "matching_items" not in st.session_state:
        reset_matching()

    with st.form("matching_form"):
        items = st.session_state.matching_items
        options = ["-- Select Term --"] + sorted([x["term"] for x in items])
        for i, item in enumerate(items):
            st.markdown(f"**Definition {i + 1}:** {item['definition']}")
            st.session_state.matching_answers[item['definition']] = st.selectbox("Select Term", options, key=f"m_{i}")
            st.write("---")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("Submit")
        if col2.form_submit_button("Early Quit"):
            st.session_state.path = "dashboard"
            st.rerun()

    if submit:
        score = 0
        for item in items:
            if st.session_state.matching_answers[item['definition']] == item['term']:
                score += 1
                st.success(f"✅ Correct: {item['term']}")
            else:
                st.error(f"❌ Incorrect: {item['definition']} → {item['term']}")
        st.header(f"Score: {score}/10")
        if st.button("New Questions"):
            reset_matching()
            st.rerun()


def mcq_path():
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.path = "dashboard"
        st.rerun()

    st.markdown("# 🔘 **EcoLEX Recall**")
    if 'mcq_data' not in st.session_state:
        reset_mcq()

    if not st.session_state.mcq_complete:
        idx = st.session_state.mcq_idx
        q = st.session_state.mcq_data[idx]
        st.markdown(f"### Question {idx + 1} of 20")
        choice = st.radio(q["q"], options=q["o"], key=f"mcq_{idx}")

        col1, col2 = st.columns(2)
        if col1.button("Submit Answer"):
            if choice == q["a"]:
                st.session_state.mcq_score += 1
                st.success("Correct!")
            else:
                st.error(f"Wrong! Correct: {q['a']}")

            if idx + 1 < 20:
                st.session_state.mcq_idx += 1
                st.rerun()
            else:
                st.session_state.mcq_complete = True
                st.rerun()

        if col2.button("Early Quit"):
            st.session_state.mcq_complete = True
            st.rerun()
    else:
        st.header(f"Final Score: {st.session_state.mcq_score}/20")
        if st.session_state.mcq_score / 20 >= 0.7:
            st.balloons()
            st.success("Bar Ready!")
        if st.button("Restart"):
            reset_mcq()
            st.rerun()


def chatbot_path():
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.path = "dashboard"
        st.rerun()

    st.markdown("# 🏛️ **EcoLEX Chatbot**")
    st.markdown("**A Fine-tuned Philippine Environmental Law Knowledge Assistant**")
    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about Environmental Law..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching legal records..."):
                response = generate_rag_answer(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


# --- MAIN DASHBOARD ---
def main():
    if 'path' not in st.session_state:
        st.session_state.path = "dashboard"

    if st.session_state.path == "dashboard":
        st.set_page_config(page_title="EcoLEX Dashboard", page_icon="⚖️")
        st.title("⚖️ **EcoLEX: Bar Exam Reviewer**")
        st.markdown("### Created by: Engr. Charles Arthel Rey, M.Sc., J.D. (cand)")
        st.divider()

        st.write("Choose your review module:")
        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        if c1.button("✍️ Bar Simulator\n(AI Graded)", use_container_width=True):
            st.session_state.path = "essay"
            st.rerun()

        if c2.button("🧩 Matching Type\n(10 Items)", use_container_width=True):
            st.session_state.path = "matching"
            st.rerun()

        if c3.button("🔘 Multiple Choice\n(20 Items)", use_container_width=True):
            st.session_state.path = "mcq"
            st.rerun()

        if c4.button("🏛️ EcoLEX Chatbot\n(RAG Knowledge Base)", use_container_width=True):
            st.session_state.path = "chatbot"
            st.rerun()

        #st.sidebar.markdown("### Review Resources")
        #st.sidebar.info("Coverage: Rules of Procedure for Environmental Cases.")


    elif st.session_state.path == "essay":
        essay_path()
    elif st.session_state.path == "matching":
        matching_path()
    elif st.session_state.path == "mcq":
        mcq_path()
    elif st.session_state.path == "chatbot":
        chatbot_path()


if __name__ == '__main__':
    main()
