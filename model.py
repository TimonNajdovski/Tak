INVALID_MOVE = 'X'

class Igra:
    
    def __init__(self, velikost):
            slovar_plosckov = {3: [10, 0], 4: [15, 0], 5: [21, 1], 6: [30, 1], 8: [50, 2]}
            self.velikost = velikost
            self.ploscki = {'White': slovar_plosckov[velikost], 'Black': slovar_plosckov[velikost]}
            Polje = []
            for i in range(velikost):
                Vrstica = []
                for j in range(velikost):
                    Vrstica.append([])
                Polje.append(Vrstica)
            self.polje = Polje
            self.povezave = []
    
    def barva_polja(self, mesto):
        if self.polje[mesto[0]][mesto[1]]:
            return self.polje[mesto[0]][mesto[1]][-1][0]

    def vrsta_ploscka(self, mesto):
        if self.polje[mesto[0]][mesto[1]]:
            return self.polje[mesto[0]][mesto[1]][-1][-1]

    def opremi_z_barvo(self, mesto):
        if self.polje[mesto[0]][mesto[1]]:
            return (mesto[0],mesto[1],self.barva_polja(mesto))

    def je_zasedeno(self, mesto):
        return bool(self.polje[mesto[0]][mesto[1]])
    
    def sosednja_mesta(self, mesto):
        sosedi = []
        for i in [-1, 1]:
            sosed = (mesto[0] + i, mesto[1])
            if sosed[0] not in [-1, self.velikost]:
                if self.opremi_z_barvo(sosed) and self.barva_polja(mesto) == self.barva_polja(sosed):
                    sosedi.append(self.opremi_z_barvo(sosed))
        for i in [-1, 1]:
            sosed = (mesto[0], mesto[1] + i)
            if sosed[1] not in [-1, self.velikost]:
                if self.opremi_z_barvo(sosed) and self.barva_polja(mesto) == self.barva_polja(sosed):
                        sosedi.append(self.opremi_z_barvo(sosed))
        return sosedi

    def ustvari_povezave(self):
        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.polje[i][j] and self.vrsta_ploscka((i,j)) != 'w':
                    if self.povezave == []:
                        self.povezave.append([self.opremi_z_barvo((i,j))])
                    else:
                        ze_povezani = [mesto for povezava in self.povezave for mesto in povezava]
                        if self.opremi_z_barvo((i,j)) not in ze_povezani:
                            if not set(self.sosednja_mesta((i,j))).intersection(set(ze_povezani)):
                                self.povezave.append([self.opremi_z_barvo((i,j))])                            
                            else:
                                for povezava in self.povezave:
                                    for sosed in self.sosednja_mesta((i,j)):                                
                                        if sosed in povezava:
                                            povezava.append(self.opremi_z_barvo((i,j)))
                                            break

    def update_povezave(self):
        self.ustvari_povezave()
        output = []
        while len(self.povezave) > 0:
            prva, *ostale = self.povezave
            prva = set(prva)
            if ostale:
                for povezava in ostale:
                    ostale2 = []
                    if len(prva.intersection(set(povezava))) > 0:
                        prva |= set(povezava)
                    else:
                        ostale2.append(povezava)
                output.append(list(prva))
                self.povezave = ostale2
            else:
                output.append(list(prva))
                self.povezave.clear()
        self.povezave = output
        self.ustvari_povezave()

    def konec_igre(self):
        def robni_ploscek(mesto):
            robovi = []
            if mesto[0] == 0:
                robovi.append('zgornji')
            if mesto[0] == self.velikost - 1:
                robovi.append('spodnji')
            if mesto[1] == 0:
                robovi.append('levi')
            if mesto[1] == self.velikost - 1:
                robovi.append('desni')
            return robovi
        for povezava in self.povezave:
            robni = [povezava[0][-1]]
            for mesto in povezava:
                for rob in robni_ploscek(mesto):
                    robni.append(rob)
            if 'zgornji' in robni and 'spodnji' in robni:
                return (True, robni[0])
            elif 'levi' in robni and 'desni' in robni:
                return (True, robni[0])
        return False

    def poteza(self, barva, mesto, ploscek):
        
        #validity test
        if max(mesto) - 1 > self.velikost:
            return INVALID_MOVE
        polje = self.polje[mesto[0]][mesto[1]]
        if polje:    
            if ploscek != 'c':
                if polje[-1][-1] in ['c', 'w']:
                    return INVALID_MOVE
            else:
                if polje[-1][-1] == 'c':
                    return INVALID_MOVE

        #prekinitev povezave
        if polje and (barva != self.barva_polja(mesto) or ploscek == 'w'):
            for povezava in self.povezave:
                if self.opremi_z_barvo(mesto) in povezava:
                    self.povezave.remove(povezava)
    
        #združitev povezav
        seznam_sosednjih_povezav = []
        for sosed in self.sosednja_mesta(mesto):
            for povezava in self.povezave:
                if sosed in povezava and povezava not in seznam_sosednjih_povezav:
                    seznam_sosednjih_povezav.append(povezava)
        if len(seznam_sosednjih_povezav) > 1:
            for povezava in seznam_sosednjih_povezav:
                self.povezave.remove(povezava)

        if all([polje, self.vrsta_ploscka(mesto) == 'w', ploscek == 'c']):
            polje[-1] = polje[-1][:-1] + 'f'
        polje.append(barva + '_' + ploscek)
        self.update_povezave()