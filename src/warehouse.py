#!/usr/bin/env python3
"""
Cloud Data Warehouse
Modern cloud-based data warehouse solution with ETL capabilities and analytics.
"""

import sqlite3
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import random

app = Flask(__name__, static_folder='../docs', static_url_path='/')

class CloudDataWarehouse:
    """Cloud data warehouse implementation with analytics capabilities."""
    
    def __init__(self, db_path="warehouse.db"):
        self.db_path = db_path
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """Initialize the data warehouse database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create dimension tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                email TEXT,
                country TEXT,
                segment TEXT,
                created_date DATE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                subcategory TEXT,
                price DECIMAL(10,2),
                cost DECIMAL(10,2)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_time (
                date_id INTEGER PRIMARY KEY,
                date DATE,
                year INTEGER,
                quarter INTEGER,
                month INTEGER,
                day INTEGER,
                weekday TEXT
            )
        """)
        
        # Create fact table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                sale_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                date_id INTEGER,
                quantity INTEGER,
                revenue DECIMAL(10,2),
                profit DECIMAL(10,2),
                FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
                FOREIGN KEY (date_id) REFERENCES dim_time(date_id)
            )
        """)
        
        # Create data quality monitoring table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_quality_metrics (
                metric_id INTEGER PRIMARY KEY,
                table_name TEXT,
                metric_name TEXT,
                metric_value REAL,
                threshold_value REAL,
                status TEXT,
                check_date DATETIME
            )
        """)
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """Load sample data for demonstration."""
        conn = sqlite3.connect(self.db_path)
        
        # Check if data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dim_customers")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample customers
        customers = [
            (1, "John Smith", "john@email.com", "USA", "Enterprise", "2023-01-15"),
            (2, "Maria Garcia", "maria@email.com", "Spain", "SMB", "2023-02-20"),
            (3, "Li Wei", "li@email.com", "China", "Enterprise", "2023-01-10"),
            (4, "Ahmed Hassan", "ahmed@email.com", "Egypt", "Consumer", "2023-03-05"),
            (5, "Sarah Johnson", "sarah@email.com", "Canada", "SMB", "2023-01-25")
        ]
        
        cursor.executemany("""
            INSERT INTO dim_customers (customer_id, customer_name, email, country, segment, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, customers)
        
        # Sample products
        products = [
            (1, "Laptop Pro", "Electronics", "Computers", 1299.99, 800.00),
            (2, "Smartphone X", "Electronics", "Mobile", 899.99, 500.00),
            (3, "Office Chair", "Furniture", "Seating", 299.99, 150.00),
            (4, "Desk Lamp", "Furniture", "Lighting", 79.99, 30.00),
            (5, "Wireless Mouse", "Electronics", "Accessories", 49.99, 20.00)
        ]
        
        cursor.executemany("""
            INSERT INTO dim_products (product_id, product_name, category, subcategory, price, cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """, products)
        
        # Generate time dimension for last 90 days
        start_date = datetime.now() - timedelta(days=90)
        for i in range(90):
            current_date = start_date + timedelta(days=i)
            cursor.execute("""
                INSERT INTO dim_time (date_id, date, year, quarter, month, day, weekday)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                int(current_date.strftime("%Y%m%d")),
                current_date.strftime("%Y-%m-%d"),
                current_date.year,
                (current_date.month - 1) // 3 + 1,
                current_date.month,
                current_date.day,
                current_date.strftime("%A")
            ))
        
        # Generate sample sales data
        for i in range(200):
            sale_date = start_date + timedelta(days=random.randint(0, 89))
            date_id = int(sale_date.strftime("%Y%m%d"))
            customer_id = random.randint(1, 5)
            product_id = random.randint(1, 5)
            quantity = random.randint(1, 5)
            
            # Get product price and cost
            cursor.execute("SELECT price, cost FROM dim_products WHERE product_id = ?", (product_id,))
            price, cost = cursor.fetchone()
            
            revenue = price * quantity
            profit = (price - cost) * quantity
            
            cursor.execute("""
                INSERT INTO fact_sales (customer_id, product_id, date_id, quantity, revenue, profit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_id, product_id, date_id, quantity, revenue, profit))
        
        conn.commit()
        conn.close()
    
    def get_sales_analytics(self):
        """Get sales analytics and KPIs."""
        conn = sqlite3.connect(self.db_path)
        
        # Total revenue and profit
        query = """
            SELECT 
                SUM(revenue) as total_revenue,
                SUM(profit) as total_profit,
                COUNT(*) as total_transactions,
                AVG(revenue) as avg_transaction_value
            FROM fact_sales
        """
        
        df = pd.read_sql_query(query, conn)
        kpis = df.iloc[0].to_dict()
        
        # Sales by category
        query = """
            SELECT 
                p.category,
                SUM(s.revenue) as revenue,
                SUM(s.quantity) as quantity
            FROM fact_sales s
            JOIN dim_products p ON s.product_id = p.product_id
            GROUP BY p.category
            ORDER BY revenue DESC
        """
        
        category_sales = pd.read_sql_query(query, conn).to_dict('records')
        
        # Sales by country
        query = """
            SELECT 
                c.country,
                SUM(s.revenue) as revenue,
                COUNT(DISTINCT s.customer_id) as customers
            FROM fact_sales s
            JOIN dim_customers c ON s.customer_id = c.customer_id
            GROUP BY c.country
            ORDER BY revenue DESC
        """
        
        country_sales = pd.read_sql_query(query, conn).to_dict('records')
        
        # Monthly trends
        query = """
            SELECT 
                t.year,
                t.month,
                SUM(s.revenue) as revenue,
                SUM(s.profit) as profit
            FROM fact_sales s
            JOIN dim_time t ON s.date_id = t.date_id
            GROUP BY t.year, t.month
            ORDER BY t.year, t.month
        """
        
        monthly_trends = pd.read_sql_query(query, conn).to_dict('records')
        
        conn.close()
        
        return {
            'kpis': kpis,
            'category_sales': category_sales,
            'country_sales': country_sales,
            'monthly_trends': monthly_trends
        }
    
    def run_data_quality_checks(self):
        """Run data quality checks and store results."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear previous checks
        cursor.execute("DELETE FROM data_quality_metrics")
        
        checks = []
        
        # Check for null values in critical fields
        tables_fields = [
            ('dim_customers', 'customer_name'),
            ('dim_customers', 'email'),
            ('dim_products', 'product_name'),
            ('fact_sales', 'revenue')
        ]
        
        for table, field in tables_fields:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {field} IS NULL")
            null_count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_count = cursor.fetchone()[0]
            
            null_percentage = (null_count / total_count * 100) if total_count > 0 else 0
            status = "PASS" if null_percentage < 5 else "FAIL"
            
            checks.append((
                table, f"Null {field}", null_percentage, 5.0, status, datetime.now()
            ))
        
        # Check for duplicate customers
        cursor.execute("SELECT COUNT(*) - COUNT(DISTINCT email) FROM dim_customers")
        duplicate_emails = cursor.fetchone()[0]
        status = "PASS" if duplicate_emails == 0 else "FAIL"
        
        checks.append((
            'dim_customers', 'Duplicate emails', duplicate_emails, 0, status, datetime.now()
        ))
        
        # Check revenue consistency
        cursor.execute("""
            SELECT COUNT(*) FROM fact_sales s
            JOIN dim_products p ON s.product_id = p.product_id
            WHERE ABS(s.revenue - (p.price * s.quantity)) > 0.01
        """)
        revenue_inconsistencies = cursor.fetchone()[0]
        status = "PASS" if revenue_inconsistencies == 0 else "FAIL"
        
        checks.append((
            'fact_sales', 'Revenue consistency', revenue_inconsistencies, 0, status, datetime.now()
        ))
        
        # Insert quality check results
        cursor.executemany("""
            INSERT INTO data_quality_metrics 
            (table_name, metric_name, metric_value, threshold_value, status, check_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, checks)
        
        conn.commit()
        conn.close()
        
        return checks
    
    def get_data_lineage(self):
        """Get data lineage information."""
        return {
            'sources': [
                {'name': 'CRM System', 'type': 'Database', 'tables': ['customers']},
                {'name': 'E-commerce Platform', 'type': 'API', 'tables': ['orders', 'products']},
                {'name': 'Payment Gateway', 'type': 'Stream', 'tables': ['transactions']}
            ],
            'transformations': [
                {'step': 1, 'process': 'Data Extraction', 'description': 'Extract data from source systems'},
                {'step': 2, 'process': 'Data Cleaning', 'description': 'Clean and validate data quality'},
                {'step': 3, 'process': 'Data Transformation', 'description': 'Transform to star schema'},
                {'step': 4, 'process': 'Data Loading', 'description': 'Load into data warehouse'}
            ],
            'targets': [
                {'name': 'Analytics Dashboard', 'type': 'BI Tool'},
                {'name': 'ML Pipeline', 'type': 'Machine Learning'},
                {'name': 'Reporting System', 'type': 'Reports'}
            ]
        }


@app.route('/')
def index():
    """Main dashboard page."""
    return app.send_static_file("index.html")

@app.route('/analytics')
def get_analytics():
    """Get sales analytics data."""
    return jsonify(warehouse.get_sales_analytics())

@app.route('/quality-check', methods=['POST'])
def run_quality_check():
    """Run data quality checks."""
    checks = warehouse.run_data_quality_checks()
    return jsonify([{
        'table_name': check[0],
        'metric_name': check[1],
        'metric_value': check[2],
        'threshold_value': check[3],
        'status': check[4],
        'check_date': check[5].isoformat()
    } for check in checks])

@app.route('/quality-metrics')
def get_quality_metrics():
    """Get existing quality metrics."""
    conn = sqlite3.connect(warehouse.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT table_name, metric_name, metric_value, threshold_value, status, check_date
        FROM data_quality_metrics
        ORDER BY check_date DESC
    """)
    
    metrics = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'table_name': metric[0],
        'metric_name': metric[1],
        'metric_value': metric[2],
        'threshold_value': metric[3],
        'status': metric[4],
        'check_date': metric[5]
    } for metric in metrics])

@app.route('/lineage')
def get_lineage():
    """Get data lineage information."""
    return jsonify(warehouse.get_data_lineage())

def main():
    """Main execution function."""
    global warehouse
    warehouse = CloudDataWarehouse()
    print("Cloud Data Warehouse")
    print("=" * 30)
    
    print("Initializing data warehouse...")
    print("Loading sample data...")
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

