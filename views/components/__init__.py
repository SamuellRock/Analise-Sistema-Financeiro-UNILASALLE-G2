"""Dashboard UI components."""

from .charts import (
    create_credit_by_modality_chart,
    create_credit_by_region_chart,
    create_credit_by_uf_chart,
    create_credit_evolution_chart,
    create_default_color_map,
    create_inadimplencia_by_modality_chart,
    create_inadimplencia_evolution_chart,
    create_juro_vs_inadimplencia_scatter,
    create_risk_distribution_chart,
    create_taxa_juros_evolution_chart,
    create_temporal_heatmap,
)
from .filters import apply_dashboard_filters, render_filters
from .kpi_cards import render_kpi_cards
from .tables import render_download_button, render_table

__all__ = [
    "apply_dashboard_filters",
    "create_credit_by_modality_chart",
    "create_credit_by_region_chart",
    "create_credit_by_uf_chart",
    "create_credit_evolution_chart",
    "create_default_color_map",
    "create_inadimplencia_by_modality_chart",
    "create_inadimplencia_evolution_chart",
    "create_juro_vs_inadimplencia_scatter",
    "create_risk_distribution_chart",
    "create_taxa_juros_evolution_chart",
    "create_temporal_heatmap",
    "render_download_button",
    "render_filters",
    "render_kpi_cards",
    "render_table",
]
