# Ecommerce Project

This is a Django-based Ecommerce application that allows users to browse products, filter by categories, sort by various criteria, search for products, and view product details.

---

## Project Features

1. **Product Listing**:

   - Displays a grid of products with images, names, prices, and stock status.
   - Includes pagination for easy navigation.

2. **Category Filtering**:

   - Users can filter products by categories using a dropdown menu.

3. **Sorting**:

   - Products can be sorted by:
     - Newest
     - Price: Low to High
     - Price: High to Low
     - Name

4. **Search Functionality**:

   - Users can search for products by name or description.

5. **Product Details**:

   - Each product has a detailed view with additional information.

6. **Stock Status**:

   - Displays whether a product is in stock or out of stock.

7. **Add to Cart Button**:

   - Disabled for out-of-stock products.

8. **Pagination**:
   - Allows users to navigate through multiple pages of products.

---

## Project Flow

1. **Homepage**:

   - Displays the product catalog with filtering, sorting, and search options.

2. **Category Filtering**:

   - Users can select a category from the dropdown to filter products.

3. **Sorting**:

   - Users can sort products using the "Sort by" dropdown.

4. **Search**:

   - Users can search for products using the search bar.

5. **Product Details**:

   - Clicking on "View Details" redirects to the product detail page.

6. **Pagination**:
   - Users can navigate between pages using the pagination controls.

---

## How to Run the Project

### Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- A virtual environment (recommended)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ecommerce.git
   cd ecommerce
   ```
2. **Create a Virtual Environment**:

   ````python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate```
   ````

3. **Install Dependencies**:
   `pip install -r requirements.txt`

4.**Apply Migrations**:
`python manage.py makemigrations
python manage.py migrate`

5. Load Sample Data (Optional): If you have a fixture file for sample data, load it:
   python manage.py loaddata sample_data.json

6.**Run the Development Server**:
python manage.py runserver

7. **Access the Application**:
   Open your browser and go to http://127.0.0.1:8000.

Project Structure
Ecommerce/
├── products/
│ ├── migrations/
│ ├── templates/
│ │ ├── home/
│ │ │ ├── product_list.html
│ │ │ ├── product\*detail.html
│ ├── static/
│ │ ├── products/
│ │ │ ├── product_style.css
│ ├── views.py
│ ├── models.py
│ ├── urls.py
├── Ecommerce/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
├── manage.py
├── requirements.txt
