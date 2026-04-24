"""
kececicurve - Parametric Space-Filling Curve Family
Keçeci Eğrisi: Tamamen özgün, çok amaçlı ve esnek bir fraktal eğri üreteci.
"""

__version__ = "0.1.2"
__author__ = "Mehmet Keçeci"

from .kececicurve import (
    # Temel eğri sınıfları
    KececiCurve,
    KececiCurveGenerator,
    KececiCurveGenerator2D,
    KececiCurveGenerator3D,
    
    # Enum tanımları
    ConnectionMode,
    ChildOrdering,
    GrowthDirection,
    
    # Klasik eğriler
    ClassicalCurves,
    
    # Görselleştirme yardımcıları
    CurveComparisonVisualizer,
    
    # Hızlı görselleştirme fonksiyonları
    quick_plot,
    flower_patterns,
    galaxy_patterns,
    snowflake_patterns,
    mandala_patterns,
    fractal_trees,
    marine_patterns,
    cosmic_web,
    neural_network_patterns,
    virus_patterns,
    peano_test,
    plot_peano_curve,
    
    # Karşılaştırma görselleştirmeleri
    locality_heatmap_comparison,
    continuity_visualization_v2,
    radar_chart_comparison,
    
    # Sierpinski görselleştirmeleri
    plot_sierpinski_comparison,
    plot_sierpinski_curve,
    plot_sierpinski_evolution,
    
    # Kuantum görselleştirme sınıfları
    MajoranaVisualizer,
    WeylVisualizer,
    StratumModelVisualizer,
    Rich3DQuantumVisualizer,
    AdvancedQuantumVisualizer,
    QuantumKececiCurve,
    
    # Galeri
    create_kececi_curve_gallery,
    
    # Menü
    show_menu,
)

__all__ = [
    "KececiCurve",
    "KececiCurveGenerator",
    "KececiCurveGenerator2D",
    "KececiCurveGenerator3D",
    "ConnectionMode",
    "ChildOrdering",
    "GrowthDirection",
    "ClassicalCurves",
    "CurveComparisonVisualizer",
    "quick_plot",
    "flower_patterns",
    "galaxy_patterns",
    "snowflake_patterns",
    "mandala_patterns",
    "fractal_trees",
    "marine_patterns",
    "cosmic_web",
    "neural_network_patterns",
    "virus_patterns",
    "locality_heatmap_comparison",
    "continuity_visualization_v2",
    "radar_chart_comparison",
    "plot_sierpinski_comparison",
    "plot_sierpinski_curve",
    "plot_sierpinski_evolution",
    "MajoranaVisualizer",
    "WeylVisualizer",
    "StratumModelVisualizer",
    "Rich3DQuantumVisualizer",
    "AdvancedQuantumVisualizer",
    "QuantumKececiCurve",
    "create_kececi_curve_gallery",
    "peano_test",
    "plot_peano_curve",
    "show_menu",
]
