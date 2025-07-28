import streamlit as st
import pandas as pd
import json
import random
import time
import google.generativeai as genai

# --- Page Configuration: Polished and Professional ---
st.set_page_config(
    page_title="CertifyAI - The Future of Learning",
    page_icon="🤖",
    layout="wide"
)

# --- Full 20-Question Mock Data - The Robust Fallback System ---
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

# --- Backend Function for Live AI Call ---
def generate_questions_with_ai(api_key, num_questions, topics, syllabus):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
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
        cleaned_json = response.text.strip().replace("json", "").replace("", "")
        return json.loads(cleaned_json)
    except Exception as e:
        # This print statement is helpful for debugging in your local terminal
        print(f"Error during AI Generation: {e}")
        return None

# --- Session State Initialization ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help with the CertifyAI app today?"}]

# --- Feature #4: Guided Welcome Page ---
if not st.session_state.app_started:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("assets/logo.jpg", use_column_width=True)
        st.title("Welcome to CertifyAI")
        st.subheader("The Future of Personalized Exam Preparation")
        st.write("")
        st.markdown(
            """
            CertifyAI is an intelligent platform that creates mock exams from any syllabus, helping you *study smarter, not harder.* 
            
            Ready to ace your next certification?
            """
        )
        st.write("")
        if st.button("🚀 Start Building My Test", use_container_width=True, type="primary"):
            st.session_state.app_started = True
            st.rerun()
else:
    # --- Main Application UI Starts Here ---
    
    # --- Complete Sidebar with All Features ---
    with st.sidebar:
        st.image("assets/logo.jpg", width=100)
        st.header("⚙ Test Configuration")
        st.write("Customize your exam.")
        num_questions = st.slider("Number of Questions:", min_value=1, max_value=20, value=5, step=1)
        selected_topics = st.multiselect("Filter by Topics:", options=ALL_TOPICS, default=ALL_TOPICS)
        st.write("---")
        st.header("💬 Chat with our Assistant")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])
        
        def get_bot_response(user_prompt):
            prompt = user_prompt.lower()
            if "hello" in prompt or "hi" in prompt: return "Hello there! How can I assist you?"
            elif "what is this" in prompt or "what do you do" in prompt: return "I'm part of CertifyAI, a platform that creates personalized practice exams from any syllabus!"
            elif "how do i use" in prompt or "help" in prompt: return "Configure your test settings on the left, then click the 'Generate My Test' button on the main page. Good luck!"
            elif "who built" in prompt or "team" in prompt: return "I was built by the talented team [Your Team Name] for the Comsoc HackX hackathon!"
            else: return "I'm a simple bot for this demo. I can answer questions about what this app is and how to use it. Try asking 'what do you do?'"
        
        if prompt := st.chat_input("Ask about the app..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            response = get_bot_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"): st.markdown(response)

    # --- Main Page Content ---
    st.image("assets/banner.jpg")
    st.header("📝 Start Your Personalized Test")

    with st.expander("Step 1: Paste Your Syllabus (Optional)"):
        syllabus_text = st.text_area("Paste syllabus text here", height=150, placeholder="Our AI can generate from any syllabus! Leave blank to use a default AWS topic.")

    if st.button("Step 2: Generate My Test ✨", type="primary", use_container_width=True):
        final_questions = None
        # --- Feature #1: Mission Control Status Panel ---
        with st.status("🚀 Launching CertifyAI Core...", state="running", expanded=True) as status:
            try:
                status.write("📡 Connecting to AI model...")
                time.sleep(1) 
                api_key = st.secrets.get("GEMINI_API_KEY")
                if not api_key:
                    status.update(label="API Key not found! Switching to fallback.", state="error", expanded=False)
                    time.sleep(1)
                    raise ValueError("API Key missing.")

                status.write("🧠 Generating unique questions...")
                time.sleep(1) 
                generated_questions = generate_questions_with_ai(api_key, num_questions, selected_topics, syllabus_text)
                
                status.write("✅ Parsing AI response...")
                time.sleep(1)
                
                if generated_questions:
                    final_questions = generated_questions
                    status.update(label="Test built successfully by Live AI!", state="complete", expanded=False)
                else:
                    raise ValueError("AI failed to generate valid questions.")
            
            except Exception as e:
                status.update(label="Live AI failed. Building test from local bank...", state="running")
                time.sleep(1)
                filtered_by_topic = [q for q in FULL_QUESTION_BANK if q['syllabus_topic'] in selected_topics]
                final_num_questions = min(num_questions, len(filtered_by_topic))
                final_questions = random.sample(filtered_by_topic, final_num_questions) if final_num_questions > 0 else []
                status.update(label="Fallback test built successfully!", state="complete", expanded=False)
        
        st.session_state.test_data = final_questions
        st.session_state.test_generated = True
        st.session_state.user_answers = {}
        # Clear previous results when a new test is generated
        if 'results' in st.session_state:
            del st.session_state.results

    if st.session_state.get('test_generated', False) and st.session_state.test_data:
        st.write("---")
        st.header("📝 Your Personalized Mock Exam")
        for i, q in enumerate(st.session_state.test_data):
            # --- Feature #2: Question "Cards" ---
            with st.container(border=True):
                st.markdown(f"*Question {i+1} of {len(st.session_state.test_data)}* | Topic: {q.get('syllabus_topic', 'N/A')}")
                st.markdown(f"##### {q['question']}")
                options = list(q['options'].values())
                st.session_state.user_answers[i] = st.radio("Options", options, key=f"q_{i}", label_visibility="collapsed")
        
        if st.button("Step 3: Submit & See Results 🚀", use_container_width=True):
            score, topic_performance = 0, {topic: {'correct': 0, 'total': 0} for topic in ALL_TOPICS}
            for i, q in enumerate(st.session_state.test_data):
                topic = q.get('syllabus_topic', 'Unknown')
                if topic not in topic_performance: topic_performance[topic] = {'correct': 0, 'total': 0}
                topic_performance[topic]['total'] += 1
                if st.session_state.user_answers.get(i) == q['options'].get(q['correct_answer']):
                    score += 1
                    topic_performance[topic]['correct'] += 1
            st.session_state.results = {'score': score, 'topic_performance': topic_performance}
            st.rerun()

    if st.session_state.get('results'):
        results = st.session_state.results
        score = results['score']
        topic_performance = results['topic_performance']
        
        # --- Feature #3: Dynamic Results Dashboard ---
        st.write("---")
        st.header("📈 Your Results Dashboard")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            overall_score = (score / len(st.session_state.test_data)) * 100 if st.session_state.test_data else 0
            st.metric("Overall Score", f"{overall_score:.1f}%", f"{score}/{len(st.session_state.test_data)} correct")
            if overall_score >= 80:
                st.balloons()
                st.success("Excellent work! You are well-prepared.")
        
        with col2:
            st.markdown("*Breakdown by Topic:*")
            perf_topics = {k: v for k, v in topic_performance.items() if v['total'] > 0}
            
            for topic, perf in perf_topics.items():
                percentage = (perf['correct'] / perf['total']) * 100
                st.markdown(f"{topic}** ({perf['correct']}/{perf['total']})")
                st.progress(int(percentage))
        
        min_percentage, weakest_topic = 100, ""
        for topic, perf in perf_topics.items():
            if perf['total'] > 0 and (percentage := (perf['correct'] / perf['total']) * 100) < min_percentage:
                min_percentage, weakest_topic = percentage, topic
        
        if weakest_topic and min_percentage < 80:
             st.warning(f"🎯 *Actionable Insight:* Your lowest score is in *{weakest_topic}*. Focus your next study session there!")
