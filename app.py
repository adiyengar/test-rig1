
"""Streamlit web application for data quality analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analyzer import DataQualityAnalyzer
from config import QUALITY_COLORS, get_quality_level
import json
import numpy as np

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
    page_title="Data Quality Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📊 Data Quality Analyzer")
    st.markdown("### Analyze product catalog data for quality and ML readiness")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This tool analyzes product catalog data with:\n"
            "- Product IDs\n"
            "- Descriptions\n"
            "- 7 categorization codes\n\n"
            "It evaluates data quality and readiness for semantic classification."
        )
        
        st.header("File Upload")
        uploaded_file = st.file_uploader(
            "Upload Excel or CSV file",
            type=["xlsx", "xls", "csv"],
            help="Upload your product catalog file"
        )
    
    # Main content
    if uploaded_file is None:
        st.info("👈 Please upload a file to begin analysis")
        
        # Show sample data format
        with st.expander("📋 Expected Data Format"):
            sample_data = pd.DataFrame({
                "product_id": ["P001", "P002", "P003"],
                "description": ["Widget A for industrial use", "Gadget B with features", "Component C"],
                "code_1": ["A123", "B456", "A123"],
                "code_2": ["X01", "X02", "X01"],
                "code_3": ["Z9", "Z8", "Z9"],
                "code_4": ["M1", "M2", "M1"],
                "code_5": ["T4", "T5", "T4"],
                "code_6": ["R7", "R8", "R7"],
                "code_7": ["Q2", "Q3", "Q2"]
            })
            st.dataframe(sample_data)
        
        return
    
    # Load data
    try:
        with st.spinner("Loading data..."):
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return
    
    # Column mapping
    st.subheader("Column Mapping")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_id_col = st.selectbox("Product ID Column", df.columns, index=0)
    with col2:
        description_col = st.selectbox("Description Column", df.columns, index=1)
    with col3:
        num_codes = st.number_input("Number of Code Columns", min_value=1, max_value=20, value=7)
    
    code_cols = st.multiselect(
        "Select Code Columns",
        [col for col in df.columns if col not in [product_id_col, description_col]],
        default=[col for col in df.columns if col not in [product_id_col, description_col]][:num_codes]
    )
    
    if not code_cols:
        st.warning("Please select at least one code column")
        return
    
    # Run analysis button
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        run_analysis(df, product_id_col, description_col, code_cols)

def run_analysis(df, product_id_col, description_col, code_cols):
    """Run the full analysis and display results."""
    
    # Initialize analyzer
    with st.spinner("Initializing analyzer..."):
        analyzer = DataQualityAnalyzer(df, product_id_col, description_col, code_cols)
    
    # Run analysis
    with st.spinner("Analyzing data quality... This may take a moment for large files."):
        progress_bar = st.progress(0)
        results = analyzer.analyze_all()
        progress_bar.progress(100)
    
    st.success("✅ Analysis complete!")
    
    # Display results in tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Executive Summary",
        "✅ Completeness",
        "📝 Description Quality",
        "🔢 Code Distribution",
        "🤖 Classifier Readiness",
        "📥 Export Report"
    ])
    
    with tab1:
        display_executive_summary(results)
    
    with tab2:
        display_completeness_analysis(results["completeness"])
    
    with tab3:
        display_description_quality(results["description_quality"])
    
    with tab4:
        display_code_distribution(results["code_distribution"])
    
    with tab5:
        display_classifier_readiness(results["classifier_readiness"])
    
    with tab6:
        display_export_options(results)

def display_executive_summary(results):
    """Display executive summary dashboard."""
    st.header("Executive Summary")
    
    overall = results["overall"]
    quality_level = overall["quality_level"]
    quality_color = QUALITY_COLORS[quality_level]
    
    # Overall score display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background-color: {quality_color}; padding: 30px; border-radius: 10px; text-align: center;'>
            <h1 style='color: white; margin: 0;'>{overall['overall_score']:.1f}/100</h1>
            <h3 style='color: white; margin: 0;'>{quality_level.upper()}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Total Rows", f"{results['completeness']['total_rows']:,}")
    
    with col3:
        ready_cols = results["classifier_readiness"]["training_viability"]["columns_ready"]
        total_cols = len(results["classifier_readiness"]["per_code_column"])
        st.metric("Columns Ready for ML", f"{ready_cols}/{total_cols}")
    
    # Component scores
    st.subheader("Component Scores")
    
    scores = overall["component_scores"]
    cols = st.columns(4)
    
    for i, (component, score) in enumerate(scores.items()):
        with cols[i]:
            level = get_quality_level(score)
            color = QUALITY_COLORS[level]
            st.markdown(f"""
            <div style='background-color: {color}20; padding: 15px; border-radius: 8px; border-left: 4px solid {color};'>
                <h4 style='margin: 0;'>{component.replace('_', ' ').title()}</h4>
                <h2 style='margin: 5px 0; color: {color};'>{score:.1f}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Critical issues
    st.subheader("⚠️ Critical Issues")
    
    issues = []
    
    # Add completeness issues
    for col, metrics in results["completeness"]["column_completeness"].items():
        if metrics["completeness_pct"] < 80:
            issues.append(f"❌ Low completeness in **{col}**: {metrics['completeness_pct']:.1f}%")
    
    # Add description issues
    desc = results["description_quality"]
    if desc["quality_flags"]["too_short_pct"] > 10:
        issues.append(f"❌ **{desc['quality_flags']['too_short_pct']:.1f}%** of descriptions are too short")
    
    if desc["duplicates"]["duplicate_count"] > 100:
        issues.append(f"⚠️ **{desc['duplicates']['duplicate_count']:,}** duplicate descriptions found")
    
    # Add classifier issues
    issues.extend([f"❌ {issue}" for issue in results["classifier_readiness"]["data_quality_issues"][:5]])
    
    if issues:
        for issue in issues[:10]:
            st.markdown(issue)
    else:
        st.success("✅ No critical issues found!")

def display_completeness_analysis(completeness):
    """Display completeness analysis."""
    st.header("Completeness Analysis")
    
    st.metric("Overall Completeness Score", f"{completeness['overall_score']:.1f}%")
    
    # Column-level completeness
    st.subheader("Column-Level Completeness")
    
    col_comp = pd.DataFrame(completeness["column_completeness"]).T
    col_comp = col_comp.sort_values("completeness_pct")
    
    # Create bar chart
    fig = px.bar(
        col_comp,
        y=col_comp.index,
        x="completeness_pct",
        orientation="h",
        title="Completeness by Column",
        labels={"completeness_pct": "Completeness %", "index": "Column"},
        color="completeness_pct",
        color_continuous_scale=["red", "yellow", "green"],
        range_color=[0, 100]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.dataframe(
        col_comp[["non_empty_count", "missing_count", "completeness_pct"]].style.background_gradient(
            subset=["completeness_pct"],
            cmap="RdYlGn",
            vmin=0,
            vmax=100
        ),
        use_container_width=True
    )
    
    # Row-level completeness
    st.subheader("Row-Level Code Coverage")
    
    row_comp = completeness["row_completeness"]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("All Codes Present", f"{row_comp['all_codes_present']:,}")
    col2.metric("Partial Codes", f"{row_comp['partial_codes']:,}")
    col3.metric("No Codes", f"{row_comp['no_codes_present']:,}")
    col4.metric("Avg Codes/Row", f"{row_comp['avg_codes_per_row']:.2f}")
    
    # Pie chart
    fig = go.Figure(data=[go.Pie(
        labels=["All Codes", "Partial Codes", "No Codes"],
        values=[row_comp['all_codes_present'], row_comp['partial_codes'], row_comp['no_codes_present']],
        hole=0.4,
        marker_colors=["#28a745", "#ffc107", "#dc3545"]
    )])
    fig.update_layout(title="Code Coverage Distribution")
    st.plotly_chart(fig, use_container_width=True)

def display_description_quality(desc_quality):
    """Display description quality analysis."""
    st.header("Description Quality Analysis")
    
    st.metric("Description Quality Score", f"{desc_quality['overall_score']:.1f}/100")
    
    # Length statistics
    st.subheader("Description Length Statistics")
    
    length_stats = desc_quality["length_stats"]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean Length", f"{length_stats['mean']:.0f} chars")
    col2.metric("Median Length", f"{length_stats['median']:.0f} chars")
    col3.metric("Min Length", f"{length_stats['min']} chars")
    col4.metric("Max Length", f"{length_stats['max']} chars")
    
    # Quality flags
    st.subheader("Quality Flags")
    
    flags = desc_quality["quality_flags"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        color = QUALITY_COLORS["critical"] if flags["too_short_pct"] > 10 else QUALITY_COLORS["good"]
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 20px; border-radius: 8px; border-left: 4px solid {color};'>
            <h4>Too Short (<20 chars)</h4>
            <h2>{flags['too_short']:,}</h2>
            <p>{flags['too_short_pct']:.1f}% of descriptions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = QUALITY_COLORS["poor"] if flags["mostly_numeric"] > 100 else QUALITY_COLORS["good"]
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 20px; border-radius: 8px; border-left: 4px solid {color};'>
            <h4>Mostly Numeric</h4>
            <h2>{flags['mostly_numeric']:,}</h2>
            <p>Descriptions with >50% numbers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = QUALITY_COLORS["poor"] if flags["high_special_chars"] > 100 else QUALITY_COLORS["good"]
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 20px; border-radius: 8px; border-left: 4px solid {color};'>
            <h4>High Special Chars</h4>
            <h2>{flags['high_special_chars']:,}</h2>
            <p>Descriptions with >30% special chars</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Vocabulary richness
    st.subheader("Vocabulary Analysis")
    
    vocab = desc_quality["vocabulary"]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Unique Words", f"{vocab['unique_words']:,}")
    col2.metric("Total Words", f"{vocab['total_words']:,}")
    col3.metric("Vocabulary Richness", f"{vocab['vocabulary_richness']:.4f}")
    
    st.info("💡 Higher vocabulary richness (closer to 1.0) indicates more diverse descriptions")
    
    # Duplicates
    st.subheader("Duplicate Descriptions")
    
    dup = desc_quality["duplicates"]
    
    col1, col2 = st.columns(2)
    col1.metric("Unique Duplicates", f"{dup['duplicate_count']:,}")
    col2.metric("Total Duplicate Rows", f"{dup['total_duplicate_rows']:,}")
    
    if dup["top_duplicates"]:
        st.write("**Top 10 Most Duplicated Descriptions:**")
        dup_df = pd.DataFrame(list(dup["top_duplicates"].items()), columns=["Description", "Count"])
        st.dataframe(dup_df, use_container_width=True)

def display_code_distribution(code_dist):
    """Display code distribution analysis."""
    st.header("Code Distribution Analysis")
    
    st.metric("Distribution Quality Score", f"{code_dist['overall_score']:.1f}/100")
    
    # Per-column analysis
    st.subheader("Code Column Analysis")
    
    for col_name, metrics in code_dist["code_columns"].items():
        with st.expander(f"📊 {col_name}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Unique Codes", f"{metrics['unique_codes']:,}")
            col2.metric("Rare Codes", f"{metrics['rare_codes_count']:,}")
            col3.metric("Entropy", f"{metrics['distribution_entropy']:.2f}")
            col4.metric("Top Code %", f"{metrics['top_code_concentration']:.1f}%")
            
            # Most common codes
            st.write("**Top 10 Most Common Codes:**")
            most_common = pd.DataFrame(
                list(metrics['most_common'].items()),
                columns=["Code", "Count"]
            )
            
            fig = px.bar(
                most_common,
                x="Code",
                y="Count",
                title=f"Top Codes in {col_name}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Rare codes
            if metrics['rare_codes_count'] > 0:
                st.write(f"**Rare Codes (appearing <0.5% of time):** {metrics['rare_codes_count']}")
                if len(metrics['rare_codes']) <= 20:
                    rare_df = pd.DataFrame(
                        list(metrics['rare_codes'].items()),
                        columns=["Code", "Count"]
                    )
                    st.dataframe(rare_df, use_container_width=True)

def display_classifier_readiness(classifier_ready):
    """Display classifier readiness analysis."""
    st.header("Machine Learning Classifier Readiness")
    
    viability = classifier_ready["training_viability"]
    
    # Overall readiness
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Readiness Score", f"{classifier_ready['overall_score']:.1f}%")
    col2.metric("Columns Ready", f"{viability['columns_ready']}")
    col3.metric("Columns Not Ready", f"{viability['columns_not_ready']}")
    
    # Per-column readiness
    st.subheader("Per-Column Training Readiness")
    
    for col_name, metrics in classifier_ready["per_code_column"].items():
        if metrics.get("status") == "insufficient_data":
            st.error(f"❌ **{col_name}**: Insufficient data")
            continue
        
        ready = metrics["ready_for_training"]
        icon = "✅" if ready else "❌"
        
        with st.expander(f"{icon} {col_name} - {'READY' if ready else 'NOT READY'}", expanded=not ready):
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Total Samples", f"{metrics['total_samples']:,}")
            col2.metric("Unique Classes", f"{metrics['unique_classes']:,}")
            col3.metric("Classes w/ Enough Data", f"{metrics['classes_with_sufficient_data']:,}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Min Class Size", f"{metrics['min_class_size']:,}")
            col2.metric("Max Class Size", f"{metrics['max_class_size']:,}")
            col3.metric("Median Class Size", f"{metrics['median_class_size']:,}")
            
            # Imbalance warning
            if metrics['class_imbalance_ratio'] > 100:
                st.warning(f"⚠️ Severe class imbalance detected (ratio: {metrics['class_imbalance_ratio']:.1f}:1)")
            
            # Ambiguous descriptions
            if metrics['ambiguous_descriptions'] > 0:
                st.warning(f"⚠️ {metrics['ambiguous_descriptions']:,} ambiguous descriptions (same text mapped to different codes)")
            
            # Description uniqueness
            st.metric(
                "Avg Description Uniqueness",
                f"{metrics['avg_description_uniqueness']:.2%}",
                help="Ratio of unique descriptions per code (higher is better)"
            )
            
            # Split recommendation
            st.info(f"**Recommended Split:** {metrics['recommended_train_test_split']}")
    
    # Critical issues
    if classifier_ready["data_quality_issues"]:
        st.subheader("⚠️ Critical Issues for ML Training")
        for issue in classifier_ready["data_quality_issues"]:
            st.error(issue)

def display_export_options(results):
    """Display export options."""
    st.header("Export Report")
    
    st.write("Download the complete analysis report in your preferred format.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        json_str = json.dumps(convert_to_serializable(results), indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name="data_quality_report.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # CSV export (summary)
        summary_data = {
            "Metric": [],
            "Score": []
        }
        
        summary_data["Metric"].append("Overall Quality")
        summary_data["Score"].append(results["overall"]["overall_score"])
        
        for component, score in results["overall"]["component_scores"].items():
            summary_data["Metric"].append(component.replace("_", " ").title())
            summary_data["Score"].append(score)
        
        summary_df = pd.DataFrame(summary_data)
        csv = summary_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Summary as CSV",
            data=csv,
            file_name="data_quality_summary.csv",
            mime="text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()

