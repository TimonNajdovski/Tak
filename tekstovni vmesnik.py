import model

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
    return polje + '\n=============================================\n'

def izpis_konca_igre(igra):
    if igra.konec_igre[1] == 'w':
        return 'White wins'
    if igra.konec_igre[1] == 'b':
        return 'Black wins'

def pozeni_igro():
    velikost = input('Choose board size:')
    while velikost not in ['3','4','5','6','8']:
        print('Invalid board size')
        velikost = input('Choose board size:')
    
    igra = model.Igra(int(velikost))
    print(izpis_igre(igra))
    
    Now_playing = 'Black'
    def switch_player():
        nonlocal Now_playing
        if Now_playing == 'Black':
            Now_playing = 'White'
        else:
            Now_playing = 'Black'

    valid_inputs = [f'{i,j}' for i in range(1,9) for j in range(1,9)]
    def validity_check_new_piece():
        Text = '{color} to play:'.format(color = Now_playing)
        while True:
            move = input(Text)
            while move not in valid_inputs:
                print('Invalid input')
                move = input(Text)
            move = move[1:-1]
            move = move.split(', ')
            move = (int(move[1]) - 1, int(move[0]) - 1)

            if igra.je_zasedeno(move) or igra.poteza(Now_playing[0].lower() ,move, 'f'):
                print('Invalid move')
            else:
                break
    
    #Začetna poteza črni
    validity_check_new_piece()
    switch_player()
    print(izpis_igre(igra))
    
    #Začetna poteza beli
    validity_check_new_piece()
    print(izpis_igre(igra))