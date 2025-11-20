"""Generate sample data for testing the embedding experiment tool."""

import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Sample data values
CATEGORIES = ["Electronics", "Automotive", "Industrial", "Consumer", "Medical", "Aerospace"]
BRANDS = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE", "BrandF", "BrandG"]
MATERIALS = ["Steel", "Aluminum", "Plastic", "Composite", "Titanium", "Copper"]
COLORS = ["Black", "White", "Gray", "Red", "Blue", "Green", "Yellow", "Silver"]
MANUFACTURERS = ["ManufacturerX", "ManufacturerY", "ManufacturerZ", "ManufacturerW"]
STATUSES = ["Active", "Discontinued", "Pending", "Active", "Active"]  # More actives
ORIGINS = ["USA", "China", "Germany", "Japan", "Mexico", "Canada"]

# Product name parts
ADJECTIVES = ["Heavy-Duty", "Precision", "Standard", "Premium", "Industrial", "Commercial"]
NOUNS = ["Widget", "Component", "Assembly", "Module", "Part", "Unit", "Device"]

def generate_product_name(category, idx):
    """Generate a realistic product name."""
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{category} {adj} {noun} {idx:04d}"

def generate_description(name, category, brand, material):
    """Generate a realistic product description."""
    templates = [
        f"{name} manufactured by {brand}, made from high-quality {material.lower()}. Suitable for {category.lower()} applications.",
        f"Professional-grade {name.lower()} featuring {material.lower()} construction. {brand} quality guaranteed.",
        f"{category} product: {name}. Constructed from durable {material.lower()}. {brand} certified.",
        f"High-performance {name.lower()} designed for demanding {category.lower()} environments. {material} composition.",
    ]
    return random.choice(templates)

def generate_catalog(num_products=1000):
    """Generate a sample product catalog."""
    
    print(f"Generating catalog with {num_products} products...")
    
    products = []
    
    for i in range(num_products):
        category = random.choice(CATEGORIES)
        brand = random.choice(BRANDS)
        material = random.choice(MATERIALS)
        name = generate_product_name(category, i)
        
        # Create product with realistic data patterns
        product = {
            # Core fields (always present)
            "product_id": f"P{i:06d}",
            "name": name,
            "description": generate_description(name, category, brand, material),
            "category": category,
            "brand": brand,
            
            # Common fields (mostly present)
            "material": material if random.random() > 0.05 else None,
            "color": random.choice(COLORS) if random.random() > 0.10 else None,
            "manufacturer": random.choice(MANUFACTURERS) if random.random() > 0.08 else None,
            "status": random.choice(STATUSES),
            "country_of_origin": random.choice(ORIGINS) if random.random() > 0.12 else None,
            
            # Numerical fields (varying completeness)
            "weight_kg": round(random.uniform(0.1, 100), 2) if random.random() > 0.15 else None,
            "length_cm": round(random.uniform(1, 200), 1) if random.random() > 0.20 else None,
            "width_cm": round(random.uniform(1, 150), 1) if random.random() > 0.20 else None,
            "height_cm": round(random.uniform(1, 100), 1) if random.random() > 0.20 else None,
            "price_usd": round(random.uniform(10, 5000), 2) if random.random() > 0.10 else None,
            "stock_quantity": random.randint(0, 1000) if random.random() > 0.15 else None,
            
            # Technical specifications (sparse)
            "voltage": random.choice([110, 220, 240, 12, 24]) if category == "Electronics" and random.random() > 0.30 else None,
            "power_watts": random.randint(10, 2000) if category == "Electronics" and random.random() > 0.35 else None,
            "temperature_rating": random.choice([-40, 85, 125, 150]) if random.random() > 0.60 else None,
            "pressure_rating": random.choice([100, 150, 200, 300]) if random.random() > 0.70 else None,
            
            # Additional categorical fields
            "warranty_months": random.choice([12, 24, 36, 60]) if random.random() > 0.25 else None,
            "certification": random.choice(["CE", "UL", "ISO", "RoHS"]) if random.random() > 0.40 else None,
            "hazmat": random.choice(["Yes", "No"]) if random.random() > 0.30 else None,
            
            # Classification codes (for ground truth)
            "code_1": f"{category[:2].upper()}{random.randint(100, 999)}",
            "code_2": f"{brand[5]}{random.randint(10, 99)}",
            "code_3": f"M{random.randint(1, 20)}",
        }
        
        # Add more sparse fields to get to 40+ columns
        for j in range(1, 16):
            if random.random() > 0.7:  # Sparse additional fields
                product[f"spec_{j}"] = f"value_{random.randint(1, 100)}"
            else:
                product[f"spec_{j}"] = None
        
        products.append(product)
    
    df = pd.DataFrame(products)
    print(f"✓ Generated {len(df)} products with {len(df.columns)} columns")
    print(f"✓ Average completeness: {df.notna().mean().mean()*100:.1f}%")
    
    return df

def generate_ground_truth(catalog_df, num_samples=100):
    """Generate ground truth test data from catalog."""
    
    print(f"\nGenerating ground truth with {num_samples} samples...")
    
    # Sample from catalog
    samples = catalog_df.sample(n=min(num_samples, len(catalog_df)))
    
    ground_truth = []
    
    for _, row in samples.iterrows():
        # Create simplified/noisy input descriptions
        noise_level = random.choice([0, 1, 2])  # 0=perfect, 1=simplified, 2=noisy
        
        if noise_level == 0:
            # Perfect match
            input_desc = row["description"]
        elif noise_level == 1:
            # Simplified - just key terms
            input_desc = f"{row['category']} {row['brand']} {row['material']}".lower()
        else:
            # Noisy - partial information
            parts = []
            if random.random() > 0.3:
                parts.append(row['category'])
            if random.random() > 0.4:
                parts.append(row['brand'])
            if random.random() > 0.5 and pd.notna(row['material']):
                parts.append(row['material'])
            input_desc = " ".join(parts).lower() if parts else row['name'].lower()
        
        ground_truth.append({
            "test_id": f"T{len(ground_truth):04d}",
            "product_id": row["product_id"],
            "input_description": input_desc,
            "correct_code": row["code_1"],  # Use code_1 as target
            "category": row["category"],  # For analysis
            "difficulty": ["easy", "medium", "hard"][noise_level]
        })
    
    df = pd.DataFrame(ground_truth)
    print(f"✓ Generated {len(df)} test cases")
    print(f"  - Easy: {len(df[df['difficulty']=='easy'])}")
    print(f"  - Medium: {len(df[df['difficulty']=='medium'])}")
    print(f"  - Hard: {len(df[df['difficulty']=='hard'])}")
    
    return df

def add_quality_issues(df, issue_rate=0.15):
    """Add realistic data quality issues to the catalog."""
    
    print(f"\nAdding data quality issues (rate: {issue_rate*100}%)")
    
    num_issues = int(len(df) * issue_rate)
    issue_indices = random.sample(range(len(df)), num_issues)
    
    for idx in issue_indices:
        issue_type = random.choice([
            "short_description",
            "missing_critical",
            "inconsistent_category",
            "duplicate"
        ])
        
        if issue_type == "short_description":
            df.at[idx, "description"] = df.at[idx, "name"][:20]
        elif issue_type == "missing_critical":
            df.at[idx, "category"] = None
            df.at[idx, "brand"] = None
        elif issue_type == "inconsistent_category":
            df.at[idx, "category"] = random.choice(["Unknown", "Misc", "Other"])
        elif issue_type == "duplicate" and idx > 0:
            # Copy from previous row
            df.at[idx, "description"] = df.at[idx-1, "description"]
    
    print(f"✓ Added {num_issues} quality issues")
    
    return df

def main():
    """Generate all sample data files."""
    
    print("=" * 60)
    print("Sample Data Generator for Embedding Experiment Tool")
    print("=" * 60)
    
    # Generate catalog
    catalog = generate_catalog(num_products=1000)
    
    # Add quality issues
    catalog = add_quality_issues(catalog, issue_rate=0.15)
    
    # Generate ground truth
    ground_truth = generate_ground_truth(catalog, num_samples=100)
    
    # Save files
    print("\nSaving files...")
    catalog.to_excel("sample_catalog.xlsx", index=False)
    print("✓ Saved: sample_catalog.xlsx")
    
    catalog.to_csv("sample_catalog.csv", index=False)
    print("✓ Saved: sample_catalog.csv")
    
    ground_truth.to_excel("sample_ground_truth.xlsx", index=False)
    print("✓ Saved: sample_ground_truth.xlsx")
    
    ground_truth.to_csv("sample_ground_truth.csv", index=False)
    print("✓ Saved: sample_ground_truth.csv")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Catalog: {len(catalog)} products, {len(catalog.columns)} columns")
    print(f"Ground Truth: {len(ground_truth)} test cases")
    print(f"\nData quality:")
    print(f"  - Avg completeness: {catalog.notna().mean().mean()*100:.1f}%")
    print(f"  - Categories: {catalog['category'].nunique()}")
    print(f"  - Brands: {catalog['brand'].nunique()}")
    print(f"  - Materials: {catalog['material'].nunique()}")
    print("\nFiles ready for demo!")
    print("=" * 60)

if __name__ == "__main__":
    main()
