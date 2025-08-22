#!/usr/bin/env python3
"""
Streamlit Apartment Price Calculator
A web application for calculating apartment prices with Israeli real estate discount system.

To run:
    pip install streamlit
    streamlit run apartment_calculator_app.py
"""

import streamlit as st
import pandas as pd

def calculate_apartment_price(
    main_price_per_meter,
    current_price_per_meter,
    apartment_size=125,
    balcony_size=12,
    storage_room_size=6,
    parking_spaces=2,
    area_type="demand",
    vat_rate=0.18
):
    """
    Calculate apartment price with discount system.
    
    Args:
        main_price_per_meter (float): Main price per square meter (excluding VAT)
        current_price_per_meter (float): Current price per square meter (excluding VAT)
        apartment_size (float): Apartment size in square meters (default: 125)
        balcony_size (float): Balcony size in square meters (default: 12)
        storage_room_size (float): Storage room size in square meters (default: 6)
        parking_spaces (int): Number of parking spaces (default: 2)
        area_type (str): Area type - "demand" or "periphery" (default: "demand")
        vat_rate (float): VAT rate as decimal (default: 0.18 for 18%)
    
    Returns:
        dict: Dictionary containing final price, discount amount, effective area, and calculation details
    """
    
    # Step 1: Add VAT to price per meter
    main_price_with_vat = main_price_per_meter * (1 + vat_rate)
    current_price_with_vat = current_price_per_meter * (1 + vat_rate)
    
    # Step 2: Calculate effective area
    apartment_effective = apartment_size * 1.0  # 100%
    balcony_effective = balcony_size * 0.3      # 30%
    storage_effective = storage_room_size * 0.4  # 40%
    parking_effective = parking_spaces * 2.0    # 200% (2 sqm per space)
    
    total_effective_area = apartment_effective + balcony_effective + storage_effective + parking_effective
    
    # Step 3: Calculate base prices using effective area (with VAT already included)
    main_total_price = main_price_with_vat * total_effective_area
    current_total_price = current_price_with_vat * total_effective_area
    
    # Step 4: Apply 25% discount to main price
    discounted_main_price = main_total_price * 0.75
    
    # Step 5: Check discount limitations
    potential_discount = current_total_price - discounted_main_price
    
    # Set discount limit based on area type
    if area_type.lower() == "periphery":
        max_discount = 600000
    else:  # demand area
        max_discount = 500000
    
    # Step 6: Apply discount cap if needed
    if potential_discount > max_discount:
        # Use maximum allowed discount
        final_discounted_price = current_total_price - max_discount
        actual_discount = max_discount
        discount_type = "Capped at Maximum"
    else:
        # Use 25% discount
        final_discounted_price = discounted_main_price
        actual_discount = potential_discount
        discount_type = "25% Discount Applied"
    
    # Step 7: Determine final price (lower of discounted price and main price)
    final_price = min(final_discounted_price, main_total_price)
    
    # Calculate actual discount applied
    if final_price == main_total_price:
        actual_discount = current_total_price - main_total_price
        discount_type = "Limited by Main Price"
    
    # Prepare detailed calculation breakdown
    calculation_details = {
        "prices_per_meter": {
            "main_excluding_vat": main_price_per_meter,
            "main_including_vat": main_price_with_vat,
            "current_excluding_vat": current_price_per_meter,
            "current_including_vat": current_price_with_vat,
            "vat_rate": f"{vat_rate * 100}%"
        },
        "area_breakdown": {
            "apartment": apartment_effective,
            "balcony": balcony_effective,
            "storage": storage_effective,
            "parking": parking_effective,
            "total_effective_area": total_effective_area
        },
        "price_calculations": {
            "main_total_price": main_total_price,
            "current_total_price": current_total_price,
            "discount_25_percent": main_total_price * 0.25,
            "discounted_main_price": discounted_main_price,
            "potential_discount": potential_discount,
            "max_allowed_discount": max_discount,
            "discount_type": discount_type
        }
    }
    
    return {
        "final_price_including_vat": final_price,
        "discount_amount": actual_discount,
        "effective_area": total_effective_area,
        "calculation_details": calculation_details
    }



def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Apartment Price Calculator",
        page_icon="🏠",
        layout="wide"
    )
    
    st.title("🏠 Mehir Lamishtaken (החנחב הריד) Price Calculator")
    st.markdown("Calculate apartment price according to 'Dira Behanaha' weird discount system")
    
    # Sidebar for inputs
    st.sidebar.header("📊 Input Parameters")
    
    # Required inputs
    st.sidebar.subheader("Price per Square Meter (excluding VAT)")
    main_price = st.sidebar.number_input(
        "Main Price per m² (₪)",
        min_value=1000,
        max_value=100000,
        value=25000,
        step=500,
        help="Maximum price that can be charged per square meter"
    )
    
    current_price = st.sidebar.number_input(
        "Current Price per m² (₪)",
        min_value=1000,
        max_value=100000,
        value=23000,
        step=500,
        help="Current market price per square meter"
    )
    
    # Area inputs
    st.sidebar.subheader("🏗️ Property Details")
    apartment_size = st.sidebar.slider(
        "Apartment Size (m²)",
        min_value=30,
        max_value=300,
        value=125,
        step=5
    )
    
    balcony_size = st.sidebar.slider(
        "Balcony Size (m²)",
        min_value=0,
        max_value=50,
        value=12,
        step=1
    )
    
    storage_size = st.sidebar.slider(
        "Storage Room Size (m²)",
        min_value=0,
        max_value=20,
        value=6,
        step=1
    )
    
    parking_spaces = st.sidebar.selectbox(
        "Number of Parking Spaces",
        options=[0, 1, 2, 3, 4],
        index=2  # default to 2
    )
    
    # Other parameters
    st.sidebar.subheader("⚙️ Other Parameters")
    area_type = st.sidebar.selectbox(
        "Area Type",
        options=["demand", "periphery"],
        index=0,
        help="Demand areas have 500K discount limit, periphery areas have 600K limit"
    )
    
    vat_rate = st.sidebar.slider(
        "VAT Rate (%)",
        min_value=0.0,
        max_value=25.0,
        value=18.0,
        step=0.5
    )
    
    # Calculate results
    try:
        result = calculate_apartment_price(
            main_price_per_meter=main_price,
            current_price_per_meter=current_price,
            apartment_size=apartment_size,
            balcony_size=balcony_size,
            storage_room_size=storage_size,
            parking_spaces=parking_spaces,
            area_type=area_type,
            vat_rate=vat_rate / 100.0
        )
        
        # Main results display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💰 Final Price",
                f"₪{result['final_price_including_vat']:,.0f}",
                f"-₪{result['discount_amount']:,.0f}"
            )
        
        with col2:
            st.metric(
                "📐 Effective Area",
                f"{result['effective_area']} m²",
                f"vs {apartment_size} m² actual"
            )
        
        with col3:
            discount_percent = (result['discount_amount'] / result['calculation_details']['price_calculations']['current_total_price']) * 100
            st.metric(
                "💸 Total Discount",
                f"₪{result['discount_amount']:,.0f}",
                f"{discount_percent:.1f}%"
            )
        
        # Price Comparison Section
        st.subheader("💰 Price Comparison")
        col1, col2, col3 = st.columns(3)
        
        details = result['calculation_details']['price_calculations']
        
        with col1:
            st.info(f"**Current Price**\n₪{details['current_total_price']:,.0f}")
        with col2:
            st.warning(f"**Main Price**\n₪{details['main_total_price']:,.0f}")
        with col3:
            st.success(f"**Final Price**\n₪{result['final_price_including_vat']:,.0f}")
        
        # Create simple bar chart data with separate rows
        price_data = pd.DataFrame({
            'Price Type': ['Current Price', 'Main Price', 'Final Price'],
            'Amount': [details['current_total_price'], details['main_total_price'], result['final_price_including_vat']]
        })
        price_data = price_data.set_index('Price Type')
        st.bar_chart(price_data)
        
        # Area Breakdown Section
        st.subheader("📐 Area Breakdown")
        
        area_details = result['calculation_details']['area_breakdown']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏠 Apartment", f"{area_details['apartment']:.1f} m²")
        with col2:
            st.metric("🌿 Balcony", f"{area_details['balcony']:.1f} m²")
        with col3:
            st.metric("📦 Storage", f"{area_details['storage']:.1f} m²")
        with col4:
            st.metric("🚗 Parking", f"{area_details['parking']:.1f} m²")
        
        # Create area chart with separate rows
        area_data = pd.DataFrame({
            'Component': ['Apartment', 'Balcony', 'Storage', 'Parking'],
            'Effective Area': [area_details['apartment'], area_details['balcony'], area_details['storage'], area_details['parking']]
        })
        area_data = area_data.set_index('Component')
        st.bar_chart(area_data)
        
        # Detailed breakdown
        with st.expander("📋 Detailed Calculation Breakdown", expanded=False):
            details = result['calculation_details']
            
            # Price per meter details
            st.subheader("Price per Square Meter")
            price_df = pd.DataFrame([
                {"Type": "Main Price (excl. VAT)", "Value": f"₪{details['prices_per_meter']['main_excluding_vat']:,.0f}"},
                {"Type": "Main Price (incl. VAT)", "Value": f"₪{details['prices_per_meter']['main_including_vat']:,.0f}"},
                {"Type": "Current Price (excl. VAT)", "Value": f"₪{details['prices_per_meter']['current_excluding_vat']:,.0f}"},
                {"Type": "Current Price (incl. VAT)", "Value": f"₪{details['prices_per_meter']['current_including_vat']:,.0f}"},
            ])
            st.table(price_df)
            
            # Area breakdown
            st.subheader("Area Breakdown")
            area_df = pd.DataFrame([
                {"Component": "Apartment", "Actual Size": f"{apartment_size} m²", "Weight": "100%", "Effective Size": f"{details['area_breakdown']['apartment']:.1f} m²"},
                {"Component": "Balcony", "Actual Size": f"{balcony_size} m²", "Weight": "30%", "Effective Size": f"{details['area_breakdown']['balcony']:.1f} m²"},
                {"Component": "Storage", "Actual Size": f"{storage_size} m²", "Weight": "40%", "Effective Size": f"{details['area_breakdown']['storage']:.1f} m²"},
                {"Component": "Parking", "Actual Size": f"{parking_spaces} spaces", "Weight": "200%", "Effective Size": f"{details['area_breakdown']['parking']:.1f} m²"},
            ])
            st.table(area_df)
            
            # Price calculations
            st.subheader("Price Calculations")
            calc_df = pd.DataFrame([
                {"Step": "Current Total Price", "Amount": f"₪{details['price_calculations']['current_total_price']:,.0f}"},
                {"Step": "Main Total Price", "Amount": f"₪{details['price_calculations']['main_total_price']:,.0f}"},
                {"Step": "25% Discount Amount", "Amount": f"₪{details['price_calculations']['discount_25_percent']:,.0f}"},
                {"Step": "Max Allowed Discount", "Amount": f"₪{details['price_calculations']['max_allowed_discount']:,.0f}"},
                {"Step": "Applied Discount", "Amount": f"₪{result['discount_amount']:,.0f}"},
                {"Step": "Discount Type", "Amount": details['price_calculations']['discount_type']},
            ])
            st.table(calc_df)
        
        # Export options
        st.subheader("📤 Export Results")
        
        # Create summary for export
        summary_data = {
            "Parameter": [
                "Main Price per m² (excl. VAT)",
                "Current Price per m² (excl. VAT)",
                "Apartment Size",
                "Balcony Size", 
                "Storage Size",
                "Parking Spaces",
                "Area Type",
                "VAT Rate",
                "Effective Area",
                "Final Price",
                "Total Discount"
            ],
            "Value": [
                f"₪{main_price:,}",
                f"₪{current_price:,}",
                f"{apartment_size} m²",
                f"{balcony_size} m²",
                f"{storage_size} m²",
                str(parking_spaces),
                area_type.title(),
                f"{vat_rate}%",
                f"{result['effective_area']} m²",
                f"₪{result['final_price_including_vat']:,.0f}",
                f"₪{result['discount_amount']:,.0f}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        
        col1, col2 = st.columns(2)
        with col1:
            csv = summary_df.to_csv(index=False)
            st.download_button(
                "📄 Download as CSV",
                csv,
                "apartment_calculation.csv",
                "text/csv"
            )
        
        with col2:
            # Show the summary table
            st.write("**Calculation Summary:**")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"Error in calculation: {str(e)}")
        st.info("Please check your input values and try again.")

if __name__ == "__main__":
    main()
