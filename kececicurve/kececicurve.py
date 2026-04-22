"""
# kececicurve.py: Keçeci Curve, Keçeci Eğrisi

Uzay Doldurma Eğrileri - Lokalite (Yerellik) Karşılaştırması
Isı haritası ile hangi eğrinin uzamsal yakınlığı daha iyi koruduğunu gösterir

Keçeci Eğrileri ile İleri Kuantum Fenomenleri Görselleştirmesi
Advanced Quantum Phenomena Visualization with Keçeci Curves

Majorana Fermiyonları, Weyl Fermiyonları, Topolojik Yarımetaller,
Hibrit Kuantum Sistemleri ve Stratum Modeli

Keçeci Eğrileri ile 3B İleri Kuantum Görselleştirmeleri
3D Advanced Quantum Visualizations with Keçeci Curves

Keçeci Eğrileri ile İleri Kuantum Hesaplamaları Görselleştirmesi
Advanced Quantum Computing Visualizations with Keçeci Curves

Keçeci Curve - Kuantum Durumları Görselleştirmesi
Quantum State Visualization with Keçeci Curves

Keçeci Curve - Parametrik Uzay Doldurma Eğrisi Ailesi
Tamamen özgün, çok amaçlı ve esnek bir fraktal eğri üreteci
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from matplotlib.patches import ConnectionPatch
from matplotlib import patches
import colorsys
from enum import Enum
from typing import List, Tuple, Callable, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# Matplotlib yapılandırması - OverflowError çözümü
mpl.rcParams['agg.path.chunksize'] = 20000
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 0.1

# ============================================================================
# ENUM TANIMLAMALARI
# ============================================================================

class ConnectionMode(Enum):
    """Eğri bağlantı modları"""
    CONTINUOUS = "continuous"      # Kesintisiz tek eğri
    LEVEL_WISE = "level_wise"      # Her seviyeyi ayrı bağla
    STAR_BURST = "star_burst"      # Merkezden dışa ışınsal
    SPIRAL = "spiral"              # Spiral bağlantı
    ZIGZAG = "zigzag"              # Zigzag desenli

class ChildOrdering(Enum):
    """Çocuk hücre sıralama stratejileri"""
    SEQUENTIAL = "sequential"       # Sıralı (0,1,2,...)
    ALTERNATING = "alternating"     # Alternatif (0,2,4,...,1,3,5,...)
    REVERSE_ALTERNATING = "reverse_alternating"  # Ters alternatif
    RANDOM = "random"               # Rastgele (seed ile tekrarlanabilir)
    ANGLE_BASED = "angle_based"     # Açıya göre sırala
    SPIRAL_INWARD = "spiral_inward" # Dıştan içe spiral
    SPIRAL_OUTWARD = "spiral_outward" # İçten dışa spiral
    QUADRANT = "quadrant"           # Çeyrek dairelere göre grupla
    CUSTOM = "custom"               # Özel fonksiyon ile

class GrowthDirection(Enum):
    """Büyüme yönü"""
    INWARD = "inward"     # İçe doğru (çocuklar ebeveynin içinde)
    OUTWARD = "outward"   # Dışa doğru (çocuklar ebeveynin dışında)
    TANGENT = "tangent"   # Teğet (çocuklar ebeveyne teğet)
    OVERLAPPING = "overlapping"  # Örtüşmeli


# ============================================================================
# KLASİK UZAY DOLDURMA EĞRİLERİ
# ============================================================================

class ClassicalCurves:
    """Klasik uzay doldurma eğrilerinin implementasyonları"""
    
    @staticmethod
    def hilbert_curve(order: int) -> List[Tuple[float, float]]:
        """
        Hilbert eğrisi - Başlangıç ve bitiş birbirinden uzak
        
        Özellikler:
        - Kare grid üzerinde çalışır (2^order × 2^order)
        - Her seviyede 4 alt bölgeye ayrılır
        - Lokalite koruması en yüksek eğrilerden biridir
        - Başlangıç ve bitiş noktaları grid'in zıt köşelerindedir
        """
        def hilbert_recursive(n: int, x: float, y: float, xi: float, xj: float, yi: float, yj: float) -> List:
            if n <= 0:
                return [(x + (xi + yi)/2, y + (xj + yj)/2)]
            
            points = []
            points.extend(hilbert_recursive(n-1, x, y, yi/2, yj/2, xi/2, xj/2))
            points.extend(hilbert_recursive(n-1, x+xi/2, y+xj/2, xi/2, xj/2, yi/2, yj/2))
            points.extend(hilbert_recursive(n-1, x+xi/2+yi/2, y+xj/2+yj/2, xi/2, xj/2, yi/2, yj/2))
            points.extend(hilbert_recursive(n-1, x+xi/2+yi, y+xj/2+yj, -yi/2, -yj/2, -xi/2, -xj/2))
            return points
        
        size = 2.0
        points = hilbert_recursive(order, -size/2, -size/2, size, 0, 0, size)
        return points
    
    @staticmethod
    def morton_curve(order: int) -> List[Tuple[float, float]]:
        """
        Morton (Z-order) eğrisi - Sıçramalı
        
        Özellikler:
        - Bit serpiştirme (bit interleaving) ile çalışır
        - Hesaplaması en hızlı eğrilerden biridir
        - Süreksizdir - eğri üzerinde sıçramalar vardır
        - Lokalite koruması Hilbert'ten düşüktür
        """
        n = 2 ** order
        points = []
        
        for i in range(n * n):
            x = y = 0
            for j in range(order):
                x |= ((i >> (2*j)) & 1) << j
                y |= ((i >> (2*j + 1)) & 1) << j
            
            px = (x / n) * 2 - 1
            py = (y / n) * 2 - 1
            points.append((px, py))
        
        return points
    
    @staticmethod
    def moore_curve(order: int) -> List[Tuple[float, float]]:
        """
        Moore eğrisi - Başlangıç ve bitiş 1 birim komşu (KAPALI DEĞİL!)
        
        Özellikler:
        - Hilbert eğrisinin döngüsel varyantıdır
        - Başlangıç ve bitiş noktaları arasında 1 birim mesafe vardır
        - Bu sayede eğri bir kenar ile birleştirilerek döngü oluşturulabilir
        - L-System ile üretilir: Axiom: LFL+F+LFL
        
        NOT: Kapalı döngü DEĞİLDİR! Başlangıç ve bitiş aynı nokta değil,
        1 birim komşudur.
        """
        # L-System sabitleri
        _AXIOM = "LFL+F+LFL"
        _RULES = {
            'L': '-RF+LFL+FR-',
            'R': '+LF-RFR-FL+'
        }
        _DIRECTIONS = [
            (1, 0),   # 0: Doğu
            (0, -1),  # 1: Güney
            (-1, 0),  # 2: Batı
            (0, 1),   # 3: Kuzey
        ]
        
        # L-System dizisini oluştur
        result = _AXIOM
        for _ in range(order):
            result = "".join(_RULES.get(ch, ch) for ch in result)
        
        # Koordinatlara çevir
        x, y = 0.0, 0.0
        direction = 0
        points = [(x, y)]
        step = 2.0 / (2 ** order)
        
        for ch in result:
            if ch == 'F':
                dx, dy = _DIRECTIONS[direction]
                x += dx * step
                y += dy * step
                points.append((x, y))
            elif ch == '+':
                direction = (direction + 1) % 4
            elif ch == '-':
                direction = (direction - 1) % 4
        
        # Merkezle
        if points:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            cx = (max(xs) + min(xs)) / 2
            cy = (max(ys) + min(ys)) / 2
            points = [(x - cx, y - cy) for x, y in points]
            
            # Başlangıç ve bitiş aynı ise son noktayı kaldır
            if len(points) >= 2 and points[0] == points[-1]:
                points = points[:-1]
        
        return points
    
    @staticmethod
    def sierpinski_curve(order: int) -> List[Tuple[float, float]]:
        """
        Sierpinski Eğrisi - Kapalı döngüsel üçgen tabanlı eğri
        
        Özellikler:
        - Sierpinski üçgeni fraktalının sınırlarını dolaşan KAPALI bir eğridir
        - Her seviyede 3 alt üçgene ayrılır
        - Başlangıç ve bitiş AYNI noktadır (kapalı döngü)
        - Üçgen geometrisi kullanan tek klasik uzay doldurma eğrisidir
        - Diğer eğrilerden farklı olarak 3'lü simetriye sahiptir
        
        NOT: Bu eğri, Sierpinski üçgeninin TÜM KENARLARINI dolaşır.
        Alt üçgenler arasında GÖRÜNÜR bağlantı çizgileri YOKTUR.
        Sadece üçgenlerin sınırları çizilir.
        """
        def midpoint(p1, p2):
            return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        
        def generate_edges(level, p1, p2, p3):
            """
            Sierpinski üçgeninin kenarlarını özyinelemeli olarak oluştur
            
            Strateji: Her seviyede üçgen 3 alt üçgene bölünür.
            Her alt üçgenin kenarları sırayla dolaşılır.
            """
            if level == 0:
                # Temel durum: Tek bir üçgenin üç kenarı
                return [p1, p2, p3, p1]
            
            # Kenarların orta noktaları
            m12 = midpoint(p1, p2)
            m23 = midpoint(p2, p3)
            m31 = midpoint(p3, p1)
            
            edges = []
            # Üst üçgen (p1, m12, m31)
            edges.extend(generate_edges(level-1, p1, m12, m31))
            # Sol alt üçgen (m12, p2, m23)
            edges.extend(generate_edges(level-1, m12, p2, m23))
            # Sağ alt üçgen (m31, m23, p3)
            edges.extend(generate_edges(level-1, m31, m23, p3))
            
            return edges
        
        # Eşkenar üçgen köşeleri
        size = 2.0
        h = size * np.sqrt(3) / 2
        
        p1 = (0.0, h/2)        # Üst köşe
        p2 = (-size/2, -h/2)   # Sol alt köşe
        p3 = (size/2, -h/2)    # Sağ alt köşe
        
        points = generate_edges(order, p1, p2, p3)
        
        # SADECE ARDIŞIK AYNILARI TEMİZLE
        cleaned = []
        for p in points:
            if not cleaned:
                cleaned.append(p)
            else:
                dist = np.sqrt((p[0] - cleaned[-1][0])**2 + (p[1] - cleaned[-1][1])**2)
                if dist > 0.0001:
                    cleaned.append(p)
        
        # Kapalı döngü için başlangıcı ekle
        if cleaned and cleaned[0] != cleaned[-1]:
            cleaned.append(cleaned[0])
        
        return cleaned


class CurveComparisonVisualizer:
    
    def __init__(self):
        pass
    
    def create_start_end_comparison(self):
        """
        Başlangıç-Bitiş ilişkisi karşılaştırması
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
        
        for idx, curve_name in enumerate(curves):
            ax = axes[idx // 3, idx % 3]
            ax.set_facecolor('#0a0a1a')
            
            points = self._get_curve_points(curve_name, 3)
            color = COMPARISON_DATA[curve_name]['color']
            
            if len(points) > 1:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                
                # Ana eğri
                ax.plot(xs, ys, '-', color=color, linewidth=2.5, alpha=0.8)
                
                # Başlangıç ve bitiş noktaları
                ax.scatter(xs[0], ys[0], color='white', s=200, marker='o', 
                          edgecolor=color, linewidth=3, zorder=10, label='Başlangıç')
                ax.scatter(xs[-1], ys[-1], color='yellow', s=200, marker='s', 
                          edgecolor=color, linewidth=3, zorder=10, label='Bitiş')
                
                # Başlangıç ve bitiş arası mesafe analizi
                dist = np.sqrt((xs[0] - xs[-1])**2 + (ys[0] - ys[-1])**2)
                
                if curve_name == 'Moore':
                    ax.plot([xs[0], xs[-1]], [ys[0], ys[-1]], '--', 
                           color='yellow', linewidth=2, alpha=0.7, 
                           label=f'1-Birim Komşu ({dist:.3f})')
                    
                    ax.text(0.5, -0.15, 
                           f"Başlangıç-Bitiş: 1-Birim Komşu\n"
                           f"(Kapalı Döngü DEĞİL)",
                           transform=ax.transAxes,
                           color='yellow', fontsize=11, ha='center',
                           bbox=dict(boxstyle='round', facecolor='#1a1a3a', 
                                    edgecolor='yellow', alpha=0.8))
                elif curve_name == 'Sierpinski':
                    status = "✅ Kapalı Döngü (aynı nokta)" if dist < 0.1 else f"Mesafe: {dist:.3f}"
                    ax.text(0.5, -0.15, f"Başlangıç-Bitiş: {status}",
                           transform=ax.transAxes,
                           color='#88ff88' if dist < 0.1 else 'white', 
                           fontsize=10, ha='center')
                else:
                    status = "Kapalı Döngü" if dist < 0.1 else f"Mesafe: {dist:.3f}"
                    ax.text(0.5, -0.15, f"Başlangıç-Bitiş: {status}",
                           transform=ax.transAxes,
                           color='white', fontsize=10, ha='center')
            
            self._add_background_grid(ax, points)
            
            title = f"\n{curve_name} Eğrisi\n{COMPARISON_DATA[curve_name]['desc']}"
            ax.set_title(title, color='white', fontsize=12, fontweight='bold')
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            
            for spine in ax.spines.values():
                spine.set_color('#333366')
        
        # 6. subplot: Karşılaştırma tablosu
        ax_info = axes[1, 2]
        ax_info.set_facecolor('#0a0a1a')
        self._draw_start_end_table(ax_info)
        
        plt.suptitle("Uzay Doldurma Eğrilerinde Başlangıç-Bitiş İlişkisi\n"
                    "Moore: 1-Birim Komşu | Sierpinski: Kapalı Döngü", 
                    color='white', fontsize=16, fontweight='bold', y=0.99)
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def create_comprehensive_comparison(self):
        """Kapsamlı karşılaştırma"""
        fig = plt.figure(figsize=(24, 14))
        fig.patch.set_facecolor('#0a0a1a')
        
        curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
        
        for idx, curve_name in enumerate(curves):
            ax = fig.add_subplot(2, 3, idx + 1)
            ax.set_facecolor('#0a0a1a')
            
            points = self._get_curve_points(curve_name, 3)
            color = COMPARISON_DATA[curve_name]['color']
            
            if len(points) > 1:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                
                ax.plot(xs, ys, '-', color=color, linewidth=2.5, alpha=0.9)
                
                ax.scatter(xs[0], ys[0], color='white', s=100, marker='o', 
                          edgecolor=color, linewidth=2, zorder=5)
                ax.scatter(xs[-1], ys[-1], color='yellow', s=100, marker='s', 
                          edgecolor=color, linewidth=2, zorder=5)
                
                if curve_name == 'Moore':
                    ax.plot([xs[0], xs[-1]], [ys[0], ys[-1]], '--', 
                           color='yellow', linewidth=1.5, alpha=0.5)
            
            self._add_background_grid(ax, points)
            
            title = f"{curve_name}\n{COMPARISON_DATA[curve_name]['desc']}"
            ax.set_title(title, color='white', fontsize=12, fontweight='bold')
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            
            for spine in ax.spines.values():
                spine.set_color('#333366')
        
        ax_table = fig.add_subplot(2, 3, 6)
        ax_table.set_facecolor('#0a0a1a')
        self._draw_comparison_table(ax_table)
        
        plt.suptitle("Uzay Doldurma Eğrileri Karşılaştırması", 
                    color='white', fontsize=18, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def _get_curve_points(self, curve_name: str, level: int) -> List:
        if curve_name == 'Keçeci':
            curve = KececiCurve(num_children=5, max_level=level, base_radius=1.5, scale_factor=0.42)
            return curve.generate()
        elif curve_name == 'Hilbert':
            return ClassicalCurves.hilbert_curve(level)
        elif curve_name == 'Morton':
            return ClassicalCurves.morton_curve(level)
        elif curve_name == 'Moore':
            return ClassicalCurves.moore_curve(level)
        elif curve_name == 'Sierpinski':
            return ClassicalCurves.sierpinski_curve(level)
        return []
    
    def _add_background_grid(self, ax, points):
        if not points:
            return
        
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        margin = 0.5
        x_min, x_max = min(xs) - margin, max(xs) + margin
        y_min, y_max = min(ys) - margin, max(ys) + margin
        
        grid_size = 0.5
        x_grid = np.arange(np.floor(x_min/grid_size)*grid_size, 
                          np.ceil(x_max/grid_size)*grid_size, grid_size)
        y_grid = np.arange(np.floor(y_min/grid_size)*grid_size, 
                          np.ceil(y_max/grid_size)*grid_size, grid_size)
        
        for x in x_grid:
            ax.axvline(x, color='white', alpha=0.05, linewidth=0.5)
        for y in y_grid:
            ax.axhline(y, color='white', alpha=0.05, linewidth=0.5)
        
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    
    def _draw_comparison_table(self, ax):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        ax.text(5, 9.5, "Özellik Karşılaştırma Tablosu", color='white', fontsize=14, 
               fontweight='bold', ha='center')
        
        headers = ['Özellik', 'Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
        header_colors = ['#666666', '#ff4444', '#4488ff', '#44ff44', '#ffff44', '#ff44ff']
        
        for i, (header, color) in enumerate(zip(headers, header_colors)):
            x = 0.5 + i * 1.6
            ax.text(x, 8.5, header, color=color, fontsize=9, fontweight='bold', ha='center')
        
        rows = [
            ('Geometri', 'Dairesel', 'Kare', 'Kare', 'Kare', 'Üçgen'),
            ('Başlangıç-Bitiş', 'Değişken', 'Uzak', 'Uzak', '1-Birim Komşu ⭐', 'Kapalı ✅'),
            ('Süreklilik', 'İsteğe Bağlı', 'Sürekli', 'Sıçramalı', 'Sürekli', 'Kapalı'),
            ('Lokalite', 'Yüksek', 'Çok Yüksek', 'Orta', 'Yüksek', 'Orta'),
        ]
        
        for row_idx, (feature, *values) in enumerate(rows):
            y = 7.0 - row_idx * 1.2
            
            ax.text(0.5, y, feature, color='#aaaaff', fontsize=9, ha='left')
            
            for col_idx, value in enumerate(values):
                x = 2.1 + col_idx * 1.6
                
                if col_idx == 0:
                    ax.text(x, y, value, color='#ff8888', fontsize=9, ha='center', fontweight='bold')
                elif col_idx == 3 and 'Komşu' in value:
                    ax.text(x, y, value, color='yellow', fontsize=9, ha='center', fontweight='bold')
                elif col_idx == 4 and 'Kapalı' in value:
                    ax.text(x, y, value, color='#88ff88', fontsize=9, ha='center', fontweight='bold')
                else:
                    ax.text(x, y, value, color='white', fontsize=9, ha='center')
        
        ax.text(5, 1.8, "⭐ Moore: 1-birim komşu (Kapalı DEĞİL)", 
               color='yellow', fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='#1a1a3a', edgecolor='yellow'))
        ax.text(5, 0.8, "✅ Sierpinski: Aynı noktada birleşir (Kapalı Döngü)", 
               color='#88ff88', fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='#1a1a3a', edgecolor='#88ff88'))
    
    def _draw_start_end_table(self, ax):
        ax.set_xlim(0, 10)
        ax.set_ylim(0,10)
        ax.axis('off')
        
        ax.text(5, 9.5, "Başlangıç-Bitiş İlişkisi", color='white', fontsize=14, 
               fontweight='bold', ha='center')
        
        info = [
            ("Hilbert", "Uzak (ayrık uçlar)", '#4488ff'),
            ("Morton", "Uzak (sıçramalı)", '#44ff44'),
            ("Moore", "1-Birim Komşu ⭐ (kapalı DEĞİL)", '#ffff44'),
            ("Sierpinski", "Kapalı Döngü ✅ (aynı nokta)", '#ff44ff'),
            ("Keçeci", "Parametrik - Ayarlanabilir", '#ff4444'),
        ]
        
        for i, (name, desc, color) in enumerate(info):
            y = 7.5 - i * 1.2
            ax.text(1, y, f"{name}:", color=color, fontsize=11, fontweight='bold')
            ax.text(3.5, y, desc, color='white', fontsize=10)
        
        ax.text(5, 1.5, "Moore: Başlangıç ve bitiş 1 birim komşudur\n"
                         "Sierpinski: Başlangıç ve bitiş aynı noktadır (Kapalı)",
               color='white', fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='#1a1a3a', edgecolor='#333366'))

# ============================================================================
# OPTİMİZE KEÇECİ EĞRİSİ - ÖNBELLEK DESTEKLİ
# ============================================================================

class KececiCurve:
    """Optimize Keçeci Eğrisi - Sonuçları önbelleğe alır"""
    
    _cache = {}
    
    def __init__(
        self,
        num_children: int = 6,
        max_level: int = 3,
        scale_factor: float = 0.45,
        base_radius: float = 1.8,
        angle_offset: float = 0.0,
        angle_variation: float = 0.0,
        growth_mode: str = 'outward',
        ordering_mode: str = 'sequential',
    ):
        self.num_children = num_children
        self.max_level = max_level
        self.scale_factor = scale_factor
        self.base_radius = base_radius
        self.angle_offset = angle_offset
        self.angle_variation = angle_variation
        self.growth_mode = growth_mode
        self.ordering_mode = ordering_mode
        self.points = []
        
        self._cache_key = (num_children, max_level, scale_factor, base_radius,
                          angle_offset, angle_variation, growth_mode, ordering_mode)
    
    def generate(self) -> List[Tuple[float, float]]:
        if self._cache_key in self._cache:
            return self._cache[self._cache_key]
        
        self.points = []
        self._generate_recursive((0.0, 0.0), self.base_radius, 0, 0.0)
        self._cache[self._cache_key] = self.points
        
        if len(self._cache) > 50:
            for key in list(self._cache.keys())[:10]:
                del self._cache[key]
        
        return self.points
    
    def _generate_recursive(self, center: Tuple, radius: float, level: int, angle: float):
        if level > self.max_level:
            self.points.append(center)
            return
        
        self.points.append(center)
        child_radius = radius * self.scale_factor
        
        children = []
        for i in range(self.num_children):
            child_angle = (2 * np.pi * i / self.num_children + 
                          self.angle_offset + 
                          self.angle_variation * level)
            
            if self.growth_mode == 'inward':
                distance = radius - child_radius
            elif self.growth_mode == 'tangent':
                distance = radius
            else:
                distance = radius + child_radius
            
            child_x = center[0] + distance * np.cos(child_angle)
            child_y = center[1] + distance * np.sin(child_angle)
            children.append((child_x, child_y, child_angle))
        
        if self.ordering_mode == 'alternating':
            even = [c for i, c in enumerate(children) if i % 2 == 0]
            odd = [c for i, c in enumerate(children) if i % 2 == 1]
            children = even + odd
        elif self.ordering_mode == 'spiral':
            children = sorted(children, key=lambda c: c[2])
        elif self.ordering_mode == 'reverse_spiral':
            children = sorted(children, key=lambda c: c[2], reverse=True)
        
        for child_x, child_y, child_angle in children:
            self._generate_recursive((child_x, child_y), child_radius, level + 1, child_angle)


# ============================================================================
# HIZLI GÖRSELLEŞTİRME FONKSİYONU
# ============================================================================

def quick_plot(curves_config: List[dict], title: str, rows: int = 2, cols: int = 3,
               bg_color: str = '#0a0a1a', special_elements: dict = None):
    """Hızlı çoklu grafik çizimi"""
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    fig.patch.set_facecolor(bg_color)
    axes_flat = axes.flatten() if rows * cols > 1 else [axes]
    
    color_themes = {
        'flower': lambda i, n: colorsys.hsv_to_rgb(0.75 + 0.15*np.sin(i/50), 0.8, 1.0),
        'galaxy': lambda i, n: colorsys.hsv_to_rgb(0.6 + 0.2*i/n, 0.7, 0.5 + 0.3*i/n),
        'snowflake': lambda i, n: colorsys.hsv_to_rgb(0.55, 0.3 + 0.3*i/n, 1.0),
        'mandala': lambda i, n: colorsys.hsv_to_rgb(0.05 + 0.3*i/n, 0.9, 0.9),
        'tree': lambda i, n: (colorsys.hsv_to_rgb(0.07, 0.8, 0.4) if i/n < 0.15 
                             else colorsys.hsv_to_rgb(0.25 + 0.15*i/n, 0.7, 0.4 + 0.4*i/n)),
        'marine': lambda i, n: colorsys.hsv_to_rgb(0.45 + 0.2*np.sin(i/40), 0.6 + 0.2*np.cos(i/50), 0.9),
        'cosmic': lambda i, n: colorsys.hsv_to_rgb(0.7, 0.5, 0.2 + 0.3*i/n),
        'neural': lambda i, n: colorsys.hsv_to_rgb(0.3 if i/n < 0.3 else (0.55 if i/n < 0.7 else 0.8), 0.8, 0.7),
        'virus': lambda i, n: colorsys.hsv_to_rgb(0.0 + 0.3*i/n, 0.85, 0.8),
    }
    
    for idx, config in enumerate(curves_config):
        if idx >= len(axes_flat):
            break
            
        ax = axes_flat[idx]
        ax.set_facecolor(bg_color)
        
        curve = KececiCurve(**config['params'])
        points = np.array(curve.generate())
        
        color_func = color_themes.get(config.get('color_theme', 'galaxy'), 
                                      lambda i, n: plt.cm.viridis(i/n))
        
        n = len(points)
        step = max(1, n // 500)
        
        for i in range(0, n - 1, step):
            end = min(i + step + 1, n)
            color = color_func(i, n)
            linewidth = config.get('linewidth', 1.2)
            ax.plot(points[i:end, 0], points[i:end, 1], '-', 
                   color=color, linewidth=linewidth, alpha=0.85)
        
        # Başlangıç noktası
        ax.scatter(points[0, 0], points[0, 1], color='white', s=40, marker='o', 
                  edgecolor='cyan', linewidth=1.5, zorder=5)
        
        # Özel elemanlar
        if special_elements and config.get('special'):
            elem = special_elements[config['special']]
            if elem == 'center_star':
                ax.scatter(0, 0, color='yellow', s=150, marker='*', 
                          edgecolor='orange', linewidth=2, zorder=10)
            elif elem == 'center_white':
                ax.scatter(0, 0, color='white', s=100, marker='o', 
                          edgecolor='cyan', linewidth=2, zorder=10)
            elif elem == 'leaf_points':
                leaf_idx = np.linspace(n//2, n-1, 10, dtype=int)
                ax.scatter(points[leaf_idx, 0], points[leaf_idx, 1], 
                          color='lightgreen', s=15, alpha=0.7, marker='^')
            elif elem == 'neuron_nodes':
                step_n = max(1, n // 30)
                sizes = 15 + 25 * np.random.random(len(points[::step_n]))
                ax.scatter(points[::step_n, 0], points[::step_n, 1], 
                          c='cyan', s=sizes, alpha=0.7, edgecolors='white', linewidth=0.5)
        
        ax.set_title(config['title'], color='white', fontsize=10, fontweight='bold')
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        if 'xlim' in config:
            ax.set_xlim(config['xlim'])
            ax.set_ylim(config['ylim'])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    for idx in range(len(curves_config), len(axes_flat)):
        axes_flat[idx].set_visible(False)
    
    plt.suptitle(title, color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


# ============================================================================
# 1. ÇİÇEK DESENLERİ
# ============================================================================

def flower_patterns():
    configs = [
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.1, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Gül\n8 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
        {'params': {'num_children': 12, 'max_level': 3, 'scale_factor': 0.3, 
                    'angle_variation': 0.15, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Kasımpatı\n12 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'alternating'},
         'title': 'Yıldız Çiçeği\n5 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
        {'params': {'num_children': 10, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.2, 'growth_mode': 'inward', 'ordering_mode': 'reverse_spiral'},
         'title': 'Lotus\n10 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
        {'params': {'num_children': 7, 'max_level': 3, 'scale_factor': 0.38, 
                    'angle_variation': 0.12, 'growth_mode': 'tangent', 'ordering_mode': 'spiral'},
         'title': 'Orkide\n7 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
        {'params': {'num_children': 16, 'max_level': 2, 'scale_factor': 0.3, 
                    'angle_variation': 0.08, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Ayçiçeği\n16 yaprak', 'color_theme': 'flower', 'special': 'center_star'},
    ]
    quick_plot(configs, "🌺 Keçeci Eğrisi - Çiçek Desenleri", rows=2, cols=3,
               special_elements={'center_star': 'center_star'})


# ============================================================================
# 2. GALAKSİ DESENLERİ
# ============================================================================

def galaxy_patterns():
    configs = [
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.25, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Sarmal\n8 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.38, 
                    'angle_variation': 0.3, 'growth_mode': 'outward', 'ordering_mode': 'reverse_spiral'},
         'title': 'Ters Sarmal\n6 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
        {'params': {'num_children': 10, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.2, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Çubuklu\n10 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.35, 'growth_mode': 'outward', 'ordering_mode': 'alternating'},
         'title': 'Düzensiz\n12 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.42, 
                    'angle_variation': 0.15, 'growth_mode': 'tangent', 'ordering_mode': 'spiral'},
         'title': 'Eliptik\n5 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
        {'params': {'num_children': 7, 'max_level': 3, 'scale_factor': 0.36, 
                    'angle_variation': 0.28, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Halka\n7 kol', 'color_theme': 'galaxy', 'special': 'center_white'},
    ]
    quick_plot(configs, "🌌 Keçeci Eğrisi - Galaksi Desenleri", rows=2, cols=3, bg_color='#050510',
               special_elements={'center_white': 'center_white'})


# ============================================================================
# 3. KAR TANELERİ
# ============================================================================

def snowflake_patterns():
    configs = [
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'sequential'},
         'title': 'Klasik\n6 kol', 'color_theme': 'snowflake'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.1, 'growth_mode': 'inward', 'ordering_mode': 'alternating'},
         'title': 'Yıldız\nİçe büyüyen', 'color_theme': 'snowflake'},
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Çift\n12 kol', 'color_theme': 'snowflake'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.45, 
                    'angle_variation': 0.05, 'growth_mode': 'tangent', 'ordering_mode': 'sequential'},
         'title': 'Dentritik\nTeğet', 'color_theme': 'snowflake'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.38, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Sarmal\nSpiral', 'color_theme': 'snowflake'},
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'sequential'},
         'title': 'Sekizgen\n8 kol', 'color_theme': 'snowflake'},
    ]
    quick_plot(configs, "❄️ Keçeci Eğrisi - Kar Taneleri", rows=2, cols=3, bg_color='#0a0a2a')


# ============================================================================
# 4. MANDALA DESENLERİ
# ============================================================================

def mandala_patterns():
    configs = [
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.5, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Klasik\n8 kat', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.48, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'alternating'},
         'title': '12 Katlı\nAlternatif', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.52, 
                    'angle_variation': 0.05, 'growth_mode': 'inward', 'ordering_mode': 'reverse_spiral'},
         'title': 'Çiçek\n6 kat', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
        {'params': {'num_children': 16, 'max_level': 2, 'scale_factor': 0.45, 
                    'angle_variation': 0.0, 'growth_mode': 'tangent', 'ordering_mode': 'spiral'},
         'title': '16 Katlı\nTeğet', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
        {'params': {'num_children': 10, 'max_level': 3, 'scale_factor': 0.48, 
                    'angle_variation': 0.03, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': '10 Katlı\nKıvrımlı', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.5, 
                    'angle_variation': 0.0, 'growth_mode': 'outward', 'ordering_mode': 'sequential'},
         'title': '5 Katlı\nBasit', 'color_theme': 'mandala', 'xlim': [-2.5, 2.5], 'ylim': [-2.5, 2.5]},
    ]
    quick_plot(configs, "🕉️ Keçeci Eğrisi - Mandala Desenleri", rows=2, cols=3, bg_color='#1a0a1a')


# ============================================================================
# 5. FRAKTAL AĞAÇLAR
# ============================================================================

def fractal_trees():
    configs = [
        {'params': {'num_children': 3, 'max_level': 4, 'scale_factor': 0.5, 
                    'angle_variation': 0.15, 'growth_mode': 'outward', 'ordering_mode': 'alternating',
                    'angle_offset': -np.pi/2},
         'title': 'Çam\n3 dal', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
        {'params': {'num_children': 4, 'max_level': 4, 'scale_factor': 0.45, 
                    'angle_variation': 0.1, 'growth_mode': 'outward', 'ordering_mode': 'spiral',
                    'angle_offset': -np.pi/2},
         'title': 'Meşe\n4 dal', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
        {'params': {'num_children': 2, 'max_level': 5, 'scale_factor': 0.6, 
                    'angle_variation': 0.2, 'growth_mode': 'outward', 'ordering_mode': 'sequential',
                    'angle_offset': -np.pi/2},
         'title': 'Söğüt\n2 dal', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.45, 
                    'angle_variation': 0.12, 'growth_mode': 'outward', 'ordering_mode': 'reverse_spiral',
                    'angle_offset': -np.pi/2},
         'title': 'Akçaağaç\n5 dal', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
        {'params': {'num_children': 3, 'max_level': 4, 'scale_factor': 0.55, 
                    'angle_variation': 0.25, 'growth_mode': 'tangent', 'ordering_mode': 'alternating',
                    'angle_offset': -np.pi/2},
         'title': 'Çınar\nTeğet', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
        {'params': {'num_children': 4, 'max_level': 4, 'scale_factor': 0.5, 
                    'angle_variation': 0.18, 'growth_mode': 'inward', 'ordering_mode': 'spiral',
                    'angle_offset': -np.pi/2},
         'title': 'Bonsai\nİçe', 'color_theme': 'tree', 'special': 'leaf_points', 'linewidth': 2.0},
    ]
    quick_plot(configs, "🌳 Keçeci Eğrisi - Fraktal Ağaçlar", rows=2, cols=3, bg_color='#0a1a0a',
               special_elements={'leaf_points': 'leaf_points'})


# ============================================================================
# 6. DENİZ CANLILARI
# ============================================================================

def marine_patterns():
    configs = [
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.2, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Deniz Yıldızı\n5 kol', 'color_theme': 'marine'},
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.15, 'growth_mode': 'inward', 'ordering_mode': 'alternating'},
         'title': 'Ahtapot\n8 kol', 'color_theme': 'marine'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.38, 
                    'angle_variation': 0.1, 'growth_mode': 'tangent', 'ordering_mode': 'reverse_spiral'},
         'title': 'Deniz Kestanesi\n6 kol', 'color_theme': 'marine'},
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.18, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Mercan\n12 kol', 'color_theme': 'marine'},
        {'params': {'num_children': 7, 'max_level': 3, 'scale_factor': 0.42, 
                    'angle_variation': 0.22, 'growth_mode': 'outward', 'ordering_mode': 'alternating'},
         'title': 'Deniz Anası\n7 kol', 'color_theme': 'marine'},
        {'params': {'num_children': 4, 'max_level': 4, 'scale_factor': 0.45, 
                    'angle_variation': 0.12, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Deniz Kabuğu\n4 kol', 'color_theme': 'marine'},
    ]
    quick_plot(configs, "🐠 Keçeci Eğrisi - Deniz Canlıları", rows=2, cols=3, bg_color='#0a1a2a')


# ============================================================================
# 7. KOZMİK AĞ
# ============================================================================

def cosmic_web():
    configs = [
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.35, 
                    'angle_variation': 0.4, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Kozmik Ağ\nGalaksi kümeleri', 'color_theme': 'cosmic', 'xlim': [-3, 3], 'ylim': [-3, 3]},
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.3, 
                    'angle_variation': 0.5, 'growth_mode': 'outward', 'ordering_mode': 'alternating'},
         'title': 'Karanlık Madde\nFilamentler', 'color_theme': 'cosmic', 'xlim': [-3, 3], 'ylim': [-3, 3]},
        {'params': {'num_children': 10, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.45, 'growth_mode': 'tangent', 'ordering_mode': 'reverse_spiral'},
         'title': 'Süperküme\nBüyük ölçek', 'color_theme': 'cosmic', 'xlim': [-3, 3], 'ylim': [-3, 3]},
    ]
    quick_plot(configs, "🌠 Keçeci Eğrisi - Kozmik Ağ", rows=1, cols=3, bg_color='#020208')


# ============================================================================
# 8. SİNİR AĞI
# ============================================================================

def neural_network_patterns():
    configs = [
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.1, 'growth_mode': 'inward', 'ordering_mode': 'alternating'},
         'title': 'Yoğun Ağ\n8 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.38, 
                    'angle_variation': 0.08, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Derin Ağ\n12 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.45, 
                    'angle_variation': 0.15, 'growth_mode': 'tangent', 'ordering_mode': 'alternating'},
         'title': 'CNN Ağı\n6 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
        {'params': {'num_children': 10, 'max_level': 3, 'scale_factor': 0.38, 
                    'angle_variation': 0.12, 'growth_mode': 'inward', 'ordering_mode': 'reverse_spiral'},
         'title': 'RNN Ağı\n10 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.5, 
                    'angle_variation': 0.05, 'growth_mode': 'outward', 'ordering_mode': 'spiral'},
         'title': 'Perceptron\n5 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
        {'params': {'num_children': 16, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.06, 'growth_mode': 'inward', 'ordering_mode': 'alternating'},
         'title': 'Tam Bağlı\n16 bağlantı', 'color_theme': 'neural', 'special': 'neuron_nodes'},
    ]
    quick_plot(configs, "🧠 Keçeci Eğrisi - Yapay Sinir Ağı", rows=2, cols=3, bg_color='#0a0a1a',
               special_elements={'neuron_nodes': 'neuron_nodes'})


# ============================================================================
# 9. VİRÜS DESENLERİ
# ============================================================================

def virus_patterns():
    configs = [
        {'params': {'num_children': 12, 'max_level': 2, 'scale_factor': 0.4, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'sequential'},
         'title': 'Adenovirüs\n12 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
        {'params': {'num_children': 20, 'max_level': 2, 'scale_factor': 0.3, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'İkozahedral\n20 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
        {'params': {'num_children': 8, 'max_level': 3, 'scale_factor': 0.4, 
                    'angle_variation': 0.05, 'growth_mode': 'tangent', 'ordering_mode': 'alternating'},
         'title': 'Herpes\n8 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
        {'params': {'num_children': 6, 'max_level': 3, 'scale_factor': 0.45, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'sequential'},
         'title': 'İnfluenza\n6 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
        {'params': {'num_children': 16, 'max_level': 2, 'scale_factor': 0.35, 
                    'angle_variation': 0.0, 'growth_mode': 'inward', 'ordering_mode': 'reverse_spiral'},
         'title': 'HIV\n16 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
        {'params': {'num_children': 5, 'max_level': 3, 'scale_factor': 0.5, 
                    'angle_variation': 0.1, 'growth_mode': 'inward', 'ordering_mode': 'spiral'},
         'title': 'Bakteriyofaj\n5 kat', 'color_theme': 'virus', 'xlim': [-2.3, 2.3], 'ylim': [-2.3, 2.3]},
    ]
    quick_plot(configs, "🦠 Keçeci Eğrisi - Virüs Kapsid Desenleri", rows=2, cols=3, bg_color='#1a0a0a')
    
# ============================================================================
# KARŞILAŞTIRMA VERİLERİ
# ============================================================================

COMPARISON_DATA = {
    'Keçeci': {
        'color': '#ff4444',
        'desc': 'Parametrik, Dairesel',
        'start_end': 'Değişken (Parametrik)',
        'continuity': 'İsteğe Bağlı',
        'locality': 'Yüksek',
        'geometry': 'Dairesel',
        'children': '2-12+',
        'dimensions': '2B ve 3B'
    },
    'Hilbert': {
        'color': '#4488ff',
        'desc': 'Sabit 4-çocuk, Kare',
        'start_end': 'Uzak (Ayrık)',
        'continuity': 'Sürekli',
        'locality': 'Çok Yüksek',
        'geometry': 'Kare',
        'children': '4',
        'dimensions': '2B'
    },
    'Morton': {
        'color': '#44ff44',
        'desc': 'Sabit 4-çocuk, Z-Sıralı',
        'start_end': 'Uzak (Sıçramalı)',
        'continuity': 'Sıçramalı',
        'locality': 'Orta',
        'geometry': 'Kare',
        'children': '4',
        'dimensions': '2B'
    },
    'Moore': {
        'color': '#ffff44',
        'desc': 'Sabit 4-çocuk, Döngüsel',
        'start_end': '1-Birim Komşu ⭐',
        'continuity': 'Sürekli',
        'locality': 'Yüksek',
        'geometry': 'Kare',
        'children': '4',
        'dimensions': '2B'
    },
    'Sierpinski': {
        'color': '#ff44ff',
        'desc': 'Sabit 3-çocuk, Üçgen',
        'start_end': 'Kapalı Döngü ✅',
        'continuity': 'Kapalı',
        'locality': 'Orta',
        'geometry': 'Üçgen',
        'children': '3',
        'dimensions': '2B'
    }
}

def locality_heatmap_comparison():
    """
    Her eğri için lokalite ısı haritası oluşturur
    
    Isı haritası: İndeks olarak yakın noktaların uzamsal mesafesini gösterir
    - Kırmızı: İndeks yakın ama uzamsal uzak (KÖTÜ lokalite)
    - Yeşil/Mavi: İndeks yakın ve uzamsal yakın (İYİ lokalite)
    """
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Hilbert', 'Morton', 'Moore', 'Sierpinski', 'Keçeci']
    titles = ['Hilbert (En İyi Lokalite)', 'Morton (Z-Order)', 'Moore (Döngüsel)', 
              'Sierpinski (Üçgen)', 'Keçeci (Parametrik)']
    
    viz = CurveComparisonVisualizer()
    
    # Tüm matrisler için global vmin/vmax hesapla
    all_matrices = []
    for curve_name in curves:
        points = viz._get_curve_points(curve_name, 4)
        points = np.array(points)
        n = min(64, len(points))
        locality_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    idx_dist = abs(i - j)
                    spatial_dist = np.linalg.norm(points[i] - points[j])
                    locality_matrix[i, j] = spatial_dist / (idx_dist + 1)
        
        all_matrices.append(locality_matrix)
    
    global_vmax = max(m.max() for m in all_matrices)
    
    for idx, (curve_name, title) in enumerate(zip(curves, titles)):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#0a0a1a')
        
        # Eğriyi oluştur
        points = viz._get_curve_points(curve_name, 4)
        points = np.array(points)
        
        # Lokalite matrisi oluştur
        n = min(64, len(points))
        locality_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    idx_dist = abs(i - j)
                    spatial_dist = np.linalg.norm(points[i] - points[j])
                    locality_matrix[i, j] = spatial_dist / (idx_dist + 1)
        
        # Isı haritasını çiz
        im = ax.imshow(locality_matrix, cmap='RdYlGn_r', aspect='auto', 
                      interpolation='bilinear', vmin=0, vmax=global_vmax)
        
        ax.set_title(f"{title}\n(Koyu yeşil = iyi lokalite, Kırmızı = kötü)", 
                    color='white', fontsize=11)
        ax.set_xlabel('İndeks', color='white')
        ax.set_ylabel('İndeks', color='white')
        ax.tick_params(colors='white')
    
    # Boş subplot'u gizle
    axes[1, 2].set_visible(False)
    
    # ================================================================
    # DÜZELTME: Renk çubuğunu doğru konuma yerleştir
    # ================================================================
    # Figürün sağ tarafında yeni bir eksen oluştur
    cbar_ax = fig.add_axes([0.92, 0.25, 0.015, 0.5])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Uzamsal Mesafe / İndeks Mesafesi\n(Düşük = İyi Lokalite)', 
                   color='white', fontsize=10)
    cbar_ax.tick_params(colors='white')
    cbar_ax.yaxis.label.set_color('white')
    
    plt.suptitle("Uzay Doldurma Eğrileri - Lokalite Karşılaştırması\n"
                "Koyu yeşil: İndeks yakınlığı = Uzamsal yakınlık (İYİ)\n"
                "Kırmızı: İndeks yakın ama uzamsal uzak (KÖTÜ)", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])  # Sağda renk çubuğu için yer bırak
    plt.show()


def continuity_visualization():
    """
    Eğrilerin sürekliliğini renk gradyanı ile gösterir
    
    - Kesintisiz renk geçişi = Sürekli eğri
    - Ani renk değişimleri = Sıçramalı eğri (Morton)
    """
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
    colors_map = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#ff44ff']
    titles = ['Keçeci (Parametrik)', 'Hilbert (Sürekli)', 'Morton (Sıçramalı)', 
              'Moore (Döngüsel)', 'Sierpinski (Kapalı)']
    
    viz = CurveComparisonVisualizer()
    
    for idx, (curve_name, base_color, title) in enumerate(zip(curves, colors_map, titles)):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#0a0a1a')
        
        points = viz._get_curve_points(curve_name, 4)
        points = np.array(points)
        
        # Her noktayı indeksine göre renklendir
        colors = plt.cm.viridis(np.linspace(0, 1, len(points)))
        
        # Noktaları çiz
        ax.scatter(points[:, 0], points[:, 1], c=colors, s=10, alpha=0.8)
        
        # Başlangıç ve bitiş
        ax.scatter(points[0, 0], points[0, 1], color='white', s=150, marker='o', 
                  edgecolor=base_color, linewidth=3, zorder=10, label='Başlangıç')
        ax.scatter(points[-1, 0], points[-1, 1], color='yellow', s=150, marker='s', 
                  edgecolor=base_color, linewidth=3, zorder=10, label='Bitiş')
        
        # Morton için sıçrama noktalarını işaretle
        if curve_name == 'Morton':
            jump_count = 0
            for i in range(1, len(points)):
                dist = np.linalg.norm(points[i] - points[i-1])
                if dist > 0.5:  # Büyük sıçrama
                    ax.plot(points[i-1:i+1, 0], points[i-1:i+1, 1], 
                           'r--', linewidth=1, alpha=0.5)
                    jump_count += 1
            ax.text(0.5, -0.15, f"{jump_count} sıçrama tespit edildi", 
                   transform=ax.transAxes, color='red', fontsize=9, ha='center')
        
        ax.set_title(f"{title}\nRenk = İlerleme Yönü (0 → 1)", color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Lejant
        if idx == 0:
            ax.legend(loc='upper right', facecolor='#1a1a3a', 
                     edgecolor='white', labelcolor='white', fontsize=9)
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    # Boş subplot'u gizle
    axes[1, 2].set_visible(False)
    
    # ================================================================
    # DÜZELTME: Renk çubuğunu doğru konuma yerleştir
    # ================================================================
    # Boş subplot'un olduğu yere renk çubuğunu yerleştirelim
    # veya sağ tarafa yeni bir eksen ekleyelim
    
    # Seçenek 1: Sağ tarafa yeni eksen
    cbar_ax = fig.add_axes([0.92, 0.25, 0.015, 0.5])
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Eğri Boyunca İlerleme\n(0 = Başlangıç, 1 = Bitiş)', 
                   color='white', fontsize=10)
    cbar_ax.tick_params(colors='white')
    cbar_ax.yaxis.label.set_color('white')
    
    plt.suptitle("Uzay Doldurma Eğrileri - Süreklilik ve İlerleme Yönü\n"
                "Morton: Ani renk değişimleri = Sıçramalar (kırmızı kesikli çizgiler)", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    plt.show()

def continuity_visualization_v2():
    """
    Alternatif: Renk çubuğunu boş subplot'a yerleştir
    """
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
    colors_map = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#ff44ff']
    titles = ['Keçeci', 'Hilbert', 'Morton (Sıçramalı)', 'Moore', 'Sierpinski']
    
    viz = CurveComparisonVisualizer()
    
    for idx, (curve_name, base_color, title) in enumerate(zip(curves, colors_map, titles)):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#0a0a1a')
        
        points = viz._get_curve_points(curve_name, 4)
        points = np.array(points)
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(points)))
        ax.scatter(points[:, 0], points[:, 1], c=colors, s=10, alpha=0.8)
        
        ax.scatter(points[0, 0], points[0, 1], color='white', s=120, marker='o', 
                  edgecolor=base_color, linewidth=2, zorder=10)
        ax.scatter(points[-1, 0], points[-1, 1], color='yellow', s=120, marker='s', 
                  edgecolor=base_color, linewidth=2, zorder=10)
        
        if curve_name == 'Morton':
            jump_count = 0
            for i in range(1, len(points)):
                dist = np.linalg.norm(points[i] - points[i-1])
                if dist > 0.5:
                    ax.plot(points[i-1:i+1, 0], points[i-1:i+1, 1], 
                           'r--', linewidth=1, alpha=0.5)
                    jump_count += 1
            ax.set_title(f"{title}\n{jump_count} sıçrama", color='white', fontsize=12)
        else:
            ax.set_title(f"{title}\nSürekli", color='white', fontsize=12)
        
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    # ================================================================
    # Boş subplot'u renk çubuğu olarak kullan
    # ================================================================
    ax_cbar = axes[1, 2]
    ax_cbar.set_facecolor('#0a0a1a')
    
    # Renk çubuğunu bu eksene çiz
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_cbar, orientation='vertical', shrink=0.8)
    cbar.set_label('İlerleme Yönü\n(0 = Başlangıç, 1 = Bitiş)', 
                   color='white', fontsize=12, labelpad=15)
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.ax.yaxis.label.set_color('white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    
    # Renk çubuğu ekseninin kenarlıklarını gizle
    ax_cbar.set_xticks([])
    ax_cbar.set_yticks([])
    for spine in ax_cbar.spines.values():
        spine.set_visible(False)
    
    # Açıklama metni ekle
    ax_cbar.text(0.5, 0.8, "Renk = İlerleme", color='white', fontsize=11, 
                ha='center', transform=ax_cbar.transAxes)
    ax_cbar.text(0.5, 0.2, "Morton: Kırmızı\nkesikli çizgiler\n= Sıçramalar", 
                color='red', fontsize=10, ha='center', transform=ax_cbar.transAxes)
    
    plt.suptitle("Uzay Doldurma Eğrileri - Süreklilik Karşılaştırması", 
                color='white', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

def radar_chart_comparison():
    """
    Eğrileri 6 farklı metrikte karşılaştıran radar grafiği
    """
    
    categories = ['Lokalite', 'Süreklilik', 'Hesaplama\nHızı', 
                  'Görsel\nEstetik', 'Esneklik', 'Uzay\nDoldurma']
    
    # Her eğri için 0-5 arası puanlar
    scores = {
        'Keçeci':     [4.5, 4.0, 3.5, 5.0, 5.0, 4.0],
        'Hilbert':    [5.0, 5.0, 4.0, 3.5, 1.0, 5.0],
        'Morton':     [3.0, 2.0, 5.0, 2.5, 1.0, 4.5],
        'Moore':      [4.5, 5.0, 4.0, 3.5, 1.0, 5.0],
        'Sierpinski': [3.5, 5.0, 3.5, 4.5, 1.0, 3.5],
    }
    
    colors = {
        'Keçeci': '#ff4444',
        'Hilbert': '#4488ff',
        'Morton': '#44ff44',
        'Moore': '#ffff44',
        'Sierpinski': '#ff44ff',
    }
    
    fig = plt.figure(figsize=(14, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    # Radar grafiği
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor('#0a0a1a')
    
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    
    for curve_name, score in scores.items():
        values = score + score[:1]
        ax.plot(angles, values, 'o-', linewidth=2.5, label=curve_name, 
               color=colors[curve_name], markersize=8)
        ax.fill(angles, values, alpha=0.15, color=colors[curve_name])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='white', fontsize=10, fontweight='bold')
    ax.set_ylim(0, 5.5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], color='white', fontsize=9)
    ax.grid(True, alpha=0.3, color='white')
    
    # Lejant
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), 
                      facecolor='#1a1a3a', edgecolor='white', labelcolor='white',
                      fontsize=11, title='Eğri Tipi', title_fontsize=12)
    legend.get_title().set_color('white')
    
    plt.suptitle("Uzay Doldurma Eğrileri - Çok Boyutlu Karşılaştırma\n"
                "Keçeci: En yüksek esneklik ve görsel estetik", 
                color='white', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

def animated_comparison():
    """
    Eğrilerin seviye seviye nasıl geliştiğini gösteren animasyonlu karşılaştırma
    """
    import matplotlib.animation as animation
    from IPython.display import HTML
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
    colors = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#ff44ff']
    viz = CurveComparisonVisualizer()
    
    # Boş subplot'u gizle
    axes[1, 2].set_visible(False)
    
    def update(frame):
        for ax in axes.flat:
            if ax.get_visible():
                ax.clear()
                ax.set_facecolor('#0a0a1a')
        
        level = frame + 1  # 1'den 4'e
        
        for idx, (curve_name, color) in enumerate(zip(curves, colors)):
            ax = axes[idx // 3, idx % 3]
            points = viz._get_curve_points(curve_name, level)
            points = np.array(points)
            
            if len(points) > 1:
                ax.plot(points[:, 0], points[:, 1], '-', color=color, linewidth=2, alpha=0.9)
                ax.scatter(points[0, 0], points[0, 1], color='white', s=80, marker='o', 
                          edgecolor=color, linewidth=2, zorder=5)
                ax.scatter(points[-1, 0], points[-1, 1], color='yellow', s=80, marker='s', 
                          edgecolor=color, linewidth=2, zorder=5)
            
            ax.set_title(f"{curve_name}\nSeviye {level} - {len(points)} nokta", 
                        color='white', fontsize=11)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            
            for spine in ax.spines.values():
                spine.set_color('#333366')
        
        plt.suptitle(f"Uzay Doldurma Eğrileri - Gelişim Animasyonu (Seviye {level}/4)", 
                    color='white', fontsize=16, fontweight='bold', y=1.02)
    
    ani = animation.FuncAnimation(fig, update, frames=4, interval=1500, repeat=True)
    
    # Jupyter'da göstermek için
    return HTML(ani.to_jshtml())

def indexing_performance_comparison():
    """
    Rastgele noktaların eğri üzerindeki sıralamasını gösteren performans karşılaştırması
    """
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Keçeci', 'Hilbert', 'Morton', 'Moore', 'Sierpinski']
    titles = ['Keçeci', 'Hilbert', 'Morton (Z-Order)', 'Moore', 'Sierpinski']
    colors = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#ff44ff']
    
    viz = CurveComparisonVisualizer()
    
    # Rastgele noktalar oluştur
    np.random.seed(42)
    n_points = 30
    random_points = np.random.uniform(-1, 1, (n_points, 2))
    
    for idx, (curve_name, title, color) in enumerate(zip(curves, titles, colors)):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#0a0a1a')
        
        # Eğriyi arka planda çiz
        curve_points = viz._get_curve_points(curve_name, 4)
        curve_points = np.array(curve_points)
        ax.plot(curve_points[:, 0], curve_points[:, 1], '-', color=color, 
               linewidth=1, alpha=0.3)
        
        # Rastgele noktaları eğri üzerinde sırala
        # (En yakın eğri noktasını bularak)
        order = []
        for rp in random_points:
            distances = np.linalg.norm(curve_points - rp, axis=1)
            nearest_idx = np.argmin(distances)
            order.append(nearest_idx)
        
        sorted_indices = np.argsort(order)
        
        # Noktaları sıralı olarak çiz
        for i, idx in enumerate(sorted_indices):
            ax.scatter(random_points[idx, 0], random_points[idx, 1], 
                      c=plt.cm.viridis(i/n_points), s=80, 
                      edgecolor='white', linewidth=1, zorder=10)
            ax.annotate(str(i), (random_points[idx, 0], random_points[idx, 1]), 
                       color='white', fontsize=8, ha='center', va='center')
        
        ax.set_title(f"{title}\nNoktalar eğri sırasına göre numaralandırıldı", 
                    color='white', fontsize=11)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    axes[1, 2].set_visible(False)
    
    plt.suptitle("Uzay Doldurma Eğrileri - Veri İndeksleme Karşılaştırması\n"
                "Aynı rastgele noktalar, her eğrinin kendi sıralamasına göre numaralandırıldı", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

def add_colorbar_to_figure(fig, cmap='viridis', label='Değer', vmin=0, vmax=1, 
                           position='right', rect=[0.92, 0.25, 0.015, 0.5]):
    """
    Figüre renk çubuğu eklemek için yardımcı fonksiyon
    
    Args:
        fig: matplotlib figure
        cmap: colormap adı
        label: renk çubuğu etiketi
        vmin, vmax: değer aralığı
        position: 'right' veya özel rect [left, bottom, width, height]
        rect: özel konum
    """
    if position == 'right':
        cbar_ax = fig.add_axes(rect)
    else:
        cbar_ax = fig.add_axes(position)
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin, vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label(label, color='white', fontsize=10)
    cbar_ax.tick_params(colors='white')
    cbar_ax.yaxis.label.set_color('white')
    
    return cbar

def locality_heatmap_both_versions():
    """
    İki farklı normalizasyon yaklaşımını karşılaştır
    """
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.patch.set_facecolor('#0a0a1a')
    
    curves = ['Hilbert', 'Morton', 'Moore', 'Sierpinski', 'Keçeci']
    titles = ['Hilbert', 'Morton', 'Moore', 'Sierpinski', 'Keçeci']
    
    viz = CurveComparisonVisualizer()
    
    # Önce tüm matrisleri hesapla
    all_matrices = []
    for curve_name in curves:
        points = viz._get_curve_points(curve_name, 4)
        points = np.array(points)
        n = min(64, len(points))
        locality_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    idx_dist = abs(i - j)
                    spatial_dist = np.linalg.norm(points[i] - points[j])
                    locality_matrix[i, j] = spatial_dist / (idx_dist + 1)
        
        all_matrices.append(locality_matrix)
    
    global_vmax = max(m.max() for m in all_matrices)
    
    # Üst sıra: Bağımsız normalizasyon
    for idx, (curve_name, title, matrix) in enumerate(zip(curves, titles, all_matrices)):
        ax = axes[0, idx]
        ax.set_facecolor('#0a0a1a')
        
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', 
                      interpolation='bilinear', vmin=0, vmax=matrix.max())
        
        ax.set_title(f"{title}\nBağımsız Normalizasyon\n(max={matrix.max():.2f})", 
                    color='white', fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Alt sıra: Ortak normalizasyon
    for idx, (curve_name, title, matrix) in enumerate(zip(curves, titles, all_matrices)):
        ax = axes[1, idx]
        ax.set_facecolor('#0a0a1a')
        
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', 
                      interpolation='bilinear', vmin=0, vmax=global_vmax)
        
        # Her eğrinin maksimum değerini yüzde olarak göster
        percentage = (matrix.max() / global_vmax) * 100
        ax.set_title(f"{title}\nOrtak Normalizasyon\n({percentage:.0f}% of max)", 
                    color='white', fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Renk çubukları
    cbar_ax1 = fig.add_axes([0.92, 0.55, 0.015, 0.3])
    sm1 = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(0, 1))
    sm1.set_array([])
    cbar1 = fig.colorbar(sm1, cax=cbar_ax1)
    cbar1.set_label('Bağımsız (0-1)', color='white', fontsize=9)
    cbar_ax1.tick_params(colors='white')
    
    cbar_ax2 = fig.add_axes([0.92, 0.15, 0.015, 0.3])
    sm2 = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(0, global_vmax))
    sm2.set_array([])
    cbar2 = fig.colorbar(sm2, cax=cbar_ax2)
    cbar2.set_label(f'Ortak (0-{global_vmax:.1f})', color='white', fontsize=9)
    cbar_ax2.tick_params(colors='white')
    
    plt.suptitle("Isı Haritası Normalizasyon Karşılaştırması\n"
                "Üst: Her eğri kendi içinde normalize | Alt: Tüm eğriler aynı ölçekte\n"
                "Ortak normalizasyon ile eğriler arası KARŞILAŞTIRMA yapılabilir!", 
                color='white', fontsize=12, y=1.05)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    plt.show()
    
    print("\n📊 ANALİZ SONUCU:")
    print("-" * 50)
    print("Eğri          | Max Değer | Ortak Ölçekteki Yüzdesi | Lokalite")
    print("-" * 50)
    
    curve_maxes = {}
    for curve_name, matrix in zip(curves, all_matrices):
        curve_maxes[curve_name] = matrix.max()
    
    for name, max_val in sorted(curve_maxes.items(), key=lambda x: x[1]):
        percentage = (max_val / global_vmax) * 100
        if max_val < 3:
            rating = "✅ ÇOK İYİ"
        elif max_val < 4:
            rating = "👍 İYİ"
        elif max_val < 6:
            rating = "👌 ORTA"
        else:
            rating = "⚠️ DÜŞÜK"
        print(f"{name:<12} | {max_val:.2f}     | {percentage:>5.1f}%              | {rating}")
    
    print("-" * 50)
    print(f"\n✅ En iyi lokalite: {min(curve_maxes, key=curve_maxes.get)}")
    print(f"⚠️ En kötü lokalite: {max(curve_maxes, key=curve_maxes.get)}")

def demonstrate_num_children_effect():
    """
    Farklı çocuk sayılarının Keçeci Eğrisi üzerindeki etkisini gösterir
    """
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.patch.set_facecolor('#0a0a1a')
    
    children_counts = [2, 3, 4, 5, 6, 7, 8, 10]
    
    for idx, n_children in enumerate(children_counts):
        ax = axes[idx // 4, idx % 4]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=n_children,
            max_level=3,
            scale_factor=0.4,
            base_radius=1.5,
            ordering_mode='spiral'
        )
        points = curve.generate()
        points = np.array(points)
        
        # Renk gradyanı ile çiz
        for i in range(len(points) - 1):
            color = plt.cm.viridis(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.scatter(points[0, 0], points[0, 1], color='white', s=80, marker='o', 
                  edgecolor='cyan', linewidth=2, zorder=5)
        
        # Şekil tanımı
        shapes = {
            2: "Çizgi/Spiral",
            3: "Üçgen",
            4: "Kare",
            5: "Beşgen",
            6: "Altıgen",
            7: "Yedigen",
            8: "Sekizgen",
            10: "Ongen"
        }
        
        shape_name = shapes.get(n_children, f"{n_children}-gen")
        ax.set_title(f"{n_children} Çocuk\n({shape_name})", 
                    color='white', fontsize=11, fontweight='bold')
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle("Keçeci Eğrisi - Çocuk Sayısının Şekil Üzerindeki Etkisi\n"
                "2: Çizgi | 3: Üçgen | 4: Kare | 5: Beşgen | 6: Altıgen | 7: Yedigen | 8: Sekizgen", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

def demonstrate_growth_mode_effect():
    """
    Farklı büyüme modlarının etkisini gösterir
    """
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.patch.set_facecolor('#0a0a1a')
    
    growth_modes = ['outward', 'inward', 'tangent', 'overlapping']
    titles = ['Dışa Büyüme\n(outward)', 'İçe Büyüme\n(inward)', 
              'Teğet Büyüme\n(tangent)', 'Örtüşmeli\n(overlapping)']
    
    for idx, (mode, title) in enumerate(zip(growth_modes, titles)):
        ax = axes[idx]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=5,
            max_level=3,
            scale_factor=0.4,
            base_radius=1.5,
            growth_mode=mode,
            ordering_mode='spiral'
        )
        points = curve.generate()
        points = np.array(points)
        
        for i in range(len(points) - 1):
            color = plt.cm.plasma(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.scatter(points[0, 0], points[0, 1], color='white', s=80, marker='o', 
                  edgecolor='cyan', linewidth=2, zorder=5)
        ax.scatter(points[-1, 0], points[-1, 1], color='yellow', s=80, marker='s', 
                  edgecolor='orange', linewidth=2, zorder=5)
        
        ax.set_title(title, color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle("Keçeci Eğrisi - Büyüme Modunun Etkisi", 
                color='white', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.show()

def demonstrate_ordering_mode_effect():
    """
    Farklı sıralama stratejilerinin etkisini gösterir
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    ordering_modes = ['sequential', 'alternating', 'spiral', 'reverse_spiral']
    titles = ['Sıralı\n(sequential)', 'Alternatif\n(alternating)', 
              'Spiral\n(spiral)', 'Ters Spiral\n(reverse_spiral)']
    
    for idx, (mode, title) in enumerate(zip(ordering_modes, titles)):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=5,
            max_level=3,
            scale_factor=0.4,
            base_radius=1.5,
            growth_mode='outward',
            ordering_mode=mode
        )
        points = curve.generate()
        points = np.array(points)
        
        for i in range(len(points) - 1):
            color = plt.cm.cool(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.scatter(points[0, 0], points[0, 1], color='white', s=80, marker='o', 
                  edgecolor='cyan', linewidth=2, zorder=5)
        ax.scatter(points[-1, 0], points[-1, 1], color='yellow', s=80, marker='s', 
                  edgecolor='orange', linewidth=2, zorder=5)
        
        ax.set_title(title, color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    # Boş subplotları gizle
    for idx in range(len(ordering_modes), 6):
        axes[idx // 3, idx % 3].set_visible(False)
    
    plt.suptitle("Keçeci Eğrisi - Sıralama Stratejisinin Etkisi", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

def demonstrate_scale_factor_effect():
    """
    Farklı ölçek faktörlerinin etkisini gösterir
    """
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.patch.set_facecolor('#0a0a1a')
    
    scale_factors = [0.2, 0.35, 0.5, 0.65]
    
    for idx, scale in enumerate(scale_factors):
        ax = axes[idx]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=5,
            max_level=3,
            scale_factor=scale,
            base_radius=1.5,
            growth_mode='outward',
            ordering_mode='spiral'
        )
        points = curve.generate()
        points = np.array(points)
        
        for i in range(len(points) - 1):
            color = plt.cm.viridis(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.scatter(points[0, 0], points[0, 1], color='white', s=80, marker='o', 
                  edgecolor='cyan', linewidth=2, zorder=5)
        
        ax.set_title(f"scale_factor = {scale}\n{'Sıkı' if scale < 0.35 else 'Gevşek' if scale > 0.5 else 'Dengeli'}", 
                    color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle("Keçeci Eğrisi - Ölçek Faktörünün Etkisi\n"
                "Düşük değer: Sıkı paketlenmiş | Yüksek değer: Dağınık", 
                color='white', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.show()

def demonstrate_angle_effects():
    """
    Açı parametrelerinin etkisini gösterir
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    # angle_offset varyasyonları
    offsets = [0, np.pi/6, np.pi/3]
    for idx, offset in enumerate(offsets):
        ax = axes[0, idx]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=5, max_level=3, scale_factor=0.4, base_radius=1.5,
            angle_offset=offset, ordering_mode='spiral'
        )
        points = np.array(curve.generate())
        
        for i in range(len(points) - 1):
            color = plt.cm.viridis(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.set_title(f"angle_offset = {offset/np.pi:.2f}π\n(Döndürme)", 
                    color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    # angle_variation varyasyonları
    variations = [0.0, 0.2, 0.4]
    for idx, var in enumerate(variations):
        ax = axes[1, idx]
        ax.set_facecolor('#0a0a1a')
        
        curve = KececiCurve(
            num_children=5, max_level=3, scale_factor=0.4, base_radius=1.5,
            angle_variation=var, ordering_mode='spiral'
        )
        points = np.array(curve.generate())
        
        for i in range(len(points) - 1):
            color = plt.cm.plasma(i / len(points))
            ax.plot(points[i:i+2, 0], points[i:i+2, 1], '-', 
                   color=color, linewidth=1.5, alpha=0.9)
        
        ax.set_title(f"angle_variation = {var}\n{'Düz' if var == 0 else 'Kıvrımlı' if var < 0.3 else 'Spiralimsi'}", 
                    color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle("Keçeci Eğrisi - Açı Parametrelerinin Etkisi\n"
                "angle_offset: Eğriyi döndürür | angle_variation: Seviyeler arası kıvrım ekler", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    
def sierpinski_edge_curve(order: int) -> List[Tuple[float, float]]:
    """
    Sierpinski Kenar Eğrisi - Sadece üçgenlerin kenarlarını dolaşır
    
    Bu versiyon, alt üçgenler arasında geçiş yaparken
    GÖRÜNÜR bağlantı çizgileri oluşturmaz.
    """
    
    def generate_triangle_edges(level: int, p1: Tuple, p2: Tuple, p3: Tuple) -> List:
        """Bir üçgenin kenarlarını oluştur"""
        if level == 0:
            # Tek bir üçgenin kenarları
            return [p1, p2, p3, p1]
        
        # Orta noktalar
        m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        
        edges = []
        
        # Üst üçgen (p1, m12, m31)
        edges.extend(generate_triangle_edges(level - 1, p1, m12, m31))
        
        # Sol alt üçgen (m12, p2, m23)
        edges.extend(generate_triangle_edges(level - 1, m12, p2, m23))
        
        # Sağ alt üçgen (m31, m23, p3)
        edges.extend(generate_triangle_edges(level - 1, m31, m23, p3))
        
        return edges
    
    # Eşkenar üçgen köşeleri
    size = 2.0
    h = size * np.sqrt(3) / 2
    
    p1 = (0.0, h)        # Üst
    p2 = (-size/2, 0.0)  # Sol alt
    p3 = (size/2, 0.0)   # Sağ alt
    
    points = generate_triangle_edges(order, p1, p2, p3)
    
    # Ardışık aynı noktaları temizle
    cleaned = []
    for p in points:
        if not cleaned:
            cleaned.append(p)
        else:
            prev = cleaned[-1]
            if abs(p[0] - prev[0]) > 0.001 or abs(p[1] - prev[1]) > 0.001:
                cleaned.append(p)
    
    return cleaned


def sierpinski_disconnected_edges(order: int) -> List[List[Tuple[float, float]]]:
    """
    Sierpinski Ayrık Kenarlar - Her üçgenin kenarlarını ayrı ayrı döndürür
    
    Bu versiyon, tüm üçgenleri bağımsız kapalı şekiller olarak döndürür.
    """
    
    def collect_all_triangles(level: int, p1: Tuple, p2: Tuple, p3: Tuple) -> List[List[Tuple]]:
        """Tüm üçgenleri topla"""
        if level == 0:
            return [[p1, p2, p3, p1]]
        
        m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        
        triangles = []
        triangles.extend(collect_all_triangles(level - 1, p1, m12, m31))
        triangles.extend(collect_all_triangles(level - 1, m12, p2, m23))
        triangles.extend(collect_all_triangles(level - 1, m31, m23, p3))
        
        return triangles
    
    size = 2.0
    h = size * np.sqrt(3) / 2
    
    p1 = (0.0, h)
    p2 = (-size/2, 0.0)
    p3 = (size/2, 0.0)
    
    return collect_all_triangles(order, p1, p2, p3)


def plot_sierpinski_comparison(order: int = 3):
    """Üç farklı Sierpinski çizimini karşılaştır"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('#0a0a1a')
    
    # 1. Sierpinski Eğrisi (bağlantı çizgileri var)
    ax1 = axes[0]
    ax1.set_facecolor('#0a0a1a')
    
    #from ClassicalCurves import ClassicalCurves
    points1 = ClassicalCurves.sierpinski_curve(order)
    xs1 = [p[0] for p in points1]
    ys1 = [p[1] for p in points1]
    ax1.plot(xs1, ys1, '-', color='#ff44ff', linewidth=1.5, alpha=0.9)
    ax1.scatter(xs1[0], ys1[0], color='white', s=80, marker='o', edgecolor='#ff44ff', linewidth=2)
    ax1.scatter(xs1[-1], ys1[-1], color='yellow', s=80, marker='s', edgecolor='#ff44ff', linewidth=2)
    ax1.set_title("Sierpinski Eğrisi\n(Sürekli - bağlantı çizgileri var)", color='white', fontsize=11)
    ax1.set_aspect('equal')
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # 2. Sierpinski Kenar Eğrisi (bağlantı çizgileri YOK)
    ax2 = axes[1]
    ax2.set_facecolor('#0a0a1a')
    
    points2 = sierpinski_edge_curve(order)
    xs2 = [p[0] for p in points2]
    ys2 = [p[1] for p in points2]
    ax2.plot(xs2, ys2, '-', color='#44ff88', linewidth=1.5, alpha=0.9)
    ax2.scatter(xs2[0], ys2[0], color='white', s=80, marker='o', edgecolor='#44ff88', linewidth=2)
    ax2.scatter(xs2[-1], ys2[-1], color='yellow', s=80, marker='s', edgecolor='#44ff88', linewidth=2)
    ax2.set_title("Sierpinski Kenar Eğrisi\n(Sadece üçgen kenarları)", color='white', fontsize=11)
    ax2.set_aspect('equal')
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    # 3. Sierpinski Ayrık Üçgenler
    ax3 = axes[2]
    ax3.set_facecolor('#0a0a1a')
    
    triangles = sierpinski_disconnected_edges(order)
    colors = plt.cm.viridis(np.linspace(0, 1, len(triangles)))
    for i, tri in enumerate(triangles):
        xs = [p[0] for p in tri]
        ys = [p[1] for p in tri]
        ax3.plot(xs, ys, '-', color=colors[i], linewidth=1, alpha=0.7)
    ax3.set_title(f"Sierpinski Ayrık Üçgenler\n({len(triangles)} bağımsız üçgen)", color='white', fontsize=11)
    ax3.set_aspect('equal')
    ax3.set_xticks([])
    ax3.set_yticks([])
    
    for ax in axes:
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle(f"Sierpinski Çizim Tipleri (order={order})", 
                color='white', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    
def plot_sierpinski_curve(order: int):
    """Sierpinski eğrisini çiz"""
    points = sierpinski_curve(order)
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Eğriyi çiz
    ax.plot(xs, ys, '-', color='#ff44ff', linewidth=2, alpha=0.9)
    
    # Başlangıç ve bitiş noktaları
    ax.scatter(xs[0], ys[0], color='white', s=150, marker='o', 
              edgecolor='#ff44ff', linewidth=2, zorder=5, label='Başlangıç')
    ax.scatter(xs[-1], ys[-1], color='yellow', s=150, marker='s', 
              edgecolor='#ff44ff', linewidth=2, zorder=5, label='Bitiş')
    
    # Kapalı döngü kontrolü
    dist = np.sqrt((xs[0] - xs[-1])**2 + (ys[0] - ys[-1])**2)
    status = "✅ Kapalı Döngü" if dist < 0.1 else "❌ Açık"
    
    ax.set_title(f"Sierpinski Eğrisi (order={order})\n"
                 f"Nokta sayısı: {len(points)} | {status}", 
                color='white', fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc='upper right', facecolor='#1a1a3a', 
             edgecolor='white', labelcolor='white')
    
    # Çerçeve
    for spine in ax.spines.values():
        spine.set_color('#333366')
    
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_sierpinski_evolution():
    """Farklı seviyelerde Sierpinski eğrisinin gelişimi"""
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.patch.set_facecolor('#0a0a1a')
    
    for idx, order in enumerate([0, 1, 2, 3]):
        ax = axes[idx]
        ax.set_facecolor('#0a0a1a')
        
        points = sierpinski_curve(order)
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        # Renk gradyanı
        for i in range(len(xs) - 1):
            color = plt.cm.plasma(i / len(xs))
            ax.plot(xs[i:i+2], ys[i:i+2], '-', color=color, linewidth=2, alpha=0.9)
        
        ax.scatter(xs[0], ys[0], color='white', s=100, marker='o', 
                  edgecolor='#ff44ff', linewidth=2, zorder=5)
        ax.scatter(xs[-1], ys[-1], color='yellow', s=100, marker='s', 
                  edgecolor='#ff44ff', linewidth=2, zorder=5)
        
        ax.set_title(f"order = {order}\n{len(points)} nokta", 
                    color='white', fontsize=11)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
    
    plt.suptitle("Sierpinski Eğrisi - Seviyelere Göre Gelişim", 
                color='white', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()  
    
def ciz_sierpinski(derinlik, p1, p2, p3, eksen):
    """
    Sierpinski üçgenini özyinelemeli olarak çizer.
    
    Args:
        derinlik (int): Çizim detay seviyesi (rekürsiyon sayısı).
        p1, p2, p3 (tuple): Üçgenin (x, y) köşe koordinatları.
        eksen: Matplotlib çizim alanı.
    """
    if derinlik == 0:
        # Temel durum: Üçgeni ekle
        ucgen = patches.Polygon([p1, p2, p3], closed=True, edgecolor='black', facecolor='skyblue')
        eksen.add_patch(ucgen)
        return

    # 1. Adım: Kenarların orta noktalarını hesapla
    m1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2) # Sol kenar ortası
    m2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2) # Alt kenar ortası
    m3 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2) # Sağ kenar ortası

    # 2. Adım: 3 yeni alt üçgen için fonksiyonu tekrar çağır
    # Üst üçgen
    ciz_sierpinski(derinlik - 1, p1, m1, m3, eksen)
    # Sol alt üçgen
    ciz_sierpinski(derinlik - 1, m1, p2, m2, eksen)
    # Sağ alt üçgen
    ciz_sierpinski(derinlik - 1, m3, m2, p3, eksen)
    
def test_sierpinski():
    """Sierpinski eğrisi testi"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a1a')
    
    for idx, order in enumerate([2, 3]):
        ax = axes[idx]
        ax.set_facecolor('#0a0a1a')
        
        points = ClassicalCurves.sierpinski_curve(order)
        
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        # Renk gradyanı ile çiz
        for i in range(len(xs) - 1):
            color = plt.cm.plasma(i / len(xs))
            ax.plot(xs[i:i+2], ys[i:i+2], '-', color=color, linewidth=2, alpha=0.9)
        
        # Başlangıç ve bitiş
        ax.scatter(xs[0], ys[0], color='white', s=150, marker='o', 
                  edgecolor='#ff44ff', linewidth=2, zorder=5, label='Başlangıç')
        ax.scatter(xs[-1], ys[-1], color='yellow', s=150, marker='s', 
                  edgecolor='#ff44ff', linewidth=2, zorder=5, label='Bitiş')
        
        # Başlangıç ve bitiş aynı mı?
        dist = np.sqrt((xs[0] - xs[-1])**2 + (ys[0] - ys[-1])**2)
        status = "Kapalı Döngü" if dist < 0.01 else "❌ Açık"
        
        ax.set_title(f"Sierpinski Eğrisi (order={order})\n{status}", 
                    color='white', fontsize=12)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333366')
        
        if idx == 0:
            ax.legend(loc='upper right', facecolor='#1a1a3a',
                     edgecolor='white', labelcolor='white')
    
    plt.suptitle("Sierpinski Eğrisi - Doğru Implementasyon", 
                color='white', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()

class KececiCurveGenerator:
    """Parametrik Keçeci Eğrisi üreteci (2B)"""
    
    def __init__(
        self,
        num_children: int = 6,
        max_level: int = 4,
        scale_factor: float = 0.5,
        base_radius: float = 4.0,
        min_radius: float = 0.05,
        connection_mode: ConnectionMode = ConnectionMode.CONTINUOUS,
        child_ordering: ChildOrdering = ChildOrdering.SEQUENTIAL,
        growth_direction: GrowthDirection = GrowthDirection.INWARD,
        angle_offset: float = 0.0,
        angle_variation: float = 0.0,
        radial_variation: float = 0.0,
        perturbation: float = 0.0,
        line_style: str = '-',
        line_width: float = 0.8,
        line_color: str = 'white',
        point_size: float = 1.0,
        show_points: bool = True,
        color_by_level: bool = False,
        color_by_angle: bool = False,
        color_saturation: float = 1.0,
        alpha: float = 0.8,
        random_seed: int = None,
    ):
        self.num_children = num_children
        self.max_level = max_level
        self.scale_factor = scale_factor
        self.base_radius = base_radius
        self.min_radius = min_radius
        
        self.connection_mode = connection_mode
        self.child_ordering = child_ordering
        self.growth_direction = growth_direction
        
        self.angle_offset = angle_offset
        self.angle_variation = angle_variation
        self.radial_variation = radial_variation
        self.perturbation = perturbation
        
        self.line_style = line_style
        self.line_width = line_width
        self.line_color = line_color
        self.point_size = point_size
        self.show_points = show_points
        
        self.color_by_level = color_by_level
        self.color_by_angle = color_by_angle
        self.color_saturation = color_saturation
        self.alpha = alpha
        
        if random_seed is not None:
            np.random.seed(random_seed)
            
        self.all_points = []
        self.level_points = {}
    
    def _get_color_for_segment(self, level: int, angle: float):
        if self.color_by_level:
            hue = level / max(1, self.max_level)
            return colorsys.hsv_to_rgb(hue, self.color_saturation, 1.0)
        elif self.color_by_angle:
            hue = (angle % (2 * np.pi)) / (2 * np.pi)
            return colorsys.hsv_to_rgb(hue, self.color_saturation, 1.0)
        return self.line_color
    
    def _order_children(self, children: list, level: int) -> list:
        if self.child_ordering == ChildOrdering.SEQUENTIAL:
            return children
        elif self.child_ordering == ChildOrdering.ALTERNATING:
            even = [c for i, c in enumerate(children) if i % 2 == 0]
            odd = [c for i, c in enumerate(children) if i % 2 == 1]
            return even + odd
        elif self.child_ordering == ChildOrdering.SPIRAL_OUTWARD:
            return sorted(children, key=lambda c: c[2])
        elif self.child_ordering == ChildOrdering.SPIRAL_INWARD:
            return sorted(children, key=lambda c: c[2], reverse=True)
        elif self.child_ordering == ChildOrdering.RANDOM:
            indices = list(range(len(children)))
            np.random.shuffle(indices)
            return [children[i] for i in indices]
        elif self.child_ordering == ChildOrdering.ANGLE_BASED:
            return sorted(children, key=lambda c: c[2])
        elif self.child_ordering == ChildOrdering.QUADRANT:
            quadrants = {0: [], 1: [], 2: [], 3: []}
            for child in children:
                angle = child[2]
                quadrant = int((angle % (2 * np.pi)) / (np.pi / 2))
                quadrants[quadrant].append(child)
            result = []
            for q in range(4):
                result.extend(sorted(quadrants[q], key=lambda c: c[2]))
            return result
        return children
    
    def generate_curve(self, center=(0.0, 0.0), radius=None, level=0, angle=0.0):
        """2B eğriyi oluştur"""
        if radius is None:
            radius = self.base_radius
        
        if level > self.max_level or radius < self.min_radius:
            self.all_points.append((center, level, angle))
            if level not in self.level_points:
                self.level_points[level] = []
            self.level_points[level].append(center)
            return
        
        self.all_points.append((center, level, angle))
        if level not in self.level_points:
            self.level_points[level] = []
        self.level_points[level].append(center)
        
        children = []
        for i in range(self.num_children):
            child_angle = 2 * np.pi * i / self.num_children + self.angle_offset + self.angle_variation * level
            child_radius = radius * self.scale_factor
            
            if self.growth_direction == GrowthDirection.INWARD:
                distance = radius - child_radius
            elif self.growth_direction == GrowthDirection.OUTWARD:
                distance = radius + child_radius
            elif self.growth_direction == GrowthDirection.TANGENT:
                distance = radius
            else:  # OVERLAPPING
                distance = radius * (1 - self.scale_factor * 0.5)
            
            child_x = center[0] + distance * np.cos(child_angle)
            child_y = center[1] + distance * np.sin(child_angle)
            
            if self.perturbation > 0:
                child_x += np.random.normal(0, self.perturbation * radius)
                child_y += np.random.normal(0, self.perturbation * radius)
            
            children.append((child_x, child_y, child_angle))
        
        ordered_children = self._order_children(children, level)
        
        for child_x, child_y, child_angle in ordered_children:
            self.generate_curve((child_x, child_y), child_radius, level + 1, child_angle)

# ============================================================================
# 3B KEÇECİ CURVE GENERATOR
# ============================================================================

class KececiCurveGenerator3D:
    """Gelişmiş 3B Keçeci Eğrisi üreteci"""
    
    def __init__(
        self,
        num_children: int = 8,
        max_level: int = 3,
        scale_factor: float = 0.4,
        base_radius: float = 0.3,
        min_radius: float = 0.02,
        angle_offset: float = 0.0,
        angle_variation: float = 0.0,
        radial_variation: float = 0.0,
        color_by_angle: bool = True,
        color_by_level: bool = False,
        line_color: str = 'white',
        alpha: float = 0.8,
        growth_mode: str = 'outward',  # 'outward', 'inward', 'spiral'
        distribution: str = 'fibonacci',  # 'fibonacci', 'uniform', 'random'
        chirality: float = 0.0,  # Kiralite (Weyl için önemli!)
        connection_mode: ConnectionMode = ConnectionMode.CONTINUOUS,
        child_ordering: ChildOrdering = ChildOrdering.SEQUENTIAL,
        growth_direction: GrowthDirection = GrowthDirection.INWARD,
        perturbation: float = 0.0,
        line_style: str = '-',
        line_width: float = 0.8,
        point_size: float = 1.0,
        show_points: bool = True,
        color_saturation: float = 1.0,
        random_seed: int = None,
    ):
        self.num_children = num_children
        self.max_level = max_level
        self.scale_factor = scale_factor
        self.base_radius = base_radius
        self.min_radius = min_radius
        self.angle_offset = angle_offset
        self.angle_variation = angle_variation
        self.radial_variation = radial_variation
        self.color_by_angle = color_by_angle
        self.color_by_level = color_by_level
        self.line_color = line_color
        self.alpha = alpha
        self.growth_mode = growth_mode
        self.distribution = distribution
        self.chirality = chirality
        
        self.perturbation = perturbation
        self.line_style = line_style
        self.line_width = line_width
        self.point_size = point_size
        self.show_points = show_points
        self.color_by_level = color_by_level
        self.color_by_angle = color_by_angle
        self.color_saturation = color_saturation
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        self.all_points = []
        self.level_points = {}
    
    def _get_color(self, level: int, angle: float):
        if self.color_by_level:
            hue = level / max(1, self.max_level)
            return colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        elif self.color_by_angle:
            hue = (angle % (2 * np.pi)) / (2 * np.pi)
            return colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return self.line_color
    
    def _get_directions(self) -> np.ndarray:
        """3B yön vektörlerini oluştur (kiralite etkisi ile)"""
        if self.distribution == 'fibonacci':
            phi = np.pi * (3.0 - np.sqrt(5.0))
            directions = []
            for i in range(self.num_children):
                y = 1 - (i / float(max(1, self.num_children - 1))) * 2 if self.num_children > 1 else 0
                radius_xy = np.sqrt(max(0, 1 - y * y))
                theta = phi * i + self.chirality * i  # Kiralite etkisi
                x = np.cos(theta) * radius_xy
                z = np.sin(theta) * radius_xy
                directions.append(np.array([x, y, z]))
            return np.array(directions)
        
        elif self.distribution == 'weyl_cones':
            # Weyl konileri için özel dağılım
            directions = []
            for i in range(self.num_children):
                # Weyl noktaları zıt kiraliteli koniler
                if i < self.num_children // 2:
                    # Pozitif kiralite
                    theta = 2 * np.pi * i / (self.num_children // 2)
                    phi = np.pi / 4
                else:
                    # Negatif kiralite
                    theta = 2 * np.pi * (i - self.num_children // 2) / (self.num_children - self.num_children // 2)
                    phi = 3 * np.pi / 4
                
                x = np.sin(phi) * np.cos(theta)
                y = np.sin(phi) * np.sin(theta)
                z = np.cos(phi)
                directions.append(np.array([x, y, z]))
            return np.array(directions)
        
        else:
            directions = np.random.randn(self.num_children, 3)
            return directions / np.linalg.norm(directions, axis=1, keepdims=True)
    
    def generate_curve(self, center=(0.0, 0.0, 0.0), radius=None, level=0, 
                      base_angle=0.0):
        """3B eğriyi oluştur"""
        if radius is None:
            radius = self.base_radius
        
        if level > self.max_level or radius < self.min_radius:
            self.all_points.append((center, level, base_angle))
            if level not in self.level_points:
                self.level_points[level] = []
            self.level_points[level].append(center)
            return
        
        self.all_points.append((center, level, base_angle))
        if level not in self.level_points:
            self.level_points[level] = []
        self.level_points[level].append(center)
        
        directions = self._get_directions()
        child_radius = radius * self.scale_factor
        
        for i, direction in enumerate(directions):
            child_angle = base_angle + self.angle_offset + self.angle_variation * level
            
            if self.growth_mode == 'inward':
                distance = radius - child_radius
            elif self.growth_mode == 'spiral':
                distance = radius + child_radius * (1 + 0.5 * np.sin(level))
            elif self.growth_mode == 'majorana':
                # Majorana için özel: çiftler halinde
                distance = radius + child_radius * (1 + 0.3 * np.cos(2 * i))
            else:
                distance = radius + child_radius
            
            distance *= (1 + self.radial_variation * np.sin(level * np.pi/4))
            
            child_center = np.array(center) + distance * direction
            
            self.generate_curve(
                tuple(child_center), child_radius, level + 1, child_angle
            )


# ============================================================================
# 2B KEÇECİ CURVE GENERATOR
# ============================================================================

class KececiCurveGenerator2D:
    """2B Keçeci Eğrisi üreteci"""
    
    def __init__(
        self,
        num_children: int = 6,
        max_level: int = 4,
        scale_factor: float = 0.5,
        base_radius: float = 1.0,
        min_radius: float = 0.05,
        angle_offset: float = 0.0,
        angle_variation: float = 0.0,
        color_by_angle: bool = True,
        line_color: str = 'white',
        line_width: float = 1.0,
        alpha: float = 0.8,
        chirality: float = 0.0,
    ):
        self.num_children = num_children
        self.max_level = max_level
        self.scale_factor = scale_factor
        self.base_radius = base_radius
        self.min_radius = min_radius
        self.angle_offset = angle_offset
        self.angle_variation = angle_variation
        self.color_by_angle = color_by_angle
        self.line_color = line_color
        self.line_width = line_width
        self.alpha = alpha
        self.chirality = chirality
        
        self.all_points = []
    
    def _get_color(self, angle: float):
        if self.color_by_angle:
            hue = (angle % (2 * np.pi)) / (2 * np.pi)
            return colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return self.line_color
    
    def generate_curve(self, center=(0.0, 0.0), radius=None, level=0, angle=0.0):
        """2B eğriyi oluştur"""
        if radius is None:
            radius = self.base_radius
        
        if level > self.max_level or radius < self.min_radius:
            self.all_points.append((center, level, angle))
            return
        
        self.all_points.append((center, level, angle))
        
        child_radius = radius * self.scale_factor
        
        for i in range(self.num_children):
            # Kiralite etkisi
            child_angle = (2 * np.pi * i / self.num_children + self.angle_offset + 
                          self.angle_variation * level + self.chirality * level * i)
            
            distance = radius + child_radius
            
            child_x = center[0] + distance * np.cos(child_angle)
            child_y = center[1] + distance * np.sin(child_angle)
            
            self.generate_curve((child_x, child_y), child_radius, level + 1, child_angle)


# ============================================================================
# MAJORANA FERMİYONLARI GÖRSELLEŞTİRME
# ============================================================================

class MajoranaVisualizer:
    """Majorana fermiyonları için Keçeci Eğrisi görselleştiricisi"""
    
    def visualize_majorana_zero_modes(self):
        """
        Keçeci Eğrileri ile Majorana Sıfır Modları
        Keçeci Curves: Majorana Zero Modes in Topological Superconductors
        
        Majorana fermiyonları, kendi anti-parçacığı olan egzotik parçacıklardır.
        Topolojik süperiletkenlerde sıfır enerji modları olarak ortaya çıkarlar.
        """
        fig = plt.figure(figsize=(20, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # 1. Majorana tel modeli
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.set_facecolor('#0a0a1a')
        self._draw_majorana_wire(ax1)
        ax1.set_title("Keçeci 3D: Majorana Nanowire", color='white')
        
        # 2. Majorana sıfır modları
        ax2 = fig.add_subplot(2, 3, 2, projection='3d')
        ax2.set_facecolor('#0a0a1a')
        self._draw_zero_modes(ax2)
        ax2.set_title("Keçeci 3D: Zero Energy Modes", color='white')
        
        # 3. Braiding (örgü) işlemi
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        ax3.set_facecolor('#0a0a1a')
        self._draw_majorana_braiding(ax3)
        ax3.set_title("Keçeci 3D: Majorana Braiding", color='white')
        
        # 4. Enerji spektrumu
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.set_facecolor('#0a0a1a')
        self._draw_majorana_spectrum(ax4)
        ax4.set_title("Keçeci Curves: Energy Spectrum", color='white')
        
        # 5. Topolojik faz diyagramı
        ax5 = fig.add_subplot(2, 3, 5)
        ax5.set_facecolor('#0a0a1a')
        self._draw_phase_diagram(ax5)
        ax5.set_title("Keçeci Curves: Topological Phase Diagram", color='white')
        
        # 6. Majorana kübiti
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        ax6.set_facecolor('#0a0a1a')
        self._draw_majorana_qubit(ax6)
        ax6.set_title("Keçeci 3D: Majorana Qubit", color='white')
        
        plt.suptitle("Keçeci Curves: Majorana Fermions in Topological Superconductors", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    def _draw_majorana_wire(self, ax):
        """Majorana nanowire çizimi"""
        # Tel (silindir)
        z = np.linspace(-3, 3, 50)
        theta = np.linspace(0, 2*np.pi, 20)
        Z, Theta = np.meshgrid(z, theta)
        X = 0.3 * np.cos(Theta)
        Y = 0.3 * np.sin(Theta)
        
        ax.plot_surface(X, Y, Z, color='silver', alpha=0.3)
        
        # Uçlarda Majorana modları
        for z_pos, color in [(-3, '#ff4444'), (3, '#44ff44')]:
            generator = KececiCurveGenerator3D(
                num_children=8, max_level=2, scale_factor=0.3, base_radius=0.2,
                color_by_angle=True, alpha=0.9, growth_mode='majorana',
                distribution='fibonacci'
            )
            generator.generate_curve(center=(0, 0, z_pos))
            
            pts = generator.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for i in range(len(xs)-1):
                    color_pt = generator._get_color(pts[i][1], pts[i][2])
                    ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                           color=color_pt, linewidth=1.5, alpha=0.8)
        
        ax.text(0, 0.8, -3, "γ₁", color='#ff4444', fontsize=12)
        ax.text(0, 0.8, 3, "γ₂", color='#44ff44', fontsize=12)
        
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-4, 4])
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=20, azim=30)
    
    def _draw_zero_modes(self, ax):
        """Sıfır enerji modları"""
        # Enerji seviyeleri
        energies = np.linspace(-2, 2, 20)
        
        for i, E in enumerate(energies):
            r = 0.5 + abs(E) * 0.3
            theta = i * np.pi / 5
            
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            if abs(E) < 0.2:  # Sıfır mod
                color = 'red'
                size = 0.25
            else:
                color = plt.cm.coolwarm((E + 2) / 4)
                size = 0.1
            
            generator = KececiCurveGenerator3D(
                num_children=4, max_level=1, scale_factor=0.3, base_radius=size,
                color_by_angle=(abs(E) >= 0.2), line_color=color, alpha=0.8
            )
            generator.generate_curve(center=(x, y, E))
            
            pts = generator.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    if abs(E) < 0.2:
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color='red', linewidth=2, alpha=0.9)
                    else:
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color=color, linewidth=0.8, alpha=0.5)
        
        ax.axhline(y=0, color='yellow', linestyle='--', alpha=0.5)
        ax.set_xlabel('k', color='white')
        ax.set_ylabel(' ', color='white')
        ax.set_zlabel('E', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)
    
    def _draw_majorana_braiding(self, ax):
        """Majorana örgü işlemi"""
        t = np.linspace(0, 2*np.pi, 100)
        
        # İki Majorana'nın dünya çizgileri
        # γ₁
        x1 = 1.5 * np.cos(t)
        y1 = 1.5 * np.sin(t)
        z1 = t
        
        # γ₂ (zıt yönde hareket)
        x2 = 1.5 * np.cos(t + np.pi)
        y2 = 1.5 * np.sin(t + np.pi)
        z2 = t
        
        # Keçeci eğrileri ile süsle
        for i in range(0, len(t), 10):
            gen1 = KececiCurveGenerator3D(
                num_children=5, max_level=1, scale_factor=0.2, base_radius=0.08,
                color_by_angle=True, alpha=0.7
            )
            gen1.generate_curve(center=(x1[i], y1[i], z1[i]))
            pts = gen1.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color='#ff4444', linewidth=1, alpha=0.6)
            
            gen2 = KececiCurveGenerator3D(
                num_children=5, max_level=1, scale_factor=0.2, base_radius=0.08,
                color_by_angle=True, alpha=0.7
            )
            gen2.generate_curve(center=(x2[i], y2[i], z2[i]))
            pts = gen2.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color='#44ff44', linewidth=1, alpha=0.6)
        
        ax.plot(x1, y1, z1, color='#ff4444', linewidth=2, label='γ₁')
        ax.plot(x2, y2, z2, color='#44ff44', linewidth=2, label='γ₂')
        
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Time', color='white')
        ax.tick_params(colors='white')
        ax.legend()
        ax.view_init(elev=25, azim=45)
    
    def _draw_majorana_spectrum(self, ax):
        """Majorana enerji spektrumu"""
        mu = np.linspace(-3, 3, 100)
        Delta = 1.0
        
        # Enerji bantları
        E_plus = np.sqrt((abs(mu) - 2)**2 + Delta**2)
        E_minus = -E_plus
        
        ax.fill_between(mu, E_minus, E_plus, color='blue', alpha=0.2)
        ax.plot(mu, E_plus, 'cyan', linewidth=2)
        ax.plot(mu, E_minus, 'cyan', linewidth=2)
        
        # Sıfır mod (Majorana)
        topological_region = abs(mu) < 2
        ax.plot(mu[topological_region], np.zeros_like(mu[topological_region]), 
               'red', linewidth=3, label='Majorana Zero Mode')
        
        # Keçeci eğrileri ile süsle
        for mu_val in [-1.5, 0, 1.5]:
            gen = KececiCurveGenerator2D(
                num_children=4, max_level=2, scale_factor=0.2, base_radius=0.15,
                color_by_angle=True, alpha=0.7
            )
            gen.generate_curve(center=(mu_val, 0))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                for i in range(len(xs)-1):
                    color = gen._get_color(pts[i][2])
                    ax.plot(xs[i:i+2], ys[i:i+2], color=color, linewidth=1, alpha=0.6)
        
        ax.axvline(x=-2, color='yellow', linestyle='--', alpha=0.5, label='Phase Boundary')
        ax.axvline(x=2, color='yellow', linestyle='--', alpha=0.5)
        
        ax.set_xlabel('Chemical Potential μ', color='white')
        ax.set_ylabel('Energy E', color='white')
        ax.tick_params(colors='white')
        ax.legend(loc='upper right')
        ax.set_ylim([-3, 3])
        ax.grid(True, alpha=0.2)
    
    def _draw_phase_diagram(self, ax):
        """Topolojik faz diyagramı"""
        mu = np.linspace(-3, 3, 50)
        Delta = np.linspace(0, 2, 50)
        MU, DELTA = np.meshgrid(mu, Delta)
        
        # Topolojik invariant
        topological = abs(MU) < 2
        
        ax.contourf(MU, DELTA, topological, levels=[0, 0.5, 1], 
                   colors=['#1a1a3a', '#3a1a1a'], alpha=0.7)
        
        # Faz sınırları
        ax.plot([-2, -2], [0, 2], 'yellow', linestyle='--', linewidth=2)
        ax.plot([2, 2], [0, 2], 'yellow', linestyle='--', linewidth=2)
        
        # Keçeci eğrileri
        for mu_val in [-1, 0, 1]:
            for delta_val in [0.5, 1.0, 1.5]:
                gen = KececiCurveGenerator2D(
                    num_children=3, max_level=1, scale_factor=0.15, base_radius=0.08,
                    color_by_angle=True
                )
                gen.generate_curve(center=(mu_val, delta_val))
                pts = gen.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    for i in range(len(xs)-1):
                        color = gen._get_color(pts[i][2])
                        ax.plot(xs[i:i+2], ys[i:i+2], color=color, linewidth=0.8, alpha=0.5)
        
        ax.text(-1, 1, 'Topological\nPhase', color='white', ha='center', fontsize=12)
        ax.text(2.5, 1, 'Trivial\nPhase', color='white', ha='center', fontsize=12)
        
        ax.set_xlabel('Chemical Potential μ', color='white')
        ax.set_ylabel('Pairing Δ', color='white')
        ax.tick_params(colors='white')
    
    def _draw_majorana_qubit(self, ax):
        """Majorana kübiti"""
        # T-şeklinde tel
        # Yatay tel
        X, Z = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-0.2, 0.2, 5))
        Y = np.zeros_like(X)
        ax.plot_surface(X, Y, Z, color='silver', alpha=0.3)
        
        # Dikey tel
        Y, Z = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-0.2, 0.2, 5))
        X = np.zeros_like(Y)
        ax.plot_surface(X, Y, Z, color='silver', alpha=0.3)
        
        # 4 Majorana modu
        positions = [(-2, 0, 0), (2, 0, 0), (0, -2, 0), (0, 2, 0)]
        colors = ['#ff4444', '#44ff44', '#4444ff', '#ffff44']
        
        for pos, color in zip(positions, colors):
            gen = KececiCurveGenerator3D(
                num_children=6, max_level=2, scale_factor=0.25, base_radius=0.15,
                color_by_angle=True, alpha=0.8, growth_mode='majorana'
            )
            gen.generate_curve(center=pos)
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for i in range(len(xs)-1):
                    ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                           color=color, linewidth=1.5, alpha=0.7)
        
        ax.text(-2, 0.5, 0, "γ₁", color='#ff4444', fontsize=10)
        ax.text(2, 0.5, 0, "γ₂", color='#44ff44', fontsize=10)
        ax.text(0, -2.5, 0, "γ₃", color='#4444ff', fontsize=10)
        ax.text(0, 2.5, 0, "γ₄", color='#ffff44', fontsize=10)
        
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-1, 1])
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=30, azim=45)


# ============================================================================
# WEYL FERMİYONLARI VE YARIMETALLER
# ============================================================================

class WeylVisualizer:
    """Weyl fermiyonları ve yarımetaller için görselleştirici"""
    
    def visualize_weyl_semimetal(self):
        """
        Keçeci Eğrileri ile Weyl Yarımetali
        Keçeci Curves: Weyl Semimetal Band Structure
        
        Weyl fermiyonları, kütlesiz relativistik parçacıklardır.
        Weyl yarımetallerinde, iletim ve valans bantları Weyl noktalarında kesişir.
        """
        fig = plt.figure(figsize=(20, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # 1. Weyl konileri (3B)
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.set_facecolor('#0a0a1a')
        self._draw_weyl_cones(ax1)
        ax1.set_title("Keçeci 3D: Weyl Cones", color='white')
        
        # 2. Fermi yayları
        ax2 = fig.add_subplot(2, 3, 2, projection='3d')
        ax2.set_facecolor('#0a0a1a')
        self._draw_fermi_arcs(ax2)
        ax2.set_title("Keçeci 3D: Fermi Arcs", color='white')
        
        # 3. Kiral anomali
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        ax3.set_facecolor('#0a0a1a')
        self._draw_chiral_anomaly(ax3)
        ax3.set_title("Keçeci 3D: Chiral Anomaly", color='white')
        
        # 4. Brillouin bölgesi
        ax4 = fig.add_subplot(2, 3, 4, projection='3d')
        ax4.set_facecolor('#0a0a1a')
        self._draw_brillouin_zone(ax4)
        ax4.set_title("Keçeci 3D: Brillouin Zone", color='white')
        
        # 5. Berry eğriliği
        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        ax5.set_facecolor('#0a0a1a')
        self._draw_berry_curvature(ax5)
        ax5.set_title("Keçeci 3D: Berry Curvature", color='white')
        
        # 6. Weyl noktaları ağı
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        ax6.set_facecolor('#0a0a1a')
        self._draw_weyl_network(ax6)
        ax6.set_title("Keçeci 3D: Weyl Points Network", color='white')
        
        plt.suptitle("Keçeci Curves: Weyl Semimetals and Chiral Fermions", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    def _draw_weyl_cones(self, ax):
        """Weyl konileri"""
        # İki zıt kiraliteli Weyl noktası
        positions = [(-2, 0, 0), (2, 0, 0)]
        chiralities = [+1, -1]
        colors = ['#ff4444', '#4444ff']
        
        for pos, chi, color in zip(positions, chiralities, colors):
            # Koniyi oluştur
            r = np.linspace(0, 1.5, 20)
            theta = np.linspace(0, 2*np.pi, 20)
            R, Theta = np.meshgrid(r, theta)
            
            X = pos[0] + R * np.cos(Theta)
            Y = R * np.sin(Theta)
            Z = chi * R
            
            ax.plot_surface(X, Y, Z, color=color, alpha=0.3)
            ax.plot_surface(X, Y, -Z, color=color, alpha=0.3)
            
            # Keçeci eğrisi ile Weyl noktasını vurgula
            gen = KececiCurveGenerator3D(
                num_children=10, max_level=2, scale_factor=0.25, base_radius=0.2,
                color_by_angle=True, alpha=0.9, growth_mode='spiral',
                chirality=chi * 0.5
            )
            gen.generate_curve(center=pos)
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for i in range(len(xs)-1):
                    ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                           color=color, linewidth=1.5, alpha=0.7)
        
        ax.set_xlabel('k_x', color='white')
        ax.set_ylabel('k_y', color='white')
        ax.set_zlabel('E', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=30)
    
    def _draw_fermi_arcs(self, ax):
        """Fermi yayları"""
        # Yüzey Brillouin bölgesi
        kx = np.linspace(-np.pi, np.pi, 50)
        ky = np.linspace(-np.pi, np.pi, 50)
        KX, KY = np.meshgrid(kx, ky)
        
        # Fermi yayları (açık eğriler)
        for chi in [-1, 1]:
            t = np.linspace(-np.pi/2, np.pi/2, 30)
            kx_arc = chi * np.pi/2 + 0.5 * np.sin(t)
            ky_arc = t
            
            # Keçeci eğrileri ile Fermi yaylarını çiz
            for i in range(len(t)):
                gen = KececiCurveGenerator3D(
                    num_children=4, max_level=1, scale_factor=0.15, base_radius=0.05,
                    color_by_angle=True, alpha=0.7, chirality=chi
                )
                gen.generate_curve(center=(kx_arc[i], ky_arc[i], 0))
                pts = gen.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    zs = [p[0][2] for p in pts]
                    color = '#ff44ff' if chi > 0 else '#44ffff'
                    for j in range(len(xs)-1):
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color=color, linewidth=1.5, alpha=0.6)
        
        # Weyl noktalarının izdüşümleri
        ax.scatter([-np.pi/2, np.pi/2], [0, 0], [0, 0], 
                  color=['red', 'blue'], s=100, marker='*')
        
        ax.set_xlabel('k_x', color='white')
        ax.set_ylabel('k_y', color='white')
        ax.set_zlabel(' ', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=90, azim=0)
    
    def _draw_chiral_anomaly(self, ax):
        """Kiral anomali"""
        # Paralel E ve B alanları
        z = np.linspace(-3, 3, 30)
        
        # Weyl noktalarından parçacık pompalanması
        for i, z_pos in enumerate(z):
            density = 0.5 * (1 + np.tanh(z_pos))
            
            gen = KececiCurveGenerator3D(
                num_children=5, max_level=2, scale_factor=0.2, 
                base_radius=0.1 + density * 0.15,
                color_by_angle=True, alpha=0.7
            )
            gen.generate_curve(center=(0, 0, z_pos))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    color = plt.cm.plasma(density)
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color=color, linewidth=1, alpha=0.6)
        
        # E ve B alan okları
        ax.quiver(0, 0, -2.5, 0, 0, 5, color='yellow', linewidth=2, label='E ∥ B')
        
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.legend()
        ax.view_init(elev=20, azim=45)
    
    def _draw_brillouin_zone(self, ax):
        """Brillouin bölgesi"""
        # Küp çiz
        vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]) * 2
        
        edges = [
            (0,1), (1,2), (2,3), (3,0),  # Alt
            (4,5), (5,6), (6,7), (7,4),  # Üst
            (0,4), (1,5), (2,6), (3,7)   # Dikey
        ]
        
        for edge in edges:
            ax.plot3D(*zip(vertices[edge[0]], vertices[edge[1]]), 
                     color='white', alpha=0.3, linewidth=1)
        
        # Weyl noktaları (Brillouin bölgesi içinde)
        weyl_points = [(0, 0, 1.5), (0, 0, -1.5)]
        
        for pos, color in zip(weyl_points, ['#ff4444', '#4444ff']):
            gen = KececiCurveGenerator3D(
                num_children=8, max_level=2, scale_factor=0.2, base_radius=0.15,
                color_by_angle=True, alpha=0.8, distribution='weyl_cones'
            )
            gen.generate_curve(center=pos)
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for i in range(len(xs)-1):
                    ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                           color=color, linewidth=1.5, alpha=0.7)
            
            ax.scatter(*pos, color=color, s=100, marker='*')
        
        ax.set_xlabel('k_x', color='white')
        ax.set_ylabel('k_y', color='white')
        ax.set_zlabel('k_z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)
    
    def _draw_berry_curvature(self, ax):
        """Berry eğriliği"""
        # Weyl noktaları etrafında Berry eğriliği
        theta = np.linspace(0, np.pi, 20)
        phi = np.linspace(0, 2*np.pi, 20)
        Theta, Phi = np.meshgrid(theta, phi)
        
        # Berry eğriliği = manyetik monopole benzer
        R = 1.5
        X = R * np.sin(Theta) * np.cos(Phi)
        Y = R * np.sin(Theta) * np.sin(Phi)
        Z = R * np.cos(Theta)
        
        # Vektör alanı
        U = np.sin(Theta) * np.cos(Phi)
        V = np.sin(Theta) * np.sin(Phi)
        W = np.cos(Theta)
        
        ax.quiver(X[::2, ::2], Y[::2, ::2], Z[::2, ::2],
                 U[::2, ::2], V[::2, ::2], W[::2, ::2],
                 color='cyan', alpha=0.6, length=0.3)
        
        # Keçeci eğrisi ile Weyl noktası
        gen = KececiCurveGenerator3D(
            num_children=12, max_level=2, scale_factor=0.2, base_radius=0.2,
            color_by_angle=True, alpha=0.8
        )
        gen.generate_curve(center=(0, 0, 0))
        pts = gen.all_points
        if len(pts) > 1:
            xs = [p[0][0] for p in pts]
            ys = [p[0][1] for p in pts]
            zs = [p[0][2] for p in pts]
            for i in range(len(xs)-1):
                ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                       color='yellow', linewidth=1.5, alpha=0.7)
        
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)
        ax.set_title("Ω(k) ~ k/|k|³", color='white', fontsize=10)
    
    def _draw_weyl_network(self, ax):
        """Weyl noktaları ağı"""
        # Çoklu Weyl noktaları
        n_points = 8
        phi = np.pi * (3.0 - np.sqrt(5.0))
        
        for i in range(n_points):
            y = 1 - (i / float(max(1, n_points - 1))) * 2
            radius_xy = np.sqrt(max(0, 1 - y * y))
            theta = phi * i
            
            x = np.cos(theta) * radius_xy * 2.5
            z = np.sin(theta) * radius_xy * 2.5
            y = y * 2.5
            
            chirality = 1 if i % 2 == 0 else -1
            color = '#ff4444' if chirality > 0 else '#4444ff'
            
            gen = KececiCurveGenerator3D(
                num_children=6, max_level=2, scale_factor=0.2, base_radius=0.12,
                color_by_angle=True, alpha=0.7, chirality=chirality
            )
            gen.generate_curve(center=(x, y, z))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color=color, linewidth=1, alpha=0.6)
            
            ax.scatter(x, y, z, color=color, s=50, marker='*')
        
        # Bağlantılar (Fermi yayları)
        for i in range(n_points):
            if i % 2 == 0:  # Zıt kiraliteleri bağla
                y1 = 1 - (i / float(max(1, n_points - 1))) * 2
                r1 = np.sqrt(max(0, 1 - y1**2))
                x1 = np.cos(phi * i) * r1 * 2.5
                z1 = np.sin(phi * i) * r1 * 2.5
                y1 = y1 * 2.5
                
                j = (i + 1) % n_points
                y2 = 1 - (j / float(max(1, n_points - 1))) * 2
                r2 = np.sqrt(max(0, 1 - y2**2))
                x2 = np.cos(phi * j) * r2 * 2.5
                z2 = np.sin(phi * j) * r2 * 2.5
                y2 = y2 * 2.5
                
                ax.plot([x1, x2], [y1, y2], [z1, z2], 
                       color='white', alpha=0.3, linestyle='--', linewidth=0.8)
        
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-3, 3])
        ax.set_xlabel('k_x', color='white')
        ax.set_ylabel('k_y', color='white')
        ax.set_zlabel('k_z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)


# ============================================================================
# STRATUM MODELİ - ÇOK KATLI KUANTUM BİLGİSAYARLAR
# ============================================================================

class StratumModelVisualizer:
    """
    Stratum Modeli: Çok Katlı/Hibrit Kuantum Bilgisayar Mimarisi
    
    Stratum Modeli, farklı kuantum teknolojilerini katmanlı bir mimaride birleştirir:
    - Katman 1: Süperiletken kübitler (hızlı kapılar)
    - Katman 2: Majorana kübitleri (topolojik koruma)
    - Katman 3: Fotonik bağlantılar (kuantum iletişim)
    - Katman 4: Klasik kontrol (hata düzeltme)
    """
    
    def visualize_stratum_architecture(self):
        """
        Keçeci Eğrileri ile Stratum Modeli Mimarisi
        Keçeci Curves: Stratum Model - Layered Quantum Architecture
        """
        fig = plt.figure(figsize=(20, 14))
        fig.patch.set_facecolor('#0a0a1a')
        
        # 1. Tam mimari (3B)
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.set_facecolor('#0a0a1a')
        self._draw_full_architecture(ax1)
        ax1.set_title("Keçeci 3D: Stratum Architecture", color='white')
        
        # 2. Katman 1: Süperiletken kübitler
        ax2 = fig.add_subplot(2, 3, 2)
        ax2.set_facecolor('#0a0a1a')
        self._draw_superconducting_layer(ax2)
        ax2.set_title("Keçeci Curves: Layer 1 - Superconducting", color='white')
        
        # 3. Katman 2: Majorana kübitleri
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        ax3.set_facecolor('#0a0a1a')
        self._draw_majorana_layer(ax3)
        ax3.set_title("Keçeci 3D: Layer 2 - Majorana Qubits", color='white')
        
        # 4. Katman 3: Fotonik bağlantılar
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.set_facecolor('#0a0a1a')
        self._draw_photonic_layer(ax4)
        ax4.set_title("Keçeci Curves: Layer 3 - Photonic Links", color='white')
        
        # 5. Katmanlar arası bağlantı
        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        ax5.set_facecolor('#0a0a1a')
        self._draw_interlayer_connections(ax5)
        ax5.set_title("Keçeci 3D: Interlayer Coupling", color='white')
        
        # 6. Hata düzeltme döngüsü
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.set_facecolor('#0a0a1a')
        self._draw_error_correction_loop(ax6)
        ax6.set_title("Keçeci Curves: Error Correction Cycle", color='white')
        
        plt.suptitle("Keçeci Curves: Stratum Model - Hybrid Quantum Architecture", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    def _draw_full_architecture(self, ax):
        """Tam Stratum mimarisi"""
        layers = [
            {"z": -2, "color": "#4488ff", "name": "Superconducting", "type": "transmon"},
            {"z": 0, "color": "#ff4444", "name": "Majorana", "type": "topological"},
            {"z": 2, "color": "#44ff44", "name": "Photonic", "type": "optical"},
        ]
        
        for layer in layers:
            z = layer["z"]
            color = layer["color"]
            
            # Katman düzlemi
            X, Y = np.meshgrid(np.linspace(-2.5, 2.5, 10), np.linspace(-2.5, 2.5, 10))
            Z = np.ones_like(X) * z
            ax.plot_surface(X, Y, Z, color=color, alpha=0.1)
            
            # Katmandaki kübitler (Keçeci eğrileri)
            for i in range(5):
                angle = 2 * np.pi * i / 5
                r = 1.8
                x = r * np.cos(angle)
                y = r * np.sin(angle)
                
                gen = KececiCurveGenerator3D(
                    num_children=6, max_level=2, scale_factor=0.2, base_radius=0.15,
                    color_by_angle=True, alpha=0.8, growth_mode='outward'
                )
                gen.generate_curve(center=(x, y, z))
                pts = gen.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    zs = [p[0][2] for p in pts]
                    for j in range(len(xs)-1):
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color=color, linewidth=1.2, alpha=0.6)
        
        # Katmanlar arası bağlantılar
        for i in range(5):
            angle = 2 * np.pi * i / 5
            r = 1.8
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            
            ax.plot([x, x], [y, y], [-2, 2], color='white', alpha=0.2, linestyle=':')
        
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Layer', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)
    
    def _draw_superconducting_layer(self, ax):
        """Süperiletken katman"""
        # Transmon kübitleri
        positions = [
            (0, 0), (1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5),
            (0, 2.5), (-2.5, 0), (0, -2.5), (2.5, 0)
        ]
        
        for i, pos in enumerate(positions):
            # Transmon (anharmonik osilatör)
            gen = KececiCurveGenerator2D(
                num_children=5, max_level=3, scale_factor=0.3, base_radius=0.2,
                color_by_angle=True, line_width=1.2
            )
            gen.generate_curve(center=pos)
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                for j in range(len(xs)-1):
                    color = gen._get_color(pts[j][2])
                    ax.plot(xs[j:j+2], ys[j:j+2], color=color, linewidth=1, alpha=0.7)
            
            # Kapı bağlantıları
            if i < len(positions) - 1:
                for j in range(i+1, len(positions)):
                    dist = np.sqrt((positions[i][0] - positions[j][0])**2 + 
                                  (positions[i][1] - positions[j][1])**2)
                    if dist < 2.0:
                        ax.plot([positions[i][0], positions[j][0]],
                               [positions[i][1], positions[j][1]],
                               'cyan', alpha=0.3, linewidth=0.8)
        
        ax.set_xlim([-3.5, 3.5])
        ax.set_ylim([-3.5, 3.5])
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_majorana_layer(self, ax):
        """Majorana katmanı"""
        # T-şeklinde teller
        for i in range(4):
            angle = i * np.pi/2
            length = 2.0
            
            x = length * np.cos(angle)
            y = length * np.sin(angle)
            
            # Tel
            ax.plot([0, x], [0, y], [0, 0], color='silver', linewidth=3, alpha=0.5)
            
            # Uçlarda Majorana modları
            gen = KececiCurveGenerator3D(
                num_children=6, max_level=2, scale_factor=0.2, base_radius=0.12,
                color_by_angle=True, alpha=0.8, growth_mode='majorana'
            )
            gen.generate_curve(center=(x, y, 0))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color='#ff4444', linewidth=1.2, alpha=0.7)
        
        # Merkezde Majorana
        gen = KececiCurveGenerator3D(
            num_children=8, max_level=2, scale_factor=0.2, base_radius=0.18,
            color_by_angle=True, alpha=0.9, growth_mode='majorana'
        )
        gen.generate_curve(center=(0, 0, 0))
        pts = gen.all_points
        if len(pts) > 1:
            xs = [p[0][0] for p in pts]
            ys = [p[0][1] for p in pts]
            zs = [p[0][2] for p in pts]
            for j in range(len(xs)-1):
                ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                       color='yellow', linewidth=1.5, alpha=0.8)
        
        ax.set_xlim([-2.5, 2.5])
        ax.set_ylim([-2.5, 2.5])
        ax.set_zlim([-1, 1])
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=30, azim=45)
    
    def _draw_photonic_layer(self, ax):
        """Fotonik katman"""
        # Optik dalga kılavuzları
        t = np.linspace(0, 2*np.pi, 100)
        
        # Halka rezonatörler
        for i in range(3):
            r = 1.5 + i * 0.5
            x = r * np.cos(t)
            y = r * np.sin(t)
            
            ax.plot(x, y, color='#44ff44', linewidth=1.5, alpha=0.5)
            
            # Keçeci eğrileri ile fotonlar
            for j in range(0, len(t), 15):
                gen = KececiCurveGenerator2D(
                    num_children=4, max_level=1, scale_factor=0.15, base_radius=0.06,
                    color_by_angle=True, line_width=1
                )
                gen.generate_curve(center=(x[j], y[j]))
                pts = gen.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    for k in range(len(xs)-1):
                        color = gen._get_color(pts[k][2])
                        ax.plot(xs[k:k+2], ys[k:k+2], color=color, linewidth=0.8, alpha=0.6)
        
        # Doğrusal dalga kılavuzları
        for angle in [0, np.pi/3, 2*np.pi/3]:
            x = np.linspace(-2.5, 2.5, 50)
            y = np.tan(angle) * x
            mask = (x**2 + y**2) < 6
            
            ax.plot(x[mask], y[mask], color='#44ff88', linewidth=1, alpha=0.4)
        
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_interlayer_connections(self, ax):
        """Katmanlar arası bağlantılar"""
        layers_z = [-2, 0, 2]
        layer_colors = ['#4488ff', '#ff4444', '#44ff44']
        layer_names = ['SC', 'Majorana', 'Photonic']
        
        # Her katmanda noktalar
        points_per_layer = []
        for z in layers_z:
            points = []
            for i in range(4):
                angle = 2 * np.pi * i / 4 + z
                r = 1.5
                x = r * np.cos(angle)
                y = r * np.sin(angle)
                points.append((x, y, z))
            points_per_layer.append(points)
        
        # Katmanları çiz
        for z, color, name in zip(layers_z, layer_colors, layer_names):
            X, Y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
            Z = np.ones_like(X) * z
            ax.plot_surface(X, Y, Z, color=color, alpha=0.08)
            ax.text(0, 2.2, z, name, color=color, fontsize=10, ha='center')
        
        # Noktaları ve bağlantıları çiz
        for layer_idx, points in enumerate(points_per_layer):
            for x, y, z in points:
                gen = KececiCurveGenerator3D(
                    num_children=5, max_level=1, scale_factor=0.15, base_radius=0.1,
                    color_by_angle=True, alpha=0.7
                )
                gen.generate_curve(center=(x, y, z))
                pts = gen.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    zs = [p[0][2] for p in pts]
                    color = layer_colors[layer_idx]
                    for j in range(len(xs)-1):
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color=color, linewidth=1, alpha=0.5)
        
        # Katmanlar arası bağlantılar (kuantum dönüştürücüler)
        for i in range(4):
            p1 = points_per_layer[0][i]
            p2 = points_per_layer[1][i]
            p3 = points_per_layer[2][i]
            
            # Bağlantı eğrileri
            for p_start, p_end in [(p1, p2), (p2, p3)]:
                t = np.linspace(0, 1, 20)
                xs = p_start[0] * (1-t) + p_end[0] * t
                ys = p_start[1] * (1-t) + p_end[1] * t
                zs = p_start[2] * (1-t) + p_end[2] * t
                
                ax.plot(xs, ys, zs, color='yellow', linewidth=1.5, alpha=0.6, linestyle='--')
        
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Layer', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=25, azim=45)
    
    def _draw_error_correction_loop(self, ax):
        """Hata düzeltme döngüsü"""
        # Döngüsel süreç
        theta = np.linspace(0, 2*np.pi, 100)
        r = 2.0
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax.plot(x, y, color='white', linewidth=2, alpha=0.5)
        
        # Aşamalar
        stages = [
            ("Encode", 0, '#4488ff'),
            ("Error\nDetect", np.pi/2, '#ff4444'),
            ("Correct", np.pi, '#44ff44'),
            ("Measure", 3*np.pi/2, '#ffff44'),
        ]
        
        for name, angle, color in stages:
            px = r * np.cos(angle)
            py = r * np.sin(angle)
            
            gen = KececiCurveGenerator2D(
                num_children=6, max_level=2, scale_factor=0.2, base_radius=0.25,
                color_by_angle=True, line_width=1.2
            )
            gen.generate_curve(center=(px, py))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                for i in range(len(xs)-1):
                    ax.plot(xs[i:i+2], ys[i:i+2], color=color, linewidth=1.2, alpha=0.7)
            
            ax.text(px, py, name, color='white', fontsize=9, ha='center', va='center')
        
        # Sendrom kübitleri (iç halka)
        r_inner = 1.0
        for i in range(4):
            angle = i * np.pi/2 + np.pi/4
            px = r_inner * np.cos(angle)
            py = r_inner * np.sin(angle)
            
            gen = KececiCurveGenerator2D(
                num_children=4, max_level=1, scale_factor=0.15, base_radius=0.1,
                color_by_angle=True
            )
            gen.generate_curve(center=(px, py))
            pts = gen.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                for j in range(len(xs)-1):
                    color = gen._get_color(pts[j][2])
                    ax.plot(xs[j:j+2], ys[j:j+2], color=color, linewidth=0.8, alpha=0.5)
        
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_aspect('equal')
        ax.axis('off')
 
 # ============================================================================
# ZENGİN 3B KUANTUM GÖRSELLEŞTİRMELERİ
# ============================================================================

class Rich3DQuantumVisualizer:
    """3B zengin kuantum görselleştirmeleri"""
    
    def __init__(self):
        pass
    
    # --------------------------------------------------------------------------
    # 1. KUANTUM DURUM TOMOGRAFİSİ - 3B WIGNER FONKSİYONU
    # --------------------------------------------------------------------------
    
    def visualize_wigner_function_3d(self):
        """
        Keçeci 3B Eğrileri ile Wigner Fonksiyonu Görselleştirmesi
        Keçeci 3D Curves: Wigner Function Tomography
        
        Wigner fonksiyonu, kuantum durumlarının faz uzayındaki 
        yarı-olasılık dağılımını gösterir.
        """
        fig = plt.figure(figsize=(20, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Farklı kuantum durumları için Wigner fonksiyonları
        states = [
            ("Vakum Durumu |0⟩", self._wigner_vacuum),
            ("Koherent Durum |α⟩", self._wigner_coherent),
            ("Schrödinger Kedisi", self._wigner_cat),
            ("Sıkıştırılmış Durum", self._wigner_squeezed),
            ("Fock Durumu |1⟩", self._wigner_fock1),
            ("Termal Durum", self._wigner_thermal),
        ]
        
        for idx, (name, wigner_func) in enumerate(states):
            ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
            ax.set_facecolor('#0a0a1a')
            
            # Wigner fonksiyonu grid'i
            x = np.linspace(-3, 3, 40)
            y = np.linspace(-3, 3, 40)
            X, Y = np.meshgrid(x, y)
            Z = wigner_func(X, Y)
            
            # Yüzey çizimi
            surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.7, linewidth=0)
            
            # Keçeci 3B eğrisi ile kontur çizgileri
            for level in np.linspace(Z.min(), Z.max(), 5):
                if level > Z.min() + 0.1 * (Z.max() - Z.min()):
                    generator = KececiCurveGenerator3D(
                        num_children=6, max_level=2, scale_factor=0.3, base_radius=0.15,
                        color_by_angle=True, alpha=0.6, growth_mode='spiral'
                    )
                    # Kontur üzerinde bir nokta seç
                    contour_points = []
                    for i in range(len(x)//2):
                        xi, yi = x[i], y[i]
                        if abs(Z[i, i] - level) < 0.1:
                            contour_points.append((xi, yi, level))
                    
                    if contour_points:
                        center = contour_points[len(contour_points)//2]
                        generator.generate_curve(center=center)
                        
                        pts = generator.all_points
                        if len(pts) > 1:
                            xs = [p[0][0] for p in pts]
                            ys = [p[0][1] for p in pts]
                            zs = [p[0][2] for p in pts]
                            for i in range(len(xs)-1):
                                color = generator._get_color(pts[i][1], pts[i][2])
                                ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                                       color=color, linewidth=1, alpha=0.7)
            
            ax.set_title(f"Keçeci 3D Curves: {name}", color='white', fontsize=11)
            ax.set_xlabel('X', color='white')
            ax.set_ylabel('P', color='white')
            ax.set_zlabel('W(x,p)', color='white')
            ax.tick_params(colors='white')
            ax.view_init(elev=25, azim=45)
        
        plt.suptitle("Keçeci 3D Curves: Quantum State Tomography - Wigner Functions", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    def _wigner_vacuum(self, X, Y):
        return np.exp(-(X**2 + Y**2)) / np.pi
    
    def _wigner_coherent(self, X, Y):
        alpha_x, alpha_y = 1.5, 1.0
        return np.exp(-((X - alpha_x)**2 + (Y - alpha_y)**2)) / np.pi
    
    def _wigner_cat(self, X, Y):
        alpha = 2.0
        w1 = np.exp(-((X - alpha)**2 + Y**2))
        w2 = np.exp(-((X + alpha)**2 + Y**2))
        interference = 2 * np.exp(-(X**2 + Y**2)) * np.cos(2 * alpha * Y)
        return (w1 + w2 + interference) / (2 * np.pi * (1 + np.exp(-2*alpha**2)))
    
    def _wigner_squeezed(self, X, Y):
        r = 0.8
        return np.exp(-(X**2 * np.exp(2*r) + Y**2 * np.exp(-2*r))) / np.pi
    
    def _wigner_fock1(self, X, Y):
        r2 = X**2 + Y**2
        return (2 * r2 - 1) * np.exp(-r2) / np.pi
    
    def _wigner_thermal(self, X, Y):
        n_th = 1.0
        return np.exp(-(X**2 + Y**2) / (2*n_th + 1)) / (np.pi * (2*n_th + 1))
    
    # --------------------------------------------------------------------------
    # 2. KUANTUM DOLANIKLIK AĞI - 3B
    # --------------------------------------------------------------------------
    
    def visualize_entanglement_network_3d(self, n_qubits: int = 8):
        """
        Keçeci 3B Eğrileri ile Kuantum Dolanıklık Ağı
        Keçeci 3D Curves: Quantum Entanglement Network
        
        Çok parçacıklı dolanıklık durumlarının 3B ağ görselleştirmesi.
        """
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0a0a1a')
        
        # Kübitleri Fibonacci küre üzerine yerleştir
        phi = np.pi * (3.0 - np.sqrt(5.0))
        qubit_positions = []
        
        for i in range(n_qubits):
            y = 1 - (i / float(max(1, n_qubits - 1))) * 2 if n_qubits > 1 else 0
            radius_xy = np.sqrt(max(0, 1 - y * y))
            theta = phi * i
            
            x = np.cos(theta) * radius_xy * 3
            z = np.sin(theta) * radius_xy * 3
            y = y * 3
            
            qubit_positions.append((x, y, z))
        
        # Her kübit için Keçeci eğrisi
        for i, pos in enumerate(qubit_positions):
            generator = KececiCurveGenerator3D(
                num_children=5, max_level=2, scale_factor=0.25, base_radius=0.2,
                color_by_angle=True, alpha=0.8, growth_mode='outward'
            )
            generator.generate_curve(center=pos)
            
            pts = generator.all_points
            if len(pts) > 1:
                xs = [p[0][0] for p in pts]
                ys = [p[0][1] for p in pts]
                zs = [p[0][2] for p in pts]
                for j in range(len(xs)-1):
                    color = generator._get_color(pts[j][1], pts[j][2])
                    ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                           color=color, linewidth=1.5, alpha=0.7)
            
            ax.text(pos[0], pos[1], pos[2], f"|q{i}⟩", color='white', fontsize=10)
        
        # Dolanıklık bağlantıları (Keçeci eğrileri ile)
        entanglement_matrix = np.random.rand(n_qubits, n_qubits) * 0.3
        entanglement_matrix = (entanglement_matrix + entanglement_matrix.T) / 2
        
        for i in range(n_qubits):
            for j in range(i+1, n_qubits):
                strength = entanglement_matrix[i, j]
                if strength > 0.15:
                    # Dolanıklık bağlantısı için Keçeci eğrisi
                    p1 = np.array(qubit_positions[i])
                    p2 = np.array(qubit_positions[j])
                    
                    # Ara noktalar oluştur
                    mid = (p1 + p2) / 2
                    perp = np.cross(p2 - p1, [0, 0, 1])
                    if np.linalg.norm(perp) > 0:
                        perp = perp / np.linalg.norm(perp)
                    else:
                        perp = np.array([1, 0, 0])
                    
                    offset = perp * strength * 2
                    control_point = mid + offset
                    
                    # Bezier benzeri eğri için Keçeci noktaları
                    t = np.linspace(0, 1, 20)
                    curve_points = []
                    for ti in t:
                        pt = (1-ti)**2 * p1 + 2*(1-ti)*ti * control_point + ti**2 * p2
                        curve_points.append(pt)
                    
                    # Renk (dolanıklık gücüne göre)
                    color = plt.cm.plasma(strength * 2)
                    
                    xs = [p[0] for p in curve_points]
                    ys = [p[1] for p in curve_points]
                    zs = [p[2] for p in curve_points]
                    ax.plot(xs, ys, zs, color=color, linewidth=strength*3, alpha=0.6)
        
        ax.set_xlim([-4, 4])
        ax.set_ylim([-4, 4])
        ax.set_zlim([-4, 4])
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=20, azim=45)
        ax.set_title(f"Keçeci 3D Curves: Entanglement Network ({n_qubits} Qubits)", 
                    color='white', fontsize=14)
        
        plt.tight_layout()
        plt.show()
    
    # --------------------------------------------------------------------------
    # 3. ADIABATİK KUANTUM EVRİMİ
    # --------------------------------------------------------------------------
    
    def visualize_adiabatic_evolution_3d(self):
        """
        Keçeci 3B Eğrileri ile Adiabatik Kuantum Evrimi
        Keçeci 3D Curves: Adiabatic Quantum Evolution
        
        Hamiltonyen'in yavaşça değiştiği adiabatik süreç.
        """
        fig = plt.figure(figsize=(18, 10))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Zaman adımları
        time_steps = 8
        s_values = np.linspace(0, 1, time_steps)
        
        for idx, s in enumerate(s_values):
            ax = fig.add_subplot(2, 4, idx + 1, projection='3d')
            ax.set_facecolor('#0a0a1a')
            
            # Başlangıç ve hedef Hamiltonyen
            H_initial = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
            H_final = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
            
            # Anlık Hamiltonyen
            H_s = (1 - s) * H_initial + s * H_final
            
            # Özdeğerler ve özvektörler
            eigenvals, eigenvecs = np.linalg.eigh(H_s)
            
            # Enerji seviyelerini Keçeci eğrileri ile göster
            for i, (energy, vec) in enumerate(zip(eigenvals, eigenvecs.T)):
                # Enerji seviyesi yarıçapı
                radius = 0.5 + energy * 0.5
                
                # Durum vektörü yönü
                direction = vec / np.linalg.norm(vec)
                
                generator = KececiCurveGenerator3D(
                    num_children=6, max_level=2, scale_factor=0.3, base_radius=radius*0.3,
                    color_by_level=True, alpha=0.7, growth_mode='spiral',
                    angle_offset=i * 2*np.pi/3
                )
                generator.generate_curve(center=tuple(direction * radius))
                
                pts = generator.all_points
                if len(pts) > 1:
                    xs = [p[0][0] for p in pts]
                    ys = [p[0][1] for p in pts]
                    zs = [p[0][2] for p in pts]
                    for j in range(len(xs)-1):
                        color = generator._get_color(pts[j][1], pts[j][2])
                        ax.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 
                               color=color, linewidth=1.5, alpha=0.7)
            
            # Enerji seviyesi küreleri
            u = np.linspace(0, 2*np.pi, 15)
            v = np.linspace(0, np.pi, 15)
            for i, energy in enumerate(eigenvals):
                r = 0.5 + energy * 0.5
                x = r * np.outer(np.cos(u), np.sin(v))
                y = r * np.outer(np.sin(u), np.sin(v))
                z = r * np.outer(np.ones(np.size(u)), np.cos(v))
                ax.plot_wireframe(x, y, z, color=plt.cm.viridis(i/3), alpha=0.2, linewidth=0.5)
            
            ax.set_title(f"s = {s:.2f}\nE = [{eigenvals[0]:.2f}, {eigenvals[1]:.2f}, {eigenvals[2]:.2f}]", 
                        color='white', fontsize=9)
            ax.set_xlim([-1.5, 1.5])
            ax.set_ylim([-1.5, 1.5])
            ax.set_zlim([-1.5, 1.5])
            ax.set_aspect('equal')
            ax.axis('off')
            ax.view_init(elev=25, azim=45 + s*90)
        
        plt.suptitle("Keçeci 3D Curves: Adiabatic Quantum Evolution", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    # --------------------------------------------------------------------------
    # 4. TOPOLOJİK KUANTUM DURUMLARI (Anyonlar)
    # --------------------------------------------------------------------------
    
    def visualize_topological_anyons_3d(self):
        """
        Keçeci 3B Eğrileri ile Topolojik Anyonlar
        Keçeci 3D Curves: Topological Anyons
        
        Anyonların dünya çizgileri (worldlines) ve örgü (braiding) işlemleri.
        """
        fig = plt.figure(figsize=(18, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Farklı anyon konfigürasyonları
        configs = [
            ("Tek Anyon", 1, 0),
            ("İki Anyon - Trivial", 2, 0),
            ("İki Anyon - Örgü", 2, np.pi),
            ("Üç Anyon", 3, np.pi/2),
            ("Dört Anyon - Fibonacci", 4, 2*np.pi/3),
            ("Anyon Gazı", 6, np.pi/4),
        ]
        
        for idx, (name, n_anyons, phase) in enumerate(configs):
            ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
            ax.set_facecolor('#0a0a1a')
            
            # Anyon pozisyonları (dairesel)
            t_values = np.linspace(0, 4*np.pi, 100)
            
            for i in range(n_anyons):
                angle_offset = 2 * np.pi * i / n_anyons + phase
                
                # Anyon dünya çizgisi (spiral)
                r_base = 1.5
                x = (r_base + 0.3 * np.sin(t_values)) * np.cos(t_values/2 + angle_offset)
                y = (r_base + 0.3 * np.sin(t_values)) * np.sin(t_values/2 + angle_offset)
                z = t_values / 2 - 2
                
                # Keçeci eğrisi ile süsle
                for j in range(0, len(t_values), 15):
                    generator = KececiCurveGenerator3D(
                        num_children=4, max_level=1, scale_factor=0.25, base_radius=0.08,
                        color_by_angle=True, alpha=0.7, growth_mode='outward',
                        angle_offset=angle_offset + j*0.1
                    )
                    generator.generate_curve(center=(x[j], y[j], z[j]))
                    
                    pts = generator.all_points
                    if len(pts) > 1:
                        xs = [p[0][0] for p in pts]
                        ys = [p[0][1] for p in pts]
                        zs = [p[0][2] for p in pts]
                        for k in range(len(xs)-1):
                            color = generator._get_color(pts[k][1], pts[k][2])
                            ax.plot(xs[k:k+2], ys[k:k+2], zs[k:k+2], 
                                   color=color, linewidth=1, alpha=0.6)
                
                # Ana dünya çizgisi
                color = plt.cm.hsv(i / n_anyons)
                ax.plot(x, y, z, color=color, linewidth=2, alpha=0.8)
            
            ax.set_title(f"Keçeci 3D: {name}", color='white', fontsize=11)
            ax.set_xlim([-2.5, 2.5])
            ax.set_ylim([-2.5, 2.5])
            ax.set_zlim([-3, 3])
            ax.set_xlabel('X', color='white')
            ax.set_ylabel('Y', color='white')
            ax.set_zlabel('Time', color='white')
            ax.tick_params(colors='white')
            ax.view_init(elev=20, azim=45 + idx*30)
        
        plt.suptitle("Keçeci 3D Curves: Topological Quantum States - Anyon Worldlines", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
    
    # --------------------------------------------------------------------------
    # 5. KUANTUM FOURIER DÖNÜŞÜMÜ - 3B SPEKTRUM
    # --------------------------------------------------------------------------
    
    def visualize_qft_spectrum_3d(self, n_qubits: int = 4):
        """
        Keçeci 3B Eğrileri ile Kuantum Fourier Dönüşümü Spektrumu
        Keçeci 3D Curves: Quantum Fourier Transform Spectrum
        """
        N = 2 ** n_qubits
        
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0a0a1a')
        
        # QFT matrisi
        omega = np.exp(2j * np.pi / N)
        QFT = np.array([[omega**(j*k) for k in range(N)] for j in range(N)]) / np.sqrt(N)
        
        # Her baz durumu için Keçeci eğrisi
        for j in range(N):
            # Genlik ve faz
            amplitudes = np.abs(QFT[j])
            phases = np.angle(QFT[j])
            
            # Silindirik koordinatlar
            radius_base = 2.0
            for k in range(N):
                if amplitudes[k] > 0.05:
                    r = radius_base + amplitudes[k] * 1.5
                    theta = 2 * np.pi * k / N
                    z = phases[k]
                    
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    
                    generator = KececiCurveGenerator3D(
                        num_children=5, max_level=2, scale_factor=0.2, 
                        base_radius=amplitudes[k] * 0.3,
                        color_by_angle=True, alpha=0.7,
                        angle_offset=phases[k]
                    )
                    generator.generate_curve(center=(x, y, z))
                    
                    pts = generator.all_points
                    if len(pts) > 1:
                        xs = [p[0][0] for p in pts]
                        ys = [p[0][1] for p in pts]
                        zs = [p[0][2] for p in pts]
                        for i in range(len(xs)-1):
                            color = generator._get_color(pts[i][1], pts[i][2])
                            ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                                   color=color, linewidth=1, alpha=0.6)
        
        # Bağlantı çizgileri (spektrum)
        for j in range(N):
            points = []
            for k in range(N):
                amp = np.abs(QFT[j, k])
                if amp > 0.05:
                    r = 2.0 + amp * 1.5
                    theta = 2 * np.pi * k / N
                    z = np.angle(QFT[j, k])
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    points.append((x, y, z))
            
            if len(points) > 1:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                zs = [p[2] for p in points]
                color = plt.cm.viridis(j / N)
                ax.plot(xs, ys, zs, color=color, linewidth=1, alpha=0.4, linestyle='--')
        
        ax.set_xlabel('Re', color='white')
        ax.set_ylabel('Im', color='white')
        ax.set_zlabel('Phase', color='white')
        ax.tick_params(colors='white')
        ax.view_init(elev=30, azim=45)
        ax.set_title(f"Keçeci 3D Curves: QFT Spectrum ({n_qubits} Qubits, N={N})", 
                    color='white', fontsize=14)
        
        plt.tight_layout()
        plt.show()
        
# ============================================================================
# İLERİ KUANTUM HESAPLAMALARI GÖRSELLEŞTİRME
# ============================================================================

class AdvancedQuantumVisualizer:
    """İleri kuantum hesaplamaları için Keçeci Eğrisi görselleştiricisi"""
    
    def __init__(self):
        self.figures = []
    
    def _draw_curve_2d(self, ax, generator, label: str = ""):
        """2B eğriyi çiz"""
        sorted_points = sorted(generator.all_points, key=lambda p: (p[1], p[2]))
        
        if len(sorted_points) > 1:
            x_coords = [p[0][0] for p in sorted_points]
            y_coords = [p[0][1] for p in sorted_points]
            
            if generator.color_by_level or generator.color_by_angle:
                for i in range(len(x_coords) - 1):
                    color = generator._get_color_for_segment(
                        sorted_points[i][1], 
                        sorted_points[i][2]
                    )
                    ax.plot(x_coords[i:i+2], y_coords[i:i+2],
                           generator.line_style, linewidth=generator.line_width,
                           color=color, alpha=generator.alpha)
            else:
                ax.plot(x_coords, y_coords, generator.line_style,
                       linewidth=generator.line_width,
                       color=generator.line_color, alpha=generator.alpha)
        
        if generator.show_points:
            for point, level, angle in generator.all_points:
                if level == generator.max_level:
                    color = 'red'
                else:
                    color = generator.line_color or 'white'
                ax.plot(point[0], point[1], 'o', 
                       markersize=generator.point_size, color=color, alpha=0.6)
        
        if label:
            ax.text(0.02, 0.98, label, transform=ax.transAxes,
                   color='white', fontsize=10, verticalalignment='top')

    # --------------------------------------------------------------------------
    # 1. BLOCH KÜRESİ VE KÜBİT DURUMLARI
    # --------------------------------------------------------------------------
    
    def visualize_bloch_sphere_states(self):
        """
        Keçeci Eğrileri ile Bloch Küresi Üzerinde Kübit Durumları
        Keçeci Curves: Qubit States on the Bloch Sphere
        """
        fig = plt.figure(figsize=(20, 10))
        fig.patch.set_facecolor('#0a0a1a')
        
        states = [
            ("|0⟩", 0, 0, "#00ffff"),
            ("|1⟩", np.pi, 0, "#ff00ff"),
            ("|+⟩", np.pi/2, 0, "#ffff00"),
            ("|-⟩", np.pi/2, np.pi, "#ff8800"),
            ("|↻⟩", np.pi/2, np.pi/2, "#00ff00"),
            ("|↺⟩", np.pi/2, -np.pi/2, "#ff4444"),
            ("|ψ⟩", np.pi/3, np.pi/4, "#44ff88"),
            ("|φ⟩", 2*np.pi/3, 3*np.pi/4, "#8844ff"),
        ]
        
        for idx, (name, theta, phi, color) in enumerate(states):
            ax = fig.add_subplot(2, 4, idx + 1, projection='3d')
            ax.set_facecolor('#0a0a1a')
            
            # Bloch küresi
            u = np.linspace(0, 2*np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))
            
            ax.plot_surface(x, y, z, color='white', alpha=0.05, linewidth=0)
            ax.plot_wireframe(x, y, z, color='white', alpha=0.1, linewidth=0.3)
            
            # Eksenler
            ax.plot([-1.5, 1.5], [0, 0], [0, 0], 'white', alpha=0.2, linewidth=0.5)
            ax.plot([0, 0], [-1.5, 1.5], [0, 0], 'white', alpha=0.2, linewidth=0.5)
            ax.plot([0, 0], [0, 0], [-1.5, 1.5], 'white', alpha=0.2, linewidth=0.5)
            
            # Durum vektörü
            sx = np.sin(theta) * np.cos(phi)
            sy = np.sin(theta) * np.sin(phi)
            sz = np.cos(theta)
            ax.quiver(0, 0, 0, sx, sy, sz, color=color, linewidth=3, alpha=0.9, 
                     arrow_length_ratio=0.1)
            
            # Keçeci 3B eğrisi
            generator3d = KececiCurveGenerator3D(
                num_children=5, max_level=2, scale_factor=0.35, base_radius=0.2,
                angle_offset=phi, angle_variation=theta/4,
                color_by_angle=True, line_color=color, alpha=0.8
            )
            generator3d.generate_curve(center=(sx, sy, sz))
            
            if len(generator3d.all_points) > 1:
                xs = [p[0][0] for p in generator3d.all_points]
                ys = [p[0][1] for p in generator3d.all_points]
                zs = [p[0][2] for p in generator3d.all_points]
                
                for i in range(len(xs) - 1):
                    point = generator3d.all_points[i]
                    seg_color = generator3d._get_color(point[2])
                    ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 
                           color=seg_color, linewidth=1.5, alpha=0.7)
            
            ax.set_title(f"{name}\nθ={theta/np.pi:.2f}π, φ={phi/np.pi:.2f}π", 
                        color='white', fontsize=10)
            ax.set_xlim([-1.5, 1.5])
            ax.set_ylim([-1.5, 1.5])
            ax.set_zlim([-1.5, 1.5])
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Keçeci Curves: Qubit States on the Bloch Sphere", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    # --------------------------------------------------------------------------
    # 2. SHOR ALGORİTMASI (DÜZELTİLMİŞ)
    # --------------------------------------------------------------------------
    
    def visualize_shor_algorithm(self, N: int = 15, a: int = 7):
        """
        Keçeci Eğrileri ile Shor Algoritması Periyot Bulma
        Keçeci Curves: Shor's Algorithm Period Finding
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Periyot hesaplama
        period = self._find_period(a, N)
        
        # f(x) = a^x mod N değerleri (DÜZELTİLDİ)
        x_values = list(range(16))
        f_values = [pow(a, int(x), N) for x in x_values]  # int() dönüşümü eklendi
        
        # 1. Modüler Üs Alma
        ax1 = axes[0, 0]
        ax1.set_facecolor('#0a0a1a')
        for i, (x, fx) in enumerate(zip(x_values[:8], f_values[:8])):  # İlk 8 değer
            generator = KececiCurveGenerator(
                num_children=4, max_level=2, scale_factor=0.2, base_radius=0.1,
                angle_offset=fx * 2*np.pi/N, color_by_angle=True,
                line_width=1.0, show_points=True, alpha=0.7
            )
            generator.generate_curve(center=(x * 0.5, fx * 0.3))
            self._draw_curve_2d(ax1, generator)
        
        ax1.set_title(f"Keçeci Curves: f(x) = {a}^x mod {N}", color='white')
        ax1.set_xlabel("x", color='white')
        ax1.set_ylabel("f(x)", color='white')
        ax1.tick_params(colors='white')
        ax1.set_xlim(-0.5, 4.5)
        ax1.set_ylim(-0.5, N * 0.3 + 0.5)
        
        # 2. Periyodik Desen
        ax2 = axes[0, 1]
        ax2.set_facecolor('#0a0a1a')
        
        for cycle in range(3):
            offset = cycle * period
            generator = KececiCurveGenerator(
                num_children=6, max_level=3, scale_factor=0.3, base_radius=0.6,
                child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                angle_offset=offset * 2*np.pi/period,
                color_by_level=True, line_width=1.2, show_points=True, alpha=0.8
            )
            generator.generate_curve(center=(offset * 0.4, 0))
            self._draw_curve_2d(ax2, generator)
        
        ax2.set_title(f"Keçeci Curves: Period = {period}", color='white')
        ax2.axvline(x=period*0.4, color='yellow', linestyle='--', alpha=0.5)
        ax2.set_xlim(-1, period * 1.8)
        ax2.set_ylim(-1.2, 1.2)
        ax2.set_aspect('equal')
        ax2.axis('off')
        
        # 3. Kuantum Fourier Dönüşümü
        ax3 = axes[0, 2]
        ax3.set_facecolor('#0a0a1a')
        
        qft_states = 8
        for i in range(qft_states):
            phase = 2 * np.pi * i / qft_states
            generator = KececiCurveGenerator(
                num_children=5, max_level=3, scale_factor=0.3, base_radius=0.45,
                child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                angle_offset=phase, angle_variation=0.1,
                color_by_angle=True, line_width=1.0, show_points=False, alpha=0.6
            )
            angle_pos = i * 2*np.pi/qft_states
            generator.generate_curve(center=(np.cos(angle_pos)*1.2, np.sin(angle_pos)*1.2))
            self._draw_curve_2d(ax3, generator)
        
        ax3.set_title("Keçeci Curves: Quantum Fourier Transform", color='white')
        ax3.set_xlim(-2, 2)
        ax3.set_ylim(-2, 2)
        ax3.set_aspect('equal')
        ax3.axis('off')
        
        # 4. Olasılık Dağılımı
        ax4 = axes[1, 0]
        ax4.set_facecolor('#0a0a1a')
        
        peaks = [i * 16/period for i in range(period)]
        x_prob = np.linspace(0, 16, 100)
        prob = np.zeros_like(x_prob)
        for peak in peaks:
            prob += np.exp(-(x_prob - peak)**2 / 0.5)
        
        ax4.fill_between(x_prob, 0, prob, color='cyan', alpha=0.3)
        ax4.plot(x_prob, prob, 'c-', linewidth=2)
        
        for peak in peaks:
            generator = KececiCurveGenerator(
                num_children=4, max_level=2, scale_factor=0.18, base_radius=0.07,
                color_by_angle=True, line_color='yellow', line_width=1.0, show_points=True
            )
            idx = int(peak * 100 / 16)
            if idx < len(prob):
                generator.generate_curve(center=(peak, prob[idx]))
                self._draw_curve_2d(ax4, generator)
        
        ax4.set_title("Keçeci Curves: Probability Distribution", color='white')
        ax4.set_xlabel("State", color='white')
        ax4.set_ylabel("Probability", color='white')
        ax4.tick_params(colors='white')
        
        # 5. Çarpanlar
        ax5 = axes[1, 1]
        ax5.set_facecolor('#0a0a1a')
        
        factors = self._find_factors(a, period, N)
        
        circle = Circle((0, 0), 1.8, fill=False, edgecolor='white', alpha=0.3)
        ax5.add_patch(circle)
        
        for i, factor in enumerate(factors):
            angle = 2 * np.pi * i / max(1, len(factors))
            x, y = np.cos(angle) * 1.8, np.sin(angle) * 1.8
            
            generator = KececiCurveGenerator(
                num_children=min(factor, 8), max_level=3, scale_factor=0.25, base_radius=0.3,
                child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                color_by_angle=True, line_width=1.2, show_points=True
            )
            generator.generate_curve(center=(x, y))
            self._draw_curve_2d(ax5, generator)
            ax5.text(x, y, str(factor), color='white', fontsize=12, ha='center', va='center')
        
        ax5.set_title(f"Keçeci Curves: Factors of {N}: {factors}", color='white')
        ax5.set_xlim(-2.5, 2.5)
        ax5.set_ylim(-2.5, 2.5)
        ax5.set_aspect('equal')
        ax5.axis('off')
        
        # 6. Özet
        ax6 = axes[1, 2]
        ax6.set_facecolor('#0a0a1a')
        ax6.text(0.5, 0.9, "Shor's Algorithm Summary", color='white', 
                fontsize=14, ha='center', fontweight='bold')
        ax6.text(0.5, 0.7, f"N = {N}, a = {a}", color='cyan', fontsize=12, ha='center')
        ax6.text(0.5, 0.55, f"Period r = {period}", color='yellow', fontsize=12, ha='center')
        ax6.text(0.5, 0.35, f"gcd(a^(r/2) ± 1, N)", color='white', fontsize=11, ha='center')
        ax6.text(0.5, 0.2, f"= {factors}", color='lime', fontsize=14, ha='center')
        if len(factors) == 2:
            ax6.text(0.5, 0.08, f"✓ {N} = {factors[0]} × {factors[1]}", color='white', 
                    fontsize=14, ha='center', fontweight='bold')
        
        ax6.axis('off')
        
        plt.suptitle(f"Keçeci Curves: Shor's Algorithm (N={N}, a={a})", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def _find_period(self, a: int, N: int) -> int:
        """Periyot bulma"""
        a = int(a)
        N = int(N)
        for r in range(1, N):
            if pow(a, r, N) == 1:
                return r
        return N - 1
    
    def _find_factors(self, a: int, r: int, N: int) -> list:
        """Çarpanları bul"""
        a = int(a)
        r = int(r)
        N = int(N)
        
        if r % 2 != 0:
            return [1, N]
        
        x = pow(a, r//2, N)
        if x == N - 1:
            return [1, N]
        
        import math
        factor1 = math.gcd(x + 1, N)
        factor2 = math.gcd(x - 1, N)
        
        if factor1 == 1 or factor2 == 1:
            return [1, N]
        
        return [int(factor1), int(factor2)]
    
    # --------------------------------------------------------------------------
    # 3. GROVER ALGORİTMASI
    # --------------------------------------------------------------------------
    
    def visualize_grover_algorithm(self, n_qubits: int = 3, target_index: int = 5):
        """
        Keçeci Eğrileri ile Grover Arama Algoritması
        Keçeci Curves: Grover's Search Algorithm
        """
        N = 2 ** n_qubits
        optimal_iterations = int(np.pi/4 * np.sqrt(N))
        
        fig = plt.figure(figsize=(20, 10))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Başlangıç
        ax0 = plt.subplot(2, 4, 1)
        ax0.set_facecolor('#0a0a1a')
        
        for i in range(min(N, 12)):  # Sınırla
            angle = 2 * np.pi * i / N
            radius = 1.5
            x, y = radius * np.cos(angle), radius * np.sin(angle)
            
            amplitude = 1/np.sqrt(N)
            generator = KececiCurveGenerator(
                num_children=4, max_level=2, scale_factor=0.2, base_radius=amplitude * 1.2,
                color_by_angle=True, line_width=1.0, alpha=0.7
            )
            generator.generate_curve(center=(x, y))
            self._draw_curve_2d(ax0, generator)
        
        ax0.set_title(f"Keçeci Curves: Initial |ψ₀⟩", color='white')
        ax0.set_xlim(-2.5, 2.5)
        ax0.set_ylim(-2.5, 2.5)
        ax0.set_aspect('equal')
        ax0.axis('off')
        
        # Grover iterasyonları
        iterations_to_show = [1, 2, optimal_iterations]
        
        for idx, k in enumerate(iterations_to_show[:3]):
            ax = plt.subplot(2, 4, idx + 2)
            ax.set_facecolor('#0a0a1a')
            
            theta = np.arcsin(1/np.sqrt(N))
            current_theta = (2*k + 1) * theta
            
            for i in range(min(N, 12)):
                angle = 2 * np.pi * i / N
                radius = 1.5
                x, y = radius * np.cos(angle), radius * np.sin(angle)
                
                if i == target_index:
                    amplitude = np.sin(current_theta)
                    color = 'lime'
                else:
                    amplitude = np.cos(current_theta) / np.sqrt(N - 1)
                    color = None
                
                generator = KececiCurveGenerator(
                    num_children=5, max_level=3, scale_factor=0.25, base_radius=amplitude * 1.2,
                    child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                    color_by_angle=(color is None),
                    line_color=color if color else None,
                    line_width=1.2, alpha=0.8
                )
                generator.generate_curve(center=(x, y))
                self._draw_curve_2d(ax, generator)
            
            target_angle = 2 * np.pi * target_index / N
            tx, ty = 1.5 * np.cos(target_angle), 1.5 * np.sin(target_angle)
            circle = Circle((tx, ty), 0.4, fill=False, edgecolor='yellow', linewidth=2)
            ax.add_patch(circle)
            
            ax.set_title(f"Iteration {k}\nP(target) = {np.sin(current_theta)**2:.3f}", 
                        color='white')
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.set_aspect('equal')
            ax.axis('off')
        
        # Boş subplotları gizle
        for i in range(4, 8):
            ax = plt.subplot(2, 4, i + 1)
            ax.set_facecolor('#0a0a1a')
            ax.axis('off')
        
        # Genlik evrimi (alt kısım)
        ax_ev = plt.subplot(2, 1, 2)
        ax_ev.set_facecolor('#0a0a1a')
        
        iterations = np.arange(0, optimal_iterations + 2)
        theta = np.arcsin(1/np.sqrt(N))
        target_amps = [np.sin((2*k + 1) * theta)**2 for k in iterations]
        
        ax_ev.plot(iterations, target_amps, 'lime', linewidth=3, label='Target Probability')
        ax_ev.axvline(x=optimal_iterations, color='yellow', linestyle='--', alpha=0.5)
        
        ax_ev.set_title("Keçeci Curves: Amplitude Evolution", color='white')
        ax_ev.set_xlabel("Iteration", color='white')
        ax_ev.set_ylabel("Probability", color='white')
        ax_ev.legend()
        ax_ev.tick_params(colors='white')
        
        plt.suptitle(f"Keçeci Curves: Grover's Algorithm (N={N}, target=|{target_index}⟩)", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    # --------------------------------------------------------------------------
    # 4. DEUTSCH-JOZSA ALGORİTMASI
    # --------------------------------------------------------------------------
    
    def visualize_deutsch_jozsa(self):
        """
        Keçeci Eğrileri ile Deutsch-Jozsa Algoritması
        Keçeci Curves: Deutsch-Jozsa Algorithm
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Sabit fonksiyon f(x)=0
        ax1 = axes[0, 0]
        ax1.set_facecolor('#0a0a1a')
        self._draw_oracle_circuit(ax1, "Keçeci Curves: Constant f(x)=0", 'constant')
        
        # Sabit fonksiyon f(x)=1
        ax2 = axes[0, 1]
        ax2.set_facecolor('#0a0a1a')
        self._draw_oracle_circuit(ax2, "Keçeci Curves: Constant f(x)=1", 'constant_one')
        
        # Dengeli fonksiyon
        ax3 = axes[0, 2]
        ax3.set_facecolor('#0a0a1a')
        self._draw_oracle_circuit(ax3, "Keçeci Curves: Balanced Function", 'balanced')
        
        # Ölçüm sonuçları
        ax4 = axes[1, 0]
        ax4.set_facecolor('#0a0a1a')
        self._draw_measurement_result(ax4, "Keçeci Curves: Constant → |00...0⟩", True)
        
        ax5 = axes[1, 1]
        ax5.set_facecolor('#0a0a1a')
        self._draw_measurement_result(ax5, "Keçeci Curves: Balanced → NOT all |0⟩", False)
        
        # Devre
        ax6 = axes[1, 2]
        ax6.set_facecolor('#0a0a1a')
        self._draw_quantum_circuit_diagram(ax6)
        ax6.set_title("Keçeci Curves: Deutsch-Jozsa Circuit", color='white')
        
        plt.suptitle("Keçeci Curves: Deutsch-Jozsa Algorithm", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def _draw_oracle_circuit(self, ax, title: str, func_type: str):
        """Oracle devresi çizimi"""
        n_states = 8
        
        for i in range(n_states):
            x_pos = (i % 4) * 1.2 - 1.8
            y_pos = (i // 4) * 1.2 - 0.6
            
            if func_type == 'constant':
                value = 0
                color = '#4488ff'
            elif func_type == 'constant_one':
                value = 1
                color = '#44ff44'
            else:
                value = i % 2
                color = '#ff8844' if value == 0 else '#ff44ff'
            
            generator = KececiCurveGenerator(
                num_children=3, max_level=2, scale_factor=0.2, base_radius=0.1 + value * 0.07,
                child_ordering=ChildOrdering.ALTERNATING if value == 0 else ChildOrdering.SPIRAL_OUTWARD,
                color_by_angle=True, line_color=color, line_width=1.0, alpha=0.8
            )
            generator.generate_curve(center=(x_pos, y_pos))
            self._draw_curve_2d(ax, generator)
        
        ax.set_title(title, color='white')
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_measurement_result(self, ax, title: str, is_constant: bool):
        """Ölçüm sonucu görselleştirmesi"""
        if is_constant:
            for i in range(3):
                generator = KececiCurveGenerator(
                    num_children=4, max_level=3, scale_factor=0.25, base_radius=0.2,
                    child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                    color_by_angle=True, line_color='cyan', line_width=1.5, alpha=0.9
                )
                generator.generate_curve(center=(i * 1.2 - 1.2, 0))
                self._draw_curve_2d(ax, generator)
                ax.text(i * 1.2 - 1.2, -0.7, "|0⟩", color='white', ha='center')
        else:
            states = [0, 1, 0, 1, 0]
            for i, state in enumerate(states):
                x = (i % 3) * 1.2 - 1.2
                y = (i // 3) * 1.0 - 0.5
                
                generator = KececiCurveGenerator(
                    num_children=4, max_level=3, scale_factor=0.25, base_radius=0.2,
                    child_ordering=ChildOrdering.SPIRAL_INWARD if state == 1 else ChildOrdering.SPIRAL_OUTWARD,
                    color_by_angle=True,
                    line_color='yellow' if state == 1 else 'red',
                    line_width=1.5, alpha=0.9
                )
                generator.generate_curve(center=(x, y))
                self._draw_curve_2d(ax, generator)
                ax.text(x, y - 0.6, f"|{state}⟩", color='white', ha='center')
        
        ax.set_title(title, color='white')
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_quantum_circuit_diagram(self, ax):
        """Kuantum devre diyagramı"""
        for i in range(3):
            y = 0.8 - i * 0.25
            ax.plot([0.05, 0.95], [y, y], 'white', linewidth=1, alpha=0.5)
            ax.text(0.02, y, f"|0⟩", color='white', fontsize=10, va='center')
        
        for i in range(3):
            y = 0.8 - i * 0.25
            rect = Rectangle((0.2, y-0.08), 0.12, 0.16, fill=False, edgecolor='cyan', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(0.26, y, "H", color='cyan', fontsize=10, ha='center', va='center')
        
        rect = Rectangle((0.45, 0.25), 0.15, 0.65, fill=False, edgecolor='yellow', linewidth=2)
        ax.add_patch(rect)
        ax.text(0.525, 0.6, "U_f", color='yellow', fontsize=12, ha='center', va='center')
        
        for i in range(3):
            y = 0.8 - i * 0.25
            rect = Rectangle((0.7, y-0.08), 0.12, 0.16, fill=False, edgecolor='cyan', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(0.76, y, "H", color='cyan', fontsize=10, ha='center', va='center')
        
        for i in range(3):
            y = 0.8 - i * 0.25
            ax.plot(0.9, y, 'o', color='white', markersize=8)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    # --------------------------------------------------------------------------
    # 5. KUANTUM HATA DÜZELTME (ÖZET)
    # --------------------------------------------------------------------------
    
    def visualize_quantum_error_correction(self):
        """
        Keçeci Eğrileri ile Kuantum Hata Düzeltme Kodları
        Keçeci Curves: Quantum Error Correction Codes
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.patch.set_facecolor('#0a0a1a')
        
        # Bit flip kodlama
        ax1 = axes[0, 0]
        ax1.set_facecolor('#0a0a1a')
        self._draw_qec_encoding(ax1)
        ax1.set_title("Keçeci Curves: Bit Flip Encoding\n|ψ⟩ → |ψψψ⟩", color='white')
        
        # Sendrom
        ax2 = axes[0, 1]
        ax2.set_facecolor('#0a0a1a')
        self._draw_qec_syndrome(ax2)
        ax2.set_title("Keçeci Curves: Syndrome Measurement", color='white')
        
        # Düzeltme
        ax3 = axes[0, 2]
        ax3.set_facecolor('#0a0a1a')
        self._draw_qec_correction(ax3)
        ax3.set_title("Keçeci Curves: Error Correction", color='white')
        
        # Phase flip
        ax4 = axes[1, 0]
        ax4.set_facecolor('#0a0a1a')
        self._draw_phase_flip_code(ax4)
        ax4.set_title("Keçeci Curves: Phase Flip Code\n|+⟩ → |+++⟩", color='white')
        
        # Shor kodu
        ax5 = axes[1, 1]
        ax5.set_facecolor('#0a0a1a')
        self._draw_shor_code(ax5)
        ax5.set_title("Keçeci Curves: Shor's 9-Qubit Code", color='white')
        
        # Hata oranı
        ax6 = axes[1, 2]
        ax6.set_facecolor('#0a0a1a')
        self._draw_error_rate_plot(ax6)
        ax6.set_title("Keçeci Curves: Error Rate Comparison", color='white')
        
        plt.suptitle("Keçeci Curves: Quantum Error Correction", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def _draw_qec_encoding(self, ax):
        g1 = KececiCurveGenerator(num_children=5, max_level=3, scale_factor=0.2, base_radius=0.18,
                                  color_by_angle=True, line_color='cyan', line_width=1.5)
        g1.generate_curve(center=(-1.5, 0))
        self._draw_curve_2d(ax, g1)
        ax.text(-1.5, -0.6, "|ψ⟩", color='white', ha='center')
        
        for i in range(3):
            g = KececiCurveGenerator(num_children=5, max_level=3, scale_factor=0.2, base_radius=0.18,
                                     child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                                     color_by_angle=True, line_color='lime', line_width=1.2)
            g.generate_curve(center=(i * 1.0 - 0.5, 0))
            self._draw_curve_2d(ax, g)
            ax.text(i * 1.0 - 0.5, -0.6, f"|ψ⟩_{i}", color='white', ha='center')
        
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-1, 1)
        ax.axis('off')
    
    def _draw_qec_syndrome(self, ax):
        centers = [(-1.0, 0.3), (0, 0.3), (1.0, 0.3)]
        states = [0, 1, 0]
        
        for center, state in zip(centers, states):
            g = KececiCurveGenerator(num_children=4, max_level=2, scale_factor=0.18, base_radius=0.15,
                                     child_ordering=ChildOrdering.SPIRAL_INWARD if state == 1 else ChildOrdering.SPIRAL_OUTWARD,
                                     color_by_angle=True,
                                     line_color='red' if state == 1 else 'lime', line_width=1.5)
            g.generate_curve(center=center)
            self._draw_curve_2d(ax, g)
            if state == 1:
                ax.add_patch(Circle(center, 0.25, fill=False, edgecolor='red', linewidth=2, linestyle='--'))
        
        syn = [(-0.5, -0.3), (0.5, -0.3)]
        for i, c in enumerate(syn):
            g = KececiCurveGenerator(num_children=3, max_level=2, scale_factor=0.15, base_radius=0.1,
                                     color_by_angle=True, line_color='yellow', line_width=1.0)
            g.generate_curve(center=c)
            self._draw_curve_2d(ax, g)
            ax.text(c[0], c[1] - 0.35, f"S_{i}", color='white', ha='center')
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-0.8, 0.8)
        ax.axis('off')
    
    def _draw_qec_correction(self, ax):
        for i in range(3):
            g = KececiCurveGenerator(num_children=5, max_level=3, scale_factor=0.2, base_radius=0.18,
                                     child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                                     color_by_angle=True, line_color='lime', line_width=1.5)
            g.generate_curve(center=(i * 1.0 - 1.0, 0))
            self._draw_curve_2d(ax, g)
            ax.add_patch(Circle((i * 1.0 - 1.0, 0), 0.25, fill=False, edgecolor='lime', linewidth=2))
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-0.6, 0.6)
        ax.axis('off')
    
    def _draw_phase_flip_code(self, ax):
        for i in range(3):
            g = KececiCurveGenerator(num_children=6, max_level=3, scale_factor=0.22, base_radius=0.2,
                                     angle_offset=i*np.pi/3, color_by_angle=True,
                                     line_color=plt.cm.plasma(i/3), line_width=1.2)
            x = i * 1.0 - 1.0
            g.generate_curve(center=(x, 0))
            self._draw_curve_2d(ax, g)
            ax.text(x, -0.55, f"|+⟩_{i}", color='white', ha='center')
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-0.8, 0.8)
        ax.axis('off')
    
    def _draw_shor_code(self, ax):
        for i in range(3):
            for j in range(3):
                x, y = (j - 1) * 0.9, (i - 1) * 0.9
                g = KececiCurveGenerator(num_children=4, max_level=2, scale_factor=0.15, base_radius=0.1,
                                         color_by_angle=True, line_color='cyan', line_width=1.0, alpha=0.7)
                g.generate_curve(center=(x, y))
                self._draw_curve_2d(ax, g)
        
        for i in range(3):
            y = (i - 1) * 0.9
            ax.add_patch(Rectangle((-1.35, y-0.3), 2.7, 0.6, fill=False, edgecolor='yellow', linewidth=1, alpha=0.5))
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.8, 1.8)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_error_rate_plot(self, ax):
        p = np.linspace(0, 0.5, 100)
        p_uncoded = p
        p_3qubit = 3 * p**2 * (1 - p) + p**3
        
        ax.plot(p, p_uncoded, 'red', linewidth=2, label='Uncoded')
        ax.plot(p, p_3qubit, 'yellow', linewidth=2, label='3-Qubit Code')
        ax.axvline(x=0.1, color='white', linestyle='--', alpha=0.5)
        
        ax.set_xlabel("Physical Error Rate", color='white')
        ax.set_ylabel("Logical Error Rate", color='white')
        ax.legend()
        ax.tick_params(colors='white')
        ax.set_facecolor('#0a0a1a')
        ax.grid(True, alpha=0.2)
        
# ============================================================================
# KUANTUM DURUMLARI GÖRSELLEŞTİRME
# ============================================================================

class QuantumKececiCurve:
    """Kuantum durumlarını Keçeci Eğrileri ile görselleştirir"""
    
    def __init__(self):
        self.figures = []
    
    def _draw_curve(self, ax, generator, label: str = ""):
        """Eğriyi çiz"""
        sorted_points = sorted(generator.all_points, key=lambda p: (p[1], p[2]))
        
        if len(sorted_points) > 1:
            x_coords = [p[0][0] for p in sorted_points]
            y_coords = [p[0][1] for p in sorted_points]
            
            if generator.color_by_level or generator.color_by_angle:
                for i in range(len(x_coords) - 1):
                    color = generator._get_color_for_segment(
                        sorted_points[i][1], 
                        sorted_points[i][2]
                    )
                    ax.plot(x_coords[i:i+2], y_coords[i:i+2],
                           generator.line_style, linewidth=generator.line_width,
                           color=color, alpha=generator.alpha)
            else:
                ax.plot(x_coords, y_coords, generator.line_style,
                       linewidth=generator.line_width,
                       color=generator.line_color, alpha=generator.alpha)
        
        if generator.show_points:
            for point, level, angle in generator.all_points:
                if level == generator.max_level:
                    color = 'red'
                else:
                    color = generator.line_color or 'white'
                ax.plot(point[0], point[1], 'o', 
                       markersize=generator.point_size, color=color, alpha=0.6)
        
        if label:
            ax.text(0.02, 0.98, label, transform=ax.transAxes,
                   color='white', fontsize=10, verticalalignment='top')
    
    def create_superposition_state(self, num_states: int = 3):
        """Süperpozisyon durumu"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.patch.set_facecolor('#0a0a1a')
        
        colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00']
        
        for state_idx in range(min(num_states, 3)):
            ax = axes[state_idx]
            ax.set_facecolor('#0a0a1a')
            
            generator = KececiCurveGenerator(
                num_children=6 + state_idx * 2,
                max_level=4,
                scale_factor=0.45,
                base_radius=3.5,
                child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                growth_direction=GrowthDirection.OUTWARD,
                angle_offset=state_idx * np.pi/4,
                angle_variation=0.15,
                connection_mode=ConnectionMode.SPIRAL,
                color_by_angle=True,
                line_color=colors[state_idx],
                line_width=1.2,
                show_points=True,
                background_color='#0a0a1a'
            )
            
            generator.generate_curve()
            self._draw_curve(ax, generator, f"|ψ_{state_idx}⟩")
            ax.set_title(f"Durum {state_idx}", color='white')
            ax.set_aspect('equal')
            ax.axis('off')
        
        # Birleşik görünüm
        ax = axes[2]
        ax.clear()
        ax.set_facecolor('#0a0a1a')
        
        for state_idx in range(num_states):
            generator = KececiCurveGenerator(
                num_children=6 + state_idx * 2,
                max_level=4,
                scale_factor=0.45,
                base_radius=3.5,
                angle_offset=state_idx * np.pi/4,
                color_by_angle=True,
                line_color=colors[state_idx],
                line_width=1.0,
                alpha=0.5,
                show_points=False
            )
            generator.generate_curve()
            sorted_points = sorted(generator.all_points, key=lambda p: (p[1], p[2]))
            if len(sorted_points) > 1:
                x = [p[0][0] for p in sorted_points]
                y = [p[0][1] for p in sorted_points]
                ax.plot(x, y, '-', color=colors[state_idx], linewidth=1.0, alpha=0.5)
        
        ax.set_title("|Ψ⟩ = Σ cᵢ|ψᵢ⟩", color='white', fontsize=14)
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.suptitle("Kuantum Süperpozisyon", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def create_entanglement_state(self):
        """Dolanıklık durumu - Bell durumları"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.patch.set_facecolor('#0a0a1a')
        
        bell_states = [
            ("Φ⁺", 0, "#ff4444", "#4444ff"),
            ("Φ⁻", np.pi, "#ff8844", "#4488ff"),
            ("Ψ⁺", np.pi/2, "#44ff44", "#ff44ff"),
            ("Ψ⁻", 3*np.pi/2, "#ffff44", "#44ffff")
        ]
        
        for idx, (name, phase, color1, color2) in enumerate(bell_states):
            ax = axes[idx // 2, idx % 2]
            ax.set_facecolor('#0a0a1a')
            
            for particle, color in enumerate([color1, color2]):
                generator = KececiCurveGenerator(
                    num_children=8,
                    max_level=3,
                    scale_factor=0.4,
                    base_radius=2.5,
                    child_ordering=ChildOrdering.ALTERNATING if particle == 0 else ChildOrdering.SPIRAL_OUTWARD,
                    growth_direction=GrowthDirection.TANGENT,
                    angle_offset=phase if particle == 0 else phase + np.pi/2,
                    connection_mode=ConnectionMode.STAR_BURST,
                    color_by_angle=True,
                    line_color=color,
                    line_width=1.2,
                    show_points=True,
                    background_color='#0a0a1a'
                )
                
                generator.generate_curve(center=(particle * 1.5 - 0.75, 0))
                self._draw_curve(ax, generator)
            
            # Dolanıklık bağı
            ax.plot([-0.75, 0.75], [0, 0], '--', color='yellow', alpha=0.5, linewidth=1.5)
            ax.text(0, 0.3, "⌿", color='yellow', fontsize=20, ha='center', alpha=0.7)
            
            ax.set_title(f"Bell: {name}", color='white', fontsize=12)
            ax.set_xlim(-4, 4)
            ax.set_ylim(-3, 3)
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Kuantum Dolanıklık - Bell Durumları", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def create_coherence_decoherence(self):
        """Koherens → Dekoherens geçişi"""
        fig, axes = plt.subplots(1, 4, figsize=(20, 5))
        fig.patch.set_facecolor('#0a0a1a')
        
        coherence_levels = [1.0, 0.7, 0.4, 0.1]
        times = [0, 0.5, 1.0, 1.5]
        
        for idx, (coherence, t) in enumerate(zip(coherence_levels, times)):
            ax = axes[idx]
            ax.set_facecolor('#0a0a1a')
            
            generator = KececiCurveGenerator(
                num_children=7,
                max_level=4,
                scale_factor=0.4,
                base_radius=3.0,
                child_ordering=ChildOrdering.SEQUENTIAL,
                growth_direction=GrowthDirection.OUTWARD,
                angle_variation=0.1 * coherence,
                perturbation=0.15 * (1 - coherence),
                connection_mode=ConnectionMode.CONTINUOUS,
                color_by_level=True,
                color_saturation=coherence,
                line_width=1.5 * coherence + 0.3,
                show_points=True,
                background_color='#0a0a1a'
            )
            
            generator.generate_curve()
            self._draw_curve(ax, generator)
            
            state = "Koherent" if coherence > 0.7 else "Kısmi" if coherence > 0.3 else "Dekoberent"
            ax.set_title(f"{state}\nt={t:.1f}τ, C={coherence:.2f}", color='white')
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Kuantum Koherens → Dekoherens", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def create_quantum_tunneling(self):
        """Kuantum tünelleme"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.patch.set_facecolor('#0a0a1a')
        
        scenarios = [
            (0.3, 1.0, "Düşük Enerji"),
            (0.7, 1.0, "Rezonans"),
            (1.2, 1.0, "Bariyer Üstü")
        ]
        
        for idx, (energy, barrier, name) in enumerate(scenarios):
            ax = axes[idx]
            ax.set_facecolor('#0a0a1a')
            
            transmission = 1.0 if energy >= barrier else np.exp(-2 * np.sqrt(barrier - energy))
            
            generator = KececiCurveGenerator(
                num_children=6,
                max_level=4,
                scale_factor=0.4,
                base_radius=3.0,
                child_ordering=ChildOrdering.SPIRAL_OUTWARD,
                growth_direction=GrowthDirection.OVERLAPPING,
                angle_variation=0.2 * transmission,
                perturbation=0.05 / (transmission + 0.1),
                connection_mode=ConnectionMode.SPIRAL,
                color_by_angle=True,
                line_width=1.0 + transmission,
                show_points=True,
                background_color='#0a0a1a'
            )
            
            generator.generate_curve()
            self._draw_curve(ax, generator, f"T = {transmission:.3f}")
            
            # Bariyer
            barrier_x = [-1, -1, 1, 1]
            barrier_y = [0, barrier, barrier, 0]
            ax.fill(barrier_x, barrier_y, color='red', alpha=0.2)
            ax.plot(barrier_x, barrier_y, 'r-', linewidth=2, alpha=0.5)
            
            ax.set_title(f"{name}\nE={energy:.1f}, V₀={barrier:.1f}", color='white')
            ax.set_xlim(-3.5, 3.5)
            ax.set_ylim(-3, 3.5)
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Kuantum Tünelleme", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def create_interference_pattern(self):
        """Girişim deseni"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.patch.set_facecolor('#0a0a1a')
        
        slit_counts = [1, 2, 3, 4]
        
        for idx, n_slits in enumerate(slit_counts):
            ax = axes[idx // 2, idx % 2]
            ax.set_facecolor('#0a0a1a')
            
            for slit in range(n_slits):
                generator = KececiCurveGenerator(
                    num_children=8,
                    max_level=3,
                    scale_factor=0.35,
                    base_radius=2.5,
                    child_ordering=ChildOrdering.ALTERNATING,
                    growth_direction=GrowthDirection.OUTWARD,
                    angle_offset=2 * np.pi * slit / n_slits,
                    connection_mode=ConnectionMode.CONTINUOUS,
                    color_by_angle=True,
                    line_width=0.8,
                    alpha=0.4,
                    show_points=False,
                    background_color='#0a0a1a'
                )
                
                slit_pos = (slit - (n_slits-1)/2) * 1.5
                generator.generate_curve(center=(slit_pos, 0))
                
                sorted_points = sorted(generator.all_points, key=lambda p: (p[1], p[2]))
                if len(sorted_points) > 1:
                    x = [p[0][0] for p in sorted_points]
                    y = [p[0][1] for p in sorted_points]
                    color = plt.cm.hsv(slit / n_slits)
                    ax.plot(x, y, '-', color=color, linewidth=0.8, alpha=0.5)
            
            ax.set_title(f"{n_slits}-Yarık Girişimi", color='white', fontsize=12)
            ax.set_xlim(-5, 5)
            ax.set_ylim(-3, 4)
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Kuantum Girişim Desenleri", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)
    
    def create_wave_function_collapse(self):
        """Dalga fonksiyonu çöküşü"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.patch.set_facecolor('#0a0a1a')
        
        stages = ["Süperpozisyon", "Ölçüm", "Çöküş"]
        
        for idx, stage in enumerate(stages):
            ax = axes[idx]
            ax.set_facecolor('#0a0a1a')
            
            if stage == "Süperpozisyon":
                for state in range(3):
                    generator = KececiCurveGenerator(
                        num_children=6,
                        max_level=4,
                        scale_factor=0.4,
                        base_radius=3.0,
                        angle_offset=state * 2*np.pi/3,
                        color_by_angle=True,
                        line_width=1.0,
                        alpha=0.5,
                        show_points=False,
                        background_color='#0a0a1a'
                    )
                    generator.generate_curve()
                    self._draw_curve(ax, generator)
                    
            elif stage == "Ölçüm":
                generator = KececiCurveGenerator(
                    num_children=8,
                    max_level=4,
                    scale_factor=0.4,
                    base_radius=3.0,
                    child_ordering=ChildOrdering.RANDOM,
                    perturbation=0.2,
                    color_by_level=True,
                    line_width=1.5,
                    show_points=True,
                    background_color='#0a0a1a',
                    random_seed=42
                )
                generator.generate_curve()
                self._draw_curve(ax, generator)
                
                circle = Circle((0, 0), 3.5, fill=False, edgecolor='yellow', 
                              linewidth=2, linestyle='--', alpha=0.5)
                ax.add_patch(circle)
                
            else:
                generator = KececiCurveGenerator(
                    num_children=7,
                    max_level=4,
                    scale_factor=0.45,
                    base_radius=3.0,
                    child_ordering=ChildOrdering.SEQUENTIAL,
                    growth_direction=GrowthDirection.OUTWARD,
                    color_by_angle=True,
                    line_width=2.0,
                    show_points=True,
                    point_size=2.0,
                    background_color='#0a0a1a'
                )
                generator.generate_curve()
                self._draw_curve(ax, generator, "|Z⟩")
            
            ax.set_title(stage, color='white', fontsize=14)
            ax.set_xlim(-4, 4)
            ax.set_ylim(-4, 4)
            ax.set_aspect('equal')
            ax.axis('off')
        
        plt.suptitle("Dalga Fonksiyonu Çöküşü", color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()
        self.figures.append(fig)

def create_kececi_curve_gallery():
    """
    Farklı parametre kombinasyonları ile özgün Keçeci Eğrileri galerisi oluştur
    """
    
    # Farklı konfigürasyonlar - her biri tamamen özgün bir eğri
    configurations = [
        {
            "name": "Klasik Keçeci",
            "params": {
                "num_children": 6,
                "max_level": 4,
                "child_ordering": ChildOrdering.SEQUENTIAL,
                "growth_direction": GrowthDirection.INWARD,
                "connection_mode": ConnectionMode.CONTINUOUS,
            }
        },
        {
            "name": "Alternatif Spiral",
            "params": {
                "num_children": 8,
                "max_level": 3,
                "child_ordering": ChildOrdering.ALTERNATING,
                "growth_direction": GrowthDirection.OUTWARD,
                "connection_mode": ConnectionMode.SPIRAL,
                "angle_variation": 0.3,
            }
        },
        {
            "name": "Kuantum Dolanıklık",
            "params": {
                "num_children": 5,
                "max_level": 4,
                "child_ordering": ChildOrdering.RANDOM,
                "growth_direction": GrowthDirection.TANGENT,
                "connection_mode": ConnectionMode.STAR_BURST,
                "perturbation": 0.1,
                "color_by_level": True,
                "random_seed": 42,
            }
        },
        {
            "name": "Galaktik Sarmal",
            "params": {
                "num_children": 12,
                "max_level": 3,
                "child_ordering": ChildOrdering.SPIRAL_OUTWARD,
                "growth_direction": GrowthDirection.OUTWARD,
                "connection_mode": ConnectionMode.SPIRAL,
                "angle_offset": np.pi / 6,
                "angle_variation": 0.2,
                "radial_variation": 0.15,
                "color_by_angle": True,
            }
        },
        {
            "name": "Kaotik Fraktal",
            "params": {
                "num_children": 7,
                "max_level": 4,
                "child_ordering": ChildOrdering.QUADRANT,
                "growth_direction": GrowthDirection.OVERLAPPING,
                "connection_mode": ConnectionMode.ZIGZAG,
                "perturbation": 0.15,
                "level_dependent_children": True,
                "color_by_level": True,
            }
        },
        {
            "name": "Kristal Kafes",
            "params": {
                "num_children": 4,
                "max_level": 5,
                "child_ordering": ChildOrdering.REVERSE_ALTERNATING,
                "growth_direction": GrowthDirection.TANGENT,
                "connection_mode": ConnectionMode.LEVEL_WISE,
                "scale_factor": 0.4,
                "color_by_level": True,
                "line_style": "--",
            }
        },
        {
            "name": "Nöral Ağ",
            "params": {
                "num_children": 9,
                "max_level": 3,
                "child_ordering": ChildOrdering.ANGLE_BASED,
                "growth_direction": GrowthDirection.OUTWARD,
                "connection_mode": ConnectionMode.STAR_BURST,
                "angle_variation": 0.5,
                "radial_variation": 0.2,
                "color_by_angle": True,
                "line_width": 0.5,
            }
        },
        {
            "name": "Çiçek Deseni",
            "params": {
                "num_children": 6,
                "max_level": 4,
                "child_ordering": ChildOrdering.SPIRAL_INWARD,
                "growth_direction": GrowthDirection.OVERLAPPING,
                "connection_mode": ConnectionMode.CONTINUOUS,
                "angle_offset": np.pi / 4,
                "scale_factor": 0.6,
                "color_by_level": True,
                "color_saturation": 0.8,
            }
        },
    ]
    
    # Galeriyi oluştur
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for idx, config in enumerate(configurations):
        if idx < len(axes):
            generator = KececiCurveGenerator(**config["params"])
            generator.generate_curve()
            
            ax = axes[idx]
            ax.set_facecolor('black')
            
            # Eğriyi çiz (görselleştirme fonksiyonunu manuel olarak uygula)
            sorted_points = sorted(generator.all_points, key=lambda p: (p[1], p[2]))
            if len(sorted_points) > 1:
                x_coords = [p[0][0] for p in sorted_points]
                y_coords = [p[0][1] for p in sorted_points]
                
                if generator.color_by_level or generator.color_by_angle:
                    for i in range(len(x_coords) - 1):
                        color = generator._get_color_for_segment(
                            sorted_points[i][1], 
                            sorted_points[i][2]
                        )
                        ax.plot(
                            x_coords[i:i+2], y_coords[i:i+2],
                            generator.line_style, 
                            linewidth=generator.line_width,
                            color=color, alpha=0.8
                        )
                else:
                    ax.plot(
                        x_coords, y_coords,
                        generator.line_style, 
                        linewidth=generator.line_width,
                        color=generator.line_color, alpha=0.8
                    )
            
            if generator.show_points:
                for point, level, angle in generator.all_points:
                    if generator.color_by_level:
                        color = generator._get_color_for_segment(level, angle)
                    else:
                        color = 'red' if level == generator.max_level else 'white'
                    ax.plot(point[0], point[1], 'o', markersize=1, color=color, alpha=0.6)
            
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')
            ax.set_title(config["name"], color='white', fontsize=10)
            
            max_extent = generator.base_radius * (1 + 2 * generator.scale_factor * generator.max_level) * 1.1
            ax.set_xlim(-max_extent, max_extent)
            ax.set_ylim(-max_extent, max_extent)
    
    plt.suptitle("Keçeci Curve Ailesi - Parametrik Özgün Eğriler", 
                 color='white', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.show()


# Özel sıralama fonksiyonu örneği
def custom_fibonacci_ordering(children: List[Tuple[float, float, float]], level: int) -> List:
    """
    Özel sıralama: Fibonacci benzeri bir desen
    """
    n = len(children)
    if n <= 2:
        return children
    
    # Fibonacci benzeri indeks sıralaması
    order = []
    a, b = 0, 1
    for _ in range(n):
        order.append(a % n)
        a, b = b, (a + b) % n
    
    # Benzersiz indeksleri al
    seen = set()
    unique_order = []
    for idx in order:
        if idx not in seen:
            unique_order.append(idx)
            seen.add(idx)
    
    return [children[i] for i in unique_order]

def show_menu():
    """Tam menü göster"""
    print("\n" + "=" * 60)
    ...


if __name__ == "__main__":
    ...
