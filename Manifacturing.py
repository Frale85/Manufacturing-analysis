import pandas as pd
# Lettura del file CSV
df = pd.read_csv(r"C:\Users\lef1\Date.csv", sep=';', dtype=str)

# Ordinamento del DataFrame per Data, Finitura e Risorsa
df_sorted = df.sort_values(by=['Giorno', 'Finitura', 'Risorsa'])

# Raggruppamento per Data, Finitura e Risorsa
grouped = df_sorted.groupby(['Giorno', 'Finitura', 'Risorsa'])[['Codice_Parte', 'Ordine']].apply(lambda x: x.values.tolist()).reset_index()
grouped.rename(columns={0: 'Codice_Parte_Ordine'}, inplace=True)

# Funzione per contare i cambiamenti di valori in una lista
def count_value_changes(values):
    changes = 0
    if len(values) <= 1:
        return 1  # Se c'è solo un elemento, conta come 1
    previous_value = values[0]
    for value in values[1:]:
        if value != previous_value:
            changes += 1
        previous_value = value
    return changes + 1  # Conta l'ultimo cambio


# Funzione per contare le ripetizioni non consecutive
def count_non_consecutive_repeats(values):
    seen = set()
    non_consecutive_counts = 0
    for i in range(len(values)):
        if values[i] in seen and (i == 0 or values[i] != values[i-1]):
            non_consecutive_counts += 1
        seen.add(values[i])
    return non_consecutive_counts

# Funzione per contare il numero di ordini unici
def count_unique(values):
    return len(set(values))

# Lista per memorizzare i risultati
results = []


# Scorrimento e conteggio dei cambiamenti di valori per ogni DataFrame
for _, row in grouped.iterrows():
    data = [item[0] for item in row['Codice_Parte_Ordine']]  # Lista dei valori di codice parte
    ordini = [item[1] for item in row['Codice_Parte_Ordine']]  # Lista dei valori di ordine

    # Calcolo dei cambiamenti di valori
    changes = count_value_changes(data)

    # Calcolo delle ripetizioni non consecutive
    non_consecutive_repeats = count_non_consecutive_repeats(data)

    # Calcolo del numero di ordini unici
    unique_orders_count = count_unique(ordini)

    # Calcolo delle ripetizioni degli ordini
    order_repeats = len(ordini) - unique_orders_count

    # Aggiunta dei risultati alla lista
    results.append({
        'Giorno': row['Giorno'],
        'Finitura': row['Finitura'],
        'Risorsa': row['Risorsa'],
        'Codici': ', '.join(data),  # Convertire la lista in una stringa
        'Ordini': ', '.join(ordini),  # Convertire la lista in una stringa
        'Cambiamenti': changes,
        'PrimoCodice': data[0],
        'UltimoCodice': data[-1],
        'PrimoOrdine': ordini[0],  # Primo ordine
        'UltimoOrdine': ordini[-1],  # Ultimo ordine
        'RipetizioniNonConsecutive': non_consecutive_repeats,  # Ripetizioni non consecutive
        'NumeroOrdini': unique_orders_count,  # Numero di ordini unici
        'RipetizioniOrdini': order_repeats,  # Ripetizioni degli ordini
        'NumeroOrdiniUnici': unique_orders_count  # Aggiunto il numero di ordini unici alla lista dei risultati
    })
    
    # Stampa di informazioni di debug
    print(f"Processed: {row['Giorno']}, {row['Finitura']}, {row['Risorsa']}, Codici: {data}, Ordine: {ordini}, Cambiamenti: {changes}, Numero Ordini: {unique_orders_count}, Ripetizioni Ordini: {order_repeats}, Primo Ordine: {ordini[0]}, Ultimo Ordine: {ordini[-1]}")



# Creazione del DataFrame dei risultati
results_df = pd.DataFrame(results)

# Stampa dei risultati finali
for idx, result in results_df.iterrows():
    print(f"Giorno: {result['Giorno']}, Finitura: {result['Finitura']}, Risorsa: {result['Risorsa']}")
    print(f"Codici: {result['Codici']}")
    print(f"Ordini: {result['Ordini']}")
    print(f"Numero di cambiamenti di valori: {result['Cambiamenti']}")
    print(f"PrimoCodice: {result['PrimoCodice']}")
    print(f"UltimoCodice: {result['UltimoCodice']}")
    print(f"PrimoOrdine: {result['PrimoOrdine']}")
    print(f"UltimoOrdine: {result['UltimoOrdine']}")
    print(f"Ripetizioni Non Consecutive: {result['RipetizioniNonConsecutive']}")
    print(f"Numero di ordini unici: {result['NumeroOrdini']}")
    print(f"Ripetizioni degli ordini: {result['RipetizioniOrdini']}")
    print(f"Numero di ordini unici: {result['NumeroOrdiniUnici']}")
    print()


# Scrittura dei risultati in un file Excel
results_df.to_excel(r"C:\Users\lef.xlsx", index=False)
print("Risultati salvati in 'risultatiDateNicimCodOrd.xlsx'")
