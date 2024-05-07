#
# Laget av Daniel H. Blomkvist (@blomkvist på Github)
#
#

import argparse

# Dimensjoner på materialer
SPILE_BREDDE = int(23)
SPILE_HØYDE = int(48)
LEKT_BREDDE = int(48)
LEKT_HØYDE = int(48)
TOPPBORD_BREDDE = int(148)
TOPPBORD_HØYDE = int(19)

AVSTAND_EKSTRA_LEKTER_I_BUNN = int(300)

ØNSKET_OVERHENG_TOPPBORD = int(50)

class Plantekasse:
  def __init__(self, intern_lengde, intern_bredde, intern_høyde):
    self.intern_bredde = intern_bredde
    self.intern_lengde = intern_lengde
    self.intern_høyde = intern_høyde

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
        self.ant_spiler_i_høyden = self.ant_spiler_i_høyden + 1
        self.høyde_spiler_og_mellomrom = self.høyde_spiler_og_mellomrom + SPILE_HØYDE

        # Legg inn gap før neste spile som er like stort som bredden på ei spile
        if self.høyde_spiler_og_mellomrom + SPILE_BREDDE > intern_høyde:
          # Ikke plass til et fullt gap til neste spile. Gå ut av while-løkke.
          break
        else:
          self.høyde_spiler_og_mellomrom = self.høyde_spiler_og_mellomrom + SPILE_BREDDE

    self.topp_lengde = intern_lengde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE + 2 * ØNSKET_OVERHENG_TOPPBORD
    self.topp_bredde = intern_bredde + 2 * LEKT_BREDDE + 2 * SPILE_BREDDE + 2 * ØNSKET_OVERHENG_TOPPBORD
    self.lengde_lekter =  self.ant_breddelekter * self.rammebredde + int(self.ant_breddelekter) * intern_bredde + self.ant_høydelekter * self.høydelekter_lengde
    self.lengde_spiler = (2 * self.lengdespile_lengde + 2 * self.breddespile_lengde) * self.ant_spiler_i_høyden
    self.lengde_toppbord = 2 * (self.topp_lengde + self.topp_bredde)

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
