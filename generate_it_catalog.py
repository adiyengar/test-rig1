"""Generate realistic IT product catalog data (Lenovo-style) for input management system."""

import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# IT Product Categories
CATEGORIES = ["Laptop", "Desktop", "Server", "Workstation", "Tablet", "Accessory", "Monitor", "Storage", "Networking"]

# Product Series (Lenovo-style)
LAPTOP_SERIES = ["ThinkPad", "IdeaPad", "Legion", "Yoga", "ThinkBook"]
DESKTOP_SERIES = ["ThinkCentre", "IdeaCentre", "Legion Tower", "ThinkStation"]
SERVER_SERIES = ["ThinkSystem", "System x"]
WORKSTATION_SERIES = ["ThinkStation P", "ThinkStation C"]
TABLET_SERIES = ["Tab", "Yoga Tab", "ThinkPad X1 Tablet"]

# Processors
PROCESSORS = ["Intel Core i5", "Intel Core i7", "Intel Core i9", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", 
              "Intel Xeon", "AMD EPYC"]

# RAM Options
RAM_OPTIONS = [4, 8, 16, 32, 64, 128, 256]

# Storage Options
STORAGE_OPTIONS = [128, 256, 512, 1000, 2000, 4000, 8000]

# Display Sizes
DISPLAY_SIZES = [11.6, 13.3, 14, 15.6, 17.3, 21.5, 24, 27, 32]

# Operating Systems
OS_OPTIONS = ["Windows 11 Pro", "Windows 11 Home", "Windows 10 Pro", "Windows 10 Home", 
              "Ubuntu", "Red Hat", "No OS"]

# Colors
COLORS = ["Black", "Slate Gray", "Mineral Gray", "Iron Gray", "Thunder Black", "Silver"]

# Screen Resolutions
RESOLUTIONS = ["1366x768", "1920x1080", "2560x1440", "3840x2160", "1920x1200"]

def generate_product_id(category, idx):
    """Generate realistic product ID."""
    prefix_map = {
        "Laptop": "LT",
        "Desktop": "DT",
        "Server": "SRV",
        "Workstation": "WS",
        "Tablet": "TAB",
        "Accessory": "ACC",
        "Monitor": "MON",
        "Storage": "STO",
        "Networking": "NET"
    }
    prefix = prefix_map.get(category, "PRD")
    return f"{prefix}-{idx:06d}"

def generate_product_name(category, series, idx):
    """Generate realistic product name."""
    model_number = random.randint(100, 9999)
    if category == "Laptop":
        series_choice = random.choice(LAPTOP_SERIES)
        return f"Lenovo {series_choice} {model_number}"
    elif category == "Desktop":
        series_choice = random.choice(DESKTOP_SERIES)
        return f"Lenovo {series_choice} {model_number}"
    elif category == "Server":
        series_choice = random.choice(SERVER_SERIES)
        return f"Lenovo {series_choice} {model_number}"
    elif category == "Workstation":
        series_choice = random.choice(WORKSTATION_SERIES)
        return f"Lenovo {series_choice} {model_number}"
    elif category == "Tablet":
        series_choice = random.choice(TABLET_SERIES)
        return f"Lenovo {series_choice} {model_number}"
    else:
        return f"Lenovo {category} {model_number}"

def generate_description(product_name, category, processor, ram, storage, display_size=None):
    """Generate realistic product description."""
    base_desc = f"{product_name} - "
    
    if category == "Laptop":
        display_info = f"{display_size}\" display, " if display_size else ""
        desc = f"{base_desc}Premium business laptop with {processor} processor, {ram}GB RAM, {storage}GB SSD storage, {display_info}long battery life, lightweight design, ideal for professionals."
    elif category == "Desktop":
        desc = f"{base_desc}Powerful desktop computer with {processor} processor, {ram}GB RAM, {storage}GB HDD, compact tower design, perfect for office and home use."
    elif category == "Server":
        desc = f"{base_desc}Enterprise-grade server with {processor} processor, {ram}GB ECC RAM, {storage}GB storage, rack-mountable, designed for data center deployment."
    elif category == "Workstation":
        desc = f"{base_desc}Professional workstation with {processor} processor, {ram}GB RAM, {storage}GB SSD, powerful graphics capabilities, optimized for CAD and content creation."
    elif category == "Tablet":
        display_info = f"{display_size}\" display, " if display_size else ""
        desc = f"{base_desc}Versatile tablet with {display_info}long battery life, lightweight design, perfect for mobile productivity."
    else:
        desc = f"{base_desc}High-quality {category.lower()} product from Lenovo."
    
    return desc

def generate_it_catalog(num_products=500):
    """Generate a sample IT product catalog."""
    print(f"Generating IT product catalog with {num_products} products...")
    
    products = []
    
    for i in range(num_products):
        category = random.choices(
            CATEGORIES,
            weights=[30, 20, 10, 5, 8, 15, 5, 4, 3]  # More laptops and desktops
        )[0]
        
        # Get appropriate series for category
        if category == "Laptop":
            series = random.choice(LAPTOP_SERIES)
        elif category == "Desktop":
            series = random.choice(DESKTOP_SERIES)
        elif category == "Server":
            series = random.choice(SERVER_SERIES)
        elif category == "Workstation":
            series = random.choice(WORKSTATION_SERIES)
        elif category == "Tablet":
            series = random.choice(TABLET_SERIES)
        else:
            series = category
        
        product_id = generate_product_id(category, i+1)
        product_name = generate_product_name(category, series, i+1)
        
        # Technical specs
        processor = random.choice(PROCESSORS)
        ram = random.choice(RAM_OPTIONS)
        storage = random.choice(STORAGE_OPTIONS)
        
        display_size = random.choice(DISPLAY_SIZES) if category in ["Laptop", "Tablet", "Monitor"] else None
        os = random.choice(OS_OPTIONS)
        color = random.choice(COLORS) if category in ["Laptop", "Desktop", "Tablet"] else "N/A"
        resolution = random.choice(RESOLUTIONS) if category in ["Laptop", "Monitor", "Tablet"] else "N/A"
        
        # Generate description
        description = generate_description(product_name, category, processor, ram, storage, display_size)
        
        # Additional attributes
        weight = round(random.uniform(0.5, 8.0), 2) if category in ["Laptop", "Tablet"] else round(random.uniform(5.0, 50.0), 2)
        warranty_years = random.choice([1, 2, 3, 5])
        price_range = random.choice(["Budget", "Mid-range", "Premium", "Enterprise"])
        
        # Form factor
        if category == "Laptop":
            form_factor = random.choice(["Clamshell", "2-in-1", "Convertible"])
        elif category == "Desktop":
            form_factor = random.choice(["Tower", "SFF", "USFF", "All-in-One"])
        else:
            form_factor = "Standard"
        
        # Connectivity
        connectivity = random.choice(["Wi-Fi 6", "Wi-Fi 6E", "Ethernet", "Wi-Fi 6 + Ethernet"])
        ports = random.choice(["USB-C, USB-A, HDMI", "USB-A, HDMI, Ethernet", "Thunderbolt 4, USB-C", "USB-A, DisplayPort"])
        
        # Graphics
        if category in ["Laptop", "Desktop", "Workstation"]:
            graphics = random.choice(["Integrated", "NVIDIA GeForce", "AMD Radeon", "NVIDIA Quadro", "NVIDIA RTX"])
        else:
            graphics = "N/A"
        
        # Battery life (for laptops/tablets)
        battery_life = random.randint(6, 24) if category in ["Laptop", "Tablet"] else None
        
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "description": description,
            "category": category,
            "series": series,
            "brand": "Lenovo",
            "processor": processor,
            "ram_gb": ram,
            "storage_gb": storage,
            "display_size_inches": display_size if display_size else None,
            "display_resolution": resolution,
            "operating_system": os,
            "color": color,
            "weight_kg": weight,
            "warranty_years": warranty_years,
            "price_range": price_range,
            "form_factor": form_factor,
            "connectivity": connectivity,
            "ports": ports,
            "graphics": graphics,
            "battery_life_hours": battery_life,
            "release_year": random.randint(2020, 2024),
            "availability": random.choice(["In Stock", "Out of Stock", "Pre-order", "Discontinued"]),
            "target_market": random.choice(["Consumer", "Business", "Enterprise", "Education", "Gaming"]),
            "certification": random.choice(["Energy Star", "EPEAT", "TCO Certified", "RoHS", "None"]),
            "warranty_type": random.choice(["Standard", "On-site", "Premium Care", "Accident Protection"]),
            "country_of_origin": random.choice(["China", "Mexico", "USA", "Hungary"]),
            "model_number": product_name.split()[-1] if len(product_name.split()) > 1 else f"{random.randint(1000, 9999)}",
            "sku": f"SKU-{random.randint(100000, 999999)}",
            "ean": f"{random.randint(1000000000000, 9999999999999)}",
            "product_line": series,
            "generation": random.choice(["Gen 1", "Gen 2", "Gen 3", "Gen 4", "Gen 5"]),
            "material": random.choice(["Aluminum", "Carbon Fiber", "Plastic", "Magnesium Alloy", "Metal"]),
            "dimensions": f"{random.randint(30, 40)}cm x {random.randint(20, 30)}cm x {random.randint(2, 5)}cm",
            "screen_type": random.choice(["IPS", "OLED", "LCD", "TN", "VA"]) if display_size else "N/A",
            "touchscreen": random.choice([True, False]) if category in ["Laptop", "Tablet"] else False,
            "webcam": random.choice(["720p", "1080p", "5MP", "None"]),
            "keyboard": random.choice(["Backlit", "Standard", "Mechanical", "N/A"]),
            "fingerprint_reader": random.choice([True, False]),
            "face_recognition": random.choice([True, False]),
            "security_chip": random.choice(["TPM 2.0", "TPM 1.2", "None"]),
            "docking_compatible": random.choice([True, False]) if category in ["Laptop"] else False,
        }
        
        products.append(product)
    
    df = pd.DataFrame(products)
    return df

if __name__ == "__main__":
    # Generate catalog
    catalog_df = generate_it_catalog(num_products=500)
    
    # Save to CSV
    output_file = "sample_it_catalog.csv"
    catalog_df.to_csv(output_file, index=False)
    print(f"\n✅ Generated {len(catalog_df)} products")
    print(f"✅ Saved to: {output_file}")
    print(f"\nColumns ({len(catalog_df.columns)}):")
    for col in catalog_df.columns:
        print(f"  - {col}")
    
    print(f"\nSample products:")
    print(catalog_df[["product_id", "product_name", "category", "processor", "ram_gb", "storage_gb"]].head(10).to_string())
