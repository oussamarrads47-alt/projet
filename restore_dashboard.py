import os

TEMPLATE_PATH = 'core/templates/dashboard.html'

dashboard_content = """{% extends "base.html" %}
{% block title %}Tableau de Bord{% endblock %}

{% block content %}
<!-- Page Header -->
<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 animate-fade-in">
    <div>
        <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 tracking-tight">Tableau de Bord</h1>
        <p class="text-sm text-gray-500 mt-1">Vue d'ensemble strat\u00e9gique de votre parc de mat\u00e9riels</p>
    </div>
    <a href="{% url 'materiel_create' %}"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-brand-800 to-brand-700 text-white text-sm font-semibold rounded-xl hover:shadow-lg hover:shadow-brand-800/25 transition-all duration-300 hover:-translate-y-0.5">
        <i class="fas fa-plus text-xs"></i> Ajouter un Mat\u00e9riel
    </a>
</div>

<!-- Statistics Cards -->
{% include "includes/stats_cards.html" %}

<!-- Charts + Team Section -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

    <!-- Project Analytics (Bar Chart) -->
    <div class="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h3 class="text-lg font-semibold text-gray-900">R\u00e9partition par Cat\u00e9gorie</h3>
                <p class="text-xs text-gray-500 mt-0.5">Analyse des types de mat\u00e9riels</p>
            </div>
            <div class="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center">
                <i class="fas fa-chart-bar text-brand-600"></i>
            </div>
        </div>
        <canvas id="typeChart" height="200"></canvas>
    </div>

    <!-- Project Progress Ring -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col items-center justify-center">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Disponibilit\u00e9</h3>
        <p class="text-xs text-gray-500 mb-6">Taux de mat\u00e9riels en service</p>

        <!-- SVG Progress Ring -->
        <div class="relative w-44 h-44 mb-4">
            <svg class="w-full h-full -rotate-90" viewBox="0 0 160 160">
                <circle cx="80" cy="80" r="70" stroke="#f3f4f6" stroke-width="12" fill="none" />
                <circle id="progressCircle" cx="80" cy="80" r="70" stroke="url(#progressGradient)" stroke-width="12"
                    fill="none" stroke-linecap="round" stroke-dasharray="439.82" stroke-dashoffset="439.82"
                    style="transition: stroke-dashoffset 1.5s ease-out;" />
                <defs>
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#166534" />
                        <stop offset="100%" style="stop-color:#22c55e" />
                    </linearGradient>
                </defs>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span id="progressPercent" class="text-4xl font-bold text-gray-900">0%</span>
                <span class="text-xs text-gray-500 mt-1">En Service</span>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-3 w-full text-center text-xs">
            <div class="bg-green-50 rounded-lg py-2">
                <p class="font-bold text-green-700">{{ stats.en_service }}</p>
                <p class="text-green-600">Actifs</p>
            </div>
            <div class="bg-red-50 rounded-lg py-2">
                <p class="font-bold text-red-700">{{ stats.hors_service }}</p>
                <p class="text-red-600">Hors Service</p>
            </div>
        </div>
    </div>
</div>

<!-- State Chart + Time Tracker -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

    <!-- \u00c9tat Op\u00e9rationnel -->
    <div class="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h3 class="text-lg font-semibold text-gray-900">\u00c9tat Op\u00e9rationnel</h3>
                <p class="text-xs text-gray-500 mt-0.5">Distribution par \u00e9tat des actifs</p>
            </div>
            <div class="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
                <i class="fas fa-chart-pie text-blue-600"></i>
            </div>
        </div>
        <canvas id="etatChart" height="200"></canvas>
    </div>

    <!-- Time Tracker Widget -->
    <div
        class="bg-gradient-to-br from-brand-800 to-brand-900 rounded-2xl p-6 shadow-lg shadow-brand-900/20 text-white flex flex-col justify-between">
        <div>
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold">Activit\u00e9 R\u00e9cente</h3>
                <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center backdrop-blur-sm">
                    <i class="fas fa-clock text-white/90"></i>
                </div>
            </div>
            <p class="text-sm text-white/60 mb-6">Suivi de votre session</p>

            <!-- Timer -->
            <div class="text-center mb-6">
                <p id="sessionTimer" class="text-5xl font-bold tracking-tight font-mono">00:00:00</p>
                <p class="text-xs text-white/50 mt-2">Temps de session</p>
            </div>
        </div>

        <!-- Stats in widget -->
        <div class="space-y-3">
            <div class="flex items-center justify-between text-sm">
                <span class="text-white/70">Mouvements aujourd'hui</span>
                <span class="font-semibold">{{ stats.total_mouvements }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
                <span class="text-white/70">Documents trait\u00e9s</span>
                <span class="font-semibold">{{ stats.total_documents }}</span>
            </div>
            <div class="w-full h-px bg-white/10 my-2"></div>
            <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
                <span class="text-xs text-white/60">Syst\u00e8me op\u00e9rationnel</span>
            </div>
        </div>
    </div>
</div>

<!-- Recent Materials Section -->
<div class="flex items-center justify-between mb-5">
    <div>
        <h2 class="text-lg font-semibold text-gray-900">Derniers Mat\u00e9riels</h2>
        <p class="text-xs text-gray-500">R\u00e9cemment enregistr\u00e9s dans le syst\u00e8me</p>
    </div>
    <a href="{% url 'materiel_list' %}"
        class="text-sm font-medium text-brand-700 hover:text-brand-800 flex items-center gap-1.5 transition-colors">
        Voir tout <i class="fas fa-arrow-right text-xs"></i>
    </a>
</div>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    {% for m in materiels|slice:":8" %}
    <div
        class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 group">
        <div
            class="h-36 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center relative overflow-hidden">
            {% if m.image %}
            <img src="{{ m.image.url }}" alt="{{ m.designation }}"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            {% else %}
            <i class="fas fa-satellite-dish text-3xl text-gray-300"></i>
            {% endif %}
            <span class="absolute top-3 left-3 text-[10px] font-semibold px-2.5 py-1 rounded-lg
                {% if m.etat == 'service' %}bg-green-100 text-green-700
                {% elif m.etat == 'attente' %}bg-amber-100 text-amber-700
                {% elif m.etat == 'hors_service' %}bg-red-100 text-red-700
                {% else %}bg-blue-100 text-blue-700{% endif %}">
                {{ m.get_etat_display }}
            </span>
        </div>
        <div class="p-4">
            <h4 class="font-semibold text-gray-900 text-sm leading-tight truncate">{{ m.designation }}</h4>
            <p class="text-xs text-gray-500 mt-1"><i class="fas fa-barcode mr-1"></i>{{ m.numero_serie }}</p>
            <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-50">
                <span class="text-xs text-gray-400"><i class="fas fa-warehouse mr-1"></i>{{ m.magasin.nom }}</span>
                <a href="{% url 'materiel_detail' m.pk %}"
                    class="text-xs font-medium text-brand-700 hover:text-brand-800 transition-colors">
                    D\u00e9tails <i class="fas fa-arrow-right text-[9px]"></i>
                </a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-span-full bg-white rounded-2xl p-12 text-center shadow-sm border border-gray-100">
        <i class="fas fa-box-open text-4xl text-gray-300 mb-3"></i>
        <p class="text-gray-500 mb-4">Aucun mat\u00e9riel enregistr\u00e9</p>
        <a href="{% url 'materiel_create' %}"
            class="inline-flex items-center gap-2 px-5 py-2.5 bg-brand-800 text-white text-sm font-semibold rounded-xl hover:bg-brand-700 transition-colors">
            <i class="fas fa-plus"></i> Enregistrer un Mat\u00e9riel
        </a>
    </div>
    {% endfor %}
</div>

<!-- Recent Movements -->
<div class="flex items-center justify-between mb-5">
    <div>
        <h2 class="text-lg font-semibold text-gray-900">Derniers Mouvements</h2>
        <p class="text-xs text-gray-500">Historique des flux r\u00e9cents</p>
    </div>
    <a href="{% url 'mouvement_list' %}"
        class="text-sm font-medium text-brand-700 hover:text-brand-800 flex items-center gap-1.5 transition-colors">
        Voir tout <i class="fas fa-arrow-right text-xs"></i>
    </a>
</div>

<div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-8">
    <div class="overflow-x-auto">
        <table class="w-full text-sm">
            <thead>
                <tr class="border-b border-gray-100">
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Type
                    </th>
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Date
                    </th>
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Mat\u00e9riel</th>
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Document</th>
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Qt\u00e9
                    </th>
                    <th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Observations</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
                {% for mv in derniers_mouvements %}
                <tr class="hover:bg-gray-50/50 transition-colors">
                    <td class="px-6 py-4">
                        <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-lg
                            {% if mv.type == 'entree' %}bg-green-100 text-green-700
                            {% elif mv.type == 'sortie' %}bg-red-100 text-red-700
                            {% elif mv.type == 'perception' %}bg-blue-100 text-blue-700
                            {% else %}bg-purple-100 text-purple-700{% endif %}">
                            {{ mv.get_type_display }}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-gray-600">{{ mv.date|date:"d/m/Y" }}</td>
                    <td class="px-6 py-4 font-medium text-gray-900">{{ mv.materiel.designation }}</td>
                    <td class="px-6 py-4 text-gray-600">{{ mv.document.get_type_display }}</td>
                    <td class="px-6 py-4 text-gray-900 font-semibold">{{ mv.quantite }}</td>
                    <td class="px-6 py-4 text-gray-500 max-w-[200px] truncate">{{ mv.observations|truncatewords:8|default:"\u2014" }}</td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6" class="px-6 py-12 text-center text-gray-400">
                        <i class="fas fa-inbox text-2xl mb-2 block"></i> Aucun mouvement enregistr\u00e9
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script>
    (function() {
        console.log('Dashboard script execution started');

        function initDashboard() {
            if (window.dashboardInitialized) return;
            
            var progressCircle = document.getElementById('progressCircle');
            var typeChartCtx = document.getElementById('typeChart');
            var etatChartCtx = document.getElementById('etatChart');
            var hasChartJs = typeof Chart !== 'undefined';
            
            window.dashboardInitialized = true;
            console.log('Initializing dashboard components... Chart.js loaded:', hasChartJs);

            var total = {{ stats.total_materiels }};
            var enService = {{ stats.en_service }};
            var percent = total > 0 ? Math.round((enService / total) * 100) : 0;

            if (progressCircle) {
                var circumference = 2 * Math.PI * 70;
                progressCircle.style.strokeDasharray = circumference;
                progressCircle.style.strokeDashoffset = circumference;
                
                setTimeout(function () {
                    var offset = circumference - (percent / 100) * circumference;
                    progressCircle.style.strokeDashoffset = offset;
                    
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

            var gridColor = 'rgba(0,0,0,0.03)';
            var tickColor = '#6b7280';
            var legendFont = { size: 12, family: 'Inter, sans-serif', weight: '500' };

            var typeNames = {
                radio: 'Radio', telephonique: 'T\\u00e9l\\u00e9phonique', informatique: 'Informatique',
                vehicule: 'V\\u00e9hicule', armement: 'Armement', optique: 'Optique', autre: 'Autre'
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

            if (typeChartCtx && typeLabels.length > 0 && hasChartJs) {
                new Chart(typeChartCtx, {
                    type: 'bar',
                    data: {
                        labels: typeLabels,
                        datasets: [{
                            label: 'Quantit\\u00e9',
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

            var etatCtx = document.getElementById('etatChart');
            var etatColors = ['#22c55e', '#f59e0b', '#3b82f6', '#ef4444'];
            if (etatCtx && etatLabels.length > 0 && hasChartJs) {
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

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initDashboard);
        } else {
            initDashboard();
        }
        window.addEventListener('load', initDashboard);
        setTimeout(initDashboard, 1000);
        setTimeout(initDashboard, 3000);
    })();
</script>
{% endblock %}"""

with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

print(f"Restored and updated {TEMPLATE_PATH} successfully.")
