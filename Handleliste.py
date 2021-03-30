from tkinter import *
import pymysql
from datetime import datetime

handlelisteDB = pymysql.connect(host='localhost', port=3306, user='Bruker', passwd='handleliste', db='Handleliste')

def ny_handleliste():
    def ny_liste():

        ny_handleliste_markor = handlelisteDB.cursor()
        ny_handleliste_markor.execute('SELECT * FROM Handleliste')
        #Variable for automatisk ID.
        handlelisteID = 999
        #Gir automatisk ID.
        for row in ny_handleliste_markor:
            handlelisteID = handlelisteID + 1

        ny_handlelisteID = handlelisteID
            
        handleliste_navn = navn.get()
            
        regdato = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sett_inn_handleliste = ('INSERT INTO Handleliste'
                           '(HandlelisteID, HandlelisteNavn, HandlelisteReg)'
                           'VALUES(%s, %s, %s)')
        ny_data_handleliste = (ny_handlelisteID, handleliste_navn, regdato)
        ny_handleliste_markor.execute(sett_inn_handleliste, ny_data_handleliste)
        handlelisteDB.commit()

        ny_handleliste_markor.close()

    ny_handleliste = Toplevel()
    ny_handleliste.title('Registrer ny handleliste')

    #Labler
    lbl_navn = Label(ny_handleliste, text='Handlelistenavn:')
    lbl_navn.grid(row=0, column=0, padx=(58, 0), pady=(30, 10), sticky=E)

    #Entry
    navn = StringVar()
    ent_navn = Entry(ny_handleliste, width=13, textvariable=navn)
    ent_navn.grid(row=0, column=1, padx=5, pady=(30, 5), sticky=W)

    #Button
    btn_registrer = Button(ny_handleliste, text='Registrer ny handleliste', command=lambda:[ny_liste(), ny_handleliste.destroy()])
    btn_registrer.grid(row=1, column=1, padx=10, pady=30, sticky=W)

    btn_tilbake = Button(ny_handleliste, text='Tilbake til hovedvinduet', command=ny_handleliste.destroy)
    btn_tilbake.grid(row=4, column=5, padx=(20, 10), pady=10, sticky=SE)

def oversikt_handlelister():
    def oversikt_lister():
        #Fyller listen med info fra siste redigerte liste
        oversikt_markor = handlelisteDB.cursor()
        oversikt_markor.execute('SELECT * FROM Handleliste.Handleliste ORDER BY HandlelisteReg DESC')

        oversikt = []

        for row in oversikt_markor:
            oversikt += [row[1]]
            innhold_lst_oversikt.set(tuple(oversikt))

        oversikt_markor.close()

    oversikt_handlelister = Toplevel()
    oversikt_handlelister.title('Oversikt handlelister')

    #Scrollbar
    y_scroll = Scrollbar(oversikt_handlelister, orient=VERTICAL)
    y_scroll.grid(row=1, column=3, rowspan=10, padx=(0, 30), pady=(0, 30), sticky=NS)

    #Listeboks
    innhold_lst_oversikt = StringVar()
    lst_oversikt = Listbox(oversikt_handlelister, width=43, height=18, listvariable=innhold_lst_oversikt,
                        yscrollcommand=y_scroll.set)
    lst_oversikt.grid(row=1, column=0, columnspan=3, rowspan=10, padx=(60, 0), pady=(0, 30), sticky=E)
    y_scroll['command'] = lst_oversikt.yview

    #Kaller på listen for at listen skal få informasjon
    oversikt_lister()

    #Label
    lbl_overskrift = Label(oversikt_handlelister, text='Oversikt over alle handlelistene sortert på dato:')
    lbl_overskrift.grid(row=0, column=0, columnspan=2, padx=(58, 0), pady=(30, 10), sticky=W)

    #Button
    btn_tilbake = Button(oversikt_handlelister, text='Tilbake til hovedvinduet', command=oversikt_handlelister.destroy)
    btn_tilbake.grid(row=11, column=5, padx=(20, 10), pady=10, sticky=SE)


def main():
    def sist_reg_liste():
        #Fyller listen med varer
        sist_reg_markor = handlelisteDB.cursor()
        sist_reg_markor.execute('SELECT * FROM Handleliste.Vare')

        sist_reg = []

        for row in sist_reg_markor:
            sist_reg += [row[0]]
            innhold_lst_sist_reg.set(tuple(sist_reg))

        sist_reg_markor.close()

    def ny_vare():
        ny_vare_markor = handlelisteDB.cursor()
        ny_vare_markor.execute('SELECT * FROM Handleliste')

        vare_navn = varenavn.get()

        ny_listeID = 999
        
        sett_inn_vare = ('INSERT INTO Vare'
                       '(VareNavn, HandlelisteID)'
                       'VALUES(%s, %s)')
        ny_data_vare = (vare_navn, ny_listeID)
        ny_vare_markor.execute(sett_inn_vare, ny_data_vare)
        handlelisteDB.commit()

        varenavn.set('')

        ny_vare_markor.close()
        
    hovedvinduet = Tk()
    hovedvinduet.title('Handleliste')

    #Button
    btn_ny_handleliste = Button(hovedvinduet, text='Ny handleliste', command=ny_handleliste)
    btn_ny_handleliste.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    btn_oversikt_handlelister = Button(hovedvinduet, text='Oversikt handlelister', command=oversikt_handlelister)
    btn_oversikt_handlelister.grid(row=0, column=3, padx=30, pady=5, sticky=W)
    btn_registrer = Button(hovedvinduet, text='Registrer ny vare', command=lambda:[ny_vare(), sist_reg_liste()])
    btn_registrer.grid(row=8, column=2, padx=1, pady=(30, 10), sticky=W)
    
    btn_avslutt = Button(hovedvinduet, text='Avslutt program', command=hovedvinduet.destroy)
    btn_avslutt.grid(row=13, column=3, padx=(80, 10), pady=(30, 10), sticky=SE)

    #Entry
    varenavn = StringVar()
    ent_varenavn = Entry(hovedvinduet, width=13, textvariable=varenavn)
    ent_varenavn.grid(row=8, column=1, padx=5, pady=(30, 5), sticky=W)

    #Label
    lbl_sist_reg = Label(hovedvinduet, text='Sist redigerte handleliste:', font='TkHeadingFont 12 bold italic')
    lbl_sist_reg.grid(row=1, column=1, padx=30, pady=(30, 5), sticky=W)
    lbl_varenavn = Label(hovedvinduet, text='Registrer ny vare:')
    lbl_varenavn.grid(row=8, column=0, padx=(0, 0), pady=(30, 10), sticky=E)

    #Scrollbar
    y_scroll = Scrollbar(hovedvinduet, orient=VERTICAL)
    y_scroll.grid(row=3, column=2, rowspan=3, padx=(0, 30), pady=(0, 30), sticky=NS)

    #Listeboks
    innhold_lst_sist_reg = StringVar()
    lst_sist_reg = Listbox(hovedvinduet, width=30, height=18, listvariable=innhold_lst_sist_reg,
                        yscrollcommand=y_scroll.set, selectmode=MULTIPLE)
    lst_sist_reg.grid(row=3, column=0, columnspan=3, rowspan=3, padx=(30, 0), pady=(0, 30), sticky=NS)
    y_scroll['command'] = lst_sist_reg.yview

    #Kaller på listen for at listen skal få informasjon
    sist_reg_liste()

    hovedvinduet.mainloop()
    handlelisteDB.close()


main()
