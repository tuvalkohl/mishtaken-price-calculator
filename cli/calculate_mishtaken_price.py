#!/usr/bin/env python3
"""
Apartment Price Calculator with Discount System
Calculates apartment prices according to 'Dira Behanaha' discount rules.

Usage:
    python apartment_calculator.py --main-price 25000 --current-price 23000
    python apartment_calculator.py --main-price 25000 --current-price 23000 --apartment-size 100 --area-type periphery
"""

import argparse
import sys

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
    storage_effective = storage_room_size * 0.4 # 40%
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
        discount_type = "capped"
    else:
        # Use 25% discount
        final_discounted_price = discounted_main_price
        actual_discount = potential_discount
        discount_type = "25_percent"
    
    # Step 7: Determine final price (lower of discounted price and main price)
    final_price = min(final_discounted_price, main_total_price)
    
    # Calculate actual discount applied
    if final_price == main_total_price:
        actual_discount = current_total_price - main_total_price
        discount_type = "main_price_limit"
    
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
            "apartment": f"{apartment_size} sqm × 100% = {apartment_effective} effective sqm",
            "balcony": f"{balcony_size} sqm × 30% = {balcony_effective} effective sqm",
            "storage": f"{storage_room_size} sqm × 40% = {storage_effective} effective sqm",
            "parking": f"{parking_spaces} spaces × 200% = {parking_effective} effective sqm",
            "total_effective_area": f"{total_effective_area} sqm"
        },
        "price_calculations": {
            "main_total_price": f"₪{main_total_price:,.2f}",
            "current_total_price": f"₪{current_total_price:,.2f}",
            "25_percent_discount": f"₪{main_total_price * 0.25:,.2f}",
            "discounted_main_price": f"₪{discounted_main_price:,.2f}",
            "potential_discount": f"₪{potential_discount:,.2f}",
            "max_allowed_discount": f"₪{max_discount:,.2f}",
            "discount_type": discount_type
        }
    }
    
    return {
        "final_price_including_vat": final_price,
        "discount_amount": actual_discount,
        "effective_area": total_effective_area,
        "calculation_details": calculation_details
    }


def print_calculation_summary(result):
    """Print a formatted summary of the calculation results."""
    print("=" * 60)
    print("APARTMENT PRICE CALCULATION SUMMARY")
    print("=" * 60)
    
    print(f"\nFINAL PRICE: ₪{result['final_price_including_vat']:,.2f}")
    print(f"TOTAL DISCOUNT: ₪{result['discount_amount']:,.2f}")
    print(f"EFFECTIVE AREA: {result['effective_area']} sqm")
    
    details = result['calculation_details']
    
    print("\n--- PRICES PER METER ---")
    for key, value in details['prices_per_meter'].items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: ₪{value:,.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n--- AREA BREAKDOWN ---")
    for key, value in details['area_breakdown'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n--- PRICE CALCULATIONS ---")
    for key, value in details['price_calculations'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")


def main():
    """Main function to handle command line arguments and run the calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate apartment prices according to 'Dira Behanaha' discount rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --main-price 25000 --current-price 23000
  %(prog)s --main-price 25000 --current-price 23000 --apartment-size 100 --area-type periphery
  %(prog)s --main-price 30000 --current-price 28000 --balcony-size 15 --parking-spaces 1
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--main-price", 
        type=float, 
        required=True,
        help="Main price per square meter (excluding VAT)"
    )
    parser.add_argument(
        "--current-price", 
        type=float, 
        required=True,
        help="Current price per square meter (excluding VAT)"
    )
    
    # Optional arguments with defaults
    parser.add_argument(
        "--apartment-size", 
        type=float, 
        default=125,
        help="Apartment size in square meters (default: 125)"
    )
    parser.add_argument(
        "--balcony-size", 
        type=float, 
        default=12,
        help="Balcony size in square meters (default: 12)"
    )
    parser.add_argument(
        "--storage-size", 
        type=float, 
        default=6,
        help="Storage room size in square meters (default: 6)"
    )
    parser.add_argument(
        "--parking-spaces", 
        type=int, 
        default=2,
        help="Number of parking spaces (default: 2)"
    )
    parser.add_argument(
        "--area-type", 
        type=str, 
        choices=["demand", "periphery"],
        default="demand",
        help="Area type: 'demand' or 'periphery' (default: demand)"
    )
    parser.add_argument(
        "--vat-rate", 
        type=float, 
        default=18.0,
        help="VAT rate as percentage (default: 18.0)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show final price and discount (no detailed breakdown)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.main_price <= 0 or args.current_price <= 0:
        print("Error: Prices must be positive numbers", file=sys.stderr)
        sys.exit(1)
    
    if args.apartment_size <= 0:
        print("Error: Apartment size must be positive", file=sys.stderr)
        sys.exit(1)
    
    if args.vat_rate < 0:
        print("Error: VAT rate cannot be negative", file=sys.stderr)
        sys.exit(1)
    
    # Convert VAT rate from percentage to decimal
    vat_rate_decimal = args.vat_rate / 100.0
    
    try:
        # Calculate the apartment price
        result = calculate_apartment_price(
            main_price_per_meter=args.main_price,
            current_price_per_meter=args.current_price,
            apartment_size=args.apartment_size,
            balcony_size=args.balcony_size,
            storage_room_size=args.storage_size,
            parking_spaces=args.parking_spaces,
            area_type=args.area_type,
            vat_rate=vat_rate_decimal
        )
        
        if args.quiet:
            print(f"Final Price: ₪{result['final_price_including_vat']:,.2f}")
            print(f"Total Discount: ₪{result['discount_amount']:,.2f}")
        else:
            print_calculation_summary(result)
            
    except Exception as e:
        print(f"Error during calculation: {e}", file=sys.stderr)
        sys.exit(1)


# Example usage
if __name__ == "__main__":
    # Check if script is being run with command line arguments
    if len(sys.argv) > 1:
        main()
    else:
        # Run example calculations if no arguments provided
        print("No command line arguments provided. Running examples...\n")
        
        # Example calculation
        result = calculate_apartment_price(
            main_price_per_meter=25000,      # ₪25,000 per sqm excluding VAT
            current_price_per_meter=23000,   # ₪23,000 per sqm excluding VAT
            apartment_size=125,              # 125 sqm apartment
            balcony_size=12,                 # 12 sqm balcony
            storage_room_size=6,             # 6 sqm storage
            parking_spaces=2,                # 2 parking spaces
            area_type="demand",              # Demand area
            vat_rate=0.18                    # 18% VAT
        )
        
        print_calculation_summary(result)
        
        print("\n" + "=" * 60)
        print("TESTING WITH PERIPHERY AREA")
        print("=" * 60)
        
        # Test with periphery area (higher discount limit)
        result_periphery = calculate_apartment_price(
            main_price_per_meter=25000,
            current_price_per_meter=23000,
            area_type="periphery"
        )
        
        print_calculation_summary(result_periphery)
        
        print("\n" + "=" * 60)
        print("COMMAND LINE USAGE EXAMPLES:")
        print("=" * 60)
        print("python apartment_calculator.py --main-price 25000 --current-price 23000")
        print("python apartment_calculator.py --main-price 25000 --current-price 23000 --apartment-size 100 --area-type periphery")
        print("python apartment_calculator.py --main-price 30000 --current-price 28000 --balcony-size 15 --parking-spaces 1 --quiet")
        print("python apartment_calculator.py --help  # For full help")
