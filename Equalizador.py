from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def carregar_imagem_tif(arquivo):
    img = Image.open(arquivo).convert('L')
    pixels = np.array(img, dtype=int)
    return pixels

def calcular_histograma(pixels, L=256):
    histograma, _ = np.histogram(pixels, bins=L, range=(0, L))
    return histograma

def equalizar_histograma(histograma, L=256):
    total_pixels = sum(histograma) 
    probabilidades = histograma / total_pixels 
    cdf = np.cumsum(probabilidades)  
    novos_niveis = np.round((L - 1) * cdf).astype(int)

    histograma_equalizado = [0] * L
    for r, s in enumerate(novos_niveis):
        histograma_equalizado[s] += histograma[r]
    
    return novos_niveis, histograma_equalizado

def aplicar_equalizacao(pixels, novos_niveis):
    pixels_equalizados = np.array([novos_niveis[p] for p in pixels.flatten()])
    return pixels_equalizados.reshape(pixels.shape)

def processar_imagem(arquivo_entrada, arquivo_saida):
    pixels = carregar_imagem_tif(arquivo_entrada)
    histograma_original = calcular_histograma(pixels)
    novos_niveis, histograma_equalizado = equalizar_histograma(histograma_original)
    pixels_equalizados = aplicar_equalizacao(pixels, novos_niveis)
    img_equalizada = Image.fromarray(pixels_equalizados.astype(np.uint8))
    img_equalizada.save(arquivo_saida, format='TIFF')

    mostrar_histogramas(histograma_original, histograma_equalizado)

def mostrar_histogramas(histograma_original, histograma_equalizado):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(range(len(histograma_original)), histograma_original, color='gray', alpha=0.7)
    plt.title("Histograma da imagem original")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")

    plt.subplot(1, 2, 2)
    plt.bar(range(len(histograma_equalizado)), histograma_equalizado, color='gray', alpha=0.7)
    plt.title("Histograma equalizado")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")

    plt.tight_layout()
    plt.show()

arquivo_entrada = 'c:/Users/jukal/Desktop/HistogramaPDI/Entrada.tif'
arquivo_saida = 'c:/Users/jukal/Desktop/HistogramaPDI/Equalizado.tif'

processar_imagem(arquivo_entrada, arquivo_saida)
