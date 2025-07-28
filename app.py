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

# --- Hardcoded Mock AI Response ---
# No changes to this section
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
# Load the full question bank once
FULL_QUESTION_BANK = json.loads(MOCK_AI_RESPONSE)
ALL_TOPICS = sorted(list(set(q['syllabus_topic'] for q in FULL_QUESTION_BANK)))


# --- App UI and Logic ---

st.title("🤖 CertifyAI")
st.subheader("Generate instant practice exams from any syllabus.")

# Initialize session state
if 'test_generated' not in st.session_state:
    st.session_state.test_generated = False
if 'test_data' not in st.session_state:
    st.session_state.test_data = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

st.write("---")
st.write("*Follow Sarah's Journey:*")

# --- [NEW] Test Configuration Section ---
with st.container(border=True):
    st.subheader("1. Configure Your Test")
    col1, col2 = st.columns(2)

    with col1:
        # Slider for number of questions
        num_questions = st.slider(
            "Number of Questions:",
            min_value=1,
            max_value=len(FULL_QUESTION_BANK),
            value=4, # Default value
            step=1
        )

    with col2:
        # Multi-select for topics
        selected_topics = st.multiselect(
            "Filter by Topics (optional):",
            options=ALL_TOPICS,
            default=ALL_TOPICS # Default to all topics
        )

# User Input for syllabus
st.subheader("2. Provide Syllabus")
syllabus_text = st.text_area(
    "Paste Syllabus Here",
    height=150,
    placeholder="""Domain 1: Cloud Concepts..."""
)

if st.button("3. Generate My Test ✨", type="primary"):
    with st.spinner("Analyzing syllabus and consulting the AI oracle... Please wait."):
        time.sleep(2)

        # --- [MODIFIED] Logic to filter questions based on configuration ---
        # First, filter by selected topics
        filtered_questions = [
            q for q in FULL_QUESTION_BANK if q['syllabus_topic'] in selected_topics
        ]
        
        # Then, limit by the number of questions requested
        # Ensure we don't request more questions than are available
        final_num_questions = min(num_questions, len(filtered_questions))
        final_questions = filtered_questions[:final_num_questions]
        
        st.session_state.test_data = final_questions
        # --- End of modification ---

        st.session_state.test_generated = True
        st.session_state.user_answers = {} # Reset answers
        
        if not final_questions:
             st.error("No questions found for the selected topics. Please broaden your topic selection.")
        else:
            st.success("Your personalized test is ready!")


# --- Display the test (No changes to this section below) ---
if st.session_state.test_generated and st.session_state.test_data:
    st.write("---")
    st.subheader("Your Personalized Mock Exam")

    for i, q in enumerate(st.session_state.test_data):
        st.markdown(f"*Question {i+1}:* {q['question']}")
        st.markdown(f"(Topic: {q['syllabus_topic']})")
        options = list(q['options'].values())
        st.session_state.user_answers[i] = st.radio(
            "Choose your answer:", options, key=f"q_{i}"
        )
        st.write("")

    if st.button("4. Submit & See Results 🚀"):
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

        overall_score = (score / len(st.session_state.test_data)) * 100 if len(st.session_state.test_data) > 0 else 0
        st.metric("Overall Score", f"{overall_score:.1f}%", f"{score} out of {len(st.session_state.test_data)} correct")

        st.write("*This is the 'Aha!' Moment!*")
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

        if chart_data['Topic']:
            df = pd.DataFrame(chart_data).set_index('Topic')
            st.markdown("### Performance by Topic")
            st.bar_chart(df['Percentage'])
            st.table(df)

            # Find and highlight the weak area
            min_percentage = df['Percentage'].min()
            weakest_topic = df['Percentage'].idxmin()
            if min_percentage < 100:
                 st.warning(f"🎯 *Actionable Insight:* Your lowest score is in *{weakest_topic}*. Focus your next study session there!")
