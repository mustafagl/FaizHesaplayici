import pandas as pd
import os
from datetime import datetime
import json
import settings_manager
from dateutil.relativedelta import relativedelta

class DfManager:
    def __init__(self,page):
        self.create_df()
        self.page = page
        self.sm = settings_manager.SettingsManager()

    def create_df(self):

        if(os.path.isfile("main.xlsx")):
            self.df = pd.read_excel("main.xlsx",index_col=[0])
        else:
            self.df = pd.DataFrame(columns=['Müşteri Adı','Adresi','Telefon Numarası','E-Postası','USDT TRC20 Yatırma Adresi','Ek Yatırma Adresi','Başlangıç Tarihi','Ana Para', 'Ana Para Cinsi','Aylık Faiz Miktarı','Birleşik Faiz mi?','müşteri bakiye miktarı','Son Tarih','History'])
            self.df.to_excel("main.xlsx")

        self.df['Müşteri Adı']=self.df['Müşteri Adı'].astype(str)

        self.df.to_excel("main.xlsx")        

    def calculate(self):
            self.df['müşteri bakiye miktarı'] =self.df["Müşteri Adı"].apply( lambda x : self.faiz_hesapla(x,datetime.now()))
    
    def search(self, query):

        result = self.df.loc[self.df['Müşteri Adı'].str.contains(query, case=False)]
        self.page.create_show_user(result)


    def diff_day(self,d1, d2):
        delta = d1 - d2
        return delta.days



    def diff_month(self, d1, d2, tahsilat_tarihi):
        ay = d2.month
        yil = d2.year    

        if d2.day <= tahsilat_tarihi:
            yeni_tarih = datetime(yil, ay, tahsilat_tarihi)
        else:
            if ay != 12:
                yeni_tarih = datetime(yil, ay+1, tahsilat_tarihi)
            else:    
                yeni_tarih = datetime(yil+1, 1, tahsilat_tarihi)
                
        delta = yeni_tarih - d2

        delta2 = relativedelta(d1,  yeni_tarih)



        ay2 = d1.month
        yil2 = d1.year    

        if d1.day >= tahsilat_tarihi:
            yeni_tarih2 = datetime(yil2, ay2, tahsilat_tarihi)
        else:
            if ay != 1:
                yeni_tarih2 = datetime(yil2, ay2-1, tahsilat_tarihi)
            else:    
                yeni_tarih2 = datetime(yil2-1, 12, tahsilat_tarihi)

        delta3 = d1 - yeni_tarih2

        if yeni_tarih > d1:
            delta= d1 - d2
        if yeni_tarih2 <d2:
            delta3=d2-d1


        return delta2.years*12+delta2.months, max(delta.days,0) , max(delta3.days,0)        


    def faiz_hesapla(self,selected_val,dt):

        json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))
        
        ordered_data = sorted(json_history.items(), key = lambda x:datetime.strptime(x[0], '%d.%m.%Y'))

        #print("X:",ordered_data)

        bakiye=float(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["Ana Para"].values[0])
        faiz=float(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["Aylık Faiz Miktarı"].values[0])
        birlesik_faiz= None

        #print("Faiz:",faiz)
        for i in enumerate(ordered_data):

            datetime_object1 = datetime.strptime(i[1][0], '%d.%m.%Y')
            #print(len(ordered_data[i[0]][0]))
            try:
                datetime_object2 = datetime.strptime(ordered_data[i[0]+1][0], '%d.%m.%Y') 
            except:
                datetime_object2= dt


            #print(i[1][1].split(','))

            for j in i[1][1].split(','):
                if j=="Birleşik Evet":
                    birlesik_faiz= True
                if j=="Birleşik Hayır":
                    birlesik_faiz= False
                
                if j[0:6]=="Ödendi":
                    bakiye += -float(j[7:])
                    #print("F",float(j[7:]))

                if j[0:9]=="Yatırıldı":
                    bakiye += float(j[10:])

                if j[0:4]=="Faiz":
                    faiz = float(j[5:])


            #print(diff_month(datetime_object2,datetime_object1,15))
            if self.sm.currencies_dict.get("f_tip") == "Tip 1":

                if birlesik_faiz == False:
                    bakiye = bakiye+(bakiye*float(faiz)/100)/int(self.sm.currencies_dict.get("f_ay_gun")) * self.diff_day(datetime_object2,datetime_object1)
                else:
                    bakiye = bakiye* ( (1.0+float(faiz)/100)**(1/int(self.sm.currencies_dict.get("f_ay_gun"))) ) ** self.diff_day(datetime_object2,datetime_object1)

            if self.sm.currencies_dict.get("f_tip") == "Tip 2":
                c_ay,c_day1,c_day2=self.diff_month(datetime_object2,datetime_object1,int(self.sm.currencies_dict.get("f_tahsilat_gun")))
                c_ay,c_day1,c_day2=float(c_ay),float(c_day1),float(c_day2)

                if birlesik_faiz == False:
                    bakiye = bakiye+(bakiye*float(faiz)/100) * c_ay
                else:
                    bakiye = bakiye* ( (1.0+float(faiz)/100) ) ** c_ay

            if self.sm.currencies_dict.get("f_tip") == "Tip 3":
                c_ay,c_day1,c_day2=self.diff_month(datetime_object2,datetime_object1,int(self.sm.currencies_dict.get("f_tahsilat_gun")))
                c_ay,c_day1,c_day2=float(c_ay),float(c_day1),float(c_day2)

                if birlesik_faiz == False:
                    bakiye = bakiye+(bakiye*float(faiz)/100/int(self.sm.currencies_dict.get("f_ay_gun"))) * c_day1
                    bakiye = bakiye+(bakiye*float(faiz)/100) * c_ay
                    bakiye = bakiye+(bakiye*float(faiz)/100/int(self.sm.currencies_dict.get("f_ay_gun"))) * c_day2
                else:
                    bakiye = bakiye* ( (1.0+float(faiz)/100)**(1/int(self.sm.currencies_dict.get("f_ay_gun"))) ) ** c_day1
                    bakiye = bakiye* ( (1.0+float(faiz)/100) ) ** c_ay
                    bakiye = bakiye* ( (1.0+float(faiz)/100)**(1/int(self.sm.currencies_dict.get("f_ay_gun"))) ) ** c_day2



        return bakiye



    
    def save_user(self, name, adres, tel1, email, baslangic,usdtadres,ekadres, anapara, anaparacinsi, aylıkfaiz, birlesik_faiz, add_user_frame, coin_name):

        print(self.df['Müşteri Adı'].values)
        if name in self.df['Müşteri Adı'].values:
            raise ValueError("İsim zaten mevcut")

        if anaparacinsi == "Coin":
            anaparacinsi=coin_name.upper()
            if coin_name == "":
                raise ValueError("Coin ismi boş olamaz")
            if(self.sm.currencies_dict.get(f'{coin_name.upper()}/USDT')==None):
                self.sm.save_coin(coin_name)



        aylıkfaiz = aylıkfaiz.replace(",",".")
        anapara = anapara.replace(",",".")

        json_history = dict()
        json_history.update({baslangic : "Birleşik "+birlesik_faiz + ",Faiz "+aylıkfaiz})

        son = datetime.strftime(datetime.now(), '%d.%m.%Y')

        if baslangic != datetime.strptime(baslangic, "%d.%m.%Y").strftime('%d.%m.%Y'):
            raise ValueError("hatalı tarih")
        musteribakiye = 0




        self.df.loc[len(self.df.index)] = [name, adres, tel1, email, usdtadres, ekadres, baslangic, float(anapara), anaparacinsi, float(aylıkfaiz), birlesik_faiz, musteribakiye,son,json.dumps(json_history)] 
        

        
        self.df.replace('',"bilinmiyor",inplace=True)

        self.df.to_excel("main.xlsx")

        self.page.remove_screen()
        self.page.create_homepage()


    def delete_item(self, selected_val, popup):

        self.df = self.df.drop(self.df.index[self.df['Müşteri Adı'] == str(selected_val)]).reset_index(drop=True)
        self.df.to_excel("main.xlsx")
        self.page.remove_screen()
        self.page.create_show_user(self.df)    
        popup.destroy()



    def update_dataframe(self, selected_val,name, adres, tel1, email, usdtadres, ekadres, baslangic, anapara, anaparacinsi, aylıkfaiz, birlesik_faiz):

        son = datetime.strftime(datetime.now(), '%d.%m.%Y')



        if  self.df.loc[self.df['Müşteri Adı'] == str(selected_val)].values[0][0] != name and name in self.df['Müşteri Adı'].values:
            raise ValueError("İsim zaten mevcut")


        musteribakiye = self.faiz_hesapla(selected_val,datetime.now())

        self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]=[name, adres, tel1, email, usdtadres, ekadres, baslangic, anapara, anaparacinsi, aylıkfaiz, birlesik_faiz,musteribakiye,son, str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]) ]
        

        
        self.df.replace('',"bilinmiyor",inplace=True)
        self.df.to_excel("main.xlsx")
        self.page.create_show_user(self.df)


    def odeme_sil(self,selected,selected_val):

        json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))
        json_history.pop(selected[0])
        self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"History"]=json.dumps(json_history)
        self.df.to_excel("main.xlsx")
        self.page.create_odemeler(selected_val)


    def odeme_yap(self, tarih_var,odeme_var,selected_val):
        try:
            odeme_var=odeme_var.replace(",",".")
            float(odeme_var)
            json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))

            if tarih_var in json_history:
                json_history.update({tarih_var : json_history[tarih_var]+",Ödendi "+odeme_var})
            else:
                json_history.update({tarih_var : "Ödendi "+odeme_var})


            self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"History"]=json.dumps(json_history)
            self.df.to_excel("main.xlsx")
            self.page.create_odemeler(selected_val)
        except:
            pass    


    def yatırma_yap(self, tarih_var,odeme_var,selected_val):
        try:
            odeme_var=odeme_var.replace(",",".")
            float(odeme_var)    
            json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))
            if tarih_var in json_history:
                json_history.update({tarih_var : json_history[tarih_var]+",Yatırıldı "+odeme_var})
            else:
                json_history.update({tarih_var : "Yatırıldı "+odeme_var})

            
            self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"History"]=json.dumps(json_history)
            self.df.to_excel("main.xlsx")    
            self.page.create_odemeler(selected_val)
        except:
            pass


    def faiz_type_donus(self, tarih_var,selected_val):

        
        json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))

        if self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["Birleşik Faiz mi?"].values[0] == "Evet":
            temp = "Hayır"

        else:    
            temp = "Evet"

        if tarih_var in json_history:
            json_history.update({tarih_var : json_history[tarih_var]+",Birleşik "+temp})
        else:
            json_history.update({tarih_var : "Birleşik "+temp})
        
        self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"Birleşik Faiz mi?"] = temp

        self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"History"]=json.dumps(json_history)
        self.df.to_excel("main.xlsx")
        self.page.create_odemeler(selected_val)

    def faiz_amount_donus(self, tarih_var,odeme_var,selected_val):

        try:
            odeme_var=odeme_var.replace(",",".")
            float(odeme_var)
            json_history = json.loads(str(self.df.loc[self.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))
            if tarih_var in json_history:
                json_history.update({tarih_var : json_history[tarih_var]+",Faiz "+odeme_var})
            else:
                json_history.update({tarih_var : "Faiz "+odeme_var})

            self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"Aylık Faiz Miktarı"] = float(odeme_var)
            self.df.loc[self.df['Müşteri Adı'] == str(selected_val),"History"]=json.dumps(json_history)
            self.df.to_excel("main.xlsx")    
            self.page.create_odemeler(selected_val)
        except:
            pass    