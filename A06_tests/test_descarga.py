import sys
import os

# Agregamos el path al archivo utils.py
sys.path.append(os.path.abspath("01_source/01_1_download"))

from utils import obtener_fecha_ayer, generar_url_api, esta_en_la_palma, es_de_noche

def test_obtener_fecha_ayer():
    y, d = obtener_fecha_ayer()
    assert len(y) == 4 and y.isdigit()
    assert len(d) == 3 and d.isdigit()

def test_generar_url_api():
    url = generar_url_api("VNP02IMG", "2024", "091")
    assert "VNP02IMG" in url and "2024" in url and "091" in url
    assert url.startswith("https://")

def test_esta_en_la_palma_true():
    assert esta_en_la_palma(28.60, 28.63, -17.87, -17.92)

def test_esta_en_la_palma_false():
    assert not esta_en_la_palma(10.0, 10.1, -10.1, -10.0)

def test_es_de_noche():
    assert es_de_noche("Night")
    assert not es_de_noche("Day")