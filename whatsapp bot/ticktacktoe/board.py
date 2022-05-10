class Board:

    board=[[f'{i+(j*3)}' for i in range(1,4)] for j in range(3)]
    moves=0
    game_state='C'

    def __init__(self) -> None:
        pass

    def check_for_win(self, letter):
        player=letter
        
        for i in range(3):
            winning=True
            for j in self.board[i]:
                if j!=player:
                    winning=False
                    break
            if winning:
                self.game_state=player
                return True
        
        for i in range(3):
            winning=True
            for j in self.board:
                if j[i]!=player:
                    winning=False
                    break
            if winning:
                self.game_state=player
                return True
        
        if self.board[0][0]==self.board[1][1]==self.board[2][2]==player:
            self.game_state=player
            return True
            
        if self.board[0][2]==self.board[1][1]==self.board[2][0]==player:
            self.game_state=player
            return True

        if self.moves>=9:
            self.game_state='D'
            return True
    
    def check_move(self, num):
        try:
            num=int(num)

        except:
            return 'Please do not enter a letter. Enter a number available in the board'

        x=num%3-1
        y=num//3
        if x==-1:
            y=y-1

        if num>9 or num<1:
            return 'Please enter a number between and including 1 to 9 available in the board'

        # print(self.board[y][x])
        if self.board[y][x]=='X' or self.board[y][x]=='O':
            return 'Please enter a number available in the board'
        
        return 'True'
    
    def pBoard(self):
        
        li =[f'{self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}',
        '---------',
        f'{self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}',
        '---------',
        f'{self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}',]
        return(li)

    def input_move(self,num, letter):
        self.moves+=1
        x=num%3-1
        y=num//3
        if x==-1:
            y=y-1
        # print(f'{x} y-{y}')
        self.board[y][x]=letter

    def reset_board(self):
        self.board=[[f'{i+(j*3)}' for i in range(1,4)] for j in range(3)]
        self.moves=0
        self.game_state='C'


