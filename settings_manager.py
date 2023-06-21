
import json
import os

class SettingsManager:
    def __init__(self):
        self.create_currencies_dict()

    def create_currencies_dict(self):

        self.currencies_dict= dict()

        if(os.path.isfile("currencies.json")):
            with open('currencies.json', 'r') as openfile:
            
                self.currencies_dict = json.load(openfile)
        else:
            self.currencies_dict = {
                "usd/try": 19,
                "eur/try": 20,
                "f_tip": "Tip 3",
                "f_ay_gun": 30,
                "f_tahsilat_gun": 15,
            }
            
            self.currencies_json = json.dumps(self.currencies_dict, indent=4)
            
            with open("currencies.json", "w") as outfile:
                outfile.write(self.currencies_json)             


    def calculate_currencies(self,anapara,cins):
        if cins == "₺":
            tl = anapara
            dolar = float(anapara)/self.currencies_dict.get("usd/try")
            euro = float(anapara)/self.currencies_dict.get("eur/try")

        elif cins == "$":
            dolar = anapara
            tl = float(anapara)*self.currencies_dict.get("usd/try")
            euro = float(anapara)*self.currencies_dict.get("usd/try")/self.currencies_dict.get("eur/try")

        elif cins == "€":
            euro = anapara
            tl =  float(anapara)*self.currencies_dict.get("eur/try")
            dolar = float(anapara)/self.currencies_dict.get("usd/try")/self.currencies_dict.get("eur/try")

        else:
            try:
                dolar = self.currencies_dict.get(f"{cins}/USDT")
                tl = dolar*self.currencies_dict.get("usd/try")
                euro = tl / self.currencies_dict.get("eur/try")
            except:    
                tl=0
                euro=0
                dolar=0
            
            

        return (tl,dolar,euro)
    

    def save_coin(self, coin_name):

        self.currencies_dict[f'{coin_name.upper()}/USDT']=1

        currencies_json = json.dumps(self.currencies_dict, indent=4)
        
        with open("currencies.json", "w") as outfile:
            outfile.write(currencies_json)    
    

    def save_currencies(self, pg, usdtry,eurtry,f_tip,f_ay_gun,f_tahsilat_gun,entry_list):

        usdtry = usdtry.replace(",",".")
        eurtry = eurtry.replace(",",".")

        if not (0 <= int(f_ay_gun) <= 30 and 0 <= int(f_tahsilat_gun) <= 30):
            raise ValueError("f_ay_gun ve f_tahsilat_gun 0-30 aralığında olmalıdır.")
        
        self.currencies_dict = {
            "usd/try": float(usdtry),
            "eur/try": float(eurtry),
            "f_tip": f_tip,
            "f_ay_gun": f_ay_gun,
            "f_tahsilat_gun": f_tahsilat_gun,

        }
        for key,value in entry_list.items():
            self.currencies_dict[key]=float(value.get().replace(",","."))

        
        currencies_json = json.dumps(self.currencies_dict, indent=4)
        
        with open("currencies.json", "w") as outfile:
            outfile.write(currencies_json)

        pg.remove_screen()
        pg.create_homepage()    
