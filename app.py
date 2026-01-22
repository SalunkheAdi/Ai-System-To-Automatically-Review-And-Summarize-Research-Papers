import gradio as gr
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
from src.graph.graph import app_graph


def run_research(topic: str, existing_files=None, max_results=3, progress=gr.Progress()):
    """
    Runs the LangGraph workflow for the given topic and/or selected files.
    """
    if not topic.strip() and not existing_files:
        return "Please enter a topic OR select PDF files."
        
    progress(0, desc="Starting Research...")
    
    # Process files
    local_file_paths = []
    
    # 2. Existing local files (Strings)
    if existing_files:
        # these are relative paths or filenames from the checkbox, make sure we have absolute or correct relative paths
        local_file_paths.extend([os.path.abspath(f) for f in existing_files])
    
    initial_state = {
        "topic": topic,
        "local_files": local_file_paths,
        "revision_count": 0,
        "max_results": max_results
    }
    
    # Run the graph
    try:
        log_buffer = "--- STARTING WORKFLOW ---\n"
        if topic: log_buffer += f"Topic: {topic}\n"
        if local_file_paths: log_buffer += f"Files: {len(local_file_paths)}\n"
        
        yield gr.update(value=log_buffer), gr.update(visible=True) # Initial yield

        progress(0.1, desc="Searching & Extracting Papers...")
        
        # Use stream to show progress
        current_state = initial_state
        for output in app_graph.stream(initial_state):
            for key, value in output.items():
                msg = f"Finished node: {key}"
                print(msg)
                log_buffer += f"{msg}\n"
                
                if key == "search":
                    progress(0.2, desc="Papers Found. Extracting Text...")
                    log_buffer += "Papers found. Proceeding to extraction...\n"
                elif key == "extract":
                    progress(0.4, desc="Text Extracted. Analyzing...")
                    log_buffer += "Text extracted. Running analysis...\n"
                elif key == "analyze":
                    progress(0.6, desc="Analysis Complete. Synthesizing...")
                    log_buffer += "Analysis complete. Synthesizing results...\n"
                elif key == "write":
                    progress(0.8, desc="Drafting Review...")
                    log_buffer += "Draft generated. Running critique...\n"
                elif key == "critique":
                    progress(0.9, desc="Critiquing & Finalizing...")
                    log_buffer += "Critique finished. Finalizing...\n"
                
                # Update local state tracking
                current_state.update(value)
                # Yield log update
                yield gr.update(value=log_buffer), gr.update()
        
        final_review = current_state.get("final_review")
        if not final_review:
             # Fallback if manual update failed
             final_review = "Review generation completed, but output was not captured correctly."
        
        log_buffer += "--- DONE ---\n"
        progress(1.0, desc="Done!")
        # Final yield with review and full logs
        yield gr.update(value=log_buffer), final_review
        
    except Exception as e:
        print(f"ERROR: {e}")
        yield gr.update(value=f"Error occurred: {str(e)}"), f"Error: {str(e)}"

def list_pdfs():
    return [f for f in os.listdir('.') if f.lower().endswith('.pdf')]

# Define UI
with gr.Blocks(title="AI Research Paper Summarizer") as demo:
    gr.Markdown("# 🎓 AI Research Paper Summarizer")
    gr.Markdown("Automated systematic reviews powered by Semantic Scholar and OpenAI GPT.")
    
    with gr.Row():
        with gr.Column():
            topic_input = gr.Textbox(label="Research Topic", placeholder="e.g., 'Agentic workflows in software engineering'")
            
            # Auto-detected files
            existing_pdfs = list_pdfs()
            if existing_pdfs:
                gr.Markdown("### 📂 Found Local Files")
                file_selector = gr.CheckboxGroup(choices=existing_pdfs, label="Select from Existing Files", value=[])
            else:
                file_selector = gr.CheckboxGroup(visible=False) # Hidden if no files

            max_results = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="Max Papers to Analyze")
                
            submit_btn = gr.Button("Generate Review", variant="primary")
    
    with gr.Accordion("Process Logs", open=True):
        logs_output = gr.Textbox(label="Execution Logs", lines=10, interactive=False)

    output_display = gr.Markdown(label="Generated Review")
    
    # Event
    submit_btn.click(
        fn=run_research,
        inputs=[topic_input, file_selector, max_results],
        outputs=[logs_output, output_display]
    )

def check_startup():
    print("--- STARTUP CHECKS ---")
    import os
    from langchain_openai import ChatOpenAI

    # Check keys
    openai_key = os.getenv("OPENAI_API_KEY")
    sem_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY missing!")
    else:
        print(f"✅ OPENAI_API_KEY found ({openai_key[:5]}...)")

    if not sem_key:
        print("⚠️ SEMANTIC_SCHOLAR_API_KEY missing! (Using Public API - slower)")
    else:
        print(f"✅ SEMANTIC_SCHOLAR_API_KEY found ({sem_key[:5]}...)")
        
    # Check Model Access
    try:
        # We don't invoke it, just instantiate to check if package works
        llm = ChatOpenAI(model="gpt-4o-mini")
        print("✅ OpenAI gpt-4o-mini initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing OpenAI model: {e}")

if __name__ == "__main__":
    check_startup()
    demo.launch(server_name="127.0.0.1")
