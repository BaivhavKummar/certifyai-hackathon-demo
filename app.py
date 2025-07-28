import streamlit as st
import pandas as pd
import json
import random # [NEW] Import random for question shuffling

# --- Page Configuration ---
st.set_page_config(
    page_title="CertifyAI Prototype",
    page_icon="🤖",
    layout="wide"
)

# --- [NEW & EXPANDED] Hardcoded Mock AI Response ---
# Now contains 20 questions to make the demo feel rich and dynamic.
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
# Load the full question bank once
FULL_QUESTION_BANK = json.loads(MOCK_AI_RESPONSE)
ALL_TOPICS = sorted(list(set(q['syllabus_topic'] for q in FULL_QUESTION_BANK)))


# --- [UI/UX] App UI and Logic ---

st.title("🤖 CertifyAI")
st.caption("An intelligent mock test generator powered by AI")

# --- [UI/UX] Sidebar for Configuration ---
with st.sidebar:
    st.header("⚙ Test Configuration")
    st.write("Customize your exam to focus on what matters most to you.")
    
    # Slider for number of questions
    num_questions = st.slider(
        "Number of Questions:",
        min_value=1,
        max_value=len(FULL_QUESTION_BANK),
        value=5, # Default value
        step=1
    )

    # Multi-select for topics
    selected_topics = st.multiselect(
        "Filter by Topics:",
        options=ALL_TOPICS,
        default=ALL_TOPICS # Default to all topics
    )

# --- Main App Body ---
st.write("---")
st.header("Start Your Personalized Test")

# --- [UI/UX] Syllabus input now in an expander for a cleaner look ---
with st.expander("Step 1: Paste Your Syllabus (Optional)"):
    syllabus_text = st.text_area(
        "Paste syllabus text here",
        height=150,
        placeholder="""Our AI can generate from any syllabus, but for this demo, just use the controls in the sidebar!
        Domain 1: Cloud Concepts
        1.1 Define the AWS Cloud and its value proposition
        1.2 Identify aspects of AWS Cloud economics...
    
        Domain 4: Billing and Pricing
        4.1 Compare and contrast the various pricing models for AWS...""""""
    )

if st.button("Step 2: Generate My Test ✨", type="primary"):
    with st.spinner("Analyzing your configuration and building your test..."):
        # Filter questions based on selected topics
        filtered_by_topic = [q for q in FULL_QUESTION_BANK if q['syllabus_topic'] in selected_topics]
        
        # [NEW] Handle cases where no questions are available for the selection
        if not filtered_by_topic:
            st.error("No questions found for the selected topics. Please broaden your topic selection in the sidebar.")
            st.stop()

        # [MODIFIED] Randomly sample questions to prevent repetition
        # Ensure we don't request more questions than are available
        final_num_questions = min(num_questions, len(filtered_by_topic))
        final_questions = random.sample(filtered_by_topic, final_num_questions)
        
        st.session_state.test_data = final_questions
        st.session_state.test_generated = True
        st.session_state.user_answers = {} # Reset answers
        st.success(f"Success! Your {len(final_questions)}-question test is ready.")


# --- Display the test ---
if st.session_state.get('test_generated', False) and st.session_state.test_data:
    st.write("---")
    st.header("Your Personalized Mock Exam")

    for i, q in enumerate(st.session_state.test_data):
        st.markdown(f"*Question {i+1}:* {q['question']}")
        st.markdown(f"(Topic: {q['syllabus_topic']})")
        options = list(q['options'].values())
        st.session_state.user_answers[i] = st.radio(
            "Choose your answer:", options, key=f"q_{i}", label_visibility="collapsed"
        )
        st.write("")

    if st.button("Step 3: Submit & See Results 🚀"):
        # Calculate results
        score = 0
        topic_performance = {topic: {'correct': 0, 'total': 0} for topic in selected_topics}
        
        for i, q in enumerate(st.session_state.test_data):
            topic = q['syllabus_topic']
            # Initialize if somehow a topic slips through (shouldn't happen)
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0}

            topic_performance[topic]['total'] += 1
            
            selected_option_text = st.session_state.user_answers.get(i)
            correct_option_key = q['correct_answer']
            correct_option_text = q['options'][correct_option_key]

            if selected_option_text == correct_option_text:
                score += 1
                topic_performance[topic]['correct'] += 1
        
        # --- [UI/UX] Enhanced Results Dashboard ---
        st.write("---")
        st.header("📈 Your Results Dashboard")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            overall_score = (score / len(st.session_state.test_data)) * 100 if st.session_state.test_data else 0
            st.metric("Overall Score", f"{overall_score:.1f}%", f"{score}/{len(st.session_state.test_data)} correct")
            if overall_score >= 80:
                st.balloons()
                st.success("Great job! You're on the right track.")
        
        with col2:
            st.markdown("*Performance by Topic*")
            chart_data = {
                'Topic': [],
                'Percentage': []
            }
            # Only include topics that were in the test
            perf_topics = {k: v for k, v in topic_performance.items() if v['total'] > 0}

            for topic, perf in perf_topics.items():
                percentage = (perf['correct'] / perf['total']) * 100
                chart_data['Topic'].append(f"{topic} ({perf['correct']}/{perf['total']})")
                chart_data['Percentage'].append(percentage)
            
            if chart_data['Topic']:
                df = pd.DataFrame(chart_data).set_index('Topic')
                st.bar_chart(df['Percentage'])
        
        # Find and highlight the weak area
        min_percentage = 100
        weakest_topic = ""
        for topic, perf in perf_topics.items():
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total']) * 100
                if percentage < min_percentage:
                    min_percentage = percentage
                    weakest_topic = topic
        
        if weakest_topic and min_percentage < 100:
             st.warning(f"🎯 *Actionable Insight:* Your lowest score is in *{weakest_topic}*. Focus your next study session there!")
