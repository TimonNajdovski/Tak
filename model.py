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
    
    def sosednja_mesta(self, mesto):
        sez = []
        for i in [-1, 1]:
            sosed = (mesto[0] + i, mesto[1])
            if sosed[0] not in [-1, self.velikost]:
                    sez.append(sosed)
        for i in [-1, 1]:
            sosed = (mesto[0], mesto[1] + i)
            if sosed[1] not in [-1, self.velikost]:
                sez.append(sosed)
        return sez
        
    def barva_polja(self, mesto):
        if self.polje[mesto[0]][mesto[1]]:
            return self.polje[mesto[0]][mesto[1]][-1][0]
    
    slovar_povezav = {}
    def povezave(self):
        for i in range(self.velikost):
            for j in range(self.velikost):
                

    def nov_ploscek(self, barva, mesto, ploscek):
        polje = self.polje[mesto[0]][mesto[1]]
        if max(mesto) - 1 > self.velikost:
            return INVALID_MOVE
        if polje:    
            if polje[-1][-1] in ['c', 'w']:
                return INVALID_MOVE
        polje.append(barva + '_' + ploscek)

    def premik_ploscka(self, barva, mesto):
        return True
a = Igra(3)