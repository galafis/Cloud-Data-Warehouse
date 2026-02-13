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
from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

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

warehouse = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Data Warehouse</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .kpi-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .chart-container {
            height: 300px;
            margin: 20px 0;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .data-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        
        .status-pass {
            color: #27ae60;
            font-weight: bold;
        }
        
        .status-fail {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .nav-tabs {
            display: flex;
            background: white;
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .nav-tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .nav-tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .lineage-flow {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
        }
        
        .lineage-step {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            flex: 1;
            margin: 0 10px;
        }
        
        .lineage-arrow {
            font-size: 2rem;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☁️ Cloud Data Warehouse</h1>
            <p>Modern cloud-based data warehouse with analytics and monitoring</p>
        </div>
        
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('analytics')">📊 Analytics</div>
            <div class="nav-tab" onclick="showTab('quality')">🔍 Data Quality</div>
            <div class="nav-tab" onclick="showTab('lineage')">🔄 Data Lineage</div>
        </div>
        
        <div id="analytics" class="tab-content active">
            <div class="kpi-grid" id="kpiGrid">
                <!-- KPIs will be populated here -->
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3>📈 Sales by Category</h3>
                    <div class="chart-container">
                        <canvas id="categoryChart"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🌍 Sales by Country</h3>
                    <div class="chart-container">
                        <canvas id="countryChart"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📅 Monthly Trends</h3>
                    <div class="chart-container">
                        <canvas id="trendsChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="quality" class="tab-content">
            <div class="card">
                <h3>🔍 Data Quality Metrics</h3>
                <button onclick="runQualityChecks()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-bottom: 20px;">
                    🔄 Run Quality Checks
                </button>
                <table class="data-table" id="qualityTable">
                    <thead>
                        <tr>
                            <th>Table</th>
                            <th>Metric</th>
                            <th>Value</th>
                            <th>Threshold</th>
                            <th>Status</th>
                            <th>Check Date</th>
                        </tr>
                    </thead>
                    <tbody id="qualityTableBody">
                        <!-- Quality metrics will be populated here -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <div id="lineage" class="tab-content">
            <div class="card">
                <h3>🔄 Data Lineage</h3>
                <div class="lineage-flow">
                    <div class="lineage-step">
                        <h4>📥 Sources</h4>
                        <div id="sources"></div>
                    </div>
                    <div class="lineage-arrow">→</div>
                    <div class="lineage-step">
                        <h4>⚙️ Transformations</h4>
                        <div id="transformations"></div>
                    </div>
                    <div class="lineage-arrow">→</div>
                    <div class="lineage-step">
                        <h4>📤 Targets</h4>
                        <div id="targets"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let analyticsData = null;
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load data based on tab
            if (tabName === 'analytics' && !analyticsData) {
                loadAnalytics();
            } else if (tabName === 'quality') {
                loadQualityMetrics();
            } else if (tabName === 'lineage') {
                loadDataLineage();
            }
        }
        
        async function loadAnalytics() {
            try {
                const response = await fetch('/analytics');
                analyticsData = await response.json();
                
                displayKPIs(analyticsData.kpis);
                createCategoryChart(analyticsData.category_sales);
                createCountryChart(analyticsData.country_sales);
                createTrendsChart(analyticsData.monthly_trends);
                
            } catch (error) {
                console.error('Error loading analytics:', error);
            }
        }
        
        function displayKPIs(kpis) {
            const kpiGrid = document.getElementById('kpiGrid');
            
            kpiGrid.innerHTML = `
                <div class="kpi-card">
                    <div class="kpi-value">$${(kpis.total_revenue || 0).toLocaleString()}</div>
                    <div class="kpi-label">Total Revenue</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">$${(kpis.total_profit || 0).toLocaleString()}</div>
                    <div class="kpi-label">Total Profit</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">${(kpis.total_transactions || 0).toLocaleString()}</div>
                    <div class="kpi-label">Transactions</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">$${(kpis.avg_transaction_value || 0).toFixed(2)}</div>
                    <div class="kpi-label">Avg Transaction</div>
                </div>
            `;
        }
        
        function createCategoryChart(data) {
            const ctx = document.getElementById('categoryChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.map(d => d.category),
                    datasets: [{
                        data: data.map(d => d.revenue),
                        backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        function createCountryChart(data) {
            const ctx = document.getElementById('countryChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(d => d.country),
                    datasets: [{
                        label: 'Revenue',
                        data: data.map(d => d.revenue),
                        backgroundColor: '#667eea'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        function createTrendsChart(data) {
            const ctx = document.getElementById('trendsChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
                    datasets: [{
                        label: 'Revenue',
                        data: data.map(d => d.revenue),
                        borderColor: '#667eea',
                        backgroundColor: '#667eea20',
                        tension: 0.4
                    }, {
                        label: 'Profit',
                        data: data.map(d => d.profit),
                        borderColor: '#764ba2',
                        backgroundColor: '#764ba220',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        async function runQualityChecks() {
            try {
                const response = await fetch('/quality-check', { method: 'POST' });
                const checks = await response.json();
                
                displayQualityMetrics(checks);
                
            } catch (error) {
                console.error('Error running quality checks:', error);
            }
        }
        
        async function loadQualityMetrics() {
            try {
                const response = await fetch('/quality-metrics');
                const metrics = await response.json();
                
                displayQualityMetrics(metrics);
                
            } catch (error) {
                console.error('Error loading quality metrics:', error);
            }
        }
        
        function displayQualityMetrics(metrics) {
            const tbody = document.getElementById('qualityTableBody');
            
            tbody.innerHTML = metrics.map(metric => `
                <tr>
                    <td>${metric.table_name}</td>
                    <td>${metric.metric_name}</td>
                    <td>${metric.metric_value}</td>
                    <td>${metric.threshold_value}</td>
                    <td class="status-${metric.status.toLowerCase()}">${metric.status}</td>
                    <td>${new Date(metric.check_date).toLocaleString()}</td>
                </tr>
            `).join('');
        }
        
        async function loadDataLineage() {
            try {
                const response = await fetch('/lineage');
                const lineage = await response.json();
                
                document.getElementById('sources').innerHTML = lineage.sources.map(s => 
                    `<div><strong>${s.name}</strong><br><small>${s.type}</small></div>`
                ).join('');
                
                document.getElementById('transformations').innerHTML = lineage.transformations.map(t => 
                    `<div><strong>Step ${t.step}</strong><br>${t.process}<br><small>${t.description}</small></div>`
                ).join('');
                
                document.getElementById('targets').innerHTML = lineage.targets.map(t => 
                    `<div><strong>${t.name}</strong><br><small>${t.type}</small></div>`
                ).join('');
                
            } catch (error) {
                console.error('Error loading lineage:', error);
            }
        }
        
        // Load analytics on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadAnalytics();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template_string(HTML_TEMPLATE)

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
    print("Cloud Data Warehouse")
    print("=" * 30)
    
    print("Initializing data warehouse...")
    print("Loading sample data...")
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    warehouse = CloudDataWarehouse()
    main()

