import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# Constants
CHROMA_PATH = "chroma_db"

def get_chroma_db():
    """
    Initialize and return the ChromaDB client.
    Cached to prevent reloading on every run.
    """
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )
    return db

def get_llm():
    """
    Initialize the Groq LLM.
    """
    api_key = st.secrets["GROQ_API_KEY"]
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama-3.1-8b-instant", 
        groq_api_key=api_key
    )
    return llm

def get_rag_response(query, role=None, ai_literacy_level=None, generation_mode="chat"):
    """
    Perform RAG to get response.
    generation_mode: "chat" (default) or "roadmap"
    """
    db = get_chroma_db()
    llm = get_llm()
    
    # 1. Retrieve specific docs
    retriever = db.as_retriever(search_kwargs={"k": 5})
    
    # 2. Hybrid Reasoning / Prompt Engineering
    template = """
    You are the "Semiconductor Logistics AI-Upskiller", an expert mentor.
    
    Context from Knowledge Base:
    {context}
    
    User Role: {role}
    AI Literacy Level: {ai_literacy_level}/5
    Current Mode: {generation_mode}
    
    User Query: {question}
    
    Instructions:
    1. Search context for competencies/standards.
    
    2. MODE-SPECIFIC RULES (CRITICAL):
    
       IF Current Mode is "chat":
       - **DO NOT** generate a full learning path, curriculum, or 10-module table.
       - **DO NOT** generate Mermaid charts.
       - Answer the user's specific question concisely.
       - If they ask for a full roadmap/plan, provide a brief summary of key topics (bullet points) and **explicitly tell them to use the 'Personalized Roadmap' tab** for the full visual schedule.
       
       IF Current Mode is "roadmap":
       - **FORCE FORMATTING**: Output a valid Markdown table for the Training Path.
       - **IGNORE** original module numbers. RENUMBER from Module 1 to Module 10.
       - **STRICT LIMIT**: Exact 10 distinct modules.
       - **INCLUDE** a Mermaid chart (using graph TD, no parens in labels).

       IF Current Mode is "search":
       - Incorporate the provided web search results into your answer.
       - Cite the web sources where appropriate.
       - Focus on recent trends (2024-2025).
       
    3. General QA Rules (for "chat" mode):
    
       - Answer directly and professionally.
       - Use bullet points for list items.
       - Cite internal knowledge if context is missing.
    
    Response:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        # Return only the content, no usage of metadata/source filenames
        return "\n\n".join([d.page_content for d in docs])

    # NEW: Web Search Integration
    def get_context(query_text):
        # query_text is the raw user query string passed to the chain
        
        # Base RAG context
        rag_docs = retriever.invoke(query_text)
        rag_context = format_docs(rag_docs)
        
        # Check for web search flag (captured from outer scope)
        if generation_mode == "search":
            try:
                with DDGS() as ddgs:
                    # Search specifically for recent semiconductor logistics news
                    search_query = f"latest semiconductor logistics news 2024 2025 {query_text}"
                    results = list(ddgs.text(search_query, max_results=3))
                    
                    web_context = "\n\n=== WEB SEARCH RESULTS (REAL-TIME) ===\n"
                    for r in results:
                        web_context += f"Source: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}\n\n"
                    
                    return rag_context + web_context
            except Exception as e:
                return rag_context + f"\n[System: Web search failed: {str(e)}]"
        
        return rag_context

    chain = (
        {
         "context": get_context, # Dynamic context fetching
         "question": RunnablePassthrough(), 
         "role": lambda x: role, 
         "ai_literacy_level": lambda x: ai_literacy_level,
         "generation_mode": lambda x: generation_mode
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.stream(query)

import json
import re

def generate_quiz_questions(role, level):
    """
    Generate 5 multiple-choice questions to test the AI literacy and Logistics knowledge for a {role} at level {level}/10.
    Returns a list of dictionaries.
    """
    llm = get_llm()
    prompt = f"""
    Generate 5 multiple-choice questions specifically about **AI applications, tools, and digital transformation skills** for a {role} at AI literacy level {level}/5.
    
    The questions should NOT be about general logistics. They MUST test how AI is applied in that role (e.g., "Which AI algorithm helps in route optimization?", "How does Computer Vision aid quality control?").

    Return the result STRICTLY as a JSON array of objects. 
    Each object must have: 
    - "question" (string)
    - "options" (list of 4 strings)
    - "correct_answer" (integer index 0-3)
    
    Do not include any markdown formatting like ```json or ```. Just the raw JSON array.
    """
    response = llm.invoke(prompt)
    content = response.content
    
    # Clean up common markdown wrapping
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    content = content.strip()
    
    try:
        questions = json.loads(content)
        return questions
    except json.JSONDecodeError:
        # Fallback or empty
        return []

# NEW: Scenario Generation
def generate_scenario(role, level):
    """
    Generates a 2-turn role-play scenario.
    Returns a dictionary with 'scenario_text' and 'options' (optional) or just text.
    """
    llm = get_llm()
    prompt = f"""
    Create a realistic "Crisis Scenario" for a {role} in a semiconductor fab supply chain.
    The user has AI Literacy Level {level}/5.
    
    Output strictly a JSON object with:
    1. "scenario": A clear paragraph describing the emergency (e.g., machine down, logistics delay).
    2. "question": A challenging question asking the user what AI tool or strategy they would use.
    
    Do not include markdown code blocks.
    """
    response = llm.invoke(prompt)
    content = response.content
    
    # Robust JSON extraction
    try:
        # Find first { and last }
        json_match = re.search(r'(\{.*\})', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        return json.loads(content)
    except:
        return {"scenario": "System Error: Could not generate scenario.", "question": "Please try again."}

def evaluate_scenario(scenario_data, user_response):
    """
    Evaluates the user's text response to the scenario.
    """
    llm = get_llm()
    prompt = f"""
    Scenario: {scenario_data['scenario']}
    Question: {scenario_data['question']}
    User Response: {user_response}
    
    Act as a senior supervisor. specific Instructions:
    1. Grade the response (Pass/Fail).
    2. Explain WHY based on semiconductor industry standards (JIT, predictive maintenance, etc.).
    3. Keep it brief (3-4 sentences).
    """
    response = llm.invoke(prompt)
    return response.content

# NEW: Flashcards
def generate_flashcards(topic="Semiconductor Logistics"):
    """
    Generates 5 key terms and definitions.
    """
    llm = get_llm()
    prompt = f"""
    Extract 5 advanced acronyms or key terms related to {topic} and AI.
    Return strictly a JSON array of objects with keys: "term", "definition".
    No markdown formatting.
    """
    response = llm.invoke(prompt)
    content = response.content
    
    try:
        # Robust Array extraction
        json_match = re.search(r'(\[.*\])', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        # Fallback cleanup
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except:
        return []

# from langchain_community.tools import DuckDuckGoSearchResults # Removed to avoid wrapper issues
from duckduckgo_search import DDGS

# ... (imports remain the same in the file content, just ensuring I don't break them)

def search_learning_resources(role, topic="Semiconductor Logistics"):
    """
    Return curated learning resources tailored to each role.
    """
    
    # Curated resources by role
    RESOURCES = {
        "Logistics Manager": [
            ("Coursera: Supply Chain Management", "https://www.coursera.org/search?query=supply%20chain%20management"),
            ("edX: MIT Supply Chain Courses", "https://www.edx.org/school/mitx"),
            ("ASCM: Certification Programs", "https://www.ascm.org/learning-development/"),
            ("IEEE: Semiconductor Resources", "https://www.ieee.org/"),
            ("LinkedIn Learning: Logistics", "https://www.linkedin.com/learning/topics/logistics-and-supply-chain-management"),
        ],
        "Supply Chain Analyst": [
            ("Coursera: Supply Chain Analytics", "https://www.coursera.org/search?query=supply%20chain%20analytics"),
            ("MIT OpenCourseWare", "https://ocw.mit.edu/search/?q=supply+chain"),
            ("Gartner: Supply Chain", "https://www.gartner.com/en/supply-chain"),
            ("Udemy: Data Analytics", "https://www.udemy.com/courses/business/Data-and-Analytics/"),
            ("ASCM: CPIM & Certifications", "https://www.ascm.org/learning-development/"),
        ],
        "Warehouse Supervisor": [
            ("LinkedIn Learning: Warehouse Mgmt", "https://www.linkedin.com/learning/topics/warehouse-management"),
            ("Coursera: Warehouse Operations", "https://www.coursera.org/search?query=warehouse%20management"),
            ("OSHA: Warehousing Topic", "https://www.osha.gov/warehousing"),
            ("WERC: Warehouse Council", "https://werc.org/"),
            ("ASCM: Inventory Learning", "https://www.ascm.org/learning-development/"),
        ],
        "Procurement Specialist": [
            ("Coursera: Procurement", "https://www.coursera.org/search?query=procurement"),
            ("CIPS: Procurement Qualifications", "https://www.cips.org/"),
            ("SIA: Semiconductor Industry", "https://www.semiconductors.org/"),
            ("LinkedIn Learning: Sourcing", "https://www.linkedin.com/learning/topics/procurement"),
            ("Harvard Online: Business", "https://online.hbs.edu/subjects/business-management/"),
        ]
    }
    
    # Get resources for role, default to Logistics Manager if not found
    resources = RESOURCES.get(role, RESOURCES["Logistics Manager"])
    items = [f"- [{title}]({link})" for title, link in resources]
    return "\n".join(items)

def generate_skill_web(role):
    """
    Generates a Mermaid.js graph string acting as a skill map.
    """
    llm = get_llm()
    prompt = f"""
    Create a "Skill Web" for a {role} in Semiconductor Logistics using Mermaid.js syntax.
    
    Requirements:
    - Structure: Start with central node "{role}" at top.
    - Hierarchy: Branch into exactly 3 core categories (e.g., "Technical", "Management", "Compliance").
    - Depth: Each category should have 2-3 sub-nodes.
    - Layout: Use "graph TD" (Top-Down).
    - Syntax Rules (CRITICAL):
      - Use format: NodeID["Node Label"]
      - Example: A1["Logistics Manager"] --> B1["Data Analysis"]
      - NEVER output just the ID like A1 --> B1.
    - Labels: Keep labels short (1-2 words).
    - IDs: Use simple alphanumerics (A, B, C...).
    """
    response = llm.invoke(prompt)
    content = response.content
    
    # Extract Mermaid code block if present
    mermaid_match = re.search(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
    if mermaid_match:
        return mermaid_match.group(1).strip()
    
    # Fallback: Strip all fences
    content = content.replace('```mermaid', '').replace('```', '').strip()
    return content
