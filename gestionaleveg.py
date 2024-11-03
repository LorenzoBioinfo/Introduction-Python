
import re


def welcoming():
    """
     Funzioen che stampa il messaggio di Benvenuto
    """
    print("======================================================================================================")

    print("======================== Benvenuto al Gestionale del negozio 'Vegano Gourmet' ========================")
    
    print("\n")
  
def show_commands():
    """
    Funzione che mostra i comandi disponibili
    """

    print("Ecco i comandi disponibili:")
    print("aggiungi: aggiungi un prodotto al magazzino")
    print("elenca: elenca i prodotto in magazzino")
    print("vendita: registra una vendita effettuata")
    print("profitti: mostra i profitti totali")
    print("aiuto: mostra i possibili comandi")
    print("chiudi: esci dal programma")







def load_data():

    file_path = 'mystore.csv'
    
    with open(file_path, 'r') as file:
        # Inizializza un dizionario vuoto
        data_dict = {}
        first_line = True
        # Leggi il contenuto del file riga per riga
        for line in file:
            if not line.startswith("Nome"):
                try:
                   
                    values = line.strip().split("\t")
         
                    key = values[0]
                    value = [{"Quantità":values[1],"Prezzo di vendita":values[2],"Prezzo di acquisto":values[3],"Venduti":values[4]}]
                    
                        # Aggiungi l'elemento al dizionario
                    data_dict[key] = value
                except:
                    print("Al momento il magazzino è vuoto")
       
    return data_dict


def update_data(data_dict):

    file_csv = 'mystore.csv'
    with open(file_csv, 'w', newline='') as csvfile:
       
        with open(file_csv, 'w') as csvfile:
            # Ottieni le chiavi del dizionario
            chiavi = list(data_dict.keys())

            # Scrivi l'intestazione con le chiavi come colonne
            csvfile.write('Nome prodotto    Quantità    Prezzo di vendita   Prezzo di acquisto  Venduti'+"\n")
            
            for key,value in data_dict.items():
              
                row=[key]+[str(v) for v in  value[0].values()]
                csvfile.write('\t'.join(row) + '\n')


def show_products():


    store=load_data()
    if not store:
        print("Mi dispiace. Il magazzino è vuoto e non ho prodotti da mostrati")
    else:
        print("PRODOTTO QUANTITA' PREZZO")
        
        for product in store.keys():
            print(product+" "+str(store[product][0]['Quantità'])+"  " +"€ " +str(store[product][0]['Prezzo di vendita']))



def register_product():
    
    store=load_data()
    product= input("Inserisci il nome del prodotto che vuoi inserire: ")
    product = re.sub(r'\*+', '', product)



    register=True
    while register:

        check_quantity=True
        while check_quantity:
            input_quantity= input("Inserisci un numero per indicare la quantità di prodotto: ")
            try:
                
                number = re.sub(r'[^0-9]', '', input_quantity)
                quantity = int(number)  
                print(f"Hai inserito la quantità: {quantity}")
                check_quantity=False
            except ValueError:
                print("L'input non è un numero valido.")
            
        if product in store.keys():
            print("Il prodotto è già presente. La quantità verrà aggiornata")
            store[product][0]["Quantità"]=int(store[product][0]["Quantità"])+quantity
            register=False
            update_data(store)
            continue

        check_sale=True
        while check_sale:
            input_sale= input("Inserisci un numero per indicare prezzo di vendita: ")
            try:
                sale= float(input_sale)  
                print(f"Hai inserito il prezzo di vendita: {sale}")
                check_sale=False
            except ValueError:
                print("L'input non è un numero valido.")

        check_purchase=True
        
        while check_purchase:
            input_purchase = input("Inserisci un numero per indicare prezzo di acquisto: ")
            try:
                purchase = float(input_purchase)  
                print(f"Hai inserito il prezzo di acquisto: {purchase}")
                check_purchase=False
            except ValueError:
                print("L'input non è un numero valido.")

        register=False

       
        store[product]=[{"Quantità":quantity,"Prezzo di vendita":sale,"Prezzo di acquisto":purchase,"Venduti":0}]

        print(f"Aggiunto {quantity} X {product}")

        update_data(store)


def sell_product():

    products=[]
    quantities=[]
    sell=True
    while sell:

        product_name=input("Nome del prodotto: " )
        products.append(product_name)
        check_quantity=True
        while check_quantity:
            input_quantity= input("Inserisci un numero per indicare la quantità di prodotto: ")
            try:
                number = re.sub(r'[^0-9]', '', input_quantity)
                quantity = int(number)  
                print(f"Hai inserito la quantità: {quantity}")
                quantities.append(quantity)
                check_quantity=False
            except ValueError:
                    print("L'input non è un numero valido.")
                    
        other_sell=input("Aggiungere un altro prodotto ? (si/no): ")
        if other_sell=="no":
    
            print("VENDITA REGISTRATA")
            store=load_data()
     
            
            for i in range(len(products)):
                tot=[]
                if products[i] in store.keys():
                    print(str(quantities[i])+" X "+products[i] + ": € "+str(store[products[i]][0]["Prezzo di vendita"]))
                    tot.append(float(store[products[i]][0]["Prezzo di vendita"])*quantities[i])
                    store[products[i]][0]["Quantità"]=int(store[products[i]][0]["Quantità"])-int(quantities[i])
                    store[products[i]][0]["Venduti"]=quantities[i]
                else:
                    print(products[i] + " non è disponibile nel negozio")

            print("Totale : " +str(sum(tot)))

            # update quantities
            sell=False

            update_data(store)



def print_balance():

    gross=[]
    cost=[]
    

    store=load_data()

    for product in store.keys():
        gross.append(int(store[product][0]["Quantità"])*int(store[product][0]["Venduti"]))
        cost.append(float(store[product][0]["Prezzo di acquisto"])*int(store[product][0]["Venduti"]))

    gross_tot=sum(gross)
    cost_tot=sum(cost)
    net= gross_tot-cost_tot

    print(f"Profitto lordo = € {gross_tot}   Profitto netto = € {cost_tot}")


if __name__ == '__main__':

    welcoming()

    execute=True
    while execute :

        input_user=input("Cosa posso fare per te?  ")
       
    
        if input_user == "aiuto":
        
            show_commands()
        elif input_user== "E":
            print("Ciao e alla prossima!")
            execute=False
        elif input_user=="elenca":
            show_products()
        elif input_user=="aggiungi":
            register_product()
        elif input_user=="vendita":
            sell_product()
        elif input_user=="profitti":
            print_balance()
        
        else:
            print("Comando non dispobile. Riprova")