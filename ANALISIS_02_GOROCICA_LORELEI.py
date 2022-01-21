import csv
import pandas as pd
#%%
#SE IMPORTA LA BASE DE DATOS DE LA EMPRESA
synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])
#%%
#SE CREA EL DATAFRAME CON LOS DATOS DE LAS RUTAS
combinaciones = synergy_dataframe.groupby(by=['origin', 'destination',
                                               'transport_mode'])

descripcion = combinaciones.describe()['total_value']

#%%
#SE ORDENAN LOS VALORES PARA OBTENER LOS 10 RUTAS MAS DEMANDADDAS
mean = descripcion['count']

mean_sort = mean.sort_values(ascending=False)
print('\n 10 rutas mas demandadas:\n')
print(mean_sort[:10])
#%%
#SE REALIZA LA OPERACION PARA CONOCER EL PORCENTAJE DE INGRESO QUE REPRESENTA CADA PAIS
exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']


def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_pequena = pais_total_value[pais_total_value['cumsum'] < p]
    
    return lista_pequena

res = sol_3(synergy_dataframe, 80)

print('\n Paises que generan el 80% de los ingresos:\n', sol_3(synergy_dataframe, 100))

#%%

#SE GENERA FUNCION QUE CALCULA LA SUMA DE LAS VENTAS
def calculadora_promedio_valor(datos):
    num_datos = len(datos)
    total = 0
    for row in datos:
        valor = row[9]
        total += valor
    promedio = total / num_datos
    return promedio

#FUNCION PARA ORDENAR LOS RESULTADOS
def ordenar_dicc(diccionario):
    ordenado = [[value, key] for key, value in diccionario.items()]
    ordenado = sorted(ordenado, reverse=True)
    ordenado = [[llave, valor] for valor, llave in ordenado]
    return ordenado

#FUNCION PARA OBTENER LA LISTA DE LA SUMA POR TRANSPORTE
def analizar(dict):
    analisis = []
    for llave in dict:
        sub_lista = [llave]
        promedio_valor = calculadora_promedio_valor(dict[llave])
        sub_lista.append(promedio_valor)
        analisis.append(sub_lista)

    return analisis
#FUNCIONES PARA DIVIDIR LOS VALORES EN CATEGORIAS Y SERIES
def divisor(datos, cols):
    datos_separados = {}
    for row in datos:
        vals = []
        for col in cols:
            vals.append(row[col])
        key = '-'.join(vals)
        if key not in datos_separados:
            datos_separados[key] = [row]
        else:
            datos_separados[key].append(row)
    return datos_separados


def procesador(datos):
    datos_paso_1 = []
    for renglon in datos:
        renglon_separado = renglon.split(',')
        datos_paso_1.append(renglon_separado)
    datos_paso_2 = []
    for lista in datos_paso_1:
        lista_limpia = []
        for elemento in lista:
            elemento_limpio = elemento.strip()
            lista_limpia.append(elemento_limpio)
        datos_paso_2.append(lista_limpia)
    datos_paso_3 = []
    for lista in datos_paso_2:
        lista_con_conversiones = []
        for elemento in lista:
            if elemento.isdigit():
                elemento = int(elemento)
            lista_con_conversiones.append(elemento)
        datos_paso_3.append(lista_con_conversiones)
    return datos_paso_3

#FUNCION PARA LEER LA BASE DE DATOS
def lector():

    syn_log_db = []

    with open('synergy_logistics_database.csv', 'r', newline='') as sldb:
        db = csv.reader(sldb, delimiter=',')
        primer_elemento = next(db)
        tipo = type(primer_elemento)
        for row in sldb:
            syn_log_db.append(row)

    return syn_log_db

#FUNCION PARA OBTENER EL RESULTADO DEL ANALISIS 
def main():
    db = lector()
    db = procesador(db)
    div_por_direccion = divisor(db, [1])
    llaves = div_por_direccion.keys()
    analisis = analizar(div_por_direccion)
    div_por_medio = divisor(db, [7])
    analisis = analizar(div_por_medio)
    diccionario = dict(analisis)
    final = ordenar_dicc(diccionario)
    print('\n' * 3)
    for a in final:
        titulo = a[0]
        print(f'\tTotal de ventas del medio de transporte {titulo}:')
        for resultado_de_operacion in a[1:]:
            print(resultado_de_operacion)
        print('\n')

if __name__ == '__main__':
    main()


