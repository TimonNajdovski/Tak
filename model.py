INVALID_MOVE = 'X'

class Igra:
    
    def __init__(self, velikost):
            self.velikost = velikost
            Polje = []
            for i in range(velikost):
                Vrstica = []
                for j in range(velikost):
                    Vrstica.append([])
                Polje.append(Vrstica)
            self.polje = Polje
            self.povezave = []
    
    def barva_polja(self, mesto):
        return self.polje[mesto[0]][mesto[1]][-1][0]

    def vrsta_ploscka(self, mesto):
        return self.polje[mesto[0]][mesto[1]][-1][-1]

    def opremi_z_barvo(self, mesto):
        if self.polje[mesto[0]][mesto[1]]:
            return (mesto[0],mesto[1],self.barva_polja(mesto))
    
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
    
    def update_povezave(self):
        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.polje[i][j] and self.vrsta_ploscka((i,j)) != 'w':
                    if self.povezave == []:
                        self.povezave.append([self.opremi_z_barvo((i,j))])
                    else:
                        ze_povezani = [mesto for povezava in self.povezave for mesto in povezava]
                        if self.opremi_z_barvo((i,j)) in ze_povezani:
                            break
                        elif not set(self.sosednja_mesta((i,j))).intersection(set(ze_povezani)):
                            self.povezave.append([self.opremi_z_barvo((i,j))])
                        else:
                            for povezava in self.povezave:
                                for sosed in self.sosednja_mesta((i,j)):                                
                                    if sosed in povezava:
                                        povezava.append(self.opremi_z_barvo((i,j)))
                                        break
                            
                            
                        
    def nov_ploscek(self, barva, mesto, ploscek):
        polje = self.polje[mesto[0]][mesto[1]]
        if max(mesto) - 1 > self.velikost:
            return INVALID_MOVE
        if polje:    
            if polje[-1][-1] in ['c', 'w']:
                return INVALID_MOVE
        polje.append(barva + '_' + ploscek)

    def premik_ploscka(self, barva, mesto, cilj):
        return True