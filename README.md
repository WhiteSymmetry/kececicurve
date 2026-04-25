# Keçeci Curve (kececicurve, Keçeci Eğrisi)

## Keçeci Curve (kececicurve, Keçeci Eğrisi) <img src="https://github.com/WhiteSymmetry/kececicurve/blob/main/docs/logo.jpg" alt="Keçeci Curve (kececicurve, Keçeci Eğrisi)" align="right" height="140"/>

[![PyPI version](https://badge.fury.io/py/kececicurve.svg)](https://badge.fury.io/py/kececicurve/)
[![License: AGPL](https://img.shields.io/badge/License-AGPL-yellow.svg)](https://opensource.org/licenses/AGPL)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19696338.svg)](https://doi.org/10.5281/zenodo.19696338)
[![WorkflowHub DOI](https://img.shields.io/badge/DOI-10.48546%2Fworkflowhub.datafile.***-blue)](https://doi.org/10.48546/workflowhub.datafile.***)
[![figshare DOI](https://img.shields.io/badge/DOI-10.6084/m9.figshare.***-blue)](https://doi.org/10.6084/m9.figshare.***)

[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececicurve/badges/version.svg)](https://anaconda.org/bilgi/kececicurve)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececicurve/badges/latest_release_date.svg)](https://anaconda.org/bilgi/kececicurve)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececicurve/badges/platforms.svg)](https://anaconda.org/bilgi/kececicurve)
[![Anaconda-Server Badge](https://anaconda.org/bilgi/kececicurve/badges/license.svg)](https://anaconda.org/bilgi/kececicurve)

[![Open Source](https://img.shields.io/badge/Open%20Source-Open%20Source-brightgreen.svg)](https://opensource.org/)
[![Documentation Status](https://app.readthedocs.org/projects/kececicurve/badge/?0.2.0=main)](https://kececicurve.readthedocs.io/en/latest)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/10536/badge)](https://www.bestpractices.dev/projects/10536)

[![Python CI](https://github.com/WhiteSymmetry/kececicurve/actions/workflows/python_ci.yml/badge.svg?branch=main)](https://github.com/WhiteSymmetry/kececicurve/actions/workflows/python_ci.yml)
[![codecov](https://codecov.io/gh/WhiteSymmetry/kececicurve/graph/badge.svg?token=0X78S7TL0W)](https://codecov.io/gh/WhiteSymmetry/kececicurve)
[![Documentation Status](https://readthedocs.org/projects/kececicurve/badge/?version=latest)](https://kececicurve.readthedocs.io/en/latest/)
[![Binder](https://terrarium.evidencepub.io/badge_logo.svg)](https://terrarium.evidencepub.io/v2/gh/WhiteSymmetry/kececicurve/HEAD)

[![PyPI version](https://badge.fury.io/py/kececicurve.svg)](https://badge.fury.io/py/kececicurve)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Linted with Ruff](https://img.shields.io/badge/Linted%20with-Ruff-green?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)
[![Lang:Python](https://img.shields.io/badge/Lang-Python-blue?style=flat-square&logo=python)](https://python.org/)

[![PyPI Downloads](https://static.pepy.tech/badge/kececicurve)](https://pepy.tech/projects/kececicurve)
![PyPI Downloads](https://img.shields.io/pypi/dm/kececicurve?logo=pypi&label=PyPi%20downloads)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/kececicurve?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/kececicurve)

---

<p align="left">
    <table>
        <tr>
            <td style="text-align: center;">PyPI</td>
            <td style="text-align: center;">
                <a href="https://pypi.org/project/kececicurve/">
                    <img src="https://badge.fury.io/py/kececicurve.svg" alt="PyPI version" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">Conda</td>
            <td style="text-align: center;">
                <a href="https://anaconda.org/bilgi/kececicurve">
                    <img src="https://anaconda.org/bilgi/kececicurve/badges/version.svg" alt="conda-forge version" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">DOI</td>
            <td style="text-align: center;">
                <a href="https://doi.org/10.5281/zenodo.***">
                    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.***.svg" alt="DOI" height="18"/>
                </a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center;">License: AGPL</td>
            <td style="text-align: center;">
                <a href="https://opensource.org/licenses/AGPL">
                    <img src="https://img.shields.io/badge/License-AGPL-yellow.svg" alt="License" height="18"/>
                </a>
            </td>
        </tr>
    </table>
</p>

---

# 🌿 Keçeci Curve (kececicurve: Keçeci Eğrisi)  – Parametric Space-Filling Curve Family

**Keçeci Eğrisi**, uzay doldurma eğrileri ailesine yeni, tamamen özgün ve son derece esnek bir üyedir.  
Dairesel geometri, ayarlanabilir çocuk sayısı, büyüme yönü, sıralama stratejileri ve açı varyasyonları ile **klasik eğrilerin ötesine geçen** parametrik bir fraktal eğri üretecidir.

Bu depo aynı zamanda Hilbert, Morton, Moore ve Sierpinski eğrilerini de içerir; lokalite (yerellik) karşılaştırmaları, süreklilik analizleri ve **ileri kuantum fenomenlerinin (Majorana, Weyl, topolojik yarımetaller, Stratum modeli)** 2B/3B görselleştirmelerini sunar.

![Keçeci Curve Gallery](https://...)

---

## ✨ Öne Çıkan Özellikler

- **🎛️ Tamamen Parametrik Üretim**
  - Çocuk sayısı (`num_children`): 2'den 20'ye kadar istenen simetri.
  - Büyüme modları: `inward`, `outward`, `tangent`, `overlapping`.
  - Sıralama stratejileri: Sıralı, alternatif, spiral, rastgele, çeyrek tabanlı...
  - Açı ofseti ve varyasyonu ile dinamik şekil kontrolü.

- **📊 Yerleşik Karşılaştırma Araçları**
  - Lokalite ısı haritaları (Hilbert, Morton, Moore, Sierpinski ve Keçeci).
  - Radar grafikler ile çok boyutlu metrik karşılaştırması.
  - Başlangıç‑bitiş ilişkisi ve süreklilik görselleştirmeleri.

- **🔬 İleri Kuantum Görselleştirmeleri**
  - Majorana sıfır modları, örgü (braiding) ve topolojik faz diyagramları.
  - Weyl konileri, Fermi yayları, Berry eğriliği.
  - Stratum Modeli: Hibrit kuantum mimarisi (süperiletken + Majorana + fotonik).
  - 3B Wigner fonksiyonları, dolanıklık ağları, adiabatik evrim.
  - Shor, Grover, Deutsch‑Jozsa algoritmalarının eğri tabanlı animasyonları.

- **🌌 Zengin Desen Kütüphanesi**
  - Çiçek desenleri, galaksi sarmalları, kar taneleri, mandalalar, fraktal ağaçlar, deniz canlıları, sinir ağları, virüs kapsidleri ve kozmik ağ.

- **🧩 Klasik Eğriler Desteği**
  - Hilbert, Morton (Z‑order), Moore, Sierpinski, Peano eğrileri saf Python ile implemente edilmiştir.

- **⚡ Optimize Edilmiş Performans**
  - Sonuçları önbelleğe alan `KececiCurve` sınıfı sayesinde tekrarlı üretimlerde hız.

### Kullanım Alanları Karşılaştırması/Usage Area Comparison

| Kullanım Alanı/Usage Area                              | Keçeci    | Hilbert      | Morton      | Peano      | Moore       | Sierpinski  |
|------------------------------------|-------------------------------|--------------|-------------|------------|-------------|-------------|
| Veritabanı İndeksleme/Database Indexing                | ⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐⭐⭐⭐  | ⭐⭐        |
| Görüntü İşleme/Image Processing                        | ⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  | ⭐⭐        |
| Kuantum Görselleştirme/Quantum Visualization           | ⭐⭐⭐⭐⭐| ⭐⭐         | ⭐⭐        | ⭐⭐       | ⭐⭐        | ⭐⭐        |
| Prosedürel İçerik Üretimi/Procedural Content Generation| ⭐⭐⭐⭐⭐| ⭐⭐⭐       | ⭐⭐⭐      | ⭐⭐⭐     | ⭐⭐⭐      | ⭐⭐⭐      |
| Bilimsel Simülasyon/Scientific Simulation              | ⭐⭐⭐⭐⭐| ⭐⭐⭐       | ⭐⭐⭐      | ⭐⭐⭐     | ⭐⭐⭐      | ⭐⭐⭐      |
| Sanat ve Tasarım/Art & Design                          | ⭐⭐⭐⭐⭐| ⭐⭐         | ⭐          | ⭐⭐       | ⭐⭐         | ⭐⭐⭐⭐⭐ |
| Kriptografi/Cryptography                               | ⭐⭐⭐⭐  | ⭐⭐⭐       | ⭐⭐⭐      | ⭐⭐⭐     | ⭐⭐⭐       | ⭐⭐       |
| Yol Bulma/Pathfinding                                  | ⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐    | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐   | ⭐⭐       |
| Eğitim ve Görselleştirme/Education & Visualization     | ⭐⭐⭐⭐⭐| ⭐⭐⭐⭐     | ⭐⭐⭐      | ⭐⭐⭐⭐   | ⭐⭐⭐⭐     | ⭐⭐⭐⭐   |
| Harita ve CBS/GIS/Spatial Mapping                      | ⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     | ⭐⭐⭐⭐⭐   | ⭐         |

---

## 📦 Kurulum

```bash
git clone https://github.com/WhiteSymmetry/kececicurve.git
cd kececicurve
pip install -e .
```

Gereksinimler:
- Python 3.8+
- NumPy
- Matplotlib

İsterseniz bağımlılıkları manuel de kurabilirsiniz:
```bash
pip install numpy matplotlib
```

---

## 🚀 Hızlı Başlangıç

### Temel Kullanım

```python
import numpy as np
from kececicurve import KececiCurve, quick_plot

# 5 çocuklu, 3 seviyeli bir Keçeci eğrisi oluştur
curve = KececiCurve(num_children=5, max_level=3, growth_mode='outward')
points = curve.generate()  # (x, y) noktalarının listesi

# Hızlı çizim
import matplotlib.pyplot as plt
pts = np.array(points)
plt.plot(pts[:,0], pts[:,1], '-')
plt.axis('equal')
plt.show()
```

### Menü ile Tüm Görselleştirmelere Erişim

```python
from kececicurve import show_menu
show_menu()
```

Bu interaktif menü, **çiçek desenlerinden kuantum algoritmalarına** kadar 30'dan fazla görselleştirme seçeneği sunar.


======================================================================
               KEÇECİ CURVE GÖRSELLEŞTİRME MENÜSÜ
======================================================================

  DESEN GALERİLERİ / PATTERN GALLERIES
  --------------------------------------------------------------------
   1. Flower Patterns / Çiçek Desenleri
   2. Galaxy Patterns / Galaksi Desenleri
   3. Snowflake Patterns / Kar Taneleri
   4. Mandala Patterns / Mandala Desenleri
   5. Fractal Trees / Fraktal Ağaçlar
   6. Marine Patterns / Deniz Canlıları
   7. Cosmic Web / Kozmik Ağ
   8. Neural Network Patterns / Sinir Ağı Desenleri
   9. Virus Patterns / Virüs Desenleri
  10. Keçeci Curve Gallery / Keçeci Eğri Galerisi

  EĞRİ KARŞILAŞTIRMALARI / CURVE COMPARISONS
  --------------------------------------------------------------------
  11. Locality Heatmap / Lokalite Isı Haritası
  12. Continuity Visualization / Süreklilik Görselleştirmesi
  13. Radar Chart Comparison / Radar Grafik Karşılaştırması
  14. Start-End Comparison / Başlangıç-Bitiş Karşılaştırması
  15. Comprehensive Comparison (Table) / Kapsamlı Karşılaştırma (Tablo)
  16. Locality Combined Score / Lokalite Birleşik Skoru
  17. Indexing Performance Comparison / Veri İndeksleme Karşılaştırması

  KUANTUM GÖRSELLEŞTİRMELERİ / QUANTUM VISUALIZATIONS
  --------------------------------------------------------------------
  18. Majorana Zero Modes / Majorana Sıfır Modları
  19. Weyl Semimetal / Weyl Yarımetali
  20. Stratum Architecture / Stratum Mimarisi
  21. 3D Wigner Function / 3B Wigner Fonksiyonu
  22. Entanglement Network 3D / Dolanıklık Ağı 3B
  23. Adiabatic Evolution 3D / Adiabatik Kuantum Evrimi 3B
  24. Topological Anyons 3D / Topolojik Anyonlar 3B
  25. QFT Spectrum 3D / Kuantum Fourier Dönüşümü 3B

  KUANTUM ALGORİTMALARI / QUANTUM ALGORITHMS
  --------------------------------------------------------------------
  26. Shor Algorithm / Shor Algoritması
  27. Grover Algorithm / Grover Algoritması
  28. Deutsch-Jozsa Algorithm / Deutsch-Jozsa Algoritması
  29. Quantum Error Correction / Kuantum Hata Düzeltme
  30. Bloch Sphere States / Bloch Küresi Durumları
  31. Superposition States / Süperpozisyon Durumları
  32. Entanglement (Bell States) / Dolanıklık (Bell Durumları)
  33. Coherence → Decoherence / Koherens → Dekoherens
  34. Quantum Tunneling / Kuantum Tünelleme
  35. Interference Patterns / Girişim Desenleri
  36. Wave Function Collapse / Dalga Fonksiyonu Çöküşü

  KEÇECİ PARAMETRE ETKİLERİ / KEÇECİ PARAMETER EFFECTS
  --------------------------------------------------------------------
  37. Effect of Child Count / Çocuk Sayısının Etkisi
  38. Effect of Growth Mode / Büyüme Modunun Etkisi
  39. Effect of Ordering Strategy / Sıralama Stratejisinin Etkisi
  40. Effect of Scale Factor / Ölçek Faktörünün Etkisi
  41. Effect of Angle Parameters / Açı Parametrelerinin Etkisi

  SİERPİNSKİ & PEANO ÖZEL / SIERPINSKI & PEANO SPECIALS
  --------------------------------------------------------------------
  42. Sierpinski Comparison / Sierpinski Karşılaştırması
  43. Sierpinski Curve / Sierpinski Eğrisi
  44. Sierpinski Process / Sierpinski Gelişimi
  45. Sierpinski Triangle / Sierpinski Üçgeni
  46. Sierpinski Test / Sierpinski Doğrulama Testi
  47. Peano Curve / Peano Eğrisi
  48. Peano Verification Test / Peano Doğrulama Testi

  EK KARŞILAŞTIRMA VE ANALİZLER / ADDITIONAL COMPARISONS & ANALYSES
  --------------------------------------------------------------------
  49. Curve Evolution by Level / Eğrilerin Seviyeye Göre Gelişimi
  50. Connectivity & Locality / Bağlantılılık ve Lokalite
  51. Keçeci Parametric Variations / Keçeci Parametrik Varyasyonları
  52. Detailed Radar Comparison / Detaylı Radar Karşılaştırması
  53. Locality Heatmap – Both Normalizations / Lokalite Isı Haritası – İki Normalizasyon

  --------------------------------------------------------------------
   0. Exit / Çıkış
======================================================================

Seçiminiz (0-53):


---

## 📚 Kullanım Örnekleri

### 1. Çiçek Desenleri Galerisi

```python
from kececicurve import flower_patterns
flower_patterns()
```

### 2. Lokalite Isı Haritası Karşılaştırması

```python
from kececicurve import locality_heatmap_comparison
locality_heatmap_comparison()
```

### 3. Majorana Fermiyonları Görselleştirmesi

```python
from kececicurve import MajoranaVisualizer
viz = MajoranaVisualizer()
viz.visualize_majorana_zero_modes()
```

### 4. Özel Parametrelerle Kendi Eğrinizi Yaratın

```python
from kececicurve import KececiCurveGenerator, ChildOrdering, GrowthDirection

gen = KececiCurveGenerator(
    num_children=7,
    max_level=4,
    scale_factor=0.42,
    child_ordering=ChildOrdering.SPIRAL_OUTWARD,
    growth_direction=GrowthDirection.TANGENT,
    angle_variation=0.2,
    color_by_angle=True
)
gen.generate_curve()

# Noktaları çiz
# ...
```

---

## 📁 Proje Yapısı

```
kececicurve/
├── kececicurve/__init__.py               # Paket dışa aktarımları
├── kececicurve/kececicurve.py            # Ana modül (tüm sınıflar ve fonksiyonlar)
├── README.md                 # Bu dosya
├── LICENSE                   # Lisans bilgisi
└── pyproject.toml            # Paket yapılandırması
```

---

## 📜 Lisans

Bu proje **AGPL3.0-or-later Lisansı** ile lisanslanmıştır.  
Ayrıntılar için [LICENSE](LICENSE) dosyasına bakınız.

---


**Keçeci Curve** – Fraktal geometriyi, veri bilimini ve kuantum fiziğini aynı çatı altında buluşturan bir araç.  



```

---

# Pixi:

[![Pixi](https://img.shields.io/badge/Pixi-Pixi-brightgreen.svg)](https://prefix.dev/channels/bilgi)

pixi init kececicurve

cd kececicurve

pixi workspace channel add [https://prefix.dev/channels/bilgi](https://prefix.dev/channels/bilgi) --prepend

✔ Added https://prefix.dev/channels/bilgi

pixi add kececicurve

✔ Added kececicurve >=...,<1

pixi install

pixi shell

pixi run python -c "import kececicurve; print(kececicurve.__version__)"

### Çıktı: 

pixi remove kececicurve

conda install -c https://prefix.dev/channels/bilgi kececicurve

pixi run python -c "import kececicurve; print(kececicurve.__version__)"

### Çıktı: 

pixi run pip list | grep kececicurve

### kececicurve  

pixi run pip show kececicurve

Name: kececicurve

Version: 

Summary: Keçeci Numbers: Keçeci Sayıları (Keçeci Conjecture)

Home-page: https://github.com/WhiteSymmetry/kececicurve

Author: Mehmet Keçeci

Author-email: Mehmet Keçeci <...>

License: GNU AFFERO GENERAL PUBLIC LICENSE

Copyright (c) 2025-2026 Mehmet Keçeci

----

1. https://pypi.org/project/kececicurve/
2. https://anaconda.org/bilgi/kececicurve
3. https://prefix.dev/channels/bilgi/packages/kececicurve

---

## License / Lisans

This project is licensed under the AGPL3.0 or Later License. See the `LICENSE` file for details.

## Citation

If this library was useful to you in your research, please cite us. Following the [GitHub citation standards](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files), here is the recommended citation.

### BibTeX

```bibtex
@misc{kececi_2026_19696338,
  author       = {Keçeci, Mehmet},
  title        = {kececicurve},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.19696338},
  url          = {https://doi.org/10.5281/zenodo.19696338},
}
```

### APA

```

Keçeci, M. (2026). kececicurve. Open Science Articles (OSAs), Zenodo. https://doi.org/10.5281/zenodo.19696338

