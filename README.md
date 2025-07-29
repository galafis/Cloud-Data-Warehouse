# Cloud Data Warehouse

[English](#english) | [Português](#português)

## English

### Overview
A modern cloud-based data warehouse solution with comprehensive analytics, data quality monitoring, and ETL capabilities. Built with Python Flask and featuring a star schema design for optimal analytical performance.

### Features
- **Star Schema Design**: Optimized dimensional modeling for analytics
- **Real-time Analytics**: Interactive dashboards with KPIs and visualizations
- **Data Quality Monitoring**: Automated quality checks and metrics
- **Data Lineage Tracking**: Complete data flow visualization
- **ETL Pipeline**: Extract, Transform, Load capabilities
- **Multi-dimensional Analysis**: Sales analytics by category, country, and time
- **Performance Metrics**: Revenue, profit, and transaction analytics

### Technologies Used
- **Python Flask**: Backend web framework
- **SQLite**: Data warehouse database
- **Pandas**: Data manipulation and analysis
- **Chart.js**: Interactive data visualizations
- **HTML5/CSS3/JavaScript**: Modern responsive frontend

### Architecture

#### Data Model
- **Fact Table**: `fact_sales` - Central transaction data
- **Dimension Tables**: 
  - `dim_customers` - Customer information
  - `dim_products` - Product catalog
  - `dim_time` - Time dimension for temporal analysis

#### Key Components
1. **Data Warehouse Engine**: Core data storage and retrieval
2. **Analytics Engine**: KPI calculation and aggregation
3. **Quality Monitor**: Data validation and quality metrics
4. **Lineage Tracker**: Data flow and transformation tracking

### Installation

1. Clone the repository:
```bash
git clone https://github.com/galafis/Cloud-Data-Warehouse.git
cd Cloud-Data-Warehouse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python warehouse.py
```

4. Open your browser to `http://localhost:5000`

### Usage

#### Analytics Dashboard
- View real-time KPIs (revenue, profit, transactions)
- Analyze sales by product category
- Monitor performance by country
- Track monthly trends and patterns

#### Data Quality Monitoring
- Run automated quality checks
- Monitor null value percentages
- Detect data inconsistencies
- Track quality metrics over time

#### Data Lineage
- Visualize data flow from sources to targets
- Track transformation processes
- Monitor data dependencies

### API Endpoints

#### Analytics
- `GET /analytics` - Retrieve sales analytics and KPIs
- `GET /quality-metrics` - Get data quality metrics
- `POST /quality-check` - Run data quality validation
- `GET /lineage` - Get data lineage information

### Data Quality Checks
- **Null Value Detection**: Monitors critical fields for missing data
- **Duplicate Detection**: Identifies duplicate records
- **Consistency Validation**: Verifies data relationships
- **Threshold Monitoring**: Alerts when quality metrics exceed limits

### Sample Data
The application includes sample data for demonstration:
- 5 customers across different countries and segments
- 5 products in electronics and furniture categories
- 200+ sales transactions over 90 days
- Complete time dimension for temporal analysis

### Extending the Warehouse

#### Adding New Data Sources
1. Create extraction scripts for your data sources
2. Implement transformation logic
3. Update the database schema as needed
4. Add quality checks for new data

#### Custom Analytics
1. Create new analytical queries
2. Add visualization components
3. Implement new KPIs and metrics

### Performance Optimization
- Indexed dimension tables for fast lookups
- Aggregated fact tables for quick analytics
- Optimized queries for large datasets
- Caching strategies for frequently accessed data

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Português

### Visão Geral
Uma solução moderna de data warehouse baseada em nuvem com análises abrangentes, monitoramento de qualidade de dados e capacidades ETL. Construído com Python Flask e apresentando design de esquema estrela para performance analítica otimizada.

### Funcionalidades
- **Design de Esquema Estrela**: Modelagem dimensional otimizada para análises
- **Análises em Tempo Real**: Dashboards interativos com KPIs e visualizações
- **Monitoramento de Qualidade de Dados**: Verificações automáticas de qualidade e métricas
- **Rastreamento de Linhagem de Dados**: Visualização completa do fluxo de dados
- **Pipeline ETL**: Capacidades de Extração, Transformação e Carregamento
- **Análise Multidimensional**: Análises de vendas por categoria, país e tempo
- **Métricas de Performance**: Análises de receita, lucro e transações

### Tecnologias Utilizadas
- **Python Flask**: Framework web backend
- **SQLite**: Banco de dados do data warehouse
- **Pandas**: Manipulação e análise de dados
- **Chart.js**: Visualizações de dados interativas
- **HTML5/CSS3/JavaScript**: Frontend responsivo moderno

### Arquitetura

#### Modelo de Dados
- **Tabela Fato**: `fact_sales` - Dados centrais de transações
- **Tabelas Dimensão**: 
  - `dim_customers` - Informações de clientes
  - `dim_products` - Catálogo de produtos
  - `dim_time` - Dimensão temporal para análise temporal

#### Componentes Principais
1. **Engine do Data Warehouse**: Armazenamento e recuperação central de dados
2. **Engine de Análises**: Cálculo de KPIs e agregação
3. **Monitor de Qualidade**: Validação de dados e métricas de qualidade
4. **Rastreador de Linhagem**: Rastreamento de fluxo e transformação de dados

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/galafis/Cloud-Data-Warehouse.git
cd Cloud-Data-Warehouse
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python warehouse.py
```

4. Abra seu navegador em `http://localhost:5000`

### Uso

#### Dashboard de Análises
- Visualize KPIs em tempo real (receita, lucro, transações)
- Analise vendas por categoria de produto
- Monitore performance por país
- Acompanhe tendências e padrões mensais

#### Monitoramento de Qualidade de Dados
- Execute verificações automáticas de qualidade
- Monitore percentuais de valores nulos
- Detecte inconsistências de dados
- Acompanhe métricas de qualidade ao longo do tempo

#### Linhagem de Dados
- Visualize fluxo de dados de fontes para destinos
- Acompanhe processos de transformação
- Monitore dependências de dados

### Endpoints da API

#### Análises
- `GET /analytics` - Recuperar análises de vendas e KPIs
- `GET /quality-metrics` - Obter métricas de qualidade de dados
- `POST /quality-check` - Executar validação de qualidade de dados
- `GET /lineage` - Obter informações de linhagem de dados

### Verificações de Qualidade de Dados
- **Detecção de Valores Nulos**: Monitora campos críticos para dados ausentes
- **Detecção de Duplicatas**: Identifica registros duplicados
- **Validação de Consistência**: Verifica relacionamentos de dados
- **Monitoramento de Limites**: Alerta quando métricas de qualidade excedem limites

### Dados de Exemplo
A aplicação inclui dados de exemplo para demonstração:
- 5 clientes em diferentes países e segmentos
- 5 produtos em categorias de eletrônicos e móveis
- 200+ transações de vendas ao longo de 90 dias
- Dimensão temporal completa para análise temporal

### Estendendo o Warehouse

#### Adicionando Novas Fontes de Dados
1. Crie scripts de extração para suas fontes de dados
2. Implemente lógica de transformação
3. Atualize o esquema do banco de dados conforme necessário
4. Adicione verificações de qualidade para novos dados

#### Análises Personalizadas
1. Crie novas consultas analíticas
2. Adicione componentes de visualização
3. Implemente novos KPIs e métricas

### Otimização de Performance
- Tabelas dimensão indexadas para buscas rápidas
- Tabelas fato agregadas para análises rápidas
- Consultas otimizadas para grandes conjuntos de dados
- Estratégias de cache para dados frequentemente acessados

### Contribuindo
1. Faça um fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

### Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.



## 📋 Descrição

Descreva aqui o conteúdo desta seção.


## 📦 Instalação

Descreva aqui o conteúdo desta seção.


## 💻 Uso

Descreva aqui o conteúdo desta seção.


## 📄 Licença

Descreva aqui o conteúdo desta seção.
