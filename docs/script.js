let analyticsData = null;
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll(".tab-content").forEach(tab => {
                tab.classList.remove("active");
            });
            
            // Remove active class from all nav tabs
            document.querySelectorAll(".nav-tab").forEach(tab => {
                tab.classList.remove("active");
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add("active");
            event.target.classList.add("active");
            
            // Load data based on tab
            if (tabName === "analytics" && !analyticsData) {
                loadAnalytics();
            } else if (tabName === "quality") {
                loadQualityMetrics();
            } else if (tabName === "lineage") {
                loadDataLineage();
            }
        }
        
        async function loadAnalytics() {
            try {
                const response = await fetch("/analytics");
                analyticsData = await response.json();
                
                displayKPIs(analyticsData.kpis);
                createCategoryChart(analyticsData.category_sales);
                createCountryChart(analyticsData.country_sales);
                createTrendsChart(analyticsData.monthly_trends);
                
            } catch (error) {
                console.error("Error loading analytics:", error);
            }
        }
        
        function displayKPIs(kpis) {
            const kpiGrid = document.getElementById("kpiGrid");
            
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
            const ctx = document.getElementById("categoryChart").getContext("2d");
            
            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: data.map(d => d.category),
                    datasets: [{
                        data: data.map(d => d.revenue),
                        backgroundColor: ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    }
                }
            });
        }
        
        function createCountryChart(data) {
            const ctx = document.getElementById("countryChart").getContext("2d");
            
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.map(d => d.country),
                    datasets: [{
                        label: "Revenue",
                        data: data.map(d => d.revenue),
                        backgroundColor: "#667eea"
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
            const ctx = document.getElementById("trendsChart").getContext("2d");
            
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.map(d => `${d.year}-${d.month.toString().padStart(2, "0")}`),
                    datasets: [{
                        label: "Revenue",
                        data: data.map(d => d.revenue),
                        borderColor: "#667eea",
                        backgroundColor: "#667eea20",
                        tension: 0.4
                    }, {
                        label: "Profit",
                        data: data.map(d => d.profit),
                        borderColor: "#764ba2",
                        backgroundColor: "#764ba220",
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
                const response = await fetch("/quality-check", { method: "POST" });
                const checks = await response.json();
                
                displayQualityMetrics(checks);
                
            } catch (error) {
                console.error("Error running quality checks:", error);
            }
        }
        
        async function loadQualityMetrics() {
            try {
                const response = await fetch("/quality-metrics");
                const metrics = await response.json();
                
                displayQualityMetrics(metrics);
                
            } catch (error) {
                console.error("Error loading quality metrics:", error);
            }
        }
        
        function displayQualityMetrics(metrics) {
            const tbody = document.getElementById("qualityTableBody");
            
            tbody.innerHTML = metrics.map(metric => `
                <tr>
                    <td>${metric.table_name}</td>
                    <td>${metric.metric_name}</td>
                    <td>${metric.metric_value}</td>
                    <td>${metric.threshold_value}</td>
                    <td class="status-${metric.status.toLowerCase()}">${metric.status}</td>
                    <td>${new Date(metric.check_date).toLocaleString()}</td>
                </tr>
            `).join("");
        }
        
        async function loadDataLineage() {
            try {
                const response = await fetch("/lineage");
                const lineage = await response.json();
                
                document.getElementById("sources").innerHTML = lineage.sources.map(s => 
                    `<div><strong>${s.name}</strong><br><small>${s.type}</small></div>`
                ).join("");
                
                document.getElementById("transformations").innerHTML = lineage.transformations.map(t => 
                    `<div><strong>Step ${t.step}</strong><br>${t.process}<br><small>${t.description}</small></div>`
                ).join("");
                
                document.getElementById("targets").innerHTML = lineage.targets.map(t => 
                    `<div><strong>${t.name}</strong><br><small>${t.type}</small></div>`
                ).join("");
                
            } catch (error) {
                console.error("Error loading lineage:", error);
            }
        }
        
        // Load analytics on page load
        document.addEventListener("DOMContentLoaded", function() {
            loadAnalytics();
        });
