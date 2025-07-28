import streamlit as st
import pandas as pd
import json
import random
import google.generativeai as genai # [NEW] Import the Google AI library

# --- Page Configuration ---
st.set_page_config(
    page_title="CertifyAI - Live AI Prototype",
    page_icon="🤖",
    layout="wide"
)

# --- [MODIFIED] Fallback Mock Data ---
# This is now our backup system if the live AI fails.
# I've kept the full 20-question set for a robust fallback.
MOCK_AI_RESPONSE = """
[
    {"question": "Which AWS service provides a simple way to set up a new, secure, multi-account AWS environment?", "options": {"A": "AWS Organizations", "B": "AWS Control Tower", "C": "AWS IAM", "D": "AWS Config"}, "correct_answer": "B", "syllabus_topic": "Cloud Concepts"},
    {"question": "What does AWS Shield Standard provide?", "options": {"A": "DDoS protection for web applications running on EC2", "B": "Protection against all network layer DDoS attacks", "C": "Managed threat intelligence", "D": "Web Application Firewall capabilities"}, "correct_answer": "B", "syllabus_topic": "Security and Compliance"},
    {"question": "Which AWS pricing model is best suited for workloads with flexible start and end times?", "options": {"A": "On-Demand Instances", "B": "Reserved Instances", "C": "Spot Instances", "D": "Savings Plans"}, "correct_answer": "C", "syllabus_topic": "Billing and Pricing"},
    {"question": "What is the primary function of Amazon Route 53?", "options": {"A": "Content delivery network", "B": "Scalable DNS and domain name registration", "C": "Virtual private cloud networking", "D": "Load balancing"}, "correct_answer": "B", "syllabus_topic": "Core Services"},
    {"question": "Under the AWS shared responsibility model, which of the following is a responsibility of AWS?", "options": {"A": "Customer data encryption", "B": "Managing security groups", "C": "Patching guest operating systems", "D": "Maintaining physical hardware"}, "correct_answer": "D", "syllabus_topic": "Security and Compliance"},
    {"question": "Which tool helps you calculate your monthly AWS bill more efficiently?", "options": {"A": "AWS Cost Explorer", "B": "AWS Budgets", "C": "AWS Pricing Calculator", "D": "AWS Trusted Advisor"}, "correct_answer": "C", "syllabus_topic": "Billing and Pricing"},
    {"question": "Which service is used to run containerized applications on AWS?", "options": {"A": "AWS Lambda", "B": "Amazon EC2", "C": "Amazon ECS", "D": "Amazon S3"}, "correct_answer": "C", "syllabus_topic": "Core Services"},
    {"question": "What is the concept of 'elasticity' in the AWS Cloud?", "options": {"A": "The ability to pay only for what you use", "B": "The ability of the system to scale in and out based on demand", "C": "The ability to deploy to multiple geographic regions", "D": "The ability to recover quickly from failures"}, "correct_answer": "B", "syllabus_topic": "Cloud Concepts"},
    {"question": "A user wants to be notified when their AWS bill exceeds $100. Which service should they use?", "options": {"A": "AWS Cost Explorer", "B": "AWS Budgets", "C": "Amazon CloudWatch", "D": "AWS Trusted Advisor"}, "correct_answer": "B", "syllabus_topic": "Billing and Pricing"},
    {"question": "Which AWS service is designed to be a durable key-value store?", "options": {"A": "Amazon RDS", "B": "Amazon Redshift", "C": "Amazon DynamoDB", "D": "Amazon ElastiCache"}, "correct_answer": "C", "syllabus_topic": "Core Services"},
    {"question": "What is a 'VPC' in AWS?", "options": {"A": "A popular VPN client", "B": "A bill for cloud services", "C": "A logically isolated section of the AWS Cloud", "D": "A content delivery network"}, "correct_answer": "C", "syllabus_topic": "Technology"},
    {"question": "To get a discount on EC2 instances for a 1-year commitment, which option is most suitable?", "options": {"A": "Spot Instances", "B": "On-Demand Instances", "C": "Reserved Instances", "D": "Dedicated Hosts"}, "correct_answer": "C", "syllabus_topic": "Billing and Pricing"},
    {"question": "Which IAM entity should you use to grant an application running on an EC2 instance access to an S3 bucket?", "options": {"A": "IAM User", "B": "IAM Group", "C": "IAM Role", "D": "IAM Policy"}, "correct_answer": "C", "syllabus_topic": "Security and Compliance"},
    {"question": "What AWS service would you use for long-term archival of data that is rarely accessed?", "options": {"A": "Amazon S3 Standard", "B": "Amazon EFS", "C": "Amazon EBS", "D": "Amazon S3 Glacier Deep Archive"}, "correct_answer": "D", "syllabus_topic": "Core Services"},
    {"question": "Which of the following is one of the six advantages of cloud computing?", "options": {"A": "Fixed capacity management", "B": "Trade capital expense for variable expense", "C": "Slow global deployment", "D": "Managing your own data centers"}, "correct_answer": "B", "syllabus_topic": "Cloud Concepts"},
    {"question": "What is AWS KMS primarily used for?", "options": {"A": "Network security", "B": "Monitoring application logs", "C": "Managing encryption keys", "D": "User authentication"}, "correct_answer": "C", "syllabus_topic": "Security and Compliance"},
    {"question": "Which AWS support plan provides access to a Technical Account Manager (TAM)?", "options": {"A": "Basic", "B": "Developer", "C": "Business", "D": "Enterprise"}, "correct_answer": "D", "syllabus_topic": "Billing and Pricing"},
    {"question": "What service provides managed relational databases in AWS?", "options": {"A": "Amazon DynamoDB", "B": "Amazon RDS", "C": "Amazon Redshift", "D": "Amazon S3"}, "correct_answer": "B", "syllabus_topic": "Core Services"},
    {"question": "Which tool provides real-time guidance to help you provision your resources following AWS best practices?", "options": {"A": "AWS Inspector", "B": "AWS Shield", "C": "AWS Trusted Advisor", "D": "AWS Config"}, "correct_answer": "C", "syllabus_topic": "Technology"},
    {"question": "What does the term 'multi-tenancy' mean in the context of public cloud?", "options": {"A": "Each customer has their own physical server", "B": "Multiple customers share the same physical infrastructure", "C": "A system is deployed across multiple data centers", "D": "The ability to have multiple users"}, "correct_answer": "B", "syllabus_topic": "Cloud Concepts"}
]
"""
FULL_QUESTION_BANK = json.loads(MOCK_AI_RESPONSE)
ALL_TOPICS = sorted(list(set(q['syllabus_topic'] for q in FULL_QUESTION_BANK)))

# --- [NEW] Function to call the Gemini API ---
def generate_questions_with_ai(api_key, num_questions, topics, syllabus):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # A fast and capable model
        
        # This is our powerful, engineered prompt
        prompt = f"""
        You are 'CertifyAI', an expert system that creates high-quality practice exams based on a provided syllabus.
        Your task is to generate a multiple-choice quiz based on my specifications.

        *Instructions:*
        1. Read the syllabus provided below to understand the content.
        2. Generate exactly {num_questions} multiple-choice questions.
        3. If specific topics are requested, focus the questions on those topics: {', '.join(topics)}.
        4. Each question must have 4 options (A, B, C, D).
        5. You MUST identify the single correct answer for each question.
        6. You MUST specify which syllabus topic each question pertains to from the list: {', '.join(topics)}.
        7. Your final output MUST be a single, valid JSON array of objects. Do not include any other text, just the JSON.
        8. The JSON format for each object is: {{"question": "...", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "correct_answer": "...", "syllabus_topic": "..."}}

        *Syllabus:*
        ---
        {syllabus if syllabus else "AWS Cloud Practitioner Essentials"}
        ---
        """
        
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        cleaned_json = response.text.strip().replace("json", "").replace("", "")
        return json.loads(cleaned_json)

    except Exception as e:
        st.error(f"An error occurred with the AI API: {e}")
        return None # Signal that the API call failed

# --- UI and State Management (Identical to previous version) ---
st.title("🤖 CertifyAI")
st.caption("An intelligent mock test generator powered by AI")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm CertifyAI's assistant. How can I help?"}]
with st.sidebar:
    st.header("⚙ Test Configuration")
    num_questions = st.slider("Number of Questions:", min_value=1, max_value=20, value=5, step=1)
    selected_topics = st.multiselect("Filter by Topics:", options=ALL_TOPICS, default=ALL_TOPICS)
    st.write("---")
    st.header("💬 Chat with our Assistant")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    def get_bot_response(user_prompt):
        prompt = user_prompt.lower()
        if "hello" in prompt: return "Hello there! How can I assist you?"
        elif "what is this" in prompt: return "I'm part of CertifyAI, a platform that creates personalized practice exams from any syllabus!"
        elif "help" in prompt: return "Configure your test on the left, then click 'Generate My Test'!"
        else: return "I'm a simple bot for this demo. Try asking 'what is this app?'"
    if prompt := st.chat_input("Ask about the app..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)

# --- Main App Body ---
st.header("Start Your Personalized Test")
with st.expander("Step 1: Paste Your Syllabus (Optional)"):
    syllabus_text = st.text_area("Paste syllabus text here", height=150, placeholder="Our AI can generate from any syllabus! Leave blank to use a default AWS topic.")

# --- [MODIFIED] Button Logic to include Live AI Call ---
if st.button("Step 2: Generate My Test ✨", type="primary"):
    with st.spinner("🚀 Contacting the live AI... This may take a moment."):
        
        # Try to use the live API first
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Gemini API key not found. Please add it to your secrets file.")
            st.stop()
            
        generated_questions = generate_questions_with_ai(api_key, num_questions, selected_topics, syllabus_text)
        
        if generated_questions:
            # SUCCESS: Live AI worked
            st.session_state.test_data = generated_questions
            st.success("Success! Your test was generated by the live CertifyAI core.")
        else:
            # FAILURE: Fallback to mock data
            st.warning("The live AI is busy or encountered an error. Don't worry, here is a high-quality practice test from our local question bank!")
            filtered_by_topic = [q for q in FULL_QUESTION_BANK if q['syllabus_topic'] in selected_topics]
            final_num_questions = min(num_questions, len(filtered_by_topic))
            st.session_state.test_data = random.sample(filtered_by_topic, final_num_questions) if final_num_questions > 0 else []
        
        st.session_state.test_generated = True
        st.session_state.user_answers = {}

# --- Display test and results (Identical to previous version, no changes needed) ---
if st.session_state.get('test_generated', False) and st.session_state.test_data:
    st.write("---")
    st.header("Your Personalized Mock Exam")
    # ... The rest of the test display and results calculation code remains exactly the same ...
    for i, q in enumerate(st.session_state.test_data):
        st.markdown(f"*Question {i+1}:* {q['question']}")
        st.markdown(f"(Topic: {q['syllabus_topic']})")
        options = list(q['options'].values())
        st.session_state.user_answers[i] = st.radio("Choose your answer:", options, key=f"q_{i}", label_visibility="collapsed")
        st.write("")
    if st.button("Step 3: Submit & See Results 🚀"):
        score = 0
        topic_performance = {topic: {'correct': 0, 'total': 0} for topic in ALL_TOPICS}
        for i, q in enumerate(st.session_state.test_data):
            topic = q['syllabus_topic']
            if topic not in topic_performance: topic_performance[topic] = {'correct': 0, 'total': 0}
            topic_performance[topic]['total'] += 1
            selected_option_text = st.session_state.user_answers.get(i)
            correct_option_key = q['correct_answer']
            correct_option_text = q['options'][correct_option_key]
            if selected_option_text == correct_option_text:
                score += 1
                topic_performance[topic]['correct'] += 1
        st.write("---")
        st.header("📈 Your Results Dashboard")
        col1, col2 = st.columns([1, 2])
        with col1:
            overall_score = (score / len(st.session_state.test_data)) * 100 if st.session_state.test_data else 0
            st.metric("Overall Score", f"{overall_score:.1f}%", f"{score}/{len(st.session_state.test_data)} correct")
            if overall_score >= 80: st.balloons(); st.success("Great job!")
        with col2:
            st.markdown("*Performance by Topic*")
            chart_data = {'Topic': [], 'Percentage': []}
            perf_topics = {k: v for k, v in topic_performance.items() if v['total'] > 0}
            for topic, perf in perf_topics.items():
                percentage = (perf['correct'] / perf['total']) * 100
                chart_data['Topic'].append(f"{topic} ({perf['correct']}/{perf['total']})")
                chart_data['Percentage'].append(percentage)
            if chart_data['Topic']:
                df = pd.DataFrame(chart_data).set_index('Topic')
                st.bar_chart(df['Percentage'])
        min_percentage, weakest_topic = 100, ""
        for topic, perf in perf_topics.items():
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total']) * 100
                if percentage < min_percentage: min_percentage, weakest_topic = percentage, topic
        if weakest_topic and min_percentage < 100:
             st.warning(f"🎯 *Actionable Insight:* Your lowest score is in *{weakest_topic}*. Focus there!")
