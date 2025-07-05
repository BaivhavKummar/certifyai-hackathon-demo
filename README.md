# CertifyAI 🤖

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)![Status: Hackathon Prototype](https://img.shields.io/badge/status-prototype-success.svg)![Tech: AWS](https://img.shields.io/badge/tech-AWS-orange.svg)![Tech: Docker](https://img.shields.io/badge/tech-Docker-blue.svg)

**CertifyAI is a cloud-native, AI-powered learning platform that creates personalized practice exams on-the-fly from any official certification syllabus.**

---

## ✨ Live Demo

For a stable and interactive demonstration of the core user journey, please visit our live prototype:

**[🚀 View the Live Interactive Prototype 🚀](https://certifyai-hackathon-demo-bqswk3z9r4xnyacpmcqr8f.streamlit.app/)**

*(This prototype showcases the core user experience using Streamlit for a fast and reliable presentation.)*

---

## 🎯 The Problem

Preparing for professional certifications is inefficient and expensive. Students and professionals are stuck in a cycle of costly official practice tests and generic, low-quality free quizzes that don't align with the official syllabus. This creates a significant barrier to career advancement and wastes precious study time.

## 💡 Our Solution

CertifyAI solves this by providing a hyper-personalized and scalable learning ecosystem. Users can choose from a curated library of popular certifications or paste **any syllabus** to have our AI generate a relevant, high-quality mock exam instantly.

More than just a test generator, our platform provides an **actionable feedback dashboard** that pinpoints a user's weakest topics, enabling truly smart and focused studying.

---

## 👤 User Story: Sarah's Journey

> A driven IT professional aiming for her AWS certification was stuck, wasting time and money on generic practice tests. She discovered CertifyAI, pasted the official syllabus, and instantly received a relevant exam. The dashboard revealed her true weakness was in **"Billing and Pricing."** She studied smarter, not harder, saved money, and passed her exam with confidence.

---

## 🌟 Key Features (Built During This Hackathon)

*   ✨ **Dual Mode Generation:** Choose from a pre-loaded **Certification Library** or upload a **Custom Syllabus** for instant adaptation.
*   🧠 **Context-Aware AI Core:** Our LLM core maintains context, allowing for interactive test refinement and follow-up questions.
*   🤖 **Real-Time Chatbot Assistant:** An integrated bot (powered by AWS Lambda) to help users or provide the status of their test generation.
*   ⚡ **Live Progress Updates:** Using WebSockets, the UI provides live feedback to the user as their test is being generated.
*   📊 **Smart Feedback Dashboard:** Our core "wow" factor. Moves beyond a simple score to provide a visual, actionable study plan that highlights user weaknesses.
*   ☁️ **Cloud-Native Architecture:** Fully built and deployed on AWS infrastructure for scalability and reliability.

---

## 🛠️ System Architecture

We designed CertifyAI as a robust, distributed system ready for scale.

```
+----------------+      +---------------------------+      +------------------+
|   User         |----->|   React Frontend (Next.js)|----->|   Flask Backend  |
| (Web Browser)  |      |   (Hosted on Vercel/S3)   |      | (Docker on AWS ECR)|
+----------------+      +---------------------------+      +--------+---------+
                                                                     |
         +-----------------------------------------------------------+----------------------------------------------+
         |                                                           |                                              |
+--------v---------+      +------------------------+      +---------v----------+      +------------------------------+
| AWS RDS          |      | Self-Hosted MongoDB    |      | Google Gemini      |      | AWS Lambda + WebSockets      |
| (PostgreSQL)     |      |   Cluster              |      |   API              |      |   (API Gateway)              |
| - User Data      |      | - Syllabi              |      | - Question Gen.    |      | - Chatbot                    |
| - Test History   |      | - Generated Questions  |      | - Context Maint.   |      | - Real-time Status           |
+------------------+      +------------------------+      +--------------------+      +------------------------------+

```

---

## 💻 Tech Stack

| Category                  | Technology                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Frontend**              | `React`, `Next.js`, `TailwindCSS`                                                                           |
| **Backend**               | `Python`, `Flask`                                                                                           |
| **AI Core**               | `Google Gemini API`                                                                                         |
| **Databases**             | `AWS RDS (PostgreSQL)` for structured data, `MongoDB` (self-hosted cluster) for unstructured data.            |
| **Infrastructure & DevOps** | `Docker`, `AWS ECR`, `AWS ECS`, `AWS Lambda`, `AWS API Gateway`, `WebSockets`                                 |

---

## 🚀 Getting Started (Full Application)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   AWS Account & AWS CLI configured
*   Docker & Docker Compose
*   Node.js (v18+) & npm
*   Python (v3.10+) & pip

### Configuration

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/CertifyAI.git
    cd CertifyAI
    ```
2.  **Set up Environment Variables:**
    Create a `.env` file in the `backend` directory. This file will store all your secret keys.
    ```env
    # Database URLs
    DATABASE_URL="postgresql://user:password@host:port/database"
    MONGO_URI="mongodb://user:password@host:port/database"

    # AWS Credentials
    AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY"
    AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_KEY"
    AWS_REGION="your-aws-region"

    # AI API Key
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

### Running with Docker

The easiest way to run the entire stack (backend, frontend, databases) is with Docker Compose.

```bash
# From the root directory
docker-compose up --build
```
This will build the necessary images and start all the services defined in `docker-compose.yml`.

---

## 🌐 Running the Streamlit Prototype

For a quick and reliable demo without setting up the full cloud stack, you can run our Streamlit prototype via Google Colab.

1.  **Upload Code:** Ensure `app.py` and `requirements.txt` from the `/prototype` folder are in a public GitHub repo.
2.  **Open Colab:** Launch a [Google Colab Notebook](https://colab.research.google.com/drive/1-DnmLA7K8MBjtXV7P0gTH7jiavNLmPvG#scrollTo=pjswran3sjqs).
3.  **Run the Setup Script:** Paste and run the setup code from our previous conversations to install libraries, clone the repo, and launch the app with `ngrok`.

---

## 🔮 Future Scope

*   **Gamification:** Introduce leaderboards, achievements, and study streaks to increase engagement.
*   **Enterprise Tier (B2B):** A subscription model for companies to create internal training modules and track employee certification progress.
*   **AI-Generated Study Guides:** Move beyond Q&A to have the AI generate summary notes and flashcards based on a user's identified weak areas.
