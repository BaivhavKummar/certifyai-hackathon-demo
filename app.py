import streamlit as st
import time
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="CertifyAI Prototype",
    page_icon="🤖",
    layout="wide"
)

# --- Hardcoded Mock AI Response (for a reliable demo) ---
# This JSON structure should match the one you designed in your prompt engineering.
MOCK_AI_RESPONSE = """
[
  {
    "question": "Which AWS service is primarily used for scalable object storage?",
    "options": {
      "A": "Amazon EC2",
      "B": "Amazon S3",
      "C": "Amazon RDS",
      "D": "AWS Lambda"
    },
    "correct_answer": "B",
    "syllabus_topic": "Cloud Concepts"
  },
  {
    "question": "What is the AWS Well-Architected Framework pillar that focuses on the ability of a system to recover from failures?",
    "options": {
      "A": "Performance Efficiency",
      "B": "Cost Optimization",
      "C": "Reliability",
      "D": "Security"
    },
    "correct_answer": "C",
    "syllabus_topic": "Security and Compliance"
  },
  {
    "question": "Which AWS pricing model allows users to pay a low hourly rate with no long-term commitments for EC2 instances?",
    "options": {
      "A": "Reserved Instances",
      "B": "Spot Instances",
      "C": "On-Demand",
      "D": "Savings Plans"
    },
    "correct_answer": "C",
    "syllabus_topic": "Billing and Pricing"
  },
  {
    "question": "A user needs to run a serverless function that is triggered by an S3 bucket event. Which service should they use?",
    "options": {
      "A": "Amazon ECS",
      "B": "Amazon EC2",
      "C": "AWS Lambda",
      "D": "Amazon Lightsail"
    },
    "correct_answer": "C",
    "syllabus_topic": "Technology"
  },
  {
    "question": "Under the AWS Shared Responsibility Model, what is the customer responsible for?",
    "options": {
      "A": "Securing global physical infrastructure",
      "B": "Patching the host operating system of RDS",
      "C": "Configuring security groups and network ACLs",
      "D": "Managing edge locations"
    },
    "correct_answer": "C",
    "syllabus_topic": "Security and Compliance"
  },
  {
    "question": "A company wants to analyze its AWS spending and find potential savings. Which tool provides this insight?",
    "options": {
        "A": "AWS Trusted Advisor",
        "B": "AWS Cost Explorer",
        "C": "Amazon CloudWatch",
        "D": "AWS Budgets"
    },
    "correct_answer": "B",
    "syllabus_topic": "Billing and Pricing"
  }
]
"""

# --- App UI and Logic ---

st.title("🤖 CertifyAI")
st.subheader("Generate instant practice exams from any syllabus.")

# Initialize session state for the test
if 'test_generated' not in st.session_state:
    st.session_state.test_generated = False
if 'test_data' not in st.session_state:
    st.session_state.test_data = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

st.write("---")
st.write("**Follow Sarah's Journey:**")
st.info("Paste the AWS Cloud Practitioner syllabus text below, or just click 'Generate' to use a sample.")

# User Input
syllabus_text = st.text_area(
    "1. Paste Syllabus Here",
    height=150,
    placeholder="""Domain 1: Cloud Concepts
    1.1 Define the AWS Cloud and its value proposition
    1.2 Identify aspects of AWS Cloud economics...
    
    Domain 4: Billing and Pricing
    4.1 Compare and contrast the various pricing models for AWS..."""
)

if st.button("2. Generate My Test ✨", type="primary"):
    with st.spinner("Analyzing syllabus and consulting the AI oracle... Please wait."):
        time.sleep(5)  # Simulate AI thinking time
        st.session_state.test_data = json.loads(MOCK_AI_RESPONSE)
        st.session_state.test_generated = True
        st.session_state.user_answers = {} # Reset answers for new test
        st.success("Your personalized test is ready!")

# Display the test if it has been generated
if st.session_state.test_generated:
    st.write("---")
    st.subheader("Your Personalized Mock Exam")

    for i, q in enumerate(st.session_state.test_data):
        st.markdown(f"**Question {i+1}:** {q['question']}")
        st.markdown(f"*(Topic: {q['syllabus_topic']})*")
        options = list(q['options'].values())
        st.session_state.user_answers[i] = st.radio(
            "Choose your answer:", options, key=f"q_{i}"
        )
        st.write("")

    if st.button("3. Submit & See Results 🚀"):
        # Calculate results
        score = 0
        topic_performance = {}
        for i, q in enumerate(st.session_state.test_data):
            topic = q['syllabus_topic']
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0}
            
            topic_performance[topic]['total'] += 1
            
            selected_option_text = st.session_state.user_answers[i]
            correct_option_key = q['correct_answer']
            correct_option_text = q['options'][correct_option_key]

            if selected_option_text == correct_option_text:
                score += 1
                topic_performance[topic]['correct'] += 1
        
        # Display Results Dashboard
        st.write("---")
        st.subheader("📈 Your Results Dashboard")

        overall_score = (score / len(st.session_state.test_data)) * 100
        st.metric("Overall Score", f"{overall_score:.1f}%", f"{score} out of {len(st.session_state.test_data)} correct")
        
        st.write("**This is the 'Aha!' Moment!**")
        st.markdown("Here's your performance breakdown by syllabus topic. Now you know exactly where to focus your studies.")

        # Prepare data for the bar chart
        chart_data = {
            'Topic': [],
            'Percentage': [],
            'Performance': []
        }
        for topic, perf in topic_performance.items():
            percentage = (perf['correct'] / perf['total']) * 100 if perf['total'] > 0 else 0
            chart_data['Topic'].append(topic)
            chart_data['Percentage'].append(percentage)
            chart_data['Performance'].append(f"{perf['correct']}/{perf['total']}")

        df = pd.DataFrame(chart_data).set_index('Topic')

        # Highlight the weak area
        st.markdown("### Performance by Topic")
        st.bar_chart(df['Percentage'])
        st.table(df)

        st.warning("🎯 **Actionable Insight:** Your lowest score is in **Billing and Pricing**. Focus your next study session there!")
