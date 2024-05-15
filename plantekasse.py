#
# Laget av Daniel H. Blomkvist (@blomkvist på Github)
#
#

import argparse

# Dimensjoner på materialer
SPILE_BREDDE = int(23)
SPILE_HØYDE = int(48)
SPILE_LENGDE = int(4200)
LEKT_BREDDE = int(48)
LEKT_HØYDE = int(48)
LEKT_LENGDE = int(4800)
TOPPBORD_BREDDE = int(120)
TOPPBORD_HØYDE = int(28)
TOPPBORD_LENGDE = int(4500)

AVSTAND_EKSTRA_LEKTER_I_BUNN = int(300)

ØNSKET_OVERHENG_TOPPBORD = int(50)

class Lengde:
  def __init__(self, lengde):
      self.lengde = lengde
      self.next   = None

class LengdeListe:
  def __init__(self):
      self.head = None
      self.listelengde = 0

  def leggTilNyLengde(self, lengde):
    ny_lengde = Lengde(lengde)
    self.listelengde += 1

    if self.head is None:
        self.head = ny_lengde
    else:
      current_lengde = self.head
      while(current_lengde.next):
          current_lengde = current_lengde.next

      current_lengde.next = ny_lengde
    print("leggTilNyLengde: La til ny lengde på " + str(lengde) + " mm. Ny listelengde er " + str(self.listelengde))
    return

  def finnMinsteLangNok(self, ønsket_lengde):
    if self.head == None:
        print("finnMinsteLangNok: Ingen element i liste")
        return None

    index = 0
    current_lengde = self.head
    shortest = None

    while(current_lengde != None):
      print("finnMinsteLangNok: Lengde på index " + str(index) + " har lengdefelt " + str(current_lengde.lengde) + " mm, og ønsket lengde er " + str(ønsket_lengde) + " mm")

      if current_lengde.lengde >= ønsket_lengde:
        if shortest == None or current_lengde.lengde < shortest:
          shortest       = current_lengde.lengde
          shortest_index = index
          print("finnMinsteLangNok: Oppdaterte kortest til " + str(shortest) + " på indeks " + str(shortest_index))

      current_lengde = current_lengde.next
      index += 1

    if shortest:
      print("finnMinsteLangNok: returnerer indeks til korteste som er lang nok: " + str(shortest_index))
      return shortest_index
    else:
      print("finnMinsteLangNok: returnerer None fordi ingen som var lang nok ble funnet")
      return None

  def fjernLengde(self, remove_index):
    if self.head == None:
        print("fjernLengde: Ingen element i liste")
        return None

    current_lengde = self.head
    index = 0
    if index == remove_index:
        print("fjernLengde: Fjerner første element i listen")
        self.head  = self.head.next
    else:
        while(current_lengde != None and index + 1 != remove_index):
            current_lengde = current_lengde.next
            index += 1

        if current_lengde != None:
            print("fjernLengde: Fjerner element på indeks " + str(index))
            current_lengde.next = current_lengde.next.next
        else:
          print("fjernLengde: Indeks ble ikke funnet")
          return None

  def kutt(self, kutt_index, kutt_lengde):
    print("kutt: Skal kutte i index " + str(kutt_index) + " og lengden på kuttet er " + str(kutt_lengde) + " mm")
    if self.head == None:
      print("kutt: Ingen element i liste")
      return None

    current_lengde = self.head
    index = 0

    while(current_lengde != None and index != kutt_index):
      current_lengde = current_lengde.next
      index += 1

    if current_lengde != None:
      if kutt_lengde < current_lengde.lengde:
        print("kutt: Ønsket kutt mindre enn lengden til et eksisterende element på indeks " + str(index) +" . Fjerner kuttlengde fra dette elementet.")
        current_lengde.lengde = current_lengde.lengde - kutt_lengde
      elif kutt_lengde == current_lengde.lengde:
        print("kutt: Ønsket kutt identisk med lengden til et eksisterende element på indeks " + str(index) +" . Fjerner elementet.")
        self.fjernLengde(kutt_index)
      else:
        print("kutt: Ønsket kutt lengre enn lengden på lekt/bord")
    else:
      print("kutt: Indeks ble ikke funnet")

    return

  def finnTotalLengde(self):
    if self.head == None:
        return

    current_lengde = self.head
    total_lengde = 0

    while(current_lengde != None):
      total_lengde = total_lengde + current_lengde.lengde
      current_lengde = current_lengde.next

    return total_lengde

  def print(self):
    if self.head == None:
        print("Ingen lengder i liste")
        return

    print("Skriver ut lengder i liste")
    current_lengde = self.head
    index = 0

    while(current_lengde != None):
      print("Lengde " + str(index) + ": " + str(current_lengde.lengde) + " mm")
      current_lengde = current_lengde.next
      index += 1

    return


class Plantekasse:
  def __init__(self, intern_lengde, intern_bredde, intern_høyde):
    self.intern_bredde = intern_bredde
    self.intern_lengde = intern_lengde
    self.intern_høyde  = intern_høyde

    # Lengde på breddelekter er samme som breddeparameter
    # antall breddelekter er alltid 6 (2 oppe og 4 nede) + noen ekstra som støtte nederst avhengig av lengden
    if intern_lengde/AVSTAND_EKSTRA_LEKTER_I_BUNN > 1:
      self.ant_ekstra_lekter_i_bunn = (intern_lengde / AVSTAND_EKSTRA_LEKTER_I_BUNN) - 1
    else:
      self.ant_ekstra_lekter_i_bunn = 0

    self.ant_breddelekter = 6 + self.ant_ekstra_lekter_i_bunn

    # Antall lengdelekter er alltid 4. To oppe og to nede.
    self.ant_lengdelekter = 4

    # Antall høydelekter er alltid 6. Et til hvert hjørne pluss to i midten av lengden.
    self.ant_høydelekter = 6

    self.rammelengde = intern_lengde + 2 * LEKT_BREDDE
    self.rammebredde = intern_bredde + 2 * LEKT_BREDDE
    self.rammehøyde = intern_høyde + LEKT_HØYDE
    self.høydelekter_lengde = intern_høyde - LEKT_HØYDE
    self.lengdespile_lengde = intern_lengde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE
    self.breddespile_lengde = intern_bredde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE


    # Regn ut antallet spiler ut fra høyden. Hver lekt er SPILE_HØYDE høy, og det skal være SPILE_BREDDE gap mellom hver
    self.ant_spiler_i_høyden = 1
    self.høyde_spiler_og_mellomrom = 0

    while self.høyde_spiler_og_mellomrom < intern_høyde:
      if self.høyde_spiler_og_mellomrom + SPILE_HØYDE > intern_høyde:
        # Ikke plass til flere spiler. Gå ut av while-løkke.
        break
      else:
        # Plass til en ny spile.
        self.ant_spiler_i_høyden += 1
        self.høyde_spiler_og_mellomrom = self.høyde_spiler_og_mellomrom + SPILE_HØYDE

        # Legg inn gap før neste spile som er like stort som bredden på ei spile
        if self.høyde_spiler_og_mellomrom + SPILE_BREDDE > intern_høyde:
          # Ikke plass til et fullt gap til neste spile. Gå ut av while-løkke.
          break
        else:
          self.høyde_spiler_og_mellomrom = self.høyde_spiler_og_mellomrom + SPILE_BREDDE

    self.topp_lengde = intern_lengde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE + 2 * ØNSKET_OVERHENG_TOPPBORD
    self.topp_bredde = intern_bredde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE + 2 * ØNSKET_OVERHENG_TOPPBORD
    self.lengde_lekter =  self.ant_lengdelekter * self.rammelengde + int(self.ant_breddelekter) * intern_bredde + self.ant_høydelekter * self.høydelekter_lengde
    self.lengde_spiler = (2 * self.lengdespile_lengde + 2 * self.breddespile_lengde) * self.ant_spiler_i_høyden
    self.lengde_toppbord = 2 * (self.topp_lengde + self.topp_bredde)


    # Lag ei liste over dimensjonene og sorter dem med største først
    dimension_list = [{"bredde": self.intern_bredde, "lengde": self.intern_lengde, "høyde": self.intern_høyde}]
    dimension_list = dict(sorted(dimension_list[0].items(), key=lambda item: item[1], reverse=True))

    # Regn ut hvor mange lengder som trengs av hver type lekt/bord
    self.antall_lekter_nødvendig   = 0
    self.antall_spiler_nødvendig   = 0
    self.antall_toppbord_nødvendig = 0
    self.lekter_liste   = LengdeListe()
    self.spiler_liste   = LengdeListe()
    self.toppbord_liste = LengdeListe()
    for i in dimension_list:
      print(i)
      if i == "bredde":
        # Lekter
        for j in range(int(self.ant_breddelekter)):
          print(str(i) + ": " + str(j))
          # Søk etter minste som er lang nok.
          funnet_index = self.lekter_liste.finnMinsteLangNok(self.intern_bredde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde lekt
            self.lekter_liste.leggTilNyLengde(LEKT_LENGDE)
            # Øk teller på antall lekter nødvendig
            self.antall_lekter_nødvendig += 1
            print("init: Oppdaterte antall lekter nødvendig til " + str(self.antall_lekter_nødvendig))
            # Søk igjen
            funnet_index = self.lekter_liste.finnMinsteLangNok(self.intern_bredde)
          # Utfør kuttet
          self.lekter_liste.kutt(funnet_index, self.intern_bredde)

        # Spiler
        for j in range(2 * self.ant_spiler_i_høyden):
          print(str(i) + ": " + str(j))
          # Søk etter minste som er lang nok.
          funnet_index = self.spiler_liste.finnMinsteLangNok(self.breddespile_lengde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde spile
            self.spiler_liste.leggTilNyLengde(SPILE_LENGDE)
            # Øk teller på antall spiler nødvendig
            self.antall_spiler_nødvendig += 1
            print("init: Oppdaterte antall spiler nødvendig til " + str(self.antall_spiler_nødvendig))
            # Søk igjen
            funnet_index = self.spiler_liste.finnMinsteLangNok(self.breddespile_lengde)
          # Utfør kuttet
          self.spiler_liste.kutt(funnet_index, self.breddespile_lengde)

        # Toppbord
        for j in range(2):
          print(str(i) + ": " + str(j))
          # Søk etter minste som er lang nok.
          funnet_index = self.toppbord_liste.finnMinsteLangNok(self.topp_bredde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde toppbord
            self.toppbord_liste.leggTilNyLengde(TOPPBORD_LENGDE)
            # Øk teller på antall toppbord nødvendig
            self.antall_toppbord_nødvendig += 1
            print("init: Oppdaterte antall toppbord nødvendig til " + str(self.antall_toppbord_nødvendig))
            # Søk igjen
            funnet_index = self.toppbord_liste.finnMinsteLangNok(self.topp_bredde)
          # Utfør kuttet
          self.toppbord_liste.kutt(funnet_index, self.topp_bredde)
      elif i == "lengde":
        # Lekter
        for j in range(self.ant_lengdelekter):
          # Søk etter minste som er lang nok.
          funnet_index = self.lekter_liste.finnMinsteLangNok(self.rammelengde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde lekt
            self.lekter_liste.leggTilNyLengde(LEKT_LENGDE)
            # Øk teller på antall lekter nødvendig
            self.antall_lekter_nødvendig += 1
            print("init: Oppdaterte antall lekter nødvendig til " + str(self.antall_lekter_nødvendig))
            # Søk igjen
            funnet_index = self.lekter_liste.finnMinsteLangNok(self.rammelengde)
          # Utfør kuttet
          self.lekter_liste.kutt(funnet_index, self.rammelengde)
        # Spiler
        for j in range(2 * self.ant_spiler_i_høyden):
          # Søk etter minste som er lang nok.
          funnet_index = self.spiler_liste.finnMinsteLangNok(self.lengdespile_lengde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde lekt
            self.spiler_liste.leggTilNyLengde(SPILE_LENGDE)
            # Øk teller på antall spiler nødvendig
            self.antall_spiler_nødvendig += 1
            print("init: Oppdaterte antall spiler nødvendig til " + str(self.antall_spiler_nødvendig))
            # Søk igjen
            funnet_index = self.spiler_liste.finnMinsteLangNok(self.lengdespile_lengde)
          # Utfør kuttet
          self.spiler_liste.kutt(funnet_index, self.lengdespile_lengde)
        # Toppbord
        for j in range(2):
          # Søk etter minste som er lang nok.
          funnet_index = self.toppbord_liste.finnMinsteLangNok(self.topp_lengde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde toppbord
            self.toppbord_liste.leggTilNyLengde(TOPPBORD_LENGDE)
            # Øk teller på antall toppbord nødvendig
            self.antall_toppbord_nødvendig += 1
            print("init: Oppdaterte antall toppbord nødvendig til " + str(self.antall_toppbord_nødvendig))
            # Søk igjen
            funnet_index = self.toppbord_liste.finnMinsteLangNok(self.topp_lengde)
          # Utfør kuttet
          self.toppbord_liste.kutt(funnet_index, self.topp_lengde)
      else:
        # i == høyde
        for j in range(self.ant_høydelekter):
          # Søk etter minste som er lang nok.
          funnet_index = self.lekter_liste.finnMinsteLangNok(self.høydelekter_lengde)
          if funnet_index == None:
            print("init: fant ikke noen lange nok")
            # Legg til ny full-lengde lekt
            self.lekter_liste.leggTilNyLengde(LEKT_LENGDE)
            # Øk teller på antall lekter nødvendig
            self.antall_lekter_nødvendig += 1
            print("init: Oppdaterte antall lekter nødvendig til " + str(self.antall_lekter_nødvendig))
            # Søk igjen
            funnet_index = self.lekter_liste.finnMinsteLangNok(self.høydelekter_lengde)
          # Utfør kuttet
          self.lekter_liste.kutt(funnet_index, self.høydelekter_lengde)


  def print(self):
    lekter_dim_str = str(LEKT_BREDDE) + "x" + str(LEKT_HØYDE)
    spiler_dim_str = str(SPILE_BREDDE) + "x" + str(SPILE_HØYDE)
    toppbord_dim_str = str(TOPPBORD_BREDDE) + "x" + str(TOPPBORD_HØYDE)

    print("*************************************************")
    print("\tSpesifikasjon for plantekasse")
    print("*************************************************")
    print("Innvendige mål (LxBxH): " + str(self.intern_lengde) + "x" + str(self.intern_bredde) + "x" + str(self.intern_høyde))
    print("Utvendige mål på ramme uten spiler (LxBxH): " + str(self.rammelengde) + "x" + str(self.rammebredde) + "x" + str(self.rammehøyde))
    print("Utvendige mål på ramme med påmonterte spiler (LxBxH): " + str(self.rammelengde + 2*SPILE_BREDDE) + "x" + str(self.rammebredde + 2*SPILE_BREDDE) + "x" + str(self.rammehøyde))
    print("\n")
    print("Lengdelekter (" + lekter_dim_str + "): " + str(self.ant_lengdelekter) + " lekter á " + str(self.rammelengde) + " mm")
    print("Breddelekter (" + lekter_dim_str + "): " + str(int(self.ant_breddelekter)) + " lekter á " + str(self.intern_bredde) + " mm")
    print("Høydelekter (" + lekter_dim_str + "): " + str(self.ant_høydelekter) + " lekter á " + str(self.høydelekter_lengde) + " mm")
    print("\n")
    print("Ordinært antall breddelekter (" + lekter_dim_str + ") i bunn: 4 (to på hver ende i lengden). Antall breddelekter (" + lekter_dim_str + ") i topp: 2")
    print("Antall ekstra lekter (" + lekter_dim_str + ") i bunn: " + str(int(self.ant_ekstra_lekter_i_bunn)))
    print("\n")
    print("Spiler blir montert fra bunn mot topp, og første spile blir montert på utsiden av nederste lekt på rammen. Mellomrom mellom spiler er lik bredden av ei spile (" + str(SPILE_BREDDE) + " mm).")
    print("Antall spiler i høyden: " + str(self.ant_spiler_i_høyden))
    print("Høyde på spiler og mellomrom: " + str(self.høyde_spiler_og_mellomrom) + " mm")
    print("\n")
    print("Lengdespiler (" + spiler_dim_str + "): " + str(2 * self.ant_spiler_i_høyden) + " spiler á " + str(self.lengdespile_lengde) + " mm")
    print("Breddespiler (" + spiler_dim_str + "): " + str(2 * self.ant_spiler_i_høyden) + " spiler á " + str(self.breddespile_lengde) + " mm")
    print("\n")
    print("Toppbord (" + toppbord_dim_str + ") ønsket overheng: " + str(ØNSKET_OVERHENG_TOPPBORD) + " mm")
    print("Toppbord (" + toppbord_dim_str + ") lengde: 2 bord á " + str(self.topp_lengde) + " mm")
    print("Toppbord (" + toppbord_dim_str + ") bredde: 2 bord á " + str(self.topp_bredde) + " mm")
    print("\n")
    print("Totale lengder:")
    print(lekter_dim_str + ": " + str(int(self.lengde_lekter)) + " mm")
    print(spiler_dim_str + ": " + str(self.lengde_spiler) + " mm")
    print(toppbord_dim_str + ": " + str(self.lengde_toppbord) + " mm")
    print("\n")
    print("Antall lekter nødvendig av ulike dimensjoner:")
    print(lekter_dim_str + ": " + str(self.antall_lekter_nødvendig) + " á " + str(LEKT_LENGDE) + " mm")
    print(spiler_dim_str + ": " + str(self.antall_spiler_nødvendig) + " á " + str(SPILE_LENGDE) + " mm")
    print(toppbord_dim_str + ": " + str(self.antall_toppbord_nødvendig) + " á " + str(TOPPBORD_LENGDE) + " mm")
    print("\n")
    print("Rest av lekter:")
    self.lekter_liste.print()
    print("\n")
    print("Rest av spiler:")
    self.spiler_liste.print()
    print("\n")
    print("Rest av toppbord:")
    self.toppbord_liste.print()


def main():
  parser = argparse.ArgumentParser(
                      prog='Plantekasse',
                      description='Regner ut hvor mye material man trenger til en plantekasse ut fra ønskede indre dimensjoner. Alle mål i mm.',
                      epilog='Dette er slutten paa hjelpeteksten')
  parser.add_argument('-x', '--lengde', type=int, help='Ønsket intern lengde i millimeter')
  parser.add_argument('-y', '--bredde', type=int, help='Ønsket intern bredde i millimeter')
  parser.add_argument('-z', '--høyde', type=int, help='Ønsket intern høyde i millimeter')

  args = parser.parse_args()

  plantekasse = Plantekasse(args.lengde, args.bredde, args.høyde)
  plantekasse.print()

if __name__ == "__main__":
    main()
