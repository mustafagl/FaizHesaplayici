import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk
import df_manager
import json
from functools import partial


class Pages():
    def __init__(self, master):
        self.master=master
        self.dfm = df_manager.DfManager(self)

        
    def remove_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_home(self,frame):
        frame.pack_forget()
        self.create_homepage()            

    def create_homepage(self):    
        
        self.remove_screen()


        now = datetime.now()


        date_label = tk.Label(self.master, text="Bugünün Tarihi: {}".format(now.strftime("%Y-%m-%d")))
        date_label.grid(row=0, column=1, sticky="nsew")

        add_user_button = tk.Button(self.master, text="Kullanıcı Ekle", command=self.create_add_user)
        add_user_button.grid(row=1, column=0, padx=(50,10), pady=(0,100), sticky="nsew")

        show_user_button = tk.Button(self.master, text="Kullanıcıları Göster", command=lambda: self.create_show_user(self.dfm.df))
        show_user_button.grid(row=1, column=1, padx=(10,10), pady=(0,100), sticky="nsew")
            
        pair_button = tk.Button(self.master, text="Kurlar",command= self.create_pairs)
        pair_button.grid(row=1, column=2,padx=(10,50), pady=(0,100), sticky="nsew")    
        
        exit_button = tk.Button(self.master, text="Çıkış", command=self.master.quit)
        exit_button.grid(row=2, column=0,columnspan=3, padx=100, pady=100, sticky="nsew")



        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)




    def create_add_user(self):

        self.remove_screen()

        add_user_frame = tk.Frame(self.master)
        add_user_frame.pack()

        scrollbar = tk.Scrollbar(add_user_frame)
        scrollbar.pack(side="right", fill="y",pady=10)

        canvas = tk.Canvas(add_user_frame, width=800, height=1200, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, pady=(100,10))

        frame = tk.Frame(canvas)
        frame.pack(side="left", fill="both", expand=True,pady=10)
        
        name = tk.StringVar()
        adres = tk.StringVar()
        tel1 = tk.StringVar()
        email = tk.StringVar()
        usdtadres = tk.StringVar()
        ekadres = tk.StringVar()
        baslangic = tk.StringVar()
        anapara = tk.StringVar()
        anaparacinsi = tk.StringVar()
        aylıkfaiz = tk.StringVar()
        birlesik_faiz = tk.StringVar()

        

        name_label = tk.Label(frame, text="Müşteri Adı:")
        name_label.grid(row=0, column=0, pady=5)

        name_entry = tk.Entry(frame, textvariable=name)
        name_entry.grid(row=0, column=1, pady=5)




        adreslabel = tk.Label(frame, text="Adresi:")
        adreslabel.grid(row=1, column=0, pady=5)

        adresentry = tk.Entry(frame, textvariable=adres)
        adresentry.grid(row=1, column=1, pady=5)

        tel1label = tk.Label(frame, text="Telefon Numarası:")
        tel1label.grid(row=2, column=0, pady=5)

        tel1entry = tk.Entry(frame, textvariable=tel1)
        tel1entry.grid(row=2, column=1, pady=5)

        emaillabel = tk.Label(frame, text="E-Postası:")
        emaillabel.grid(row=3, column=0, pady=5)

        emailentry = tk.Entry(frame, textvariable=email)
        emailentry.grid(row=3, column=1, pady=5)


        usdtadreslabel = tk.Label(frame, text="USDT TRC20 Yatırma Adresi:")
        usdtadreslabel.grid(row=4, column=0, pady=5)

        usdtadresentry = tk.Entry(frame, textvariable=usdtadres)
        usdtadresentry.grid(row=4, column=1, pady=5)    

        ekadreslabel = tk.Label(frame, text="Ek Yatırma Adresi:")
        ekadreslabel.grid(row=5, column=0, pady=5)

        ekadresentry = tk.Entry(frame, textvariable=ekadres)
        ekadresentry.grid(row=5, column=1, pady=5)        



        baslangiclabel = tk.Label(frame, text="Başlangıç Tarihi:")
        baslangiclabel.grid(row=6, column=0, pady=5)

        baslangicentry=DateEntry(frame,textvariable=baslangic,date_pattern="dd.mm.yyyy")
        baslangicentry.grid(row=6, column=1, pady=5)


        anaparalabel = tk.Label(frame, text="Giriş Miktarı:")
        anaparalabel.grid(row=7, column=0, pady=5)

        anaparaentry = tk.Entry(frame, textvariable=anapara)
        anaparaentry.grid(row=7, column=1, pady=5)



        anaparacinsilabel = tk.Label(frame, text="Ana Para Cinsi:")
        anaparacinsilabel.grid(row=8, column=0, pady=5)

        anaparacinsi.set("₺")
        anaparacinsientry = tk.OptionMenu(frame, anaparacinsi,"₺","$","€","Coin")
        anaparacinsientry.grid(row=8, column=1, pady=5,sticky="nsew")



        coin_name = tk.StringVar()

        coin_ad_label = tk.Label(frame,text="Coin Adı: ")
        coin_ad_entry = tk.Entry(frame,textvariable=coin_name)
        

        coin_ad_label.grid_forget()   
        coin_ad_entry.grid_forget()   


        def show_entry(*args):
            # Show the entry widget when Option 2 is selected, hide it otherwise
            if anaparacinsi.get() == "Coin":
                coin_ad_label.grid(row=8, column=2, pady=5,sticky="w")
                coin_ad_entry.grid(row=8, column=3, pady=5,sticky="w")
            else:    
                coin_ad_label.grid_forget()
                coin_ad_entry.grid_forget()

        anaparacinsi.trace("w", show_entry)
        


        aylıkfaizlabel = tk.Label(frame, text="Aylık Faiz Miktarı:")
        aylıkfaizlabel.grid(row=9, column=0, pady=5)

        aylıkfaizentry = tk.Entry(frame, textvariable=aylıkfaiz)
        aylıkfaizentry.grid(row=9, column=1, pady=5)



        birlesikfaizlabel = tk.Label(frame, text="Birleşik Faiz:")
        birlesikfaizlabel.grid(row=10, column=0, pady=5)



        birlesik_faiz.set("Evet")
        birlesikfaizentry = tk.OptionMenu(frame, birlesik_faiz,"Evet","Hayır")
        birlesikfaizentry.grid(row=10, column=1, pady=5,sticky="w")



        save_button = tk.Button(add_user_frame, text="Save", command=lambda: self.dfm.save_user(name.get(), adres.get(), tel1.get(), email.get(), baslangic.get(), usdtadres.get(),ekadres.get(), anapara.get(), anaparacinsi.get(), aylıkfaiz.get(), birlesik_faiz.get(), add_user_frame, coin_name.get()))
        save_button.pack(side="right")

        back_button = tk.Button(add_user_frame, text="Back", command=lambda: self.go_home(add_user_frame))
        back_button.pack(side="left")


        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollbar.config(command=canvas.yview)



    def create_show_user(self,result):

        self.dfm.calculate()
        #df['müşteri bakiye miktarı'] = df["Müşteri Adı"].apply( lambda x : faiz_hesapla(x,datetime.now()))


        name_var=tk.StringVar()
        name = tk.StringVar()
        adres = tk.StringVar()
        tel1 = tk.StringVar()
        email = tk.StringVar()
        usdtadres = tk.StringVar()
        ekadres = tk.StringVar()
        baslangic = tk.StringVar()
        anapara = tk.StringVar()
        anaparacinsi = tk.StringVar()
        aylıkfaiz = tk.StringVar()
        birlesik_faiz = tk.StringVar()


        self.remove_screen()


        search_frame = tk.Frame(self.master)

        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


        search_entry = tk.Entry(search_frame,textvariable=name_var)
        search_entry.focus_set()    
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        search_button = tk.Button(search_frame, text="Search", command=lambda: self.dfm.search(name_var.get()))
        search_button.pack(side=tk.RIGHT)
        


        show_user_frame = tk.Frame(self.master)



        show_user_frame.pack()


        table = ttk.Treeview(show_user_frame, columns=('Müşteri Adı','Adresi','Telefon Numarası','E-Postası','Başlangıç tarihi','Giriş Miktarı', 'Ana Para Cinsi','Aylık Faiz Miktarı','Birleşik Faiz','Müşteri Bakiye Miktarı','Bir Sonraki Tahsilat Bakiye'), show="headings")
        table.pack()


        table.column("Müşteri Adı", width=120, anchor="center")
        table.heading("Müşteri Adı", text="Müşteri Adı")
        

        table.column("Adresi", width=120, anchor="center")
        table.heading("Adresi", text="Adresi")
        
        table.column("Telefon Numarası", width=120, anchor="center")
        table.heading("Telefon Numarası", text="Telefon Numarası")


        table.column("E-Postası", width=120, anchor="center")
        table.heading("E-Postası", text="E-Postası")                

        table.column("Başlangıç tarihi", width=120, anchor="center")
        table.heading("Başlangıç tarihi", text="Başlangıç tarihi")     

        table.column("Giriş Miktarı", width=120, anchor="center")
        table.heading("Giriş Miktarı", text="Giriş Miktarı")     

        table.column("Ana Para Cinsi", width=120, anchor="center")
        table.heading("Ana Para Cinsi", text="Ana Para Cinsi")      

        table.column("Aylık Faiz Miktarı", width=120, anchor="center")
        table.heading("Aylık Faiz Miktarı", text="Aylık Faiz Miktarı")     

        table.column("Birleşik Faiz", width=120, anchor="center")
        table.heading("Birleşik Faiz", text="Birleşik Faiz")     

        table.column("Müşteri Bakiye Miktarı", width=120, anchor="center")
        table.heading("Müşteri Bakiye Miktarı", text="Müşteri Bakiye Miktarı")     

        table.column("Bir Sonraki Tahsilat Bakiye", width=120, anchor="center")
        table.heading("Bir Sonraki Tahsilat Bakiye", text="Bir Sonraki Tahsilat Bakiye")         
                
        dt_now=datetime.now()            
        dt= datetime(dt_now.year, dt_now.month, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun"))) if dt_now.day<=int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun")) else datetime(dt_now.year, dt_now.month+1, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun"))) if dt_now.month!= 12 else datetime(dt_now.year+1, 1, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun")))
        for i in range(len(result)):

            table.insert("", "end", values=(result.iloc[i]['Müşteri Adı'], result.iloc[i]['Adresi'], result.iloc[i]['Telefon Numarası'], result.iloc[i]['E-Postası'], result.iloc[i]['Başlangıç Tarihi'], result.iloc[i]['Ana Para'],result.iloc[i]['Ana Para Cinsi'], result.iloc[i]['Aylık Faiz Miktarı'], result.iloc[i]['Birleşik Faiz mi?'],round(result.iloc[i]['müşteri bakiye miktarı'],1),round(self.dfm.faiz_hesapla(result.iloc[i]['Müşteri Adı'],dt),1)))

        def retrieve_selected_value(user_details_frame):
            selected = table.selection()
            if len(selected) > 0:
                item = table.item(selected[0])
                global selected_val
                selected_val=item['values'][0]

                for widget in user_details_frame.winfo_children():
                    widget.destroy()



                user = self.dfm.df.loc[self.dfm.df['Müşteri Adı'] == str(selected_val)].values



                name.set(user[0,0])
                adres.set(user[0,1])
                tel1.set(user[0,2])
                email.set(user[0,3])
                usdtadres.set(user[0,4])
                ekadres.set(user[0,5])
                baslangic.set(user[0,6])
                anapara.set(user[0,7])
                anaparacinsi.set(user[0,8])
                aylıkfaiz.set(user[0,9])
                birlesik_faiz.set(user[0,10])

                


                name_label = tk.Label(user_details_frame, text="Müşteri Adı:")
                name_label.grid(row=0, column=0, pady=5)

                name_entry = tk.Entry(user_details_frame,textvariable=name)
                name_entry.grid(row=0, column=1, pady=5)



                adres_label = tk.Label(user_details_frame, text="Adresi:")
                adres_label.grid(row=0, column=2, pady=5)

                adres_entry = tk.Entry(user_details_frame, textvariable=adres)
                adres_entry.grid(row=0, column=3, pady=5)


                tel1label = tk.Label(user_details_frame, text="Telefon Numarası:")
                tel1label.grid(row=1, column=0, pady=5)

                tel1entry = tk.Entry(user_details_frame, textvariable=tel1)
                tel1entry.grid(row=1, column=1, pady=5)



                emaillabel = tk.Label(user_details_frame, text="E-Postası:")
                emaillabel.grid(row=1, column=2, pady=5)

                emailentry = tk.Entry(user_details_frame, textvariable=email)
                emailentry.grid(row=1, column=3, pady=5)

                usdtadreslabel = tk.Label(user_details_frame, text="USDT TRC20 Yatırma Adresi:")
                usdtadreslabel.grid(row=2, column=0, pady=5)

                usdtadresentry = tk.Entry(user_details_frame, textvariable=usdtadres)
                usdtadresentry.grid(row=2, column=1, pady=5)    

                ekadreslabel = tk.Label(user_details_frame, text="Ek Yatırma Adresi:")
                ekadreslabel.grid(row=2, column=2, pady=5)

                ekadresentry = tk.Entry(user_details_frame, textvariable=ekadres)
                ekadresentry.grid(row=2, column=3, pady=5)      


                tl,dolar,euro=self.dfm.sm.calculate_currencies(user[0,7],user[0,8])

                date_label = tk.Label(user_details_frame, text=str(round(float(tl),1))+"₺")
                date_label.grid(row=6, column=0, sticky="nsew")

                date_label2 = tk.Label(user_details_frame, text=str(round(float(dolar),1))+"$")
                date_label2.grid(row=6, column=1,columnspan=2, sticky="nsew")

                date_label3 = tk.Label(user_details_frame, text=str(round(float(euro),1))+"€")
                date_label3.grid(row=6, column=3, sticky="nsew")

                
                delete_button = tk.Button(user_details_frame, text="Sil", command=lambda: self.delete_warning_popup("Silmek istediğinizden emin misiniz?",selected_val))
                delete_button.grid(row=7,column=0,columnspan=1,  sticky="NWES")        

                update_button = tk.Button(user_details_frame, text="Güncelle", command=lambda: self.dfm.update_dataframe(selected_val,name.get(), adres.get(), tel1.get(), email.get(), usdtadres.get(), ekadres.get(), baslangic.get(), anapara.get(), anaparacinsi.get(), aylıkfaiz.get(), birlesik_faiz.get()))
                update_button.grid(row=7,column=1,columnspan=2,  sticky="NWES")        


                odeme_button = tk.Button(user_details_frame, text="İşlemler", command=lambda: self.create_odemeler(selected_val))
                odeme_button.grid(row=7,column=3,columnspan=1,  sticky="NWES")     


                tel1entry.update()


        user_details_frame = tk.Frame(self.master)

        table.bind("<ButtonRelease-1>", lambda event: retrieve_selected_value(user_details_frame))

        user_details_frame.pack()




        actions_frame = tk.Frame(self.master)
        actions_frame.pack()

        back_button = tk.Button(actions_frame, text="Geri", command=lambda: self.go_home(show_user_frame))
        back_button.grid(row=0,column=0,columnspan=1,  sticky="NWES")    


        bakiye_total_label = tk.Label(actions_frame, text= f"Şu anki Toplam Müşteri Bakiyesi: {self.dfm.df['müşteri bakiye miktarı'].sum()}")
        bakiye_total_label.grid(row=1, column=0, pady=5)




        sum_next=0
        for t in table.get_children():
            val = table.item(t, 'values')[-1]
            sum_next+=float(val)




        bakiye_total_sonraki_label = tk.Label(actions_frame, text= f"Bu ay kazanılan toplam müşteri Bakiyesi: {sum_next}")
        bakiye_total_sonraki_label.grid(row=2, column=0, pady=5)


        dt_now=datetime.now()            
        dt= datetime(dt_now.year, dt_now.month, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun"))) if dt_now.day>int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun")) else datetime(dt_now.year, dt_now.month-1, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun"))) if dt_now.month!= 1 else datetime(dt_now.year-1, 12, int(self.dfm.sm.currencies_dict.get("f_tahsilat_gun")))


        sum_next=0
        for t in table.get_children():
            val = table.item(t, 'values')[-1]

            if table.item(t, 'values')[-3] == "Hayır":
                sum_next+=float(val)-round(self.dfm.faiz_hesapla(table.item(t, 'values')[-0],dt),1)

        bakiye_basit_odeme_label = tk.Label(actions_frame, text= f"bu ayki ödeme miktarı: {sum_next}")
        bakiye_basit_odeme_label.grid(row=3, column=0, pady=5)


    def delete_warning_popup(self, msg, selected_val):
        popup = tk.Tk()
        popup.wm_title("!")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="SİL", command = lambda : self.dfm.delete_item(selected_val,popup))
        B1.pack()

        # Pencerenin genişliği ve yüksekliği
        width = popup.winfo_width()
        height = popup.winfo_height()

        # Ekranın genişliği ve yüksekliği
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Pencerenin konumu
        x = (screen_width - width) // 2 - 100
        y = (screen_height - height) // 2 -200

        # Pencerenin konumunu ayarlayın
        popup.geometry(f"{200}x{100}+{x}+{y}")

        popup.mainloop()


    def create_odemeler(self,selected_val):


        self.remove_screen()


        odemeler_frame = tk.Frame(self.master)
        odemeler_frame.pack()
        listbox = tk.Listbox(odemeler_frame, height = 10,
                    width = 40,
                    bg = "grey",
                    activestyle = 'dotbox',
                    font = "Helvetica",
                    fg = "white")
        

        json_history = json.loads(str( self.dfm.df.loc[ self.dfm.df['Müşteri Adı'] == str(selected_val)]["History"].values[0]))

        for item in enumerate(json_history.items()):
            listbox.insert(item[0], item[1])
        
    

        tarih_var = tk.StringVar()
        odeme_var = tk.StringVar()
        tarihentry=DateEntry(odemeler_frame,textvariable=tarih_var,locale='tr_TR')
        odemeentry = tk.Entry(odemeler_frame, textvariable=odeme_var)

        B1 = tk.Button(odemeler_frame, text="Öde", command = lambda: self.dfm.odeme_yap(tarih_var.get(),odeme_var.get(),selected_val))
        B2 = tk.Button(odemeler_frame, text="Yatır", command = lambda: self.dfm.yatırma_yap(tarih_var.get(),odeme_var.get(),selected_val))
        B3 = tk.Button(odemeler_frame, text="Faiz Dönüşüm (Basit-Birleşik)", command = lambda: self.dfm.faiz_type_donus(tarih_var.get(),selected_val))
        B4 = tk.Button(odemeler_frame, text="Faiz Miktarı Ayarla", command = lambda: self.dfm.faiz_amount_donus(tarih_var.get(),odeme_var.get(),selected_val))
        B5 = tk.Button(odemeler_frame, text="Sil", command = lambda: self.dfm.odeme_sil(listbox.get(listbox.curselection()[0]),selected_val))
        B6 = tk.Button(odemeler_frame, text="Geri", command = lambda:  self.create_show_user( self.dfm.df))

        listbox.pack()   
        tarihentry.pack()
        odemeentry.pack()

        B1.pack()
        B2.pack()
        B3.pack()
        B4.pack()
        B5.pack()
        B6.pack()


    def create_pairs(self):

        usdtry = tk.StringVar()
        eurtry = tk.StringVar()

        usdtry = tk.StringVar()
        eurtry = tk.StringVar()

        usdtry = tk.StringVar()
        eurtry = tk.StringVar()        


        self.remove_screen()


        canvas = tk.Canvas(self.master)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.master, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        add_pairs_frame = tk.Frame(canvas)

        # Add the frame to the canvas

        screen_width = canvas.winfo_screenwidth()
        screen_height = canvas.winfo_screenheight()
        canvas.create_window((screen_width // 2, 0), window=add_pairs_frame, anchor=tk.N)

        kur_settings_label = tk.Label(add_pairs_frame, text="Kur Ayarları")


        usdtrylabel = tk.Label(add_pairs_frame, text="USD/TRY:")

        
        usdtryentry = tk.Entry(add_pairs_frame, textvariable=usdtry)

        eurtrylabel = tk.Label(add_pairs_frame, text="EUR/TRY:")

        
        eurtryentry = tk.Entry(add_pairs_frame, textvariable=eurtry)

        entry_list={}
        
        counter=0

        for key,value in self.dfm.sm.currencies_dict.items():
            if key.endswith('/USDT'):
                print(key, value)
                
                y = tk.Label(add_pairs_frame, text=f"{key}")

                x=tk.Entry(add_pairs_frame)

                entry_list[key]=x
                y.grid(row=3+counter, column=0,pady=5,sticky="w")
                x.grid(row=3+counter, column=1,pady=5,sticky="w")

                x.insert(0, value)

                counter+=1




        birlesik_faiz_settings_label = tk.Label(add_pairs_frame, text="Faiz Ayarları")

        var = tk.StringVar()
        var.set(str(self.dfm.sm.currencies_dict.get("f_tip")))
        day = tk.StringVar()
        day.set(str(self.dfm.sm.currencies_dict.get("f_ay_gun")))
        tahsilat_day = tk.StringVar()
        tahsilat_day.set(str(self.dfm.sm.currencies_dict.get("f_tahsilat_gun")))


        birlesik_faiz_settings_1 = tk.Radiobutton(add_pairs_frame, variable=var, value="Tip 1", text="Günlüğe Çevirerek hesapla")
        birlesik_faiz_settings_2 = tk.Radiobutton(add_pairs_frame, variable=var, value="Tip 2", text="Tahsilat Tarihine göre hesapla")
        birlesik_faiz_settings_3 = tk.Radiobutton(add_pairs_frame, variable=var, value="Tip 3", text="Tahsilat Tarihi + Günlüğe çevir")



        ay2daylabel = tk.Label(add_pairs_frame,text="Aydaki gün sayısı: ")
        ay2dayentry = tk.Entry(add_pairs_frame,textvariable=day)
        
        ay2daylabel.grid_forget()
        ay2dayentry.grid_forget()

        tahsilattarihlabel = tk.Label(add_pairs_frame,text="Tahsilat Tarihi: ")
        tahsilattarihentry = tk.Entry(add_pairs_frame,textvariable=tahsilat_day)
        
        tahsilattarihlabel.grid_forget()   
        tahsilattarihentry.grid_forget()   

        ay2daylabel2 = tk.Label(add_pairs_frame,text="Aydaki gün sayısı: ")
        ay2dayentry2 = tk.Entry(add_pairs_frame,textvariable=day)
        
        ay2daylabel2.grid_forget()
        ay2dayentry2.grid_forget()

        tahsilattarihlabel2 = tk.Label(add_pairs_frame,text="Tahsilat Tarihi: ")
        tahsilattarihentry2 = tk.Entry(add_pairs_frame,textvariable=tahsilat_day)
        
        tahsilattarihlabel2.grid_forget()   
        tahsilattarihentry2.grid_forget()   


        def show_entry():
            # Show the entry widget when Option 2 is selected, hide it otherwise
            if var.get() == "Tip 1":
                ay2daylabel.grid(row=counter+5,column=0,pady=10,sticky="w")             
                ay2dayentry.grid(row=counter+5,column=1,pady=10,sticky="w") 
            else:
                ay2daylabel.grid_forget()
                ay2dayentry.grid_forget()

            if var.get() == "Tip 2":
                tahsilattarihlabel.grid(row=counter+7,column=0,pady=10,sticky="w")             
                tahsilattarihentry.grid(row=counter+7,column=1,pady=10,sticky="w") 
            else:
                tahsilattarihlabel.grid_forget()   
                tahsilattarihentry.grid_forget()   

            if var.get() == "Tip 3":
                ay2daylabel2.grid(row=counter+9,column=0,pady=10,sticky="w")             
                ay2dayentry2.grid(row=counter+9,column=1,pady=10,sticky="w") 
                tahsilattarihlabel2.grid(row=counter+10,column=0,pady=10,sticky="w")             
                tahsilattarihentry2.grid(row=counter+10,column=1,pady=10,sticky="w")             
            else:
                ay2daylabel2.grid_forget()
                ay2dayentry2.grid_forget()
                tahsilattarihlabel2.grid_forget()
                tahsilattarihentry2.grid_forget()            



        ay2dayentry.update()
        tahsilattarihentry.update()
        ay2dayentry2.update()
        tahsilattarihentry2.update()
        show_entry()

        birlesik_faiz_settings_1.config(command=show_entry)
        birlesik_faiz_settings_2.config(command=show_entry)
        birlesik_faiz_settings_3.config(command=show_entry)


        back_button = tk.Button(add_pairs_frame, text="Back", command=partial(self.go_home,add_pairs_frame))

        save_button = tk.Button(add_pairs_frame, text="Save" , command= lambda:self.dfm.sm.save_currencies(self,usdtry.get(),eurtry.get(),var.get(),day.get(),tahsilat_day.get(),entry_list))


        kur_settings_label.grid(row=0, column=1, columnspan=2,pady=(100,5),sticky="w")
        usdtrylabel.grid(row=1, column=0,pady=5,sticky="w")
        usdtryentry.grid(row=1, column=1,pady=5,sticky="w")
        eurtrylabel.grid(row=2, column=0,pady=5,sticky="w")
        eurtryentry.grid(row=2, column=1,pady=5,sticky="w")



        birlesik_faiz_settings_label.grid(row=counter+3, column=1, columnspan=2,pady=5,sticky="w")
        birlesik_faiz_settings_1.grid(row=counter+4,column=0,columnspan=2,pady=10,sticky="w")    
        birlesik_faiz_settings_2.grid(row=counter+6,column=0,columnspan=2,pady=10,sticky="w")   
        birlesik_faiz_settings_3.grid(row=counter+8,column=0,columnspan=2,pady=10,sticky="w")   

        back_button.grid(row=counter+13,column=0,pady=10,sticky="w")    
        save_button.grid(row=counter+13,column=1,pady=10,sticky="w")    


        eurtryentry.update()
        eurtryentry.insert(0, str(self.dfm.sm.currencies_dict.get("eur/try")))
        usdtryentry.insert(0, str(self.dfm.sm.currencies_dict.get("usd/try")))
        add_pairs_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

