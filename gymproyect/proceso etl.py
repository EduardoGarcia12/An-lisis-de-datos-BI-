import pandas as pd
import numpy as np
import os

# Sucios 
v_sucias = r"C:\Users\zabu\Desktop\gymproyect\ventas_gym_mexico_2026.csv"
s_sucios = r"C:\Users\zabu\Desktop\gymproyect\dim_socios_mexico.csv"
p_sucios = r"C:\Users\zabu\Desktop\gymproyect\dim_productos_mexico.csv"

# Limpios
v_limpios = r"C:\Users\zabu\Desktop\gymproyect\ventas_gym_mexico_2026_limpios.csv"
s_limpios = r"C:\Users\zabu\Desktop\gymproyect\dim_socios_mexico_limpios.csv"
p_limpios = r"C:\Users\zabu\Desktop\gymproyect\dim_productos_mexico_limpios.csv"


def proceso_etl(ruta_v, ruta_s, ruta_p, out_v, out_s, out_p):
    print("Iniciando proceso ETL...")
    
    try:
        #EXTRACCIÓN
        # Usamos encoding 'utf-8' para manejar caracteres de estados de México
        df1 = pd.read_csv(ruta_v, encoding='utf-8')
        df2 = pd.read_csv(ruta_s, encoding='utf-8')
        df3 = pd.read_csv(ruta_p, encoding='utf-8')

        #LIMPIAMOS
        
        #Eliminación de Duplicados reales (basado en IDs únicos)
        df1 = df1.drop_duplicates(subset=['ID_Transaccion'])
        df2 = df2.drop_duplicates(subset=['ID_Socio'])
        df3 = df3.drop_duplicates(subset=['ID_Producto'])

        #Limpieza y formato de Fechas
        df1['Fecha'] = pd.to_datetime(df1['Fecha'], errors='coerce')
        df2['Fecha_Inscripcion'] = pd.to_datetime(df2['Fecha_Inscripcion'], errors='coerce')

        #Validación de Tipos Numéricos
        df1['Monto_Final'] = pd.to_numeric(df1['Monto_Final'], errors='coerce')
        df2['Edad'] = pd.to_numeric(df2['Edad'], errors='coerce')
        df3['Precio_Lista'] = pd.to_numeric(df3['Precio_Lista'], errors='coerce')

        #Manejo de Nulos (Imputación con la media)
        if df2['Edad'].isnull().any():
            df2['Edad'] = df2['Edad'].fillna(df2['Edad'].mean())
            
        if df1['Monto_Final'].isnull().any():
            df1['Monto_Final'] = df1['Monto_Final'].fillna(df1['Monto_Final'].mean())

        #CARGA
        # 'utf-8-sig' ayuda a que Excel y herramientas BI reconozcan acentos en Windows
        df1.to_csv(out_v, index=False, encoding='utf-8-sig')
        df2.to_csv(out_s, index=False, encoding='utf-8-sig')
        df3.to_csv(out_p, index=False, encoding='utf-8-sig')

        print(f"--- Reporte de Calidad ---")
        print(f"Ventas procesadas: {len(df1)}")
        print(f"Socios procesados: {len(df2)}")
        print(f"Productos procesados: {len(df3)}")
        print("--------------------------")
        return True

    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        return False

if __name__ == '__main__':
    exito = proceso_etl(v_sucias, s_sucios, p_sucios, v_limpios, s_limpios, p_limpios)
    if exito:
        print("¡Proceso ETL finalizado correctamente!")
    else:
        print("El proceso falló. Revisa los errores arriba.")