# Semiconductor Logistics AI-Upskiller 🚛⚡

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Groq](https://img.shields.io/badge/LLM-Groq_Llama3-orange)

An intelligent, AI-powered educational platform designed to upskill logistics professionals in the semiconductor industry. This tool leverages **RAG (Retrieval-Augmented Generation)** to provide role-specific guidance, personalized learning roadmaps, and dynamic skill assessments.

---

## 🌟 Key Features

### 1. 🤖 Career & Competency Chat
*   **Context-Aware AI:** Ask questions about semiconductor logistics standards, competencies, and training. The AI answers using a curated knowledge base.
*   **Role-Specific Context:** Tailors answers based on your selected role (e.g., Logistics Manager vs. Warehouse Supervisor).

### 2. 🌐 Deep Research (New)
*   **Real-Time Intelligence:** A dedicated tab to search the live web for 2024-2025 industry trends using DuckDuckGo.
*   **Quick Presets:** Instant reports on "Market Trends", "Supply Risks", and "AI Tools".

### 3. 🏭 Fab Crisis Simulator (New)
*   **Interactive Role-Play:** A generic text-based simulation where you face industry crises (e.g., machine downtime, logistics bottlenecks).
*   **AI Supervisor:** Receive instant grading and feedback on your decision-making skills.

### 4. 🧠 Smart-Study Flashcards (New)
*   **Spaced Repetition:** Auto-generates flashcards for key industry acronyms and terms.
*   **Interactive UI:** Flip cards to reveal definitions and cycle through decks.

### 5. 🕸️ Interactive Skill-Web (New)
*   **Visual Knowledge Graph:** Generates a dynamic Mermaid.js spider-map of competencies.
*   **Hierarchical Discovery:** Explore skills from high-level categories down to specific tools.

### 6. 📊 Competency Radar (New)
*   **Dynamic Sidebar:** A real-time spider chart in the sidebar that visualizes your current skill mix vs. target role expectations.

### 7. 🗺️ Personalized Learning Path
*   **Custom Roadmaps:** Generates a structured **10-module curriculum** based on your specific role and current AI literacy level.
*   **Visual Roadmap:** Displays a dynamic flow chart of your learning journey.
*   **Curated Resources:** Provides direct links to high-quality courses and certifications.

### 8. 📝 Skill Assessment Quiz
*   **AI-Focused Questions:** Generates 5 unique multiple-choice questions specifically testing **AI applications and digital transformation skills** relevant to your role.
*   **Instant Feedback:** Scores your performance and provides detailed explanations.

---

## 🛠️ Technology Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **Orchestration:** [LangChain](https://www.langchain.com/)
*   **Vector Database:** [ChromaDB](https://www.trychroma.com/)
*   **LLM:** [Groq](https://groq.com/) (Llama 3.1 8b-Instant)
*   **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)


---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+ installed.
*   A [Groq API Key](https://console.groq.com/keys).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd "Supply Chain EL"
    ```

2.  **Install dependencies:**
    Create a `requirements.txt` or install directly:
    ```bash
    pip install streamlit streamlit-mermaid langchain-chroma langchain-huggingface langchain-groq langchain-community
    ```

### Configuration

1.  **Set up Secrets:**
    Create a `secrets.toml` file in a `.streamlit` folder (or use your OS environment variables):
    
    **path:** `.streamlit/secrets.toml`
    ```toml
    GROQ_API_KEY = "your_actual_api_key_here"
    ```

---

## 📖 Usage

### 1. Ingest Knowledge Base
Before running the app, you need to populate the vector database with the provided industry documents.

```bash
python ingest.py
```
*   *This will read files from `Industry Reports`, `Job Descriptions`, and `Training Curricula`, chunk them, and save embeddings to `chroma_db/`.*

### 2. Run the Application
Launch the web interface:

```bash
streamlit run main.py
```
*   *The app will open in your default browser at `http://localhost:8501`.*

### 3. Development Tools
The project includes scripts to validate resources and test connectivity:

*   **Link Validation:**
    ```bash
    python validate_links.py
    ```
    *Checks if the curated learning resource URLs are still active.*


---

## 📂 Project Structure

```text
├── .streamlit/          # Streamlit configuration (secrets)
├── chroma_db/           # Vector database storage (created after ingestion)
├── Industry Reports/    # PDF/Txt Source documents
├── Job Descriptions/    # PDF/Txt Source documents
├── Training Curricula/  # PDF/Txt Source documents
├── engine.py            # Core logic: RAG chain, Prompt templates, LLM setup
├── ingest.py            # Data ingestion script for ChromaDB
├── main.py              # Main Streamlit application UI
├── utils.py             # Helper utility functions
├── validate_links.py    # Script to validate resource URLs
└── README.md            # Project documentation
```

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for specific features or bug fixes.

---

## 📄 License
This project is licensed under the MIT License.
