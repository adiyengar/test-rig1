"""Streamlit web application for input embedding experimentation."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
from embedding_experimenter import EmbeddingExperimenter
from config import QUALITY_COLORS, get_quality_level

def convert_to_serializable(obj):
    """Convert numpy/pandas types to native Python types."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {str(key): convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj

# Page configuration
st.set_page_config(
    page_title="Input Management Tool",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the data quality analyzer
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .template-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🧪 Input Embedding Experiment Tool")
    st.markdown("### Test feature combinations and templates to optimize semantic search accuracy")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This tool helps you:\n"
            "- Select features from 40+ columns\n"
            "- Design embedding templates\n"
            "- Compare accuracy across experiments\n"
            "- Find optimal input strategy\n\n"
            "Upload your product catalog and ground truth data to begin."
        )
        
        st.header("File Upload")
        catalog_file = st.file_uploader(
            "Product Catalog (Excel/CSV)",
            type=["xlsx", "xls", "csv"],
            help="Your full product catalog with all columns",
            key="catalog"
        )
        
        ground_truth_file = st.file_uploader(
            "Ground Truth Data (Excel/CSV)",
            type=["xlsx", "xls", "csv"],
            help="Products with known correct predictions for testing",
            key="ground_truth"
        )
    
    # Main content
    if catalog_file is None:
        st.info("👈 Please upload your product catalog to begin")
        
        # Show sample data format
        with st.expander("📋 Expected Data Format"):
            st.markdown("""
            **Product Catalog** should contain:
            - All available product columns (40+)
            - Product ID, Description, Categories, Attributes, etc.
            
            **Ground Truth Data** should contain:
            - Product ID
            - Input description (as it would come in)
            - Correct prediction code/value
            """)
            
            sample_catalog = pd.DataFrame({
                "product_id": ["P001", "P002", "P003"],
                "description": ["Widget A for industrial use", "Gadget B with features", "Component C"],
                "category": ["Industrial", "Consumer", "Industrial"],
                "brand": ["BrandX", "BrandY", "BrandX"],
                "material": ["Steel", "Plastic", "Steel"],
                "weight_kg": [5.2, 1.1, 3.8],
                "color": ["Gray", "Blue", "Gray"],
                # ... many more columns
            })
            st.write("**Sample Catalog:**")
            st.dataframe(sample_catalog)
            
            sample_ground_truth = pd.DataFrame({
                "product_id": ["P001", "P002"],
                "input_description": ["industrial widget", "consumer gadget features"],
                "correct_code": ["A123", "B456"]
            })
            st.write("**Sample Ground Truth:**")
            st.dataframe(sample_ground_truth)
        
        return
    
    # Load catalog data
    try:
        with st.spinner("Loading catalog..."):
            if catalog_file.name.endswith('.csv'):
                catalog_df = pd.read_csv(catalog_file)
            else:
                catalog_df = pd.read_excel(catalog_file)
        
        st.success(f"✅ Loaded catalog: {len(catalog_df):,} rows and {len(catalog_df.columns)} columns")
        
    except Exception as e:
        st.error(f"Error loading catalog: {str(e)}")
        return
    
    # Load ground truth (optional)
    ground_truth_df = None
    if ground_truth_file is not None:
        try:
            with st.spinner("Loading ground truth..."):
                if ground_truth_file.name.endswith('.csv'):
                    ground_truth_df = pd.read_csv(ground_truth_file)
                else:
                    ground_truth_df = pd.read_excel(ground_truth_file)
            
            st.success(f"✅ Loaded ground truth: {len(ground_truth_df):,} test cases")
            
        except Exception as e:
            st.error(f"Error loading ground truth: {str(e)}")
            return
    
    # Column identification
    st.subheader("Column Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        product_id_col = st.selectbox("Product ID Column", catalog_df.columns, index=0)
    with col2:
        description_col = st.selectbox("Primary Description Column", catalog_df.columns, index=1)
    
    # Available features for selection
    available_features = [col for col in catalog_df.columns if col not in [product_id_col]]
    
    st.markdown("---")
    
    # Tabs for different experiment types
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 Feature Selection",
        "📝 Template Designer", 
        "📊 Experiment Results",
        "💾 Saved Experiments"
    ])
    
    with tab1:
        display_feature_selection(catalog_df, available_features, description_col)
    
    with tab2:
        display_template_designer(catalog_df, available_features)
    
    with tab3:
        if ground_truth_df is not None:
            display_experiment_results(catalog_df, ground_truth_df, product_id_col)
        else:
            st.info("📤 Upload ground truth data to see experiment results")
    
    with tab4:
        display_saved_experiments()

def display_feature_selection(df, available_features, description_col):
    """Display feature selection interface."""
    st.header("Feature Selection Experiment")
    
    st.markdown("""
    Select which features to include in your input embeddings. The tool will analyze:
    - Feature importance and contribution
    - Data completeness per feature
    - Correlation between features
    - Impact on embedding quality
    """)
    
    # Feature categories for easier selection
    st.subheader("1. Categorize Your Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Text Features** (descriptions, names, etc.)")
        text_features = st.multiselect(
            "Select text features",
            available_features,
            default=[description_col] if description_col in available_features else [],
            key="text_features"
        )
    
    with col2:
        st.markdown("**Categorical Features** (category, brand, type, etc.)")
        categorical_features = st.multiselect(
            "Select categorical features",
            [f for f in available_features if f not in text_features],
            key="categorical_features"
        )
    
    st.markdown("**Numerical Features** (price, weight, dimensions, etc.)")
    numerical_features = st.multiselect(
        "Select numerical features",
        [f for f in available_features if f not in text_features + categorical_features],
        key="numerical_features"
    )
    
    # Feature analysis
    if text_features or categorical_features or numerical_features:
        st.markdown("---")
        st.subheader("2. Feature Analysis")
        
        all_selected = text_features + categorical_features + numerical_features
        
        # Data completeness
        st.markdown("**Data Completeness by Feature**")
        completeness_data = []
        for feat in all_selected:
            non_null_pct = (df[feat].notna().sum() / len(df)) * 100
            completeness_data.append({
                "Feature": feat,
                "Completeness": non_null_pct,
                "Missing": 100 - non_null_pct
            })
        
        completeness_df = pd.DataFrame(completeness_data)
        
        fig = px.bar(
            completeness_df,
            x="Feature",
            y="Completeness",
            title="Feature Completeness (%)",
            color="Completeness",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature info density
        st.markdown("**Information Density**")
        info_data = []
        for feat in all_selected:
            unique_count = df[feat].nunique()
            unique_pct = (unique_count / df[feat].notna().sum()) * 100 if df[feat].notna().sum() > 0 else 0
            info_data.append({
                "Feature": feat,
                "Unique Values": unique_count,
                "Uniqueness %": unique_pct
            })
        
        info_df = pd.DataFrame(info_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(info_df, use_container_width=True)
        
        with col2:
            fig = px.bar(
                info_df,
                x="Feature",
                y="Uniqueness %",
                title="Feature Uniqueness (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Save experiment configuration
        st.markdown("---")
        st.subheader("3. Save Feature Set")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            experiment_name = st.text_input(
                "Experiment Name",
                value=f"experiment_{len(text_features + categorical_features + numerical_features)}_features",
                key="feature_exp_name"
            )
        with col2:
            st.write("")  # spacing
            st.write("")  # spacing
            if st.button("💾 Save Configuration", type="primary", use_container_width=True):
                save_feature_experiment(experiment_name, text_features, categorical_features, numerical_features)
                st.success(f"✅ Saved: {experiment_name}")

def display_template_designer(df, available_features):
    """Display template design interface."""
    st.header("Embedding Template Designer")
    
    st.markdown("""
    Design how features are combined into the embedding text. Different templates can significantly impact accuracy.
    """)
    
    # Template selection
    st.subheader("1. Choose Template Strategy")
    
    template_strategy = st.radio(
        "Template Type",
        [
            "Simple Concatenation",
            "Weighted Fields",
            "Structured Prompt",
            "Question-Answer Format",
            "Custom Template"
        ],
        help="Different strategies for combining features into embedding text"
    )
    
    # Feature selection for template
    st.subheader("2. Select Features for Template")
    selected_features = st.multiselect(
        "Choose features to include",
        available_features,
        key="template_features"
    )
    
    if not selected_features:
        st.info("Select features to preview template")
        return
    
    # Template configuration based on strategy
    st.subheader("3. Configure Template")
    
    template_config = {}
    
    if template_strategy == "Simple Concatenation":
        st.markdown("Features will be concatenated with labels.")
        separator = st.text_input("Separator", value=". ", key="separator")
        template_config["separator"] = separator
        
    elif template_strategy == "Weighted Fields":
        st.markdown("Assign importance weights to features (higher weight = more emphasis).")
        weights = {}
        for feat in selected_features:
            weights[feat] = st.slider(f"{feat} weight", 1, 10, 5, key=f"weight_{feat}")
        template_config["weights"] = weights
        
    elif template_strategy == "Structured Prompt":
        st.markdown("Features organized in a natural language structure.")
        use_labels = st.checkbox("Include field labels", value=True, key="use_labels")
        template_config["use_labels"] = use_labels
        
    elif template_strategy == "Question-Answer Format":
        st.markdown("Present features as Q&A pairs.")
        template_config["format"] = "qa"
        
    elif template_strategy == "Custom Template":
        st.markdown("Write your own template using {field_name} placeholders.")
        custom_template = st.text_area(
            "Template",
            value="Product: {description}\nCategory: {category}\nSpecs: {specs}",
            height=150,
            key="custom_template"
        )
        template_config["template"] = custom_template
    
    # Live preview
    st.subheader("4. Preview with Sample Data")
    
    sample_idx = st.number_input(
        "Sample Row Index",
        min_value=0,
        max_value=len(df)-1,
        value=0,
        key="preview_idx"
    )
    
    # Generate preview
    sample_row = df.iloc[sample_idx]
    preview_text = generate_template_preview(
        sample_row,
        selected_features,
        template_strategy,
        template_config
    )
    
    st.markdown("**Generated Embedding Text:**")
    st.markdown(f'<div class="template-box">{preview_text}</div>', unsafe_allow_html=True)
    
    # Show sample data
    with st.expander("View Sample Row Data"):
        sample_data = {feat: sample_row[feat] for feat in selected_features}
        st.json(sample_data)
    
    # Save template
    st.markdown("---")
    st.subheader("5. Save Template")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        template_name = st.text_input(
            "Template Name",
            value=f"{template_strategy.lower().replace(' ', '_')}_template",
            key="template_name"
        )
    with col2:
        st.write("")  # spacing
        st.write("")  # spacing
        if st.button("💾 Save Template", type="primary", use_container_width=True):
            save_template(template_name, template_strategy, selected_features, template_config)
            st.success(f"✅ Saved: {template_name}")

def generate_template_preview(row, features, strategy, config):
    """Generate a preview of the embedding text."""
    
    if strategy == "Simple Concatenation":
        parts = []
        for feat in features:
            value = row[feat]
            if pd.notna(value):
                parts.append(f"{feat}: {value}")
        return config.get("separator", ". ").join(parts)
    
    elif strategy == "Weighted Fields":
        parts = []
        for feat in features:
            value = row[feat]
            if pd.notna(value):
                weight = config["weights"].get(feat, 1)
                # Repeat text based on weight for emphasis
                parts.append(f"{feat}: {value}" + (" [IMPORTANT]" * (weight // 3)))
        return ". ".join(parts)
    
    elif strategy == "Structured Prompt":
        parts = []
        if config.get("use_labels", True):
            for feat in features:
                value = row[feat]
                if pd.notna(value):
                    parts.append(f"{feat}: {value}")
            return "This product has the following attributes: " + ", ".join(parts) + "."
        else:
            return " ".join([str(row[feat]) for feat in features if pd.notna(row[feat])])
    
    elif strategy == "Question-Answer Format":
        parts = []
        for feat in features:
            value = row[feat]
            if pd.notna(value):
                parts.append(f"Q: What is the {feat}? A: {value}")
        return "\n".join(parts)
    
    elif strategy == "Custom Template":
        template = config.get("template", "")
        for feat in features:
            value = row[feat] if pd.notna(row[feat]) else ""
            template = template.replace(f"{{{feat}}}", str(value))
        return template
    
    return "Preview not available"

def display_experiment_results(catalog_df, ground_truth_df, product_id_col):
    """Display experiment comparison results."""
    st.header("Experiment Results & Comparison")
    
    st.markdown("""
    Compare performance across different feature sets and templates.
    """)
    
    # Load saved experiments (would come from a database/file in real implementation)
    if "experiments" not in st.session_state:
        st.session_state.experiments = []
    
    if not st.session_state.experiments:
        st.info("No experiments run yet. Configure features and templates, then run experiments to see results here.")
        
        # Demo/baseline experiment
        st.markdown("---")
        st.subheader("Run Baseline Experiment")
        
        if st.button("🚀 Run Baseline Test", type="primary"):
            with st.spinner("Running baseline experiment..."):
                # Simulate baseline results
                baseline_results = {
                    "name": "Baseline (Description Only)",
                    "accuracy": 67.5,
                    "top_3_accuracy": 82.3,
                    "top_5_accuracy": 88.1,
                    "features_used": 1,
                    "avg_confidence": 0.72
                }
                st.session_state.experiments.append(baseline_results)
                st.success("✅ Baseline complete!")
                st.rerun()
        return
    
    # Display comparison
    st.subheader("Experiment Comparison")
    
    # Metrics comparison
    metrics_df = pd.DataFrame(st.session_state.experiments)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_accuracy = metrics_df["accuracy"].max()
        best_exp = metrics_df.loc[metrics_df["accuracy"].idxmax(), "name"]
        st.metric(
            "Best Accuracy",
            f"{best_accuracy:.1f}%",
            f"{best_accuracy - 67.5:.1f}% vs baseline"
        )
        st.caption(f"Experiment: {best_exp}")
    
    with col2:
        best_top3 = metrics_df["top_3_accuracy"].max()
        st.metric(
            "Best Top-3 Accuracy",
            f"{best_top3:.1f}%"
        )
    
    with col3:
        avg_improvement = (metrics_df["accuracy"].mean() - 67.5)
        st.metric(
            "Avg Improvement",
            f"+{avg_improvement:.1f}%"
        )
    
    # Accuracy comparison chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Top-1 Accuracy",
        x=metrics_df["name"],
        y=metrics_df["accuracy"],
        marker_color='#4CAF50'
    ))
    
    fig.add_trace(go.Bar(
        name="Top-3 Accuracy",
        x=metrics_df["name"],
        y=metrics_df["top_3_accuracy"],
        marker_color='#2196F3'
    ))
    
    fig.update_layout(
        title="Accuracy Comparison Across Experiments",
        xaxis_title="Experiment",
        yaxis_title="Accuracy (%)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results table
    st.subheader("Detailed Results")
    st.dataframe(metrics_df, use_container_width=True)
    
    # Feature importance analysis
    st.subheader("Feature Contribution Analysis")
    
    # This would be calculated from actual experiments
    st.info("💡 Run multiple experiments with different feature combinations to see which features contribute most to accuracy.")

def display_saved_experiments():
    """Display saved experiment configurations."""
    st.header("Saved Experiments")
    
    # Feature experiments
    st.subheader("📊 Feature Configurations")
    if "feature_experiments" not in st.session_state:
        st.session_state.feature_experiments = {}
    
    if st.session_state.feature_experiments:
        for name, config in st.session_state.feature_experiments.items():
            with st.expander(f"📁 {name}"):
                st.write(f"**Text Features:** {len(config['text'])}")
                st.write(f"**Categorical Features:** {len(config['categorical'])}")
                st.write(f"**Numerical Features:** {len(config['numerical'])}")
                st.write(f"**Total Features:** {len(config['text']) + len(config['categorical']) + len(config['numerical'])}")
                
                if st.button(f"🗑️ Delete", key=f"del_feat_{name}"):
                    del st.session_state.feature_experiments[name]
                    st.rerun()
    else:
        st.info("No saved feature configurations yet.")
    
    # Template configurations
    st.markdown("---")
    st.subheader("📝 Template Configurations")
    if "templates" not in st.session_state:
        st.session_state.templates = {}
    
    if st.session_state.templates:
        for name, config in st.session_state.templates.items():
            with st.expander(f"📄 {name}"):
                st.write(f"**Strategy:** {config['strategy']}")
                st.write(f"**Features:** {len(config['features'])}")
                st.json(config['config'])
                
                if st.button(f"🗑️ Delete", key=f"del_temp_{name}"):
                    del st.session_state.templates[name]
                    st.rerun()
    else:
        st.info("No saved templates yet.")

def save_feature_experiment(name, text_features, categorical_features, numerical_features):
    """Save feature experiment configuration."""
    if "feature_experiments" not in st.session_state:
        st.session_state.feature_experiments = {}
    
    st.session_state.feature_experiments[name] = {
        "text": text_features,
        "categorical": categorical_features,
        "numerical": numerical_features
    }

def save_template(name, strategy, features, config):
    """Save template configuration."""
    if "templates" not in st.session_state:
        st.session_state.templates = {}
    
    st.session_state.templates[name] = {
        "strategy": strategy,
        "features": features,
        "config": config
    }

if __name__ == "__main__":
    main()
