import os

TEMPLATE_PATH = 'core/templates/dashboard.html'

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# We'll replace the entire block extra_js with a more robust version
new_js_block = """{% block extra_js %}
<script>
    (function() {
        console.log('Dashboard script execution started');

        function initDashboard() {
            if (window.dashboardInitialized) return;
            window.dashboardInitialized = true;
            console.log('Initializing dashboard components...');

            // Progress ring animation
            var total = {{ stats.total_materiels }};
            var enService = {{ stats.en_service }};
            var percent = total > 0 ? Math.round((enService / total) * 100) : 0;

            var circle = document.getElementById('progressCircle');
            if (circle) {
                var circumference = 2 * Math.PI * 70;
                circle.style.strokeDasharray = circumference;
                circle.style.strokeDashoffset = circumference;
                
                setTimeout(function () {
                    var offset = circumference - (percent / 100) * circumference;
                    circle.style.strokeDashoffset = offset;
                    
                    var counter = document.getElementById('progressPercent');
                    if (counter) {
                        var current = 0;
                        var interval = setInterval(function () {
                            if (current >= percent) { clearInterval(interval); return; }
                            current++;
                            counter.textContent = current + '%';
                        }, 20);
                    }
                }, 300);
            }

            // Session Timer
            var seconds = 0;
            var timerEl = document.getElementById('sessionTimer');
            if (timerEl) {
                setInterval(function () {
                    seconds++;
                    var h = String(Math.floor(seconds / 3600)).padStart(2, '0');
                    var m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
                    var s = String(seconds % 60).padStart(2, '0');
                    timerEl.textContent = h + ':' + m + ':' + s;
                }, 1000);
            }

            // Chart data
            var gridColor = 'rgba(0,0,0,0.03)';
            var tickColor = '#6b7280';
            var legendFont = { size: 12, family: 'Inter, sans-serif', weight: '500' };

            var typeNames = {
                radio: 'Radio', telephonique: 'T\\\\u00e9l\\\\u00e9phonique', informatique: 'Informatique',
                vehicule: 'V\\\\u00e9hicule', armement: 'Armement', optique: 'Optique', autre: 'Autre'
            };
            var etatNames = {
                service: 'En Service', attente: 'En Attente',
                approvisionnement: 'Approvisionnement', hors_service: 'Hors Service'
            };

            var typeLabels = [];
            var typeCounts = [];
            {% for item in types_data %}
            typeLabels.push(typeNames['{{ item.type_materiel }}'] || '{{ item.type_materiel }}');
            typeCounts.push({{ item.count }});
            {% endfor %}

            var etatLabels = [];
            var etatCounts = [];
            {% for item in etats_data %}
            etatLabels.push(etatNames['{{ item.etat }}'] || '{{ item.etat }}');
            etatCounts.push({{ item.count }});
            {% endfor %}

            // Type Chart
            var typeCtx = document.getElementById('typeChart');
            if (typeCtx && typeLabels.length > 0 && typeof Chart !== 'undefined') {
                new Chart(typeCtx, {
                    type: 'bar',
                    data: {
                        labels: typeLabels,
                        datasets: [{
                            label: 'Quantit\\\\u00e9',
                            data: typeCounts,
                            backgroundColor: function (ctx) {
                                var chart = ctx.chart;
                                var area = chart.chartArea;
                                if (!area) return '#22c55e';
                                var g = chart.ctx.createLinearGradient(0, area.bottom, 0, area.top);
                                g.addColorStop(0, '#bbf7d0');
                                g.addColorStop(1, '#166534');
                                return g;
                            },
                            borderRadius: 8,
                            borderSkipped: false,
                            barPercentage: 0.6
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { beginAtZero: true, ticks: { stepSize: 1, color: tickColor, font: { size: 11 } }, grid: { color: gridColor, drawBorder: false } },
                            x: { ticks: { color: tickColor, font: { size: 11 } }, grid: { display: false } }
                        }
                    }
                });
            }

            // Etat Chart
            var etatColors = ['#22c55e', '#f59e0b', '#3b82f6', '#ef4444'];
            var etatCtx = document.getElementById('etatChart');
            if (etatCtx && etatLabels.length > 0 && typeof Chart !== 'undefined') {
                new Chart(etatCtx, {
                    type: 'doughnut',
                    data: {
                        labels: etatLabels,
                        datasets: [{
                            data: etatCounts,
                            backgroundColor: etatColors,
                            borderWidth: 0,
                            hoverOffset: 6,
                            spacing: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { padding: 20, usePointStyle: true, pointStyleWidth: 10, color: tickColor, font: legendFont }
                            }
                        }
                    }
                });
            }
        }

        // Try multiple triggers
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initDashboard);
        } else {
            initDashboard();
        }
        window.addEventListener('load', initDashboard);
        // Fallback for cases where events don't fire correctly
        setTimeout(initDashboard, 1000);
        setTimeout(initDashboard, 3000);
    })();
</script>
{% endblock %}"""

start_tag = "{% block extra_js %}"
end_tag = "{% endblock %}"

start_index = content.find(start_tag)
end_index = content.find(end_tag, start_index)

if start_index != -1 and end_index != -1:
    new_content = content[:start_index] + new_js_block + content[end_index + len(end_tag):]
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {TEMPLATE_PATH} successfully.")
else:
    print("Could not find extra_js block.")
