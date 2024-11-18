# GeoEgy Backend

## Overview
GeoEgy Backend is a Flask-based backend application for managing orders and places.

## Features
- User authentication and profile management
- Place searching and order placement
- Admin functionalities for order management

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/your-username/geoegy-backend.git
   cd geoegy-backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Ensure SQLite is installed.
   - Initialize the database:
     ```
     python run.py
     ```

## Configuration
- Update `config.py` for any necessary configuration changes.

## Usage
1. Run the application:
   ```
   python run.py
   ```
2. Access the API:
   - Endpoint documentation:
     - `/order/place` (POST): Place a new order.
     - `/order/get_orders?phone_number=<phone_number>` (GET): Get orders for a user.
     - `/order/accept_order/<order_id>` (POST): Accept an order (admin only).
     - `/place/search?query=<query>` (GET): Search for places.
     - `/user/login` (POST): Login or create a user.
     - `/user/get_profile?phone_number=<phone_number>` (GET): Get user profile.

## Contributing
- Fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
