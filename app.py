"""Main entry point - displays context before tools."""
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Index Management Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Read and display only up to System Architecture section
@st.cache_data
def load_jtbd_content():
    """Load the semantic search JTBD markdown file up to System Architecture."""
    jtbd_path = Path("semantic_search_teams_jtbd.md")
    if jtbd_path.exists():
        with open(jtbd_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Find where System Architecture section ends (before "TEAM 1: INDEX MANAGEMENT TEAM")
            content_lines = []
            for line in lines:
                # Stop before "TEAM 1: INDEX MANAGEMENT TEAM" or "## Mission Statement"
                if line.strip().startswith("# TEAM") or line.strip().startswith("## Mission"):
                    break
                content_lines.append(line)
            return ''.join(content_lines)
    return None

# Main content
st.title("📊 Semantic Search Engine: Tools & Management")

# Display JTBD content (only System Architecture section)
jtbd_content = load_jtbd_content()
if jtbd_content:
    st.markdown(jtbd_content)
else:
    st.warning("Could not load context document. Please ensure semantic_search_teams_jtbd.md exists.")

# Navigation instructions
st.divider()
st.info("👈 **Use the sidebar to navigate to:**\n- **Index Management Tool** - Analyze and maintain lookup index quality\n- **Input Management Tool** - Experiment with input embeddings")
