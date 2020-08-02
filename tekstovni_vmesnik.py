import model
import copy

def izpis_igre(igra):
    polje = '=============================================\n'
    for j in range(igra.velikost):
        polje += '\t\t+'
        for i in range(igra.velikost):
            polje += '---+'
        polje += '\n\t\t|'
        for i in range(igra.velikost):
            if igra.polje[j][i]:
                polje += igra.polje[j][i][-1] + '|'
            else:
                polje += '   |'
        polje += '\n'
    polje += '\t\t+'
    for i in range(igra.velikost):
        polje += '---+'
    polje += '   Pieces: {a}  Capstones : {b}'.format(a = igra.ploscki[igra.now_playing][0], b = igra.ploscki[igra.now_playing][1])
    return polje + '\n=============================================\n'

def pozeni_igro():
    backups = []
    velikost = input('Choose board size:')
    while velikost not in ['3','4','5','6','8']:
        print('Invalid board size')
        velikost = input('Choose board size:')
    
    igra = model.Igra(int(velikost))
    print(izpis_igre(igra))
    
    def switch_player():
        if igra.now_playing == 'Black':
            igra.now_playing = 'White'
        else:
            igra.now_playing = 'Black'

    valid_inputs = [f'{i,j}' for i in range(1, igra.velikost + 1) for j in range(1, igra.velikost + 1)]
    def validity_check_input():
        move = input('>>>')
        while move not in valid_inputs:
            print('Invalid input')
            move = input('>>>')
        move = move[1:-1]
        move = move.split(', ')
        move = (int(move[1]) - 1, int(move[0]) - 1)
        return move


    def validity_check_move_piece():
        a, b, c = copy.deepcopy(igra.polje), copy.deepcopy(igra.povezave), copy.deepcopy(igra.ploscki)
        backups.append((a, b, c))
        
        print('Choose piece to move')
        while True:
            start = validity_check_input()
            if igra.je_zasedeno(start) is False:
                print('No pieces to move')
            elif igra.barva_polja(start) != igra.now_playing[0].lower():
                print('You do not own this piece')
            else:
                kupcek = copy.deepcopy(igra.polje[start[0]][start[1]])
                igra.polje[start[0]][start[1]].clear()
                while len(kupcek) > 5:
                    igra.polje[start[0]][start[1]].append(kupcek[0])
                    kupcek.pop(0)
                print(kupcek)
                break

        slovarcek = {'1': (-1, 0), '2': (1, 0), '3': (0, -1), '4': (0, 1)}  
        dovoljen_premik = None
        while kupcek:
            move = validity_check_input()
            if move == start:
                if igra.poteza(kupcek[0][0], start, kupcek[0][2]):
                    print('Invalid move')
                else:
                    kupcek.pop(0)
                    print(izpis_igre(igra))
            for premik in slovarcek.values():
                if move == tuple(map(sum, zip(start, premik))):
                    if igra.poteza(kupcek[0][0], move, kupcek[0][2]):
                        print('Invalid move')
                    else:
                        kupcek.pop(0)
                        start = move
                        dovoljen_premik = premik
                        print(izpis_igre(igra))
                        print(kupcek)
                        break
            
        while kupcek:
            move = validity_check_input()
            if move == start:
                if igra.poteza(kupcek[0][0], start, kupcek[0][2]):
                    print('Invalid move')
                else:
                    kupcek.pop(0)
                    print(izpis_igre(igra))
            elif move == tuple(map(sum, zip(start, dovoljen_premik))):
                if igra.poteza(kupcek[0][0], move, kupcek[0][2]):
                    print('Invalid move')
                else:
                    kupcek.pop(0)
                    start = move
                    print(izpis_igre(igra))
                    print(kupcek)
            else:
                print('Invalid move')
        
    def validity_check_new_piece(ploscek = 'f'):
        a, b, c = copy.deepcopy(igra.polje), copy.deepcopy(igra.povezave), copy.deepcopy(igra.ploscki)
        backups.append((a, b, c))
        
        while True:
            move = validity_check_input()
            if igra.je_zasedeno(move) or igra.poteza(igra.now_playing[0].lower() ,move, ploscek):
                print('Invalid move')
            else:
                if ploscek in ['f', 'w']:
                    igra.ploscki[igra.now_playing] = [igra.ploscki[igra.now_playing][0] - 1, igra.ploscki[igra.now_playing][1]]
                else:
                    igra.ploscki[igra.now_playing] = [igra.ploscki[igra.now_playing][0], igra.ploscki[igra.now_playing][1] - 1]
                break
    
    def izpis_konca_igre(igra):
        if igra.konec_igre():
            if igra.konec_igre() == 'Tie':
                return '-----Tie-----'
            if igra.konec_igre()[1] == 'w':
                return '-----White wins-----'
            if igra.konec_igre()[1] == 'b':
                return '-----Black wins-----'
        else:
            return '-----{color} wins-----'.format(color = igra.now_playing)
    
    #Začetna poteza črni
    print('---Black to open---')
    validity_check_new_piece()
    switch_player()
    print(izpis_igre(igra))
    
    #Začetna poteza beli
    print('---White to open---')
    validity_check_new_piece()
    print(izpis_igre(igra))
    
    while igra.konec_igre() is False:
        Text = '---{colour} to play---\n1. New piece\n2. Move piece\n3. Board state\n4. Undo\n5. Resign'.format(colour = igra.now_playing)
        print(Text)
        izbira = input('>>>')
        while izbira not in ['1','2','3','4','5']:
            izbira = input('>>>')
        
        if izbira == '1':
            if igra.ploscki[igra.now_playing][1] > 0 and igra.ploscki[igra.now_playing][0] > 0:
                print('1. Flat\n2. Wall\n3. Capstone\n4. Cancel')
                izbira2 = input('>>>')
                while izbira2 not in ['1','2','3','4']:
                    izbira2 = input('>>>')
                if izbira2 == '4':
                    print(izpis_igre(igra))
                    continue
                else:
                    slovarcek = {'1': 'f', '2': 'w', '3': 'c'}
                    validity_check_new_piece(slovarcek[izbira2])
                    switch_player()
                    print(izpis_igre(igra))

            elif igra.ploscki[igra.now_playing][0] == 0:
                print('3. Capstone\n4.Cancel')
                izbira2 = input('>>>')
                while izbira2 not in ['3','4']:
                    izbira2 = input('>>>')
                if izbira2 == '4':
                    print(izpis_igre(igra))
                    continue
                else:
                    slovarcek = {'1': 'f', '2': 'w', '3': 'c'}
                    validity_check_new_piece(slovarcek[izbira2])
                    switch_player()
                    print(izpis_igre(igra))

            else:
                print('1. Flat\n2. Wall\n4.Cancel')
                izbira2 = input('>>>')
                while izbira2 not in ['1','2','4']:
                    izbira2 = input('>>>')
                if izbira2 == '4':
                    print(izpis_igre(igra))
                    continue
                else:
                    slovarcek = {'1': 'f', '2': 'w'}
                    validity_check_new_piece(slovarcek[izbira2])
                    switch_player()
                    print(izpis_igre(igra))
        
        elif izbira == '2':
            validity_check_move_piece()
            if igra.polje != backups[-1][0]:
                switch_player()

        elif izbira == '3':
            print('Choose square to show')
            polje = validity_check_input()
            if igra.polje[polje[0]][polje[1]]:
                print(igra.polje[polje[0]][polje[1]])
            else:
                print('This square is empty')
        
        elif izbira == '4':
            if backups:    
                igra.polje, igra.povezave, igra.ploscki = backups[-1][0], backups[-1][1], backups[-1][2]
                backups.pop(-1)
                switch_player()
                print(izpis_igre(igra))
        
        elif izbira == '5':
            switch_player()
            break
    
    print(izpis_konca_igre(igra))
pozeni_igro()