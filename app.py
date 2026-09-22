import streamlit as st
from google import genai

# Page configuration for global audience
st.set_page_config(
    page_title="AI Content Repurposing Workflow",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 AI Content Repurposing Workflow")
st.markdown("Transform long-form text, transcripts, or meeting notes into professional, platform-ready content instantly.")

# Global output modes with expert English system instructions
OUTPUT_MODES = {
    "🌐 SEO Blog Post": """
You are an expert SEO content editor.
Your job: Clean up the raw source text, fix typos, structure it with clear H2/H3 headings, and optimize it for a professional blog post. Return ONLY in clean Markdown.
    """,
    "✉️ Newsletter Edition": """
You are an expert copywriter.
Your job: Distill the raw source text into a compelling newsletter format. Include a catchy subject line suggestion, an engaging intro, 3 key takeaways as bullet points, and a strong closing/Call to Action. Return ONLY in clean Markdown.
    """,
    "📚 Notion Knowledge Base Summary": """
You are a professional knowledge management expert.
Your job: Structure the raw source text into a clean, highly organized internal wiki/Notion document. Use clear hierarchical bullet points, categorize key insights, and list concrete next steps or takeaways. Return ONLY in clean Markdown.
    """
}

# UI components in English
selected_mode = st.selectbox(
    "Select Output Format:",
    options=list(OUTPUT_MODES.keys())
)

raw_text_input = st.text_area(
    "Paste your raw long-form text, transcript, or notes below:",
    height=250,
    placeholder="Paste your raw content here..."
)

if st.button("🚀 Generate Content", type="primary"):
    if not raw_text_input.strip():
        st.warning("Please enter some text before generating!")
    else:
        with st.spinner("AI is processing and repurposing your content..."):
            try:
                # Initialize Gemini client
                client = genai.Client(api_key="AQ.Ab8RN6JtgRjzAEGWTXoamNnfaBSpb5qTK9W8byPp1TS27W4jUw")
                
                # Build prompt
                system_instruction = OUTPUT_MODES[selected_mode].strip()
                full_prompt = f"{system_instruction}\n\n--- RAW SOURCE TEXT ---\n{raw_text_input}\n--- END SOURCE TEXT ---"
                
                # Call Gemini 3.6 Flash
                interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=full_prompt,
                )
                
                markdown_result = (interaction.output_text or "").strip()
                
                # Strip markdown code blocks if wrapped
                if markdown_result.startswith("```"):
                    lines = markdown_result.splitlines()
                    if lines and lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    markdown_result = "\n".join(lines).strip()
                
                st.success("🎉 Content successfully generated!")
                
                # Preview area
                st.markdown("### 📋 Output Preview")
                st.markdown(markdown_result)
                
                # Download button
                st.download_button(
                    label="📥 Download Markdown File (.md)",
                    data=markdown_result,
                    file_name="repurposed_content.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")