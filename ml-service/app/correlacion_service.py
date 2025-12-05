import pandas as pd
import numpy as np  

def run_correlation_from_csv(path, threshold=0.8):
    print(f"Running correlation on {path} ")
    df = pd.read_csv(path)
    #print(df.head())
    # asumir que df es numérico o seleccionar columnas numéricas

    df['PEDIDO']=df['PEDIDO']
    df['EMAIL']=df['Cliente Mail']
    df['FECHA']=df['Fecha']
    df['CANTIDAD']=df['Cantidad']
    df['PRODUCTO']=df['Producto']
    df['MARCA']=df['Marca']
    df['CATEGORIA']=df['Categoría']
    df['TIPO_CLIENTE']=df['Tipo Cliente']
    df['CATEGORIA2']=df['CATEGORIA']+'-'+df['MARCA']


    MyData_c = df[['EMAIL','PRODUCTO']]
    #print(MyData_c)
    
    categoria = df['PRODUCTO'].drop_duplicates().reset_index(drop=True)

    #print(categoria)

    categoria.to_csv("categoria.csv")

    MyData_t = pd.crosstab(MyData_c['EMAIL'], MyData_c['PRODUCTO'].fillna('n/a'))
    #print(MyData_t.head())



    corre = MyData_t.corr()

    print("Máxima correlación:", corre.max().max())
    print("Mínima correlación:", corre.min().min())


    # Eliminar la diagonal (autocorrelación = 1.0)
    corre_no_diag = corre.mask(np.eye(len(corre), dtype=bool))

    # Filtrar correlaciones mayores a 0.4 y menores a 1
    corre_filtrado = corre_no_diag.where((corre_no_diag > threshold) & (corre_no_diag < 1)).fillna(0)

    #Filtrar por umbral
    #corre_filtrado = corre.where(corre > threshold).fillna(0)

    # Eliminar filas/columnas que quedaron todas en 0 (nodos aislados)
    mask = (corre_filtrado != 0).any(axis=1)
    corre_filtrado = corre_filtrado.loc[mask, mask]

    # DEBUG: imprime formas para verificar
    print("shape original corre:", corre.shape)
    print("shape filtrado corre:", corre_filtrado.shape)
    # categorías que corresponderán exactamente con filas/columnas de la matriz
    categorias_filtradas = corre_filtrado.index.tolist()  # o .columns.tolist()

    # Export opcional
    #corre_filtrado.to_csv(os.path.join(base_dir, "corre_filtrado.csv"))

    # Ver pares de categorías con correlación fuerte
    pares_fuertes = (
        corre_filtrado.unstack()
        .dropna()
        .sort_values(ascending=False)
    )

    print("🔗 Top correlaciones entre categorías:")
    #print(pares_fuertes.head(10))

    
    # Pasar matriz como list of lists y categorias como lista
    return corre_filtrado.values.tolist(), categorias_filtradas



