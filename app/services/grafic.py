import matplotlib.pyplot as plt
import io
import pandas as pd


def graficBarras(fechas_lista, num):
    """
    Genera un gráfico de barras con la frecuencia de aparición de un número
    por mes. Devuelve la imagen en un buffer de memoria (BytesIO).
    """
    if not fechas_lista:
        raise ValueError("No hay datos disponibles para generar el gráfico.")

    # 📌 Convertir fechas a DataFrame
    df_fechas = pd.DataFrame(fechas_lista, columns=["fecha"])
    df_fechas["fecha"] = pd.to_datetime(df_fechas["fecha"], errors="coerce")
    df_fechas = df_fechas.dropna(subset=["fecha"])  # Eliminar fechas inválidas

    if df_fechas.empty:
        raise ValueError("No hay fechas válidas después del procesamiento.")

    # 📌 Crear columna Año-Mes en formato "YYYY-MM" para asegurar orden correcto
    df_fechas["año_mes"] = df_fechas["fecha"].dt.strftime("%Y-%m")

    # 📌 Contar frecuencia de cada mes
    conteo_mensual = df_fechas["año_mes"].value_counts().reset_index()
    conteo_mensual.columns = ["año_mes", "frecuencia"]
    conteo_mensual = conteo_mensual.sort_values("año_mes")

    # 📌 Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(
        conteo_mensual["año_mes"],
        conteo_mensual["frecuencia"],
        color="skyblue",
        edgecolor="black"
    )

    ax.set_title(f"Frecuencia del número {num} por Mes")
    ax.set_xlabel("Mes y Año")
    ax.set_ylabel("Frecuencia")

    # 📌 Mejorar formato del eje X
    ax.set_xticks(range(len(conteo_mensual["año_mes"])))
    ax.set_xticklabels(conteo_mensual["año_mes"], rotation=45, ha="right")

    # 📌 Ajustar diseño para evitar cortes de texto
    plt.tight_layout()

    # 📌 Guardar imagen en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return buf
