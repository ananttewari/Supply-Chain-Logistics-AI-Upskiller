import streamlit as st
import streamlit_mermaid as st_mermaid
import plotly.graph_objects as go
from engine import (
    get_rag_response, 
    generate_quiz_questions, 
    search_learning_resources,
    generate_scenario,
    evaluate_scenario,
    generate_flashcards,
    generate_skill_web
)
from utils import get_directories, generate_pdf_report

# Page Config
st.set_page_config(page_title="Semiconductor Logistics AI-Upskiller", layout="wide")

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "scenario_data" not in st.session_state:
    st.session_state.scenario_data = None
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "roadmap_text" not in st.session_state:
    st.session_state.roadmap_text = None

# Sidebar
with st.sidebar:
    st.title("Settings")
    role = st.selectbox("Select Your Role", ["Logistics Manager", "Supply Chain Analyst", "Warehouse Supervisor", "Procurement Specialist"])
    ai_literacy = st.slider("AI Literacy Level", 1, 5, 3)
    
    st.divider()
    
    st.divider()
    
    # NEW: Competency Radar
    st.subheader("Competency Radar")
    
    # Mock data based on role/level for visualization
    categories = ['Data Literacy', 'Logistics Ops', 'AI Strategy', 'Safety', 'Procurement']
    
    # Base skills + variance based on user selection
    base_val = ai_literacy
    if role == "Logistics Manager":
        values = [base_val, base_val+1, base_val, base_val, base_val-1]
    elif role == "Supply Chain Analyst":
        values = [base_val+2, base_val, base_val+1, base_val-1, base_val]
    else:
        values = [base_val, base_val, base_val, base_val, base_val]
        
    # Cap at 5
    values = [min(v, 5) for v in values]
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself'
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 5]
        )),
      showlegend=False,
      margin=dict(l=20, r=20, t=20, b=20),
      height=250
    )
    
    st.plotly_chart(fig, width="stretch")
    
    st.divider()
    
    # NEW: PDF Export
    if st.button("📄 Prepare Career Report"):
        with st.spinner("Compiling Skill-Gap Report..."):
            pdf_bytes = generate_pdf_report(
                role, 
                ai_literacy, 
                st.session_state.quiz_score, 
                st.session_state.get("roadmap_text")
            )
            
            if pdf_bytes:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="Semiconductor_Career_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Could not generate PDF. Is 'fpdf' installed?")
    
    st.info("Adjust settings to personalize your learning path.")

# Main Interface
st.title("Semiconductor Logistics AI-Upskiller")

tab_about, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "ℹ️ About Project",
    "Career Chat", 
    "Learning Path", 
    "Skill Quiz", 
    "Fab Crisis Sim", 
    "Smart-Study", 
    "Skill Web",
    "Deep Research"
])

# Tab 0: About Project (Faculty Presentation)
with tab_about:
    st.header("🎓 Academic Impact Statement")
    st.markdown("### The Semiconductor Logistics AI-Upskiller (2026 Edition)")
    
    st.divider()
    
    # 1. The Problem
    st.subheader("1. The Problem: The “Global Talent Cliff” (2026 Context)")
    st.warning(
        "As of 2026, the semiconductor industry is at a critical inflection point. "
        "While global revenues are on track to surpass $1 trillion by 2030, the sector faces a staggering shortfall of over 1 million skilled professionals. "
        "Traditional training methods are failing to keep pace with the rapid integration of Generative AI and complex geopolitical shifts in the supply chain. "
        "**Our project addresses this crisis by providing an adaptive, role-specific intelligence layer for workforce upskilling.**"
    )
    
    col_tech, col_features = st.columns(2)
    
    with col_tech:
        # 2. Technical Innovation
        st.subheader("2. Technical Innovation: Hybrid-RAG Architecture")
        st.markdown(
            """
            This application implements a **Retrieval-Augmented Generation (RAG)** pipeline designed for domain-specific accuracy.
            
            *   **Knowledge Base:** A curated repository of Tier-1 industry reports (Deloitte, McKinsey, PwC), actual Job Descriptions, and global training curricula.
            *   **Logic Engine:** Powered by **Groq (Llama 3.1)** for near-zero latency inference, ensuring a responsive and conversational learning experience.
            *   **Visual Intelligence:** Dynamic generation of **Mermaid.js** mind maps and **Plotly** competency charts to transform raw textual data into intuitive visual roadmaps.
            """
        )

    with col_features:
        # 3. Featured Learning Ecosystem
        st.subheader("3. Featured Learning Ecosystem")
        st.markdown("We have moved beyond static Q&A to create an interactive ecosystem:")
        st.markdown(
            """
            *   🏭 **The Fab Crisis Simulator:** Encourages *Active Learning* through text-based role-play of real-world logistics disruptions.
            *   📊 **Competency Radar:** Provides *Skill-Gap Analytics* to visualize a user's transformation from traditional to digital roles.
            *   🌐 **Fab News-Flash:** Integrates *Real-Time Web Search* for 2026 industry updates.
            *   🧠 **Smart-Study Flashcards:** Leverages *Spaced Repetition* for technical acronym retention.
            *   🕸️ **Interactive Skill-Web:** Provides a NotebookLM-style visual discovery of complex semiconductor hierarchies.
            """
        )
    
    st.divider()
    
    # 4. Meta-Project Disclosure
    st.subheader("4. Meta-Project Disclosure (Collaborative Workflow)")
    st.info(
        """
        In the spirit of academic transparency, this project was developed using a **Hybrid Human-AI Collaborative Workflow**:
        
        *   **AI Architecture (Member 1):** Vector DB design, semantic retrieval tuning, and prompt engineering for role-play simulations.
        *   **Full-Stack UI (Member 2):** Streamlit orchestration, session state management, and the integration of dynamic visual libraries.
        *   **Industry Research:** Data curation focused on the CHIPS Act era and the 'Sovereign Tech Stack' trends of 2025/2026.
        """
    )
    
    # Final Soundbite
    st.success(
        "💡 **Faculty Insight:** Our platform is not just a chatbot; it is a **Strategic Talent Management Tool** "
        "designed to mitigate the risks of undocumented 'tacit knowledge' loss as the veteran semiconductor workforce reaches retirement age in 2026."
    )
    
    st.divider()

# Tab 1: Career Chat
with tab1:
    st.header("Career & Competency Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about competencies, standards, or training..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream response
            # Use "chat" mode for general Q&A
            raw_stream = get_rag_response(
                prompt, 
                role=role, 
                ai_literacy_level=ai_literacy, 
                generation_mode="chat"
            )
            for chunk in raw_stream:
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            
            # Final render to remove cursor
            
            # Check for Mermaid
            import re
            mermaid_match = re.search(r"```mermaid\n(.*?)\n```", full_response, re.DOTALL)
            
            if mermaid_match:
                mermaid_code = mermaid_match.group(1)
                # Remove the mermaid block from the text display so it doesn't show raw code
                clean_text = full_response.replace(mermaid_match.group(0), "")
                response_placeholder.markdown(clean_text)
                with st.chat_message("assistant"):
                    st_mermaid.st_mermaid(mermaid_code, height="500px")
            else:
                response_placeholder.markdown(full_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# Tab 2: Learning Path
with tab2:
    st.header("Personalized Learning Path")
    st.write(f"Generated for: **{role}** (Level {ai_literacy})")
    
    if st.button("Generate Roadmap"):
        with st.spinner("Generating roadmap..."):
            # Prompt specifically for a roadmap
            roadmap_query = f"Create a comprehensive learning roadmap for a {role} with AI literacy level {ai_literacy} in the semiconductor industry. Include a mermaid chart."
            
            response_stream = get_rag_response(
                roadmap_query, 
                role, 
                ai_literacy, 
                generation_mode="roadmap"
            )
            full_text = ""
            placeholder = st.empty()
            
            for chunk in response_stream:
                full_text += chunk
                placeholder.markdown(full_text + "▌")
            
            # Save for PDF export
            st.session_state.roadmap_text = full_text
            
            # Parse and cleanup
            import re
            mermaid_match = re.search(r"```mermaid\n(.*?)\n```", full_text, re.DOTALL)
            
            if mermaid_match:
                mermaid_code = mermaid_match.group(1)
                
                # SANITIZE: Remove parentheses from node labels to prevent syntax errors
                # Replace patterns like: id["Text (with parens)"] -> id["Text - with parens"]
                # Also: id("Text (with parens)") -> id["Text - with parens"]
                def sanitize_mermaid(code):
                    # 1. Handle parentheses inside quoted labels
                    def replace_parens(match):
                        label = match.group(1)
                        # Replace ( and ) with - 
                        label = label.replace('(', ' - ').replace(')', '')
                        # Also replace other problematic chars like : if not needed
                        label = label.replace(":", " -")
                        return f'["{label}"]'
                    
                    code = re.sub(r'\["([^"]*)"\]', replace_parens, code)
                    code = re.sub(r'\("([^"]*)"\)', replace_parens, code)
                    
                    # 2. Fix unquoted labels with parentheses e.g. id(Label Text)
                    # This is harder but common. We can try to just remove all () if they are not part of node def
                    # or just brutal search replace.
                    # A safer way: ensure all nodes are id["Label"] format
                    
                    # 3. Ensure graph TD logic is preserved but cleanup syntax
                    if "graph TD" not in code:
                        code = "graph TD\n" + code
                        
                    return code
                
                mermaid_code = sanitize_mermaid(mermaid_code)
                
                clean_text = full_text.replace(mermaid_match.group(0), "")
                placeholder.markdown(clean_text)
                st.subheader("Visual Roadmap")
                st_mermaid.st_mermaid(mermaid_code, height="800px")
            else:
                placeholder.markdown(full_text)

            # Recommended Resources
            st.divider()
            st.subheader("📚 Recommended Learning Resources")
            with st.spinner("Loading curated resources..."):
                web_results = search_learning_resources(role)
                st.info(web_results)

# Tab 3: Skill Quiz
with tab3:
    st.header("Skill Assessment Quiz")
    
    if st.button("Start New Quiz"):
        with st.spinner("Generating questions..."):
            questions = generate_quiz_questions(role, ai_literacy)
            if questions:
                st.session_state.quiz_data = questions
                st.session_state.quiz_score = 0
                st.session_state.user_answers = [None] * len(questions)
                st.rerun()
            else:
                st.error("Failed to generate quiz. Please try again.")

    if st.session_state.quiz_data:
        questions = st.session_state.quiz_data
        
        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.subheader(f"Q{i+1}: {q['question']}")
                # Keys for radio widgets need to be unique and consistent
                st.session_state.user_answers[i] = st.radio(
                    "Choose an answer:", 
                    q['options'], 
                    key=f"q_{i}",
                    index=None
                )
                st.divider()
            
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = 0
                for i, q in enumerate(questions):
                    selected = st.session_state.user_answers[i]
                    if selected:
                        selected_index = q['options'].index(selected)
                        if selected_index == q['correct_answer']:
                            score += 1
                
                st.session_state.quiz_score = score
                st.success(f"You scored {score}/{len(questions)}!")
                
                # Quiz Review
                st.divider()
                st.subheader("📝 Answer Review")
                for i, q in enumerate(questions):
                    user_ans = st.session_state.user_answers[i]
                    correct_ans_txt = q['options'][q['correct_answer']]
                    
                    with st.expander(f"Q{i+1}: {q['question']}", expanded=True):
                        if user_ans == correct_ans_txt:
                            st.markdown(f"✅ **Your Answer:** {user_ans} (Correct)")
                        else:
                            st.markdown(f"❌ **Your Answer:** {user_ans}")
                            st.markdown(f"✅ **Correct Answer:** {correct_ans_txt}")

                if score >= 4:
                    st.balloons()

# NEW: Tab 4 - Fab Crisis Simulator
with tab4:
    st.header("🏭 The Fab Crisis Simulator")
    st.markdown("Test your knowledge in a risk-free text-based simulation.")
    
    if st.button("Start New Scenario"):
        with st.spinner("Initializing Fab Crisis..."):
            st.session_state.scenario_data = generate_scenario(role, ai_literacy)
            
    if st.session_state.scenario_data:
        data = st.session_state.scenario_data
        st.warning(f"🚨 ALERT: {data.get('scenario', 'Unknown Error')}")
        st.markdown(f"**Your Challenge:** {data.get('question', '')}")
        
        user_action = st.text_area("How do you respond?", placeholder="I would use Predictive Maintenance tools because...")
        
        if st.button("Submit Action Plan"):
            if user_action:
                with st.spinner("Supervisor evaluating..."):
                    feedback = evaluate_scenario(data, user_action)
                    st.success("Analysis Complete")
                    st.markdown(f"### 🤖 Supervisor Feedback:\n{feedback}")
            else:
                st.error("Please enter a response.")

# NEW: Tab 5 - Smart-Study Flashcards
with tab5:
    st.header("🧠 Smart-Study Flashcards")
    
    if st.button("Generate Deck"):
        with st.spinner("Extracting key terms..."):
            st.session_state.flashcards = generate_flashcards(topic="Semiconductor Logistics")
            
    if st.session_state.flashcards:
        cards = st.session_state.flashcards
        
        # Simple Carousel
        if "card_idx" not in st.session_state:
            st.session_state.card_idx = 0
            
        current_card = cards[st.session_state.card_idx]
        
        # UI for Card
        st.markdown(f"### Card {st.session_state.card_idx + 1}/{len(cards)}")
        
        # Flip Mechanism
        with st.chat_message("assistant"):
            st.markdown(f"# {current_card['term']}")
            with st.expander("Reveal Definition"):
                st.markdown(f"**{current_card['definition']}**")
        
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Previous"):
                st.session_state.card_idx = max(0, st.session_state.card_idx - 1)
                st.rerun()
        with col_next:
            if st.button("Next ➡️"):
                st.session_state.card_idx = min(len(cards) - 1, st.session_state.card_idx + 1)
                st.rerun()
    elif st.session_state.flashcards is not None:
        st.error("Unable to generate flashcards at this time. Please try again.")

# NEW: Tab 6 - Skill Web
with tab6:
    st.header("🕸️ The Interactive Skill-Web")
    st.markdown("Visual knowledge discovery.")
    
    if st.button("Generate Skill Web"):
        with st.spinner("Weaving the web..."):
            mermaid_graph = generate_skill_web(role)
            # Ensure safe Syntax
            if "graph TD" not in mermaid_graph and "graph LR" not in mermaid_graph:
                mermaid_graph = "graph TD\n" + mermaid_graph
            
            st.session_state.skill_web_code = mermaid_graph
            
    if "skill_web_code" in st.session_state:
        if st.session_state.skill_web_code:
            # Increased height and added overflow hint
            st_mermaid.st_mermaid(st.session_state.skill_web_code, height="800px", key="skill_web_mermaid")
            st.info("Mapping complete. Use the core nodes above to guide your study in the Learning Path tab.")
        else:
            st.error("Failed to generate Skill Web. Please try again.")

# NEW: Tab 7 - Deep Research
with tab7:
    st.header("🌐 Deep Research: Real-Time Intelligence")
    st.markdown("Search the live web for the latest 2024-2025 industry trends.")
    
    # Select a Topic
    st.write("Select a topic to generate a real-time intelligence report:")
    
    col1, col2, col3 = st.columns(3)
    preset_query = None
    
    if col1.button("🔥 Market Trends"):
        preset_query = "Latest global semiconductor market trends and forecasts 2025"
    if col2.button("⚠️ Supply Risks"):
        preset_query = "Current semiconductor supply chain disruptions and risks 2025"
    if col3.button("🤖 AI Tools"):
        preset_query = f"Top AI tools and software for {role} in 2025"

    if preset_query:
        # Determine actual query
        final_query = preset_query
        
        with st.spinner(f"Searching web for '{final_query}'..."):
            # Use existing RAG pipeline but with 'search' mode
            stream = get_rag_response(
                final_query,
                role=role, 
                ai_literacy_level=ai_literacy, 
                generation_mode="search"
            )
            
            st.divider()
            output_container = st.empty()
            full_text = ""
            for chunk in stream:
                full_text += chunk
                output_container.markdown(full_text + "▌")
            
            output_container.markdown(full_text)

