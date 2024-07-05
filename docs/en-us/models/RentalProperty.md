# RentalProperty Model Description

### Model: RentalProperty

- **uuid**: Unique identifier for the property (primary key, required, auto-generated)
- **name**: Name of the property (required)
- **description**: Short description of the property (required)
- **detailed_description**: Detailed description of the property (required)
- **landlord**: Landlord of the property (reference to User's google_id, required)
- **furniture**: Furniture included in the property (required, list, e.g., Refrigerator, Air Conditioner)
- **amenities**: Amenities available in the community (required, list, e.g., Elevator, Carriage, Water dispenser)
- **address**: Address of the property (required)
- **floor_info**: Floor information (required, e.g., "3/5")
- **rent_price**: Rent price (required)
- **negotiation**: Negotiation details (required, includes whether allowed, min and max price range)
- **property_type**: Property type (required, choices: [Entire Place, Studio, Room])
- **layout**: Layout of the property (required, choices: [1 Room, 2 Rooms, 3 Rooms, 4 Rooms])
- **allowances**: Allowances (required, includes whether pets are allowed and additional fee, whether parking is available and additional fee)
- **features**: Features (required, list, e.g., whether cooking is allowed, whether pets are allowed, whether there is a balcony)
- **building_type**: Building type (required, choices: [Apartment, Elevator Building, Townhouse, Villa])
- **area**: Area in square meters (required)
- **rent_includes**: What the rent includes (required, includes electricity, water, internet, management fee, etc.)
- **decoration_style**: Decoration style (required)
- **tenant_preferences**: Tenant preferences (required, multi-select list, e.g., Male Only, Female Only, No Nightlife Industry, Students Only, Professionals Only, Others)
- **community**: Community name (required, or enter None)
- **min_lease_months**: Minimum lease months (required)
- **has_balcony**: Whether the property has a balcony (required)
- **bathroom_info**: Bathroom information (optional)
- **building_age**: Building age (optional)
- **tags**: Tags (required, list)
- **created_at**: Creation time (required, auto-set to current time)
- **images**: Images of the property (required, list, including URL and title)
- **view_count**: Total view count of the property (required, default 0)
- **last_updated_at**: Last updated time (required, auto-set to current time)
- **last_pushed_at**: Last pushed time (optional)

### Submodels

#### Negotiation
- **allow**: Whether negotiation is allowed (required)
- **min_price**: Minimum negotiation price (required)
- **max_price**: Maximum negotiation price (required)

#### Allowance
- **allow**: Whether allowed (required)
- **additional_fee**: Additional fee (required)

#### RentIncludes
- **electric**: Electric fee details (required, includes whether it's from TaiPower, price per unit)
- **internet**: Internet details (required, includes whether included in rent, upload/download speed, additional fee)
- **water**: Water fee details (required, includes whether included in rent, additional fee)
- **management_fee**: Management fee details (required, includes whether included in rent, additional fee)

###### Electric
- **tai_power**: Whether it's from TaiPower (required)
- **price_per_unit**: Price per unit (required)

###### Internet
- **included**: Whether included in rent (required)
- **upload_speed**: Upload speed (required)
- **download_speed**: Download speed (required)
- **additional_fee**: Additional fee (required)

###### Water
- **included**: Whether included in rent (required)
- **additional_fee**: Additional fee (required)

###### ManagementFee
- **included**: Whether included in rent (required)
- **additional_fee**: Additional fee (required)

#### Image
- **url**: Image URL (required)
- **title**: Image title (required)