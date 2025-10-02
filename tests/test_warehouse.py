import pytest
import sqlite3
import os
from src.warehouse import CloudDataWarehouse

# Define o caminho do banco de dados para os testes
TEST_DB_PATH = "test_warehouse.db"

@pytest.fixture(scope="module")
def warehouse_instance():
    # Limpa qualquer banco de dados de teste anterior
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Cria uma nova instância do data warehouse para os testes
    warehouse = CloudDataWarehouse(db_path=TEST_DB_PATH)
    yield warehouse
    
    # Limpa o banco de dados após os testes
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_init_database(warehouse_instance):
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    # Verifica se as tabelas foram criadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type=\'table\';")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    
    assert "dim_customers" in table_names
    assert "dim_products" in table_names
    assert "dim_time" in table_names
    assert "fact_sales" in table_names
    assert "data_quality_metrics" in table_names
    
    conn.close()

def test_load_sample_data(warehouse_instance):
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    # Verifica se os dados de exemplo foram carregados
    cursor.execute("SELECT COUNT(*) FROM dim_customers")
    assert cursor.fetchone()[0] > 0
    
    cursor.execute("SELECT COUNT(*) FROM dim_products")
    assert cursor.fetchone()[0] > 0
    
    cursor.execute("SELECT COUNT(*) FROM fact_sales")
    assert cursor.fetchone()[0] > 0
    
    conn.close()

def test_get_sales_analytics(warehouse_instance):
    analytics = warehouse_instance.get_sales_analytics()
    
    assert "kpis" in analytics
    assert "category_sales" in analytics
    assert "country_sales" in analytics
    assert "monthly_trends" in analytics
    
    assert analytics["kpis"]["total_revenue"] > 0
    assert len(analytics["category_sales"]) > 0
    assert len(analytics["country_sales"]) > 0
    assert len(analytics["monthly_trends"]) > 0

def test_run_data_quality_checks(warehouse_instance):
    checks = warehouse_instance.run_data_quality_checks()
    assert len(checks) > 0
    
    # Verifica se os checks foram armazenados no banco de dados
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM data_quality_metrics")
    assert cursor.fetchone()[0] > 0
    conn.close()

def test_get_data_lineage(warehouse_instance):
    lineage = warehouse_instance.get_data_lineage()
    
    assert "sources" in lineage
    assert "transformations" in lineage
    assert "targets" in lineage
    
    assert len(lineage["sources"]) > 0
    assert len(lineage["transformations"]) > 0
    assert len(lineage["targets"]) > 0

