import random

My = False
Op = True

class card:
	global name
	global ATK
	global DEF
	global STANCE
	global ATTACKED
	def __init__(self,name,ATK,DEF,stance=-1):
		self.name = name
		self.ATK = ATK
		self.DEF = DEF
		self.STANCE = stance
		self.ATTACKED = False

class game_field:
	global BATTLE_FIELD
	global TRAP_FIELD
	global OMOTE_KOUGEKI
	global OMOTE_SYUBI
	global URA_SYUBI
	def __init__(self):
		self.NOTHING = False
		self.OMOTE_KOUGEKI = 0
		self.OMOTE_SYUBI = 1
		self.URA_SYUBI = 2
		self.BATTLE_FIELD	= [self.NOTHING,self.NOTHING,self.NOTHING,self.NOTHING,self.NOTHING]
		self.TRAP_FIELD		= [self.NOTHING,self.NOTHING,self.NOTHING,self.NOTHING,self.NOTHING]

	def put_card(self,index,card):
		self.BATTLE_FIELD[index] = card

	def change_card_stance(self,index,stance):
		self.BATTLE_FIELD[index].STANCE = stance

	def remove_card(self,index):
		self.BATTLE_FIELD[index] = self.NOTHING

	def show_game_field(self):
		for i in range(5):
			if self.BATTLE_FIELD[i] == False:
				print("{}:".format(i))
			elif self.BATTLE_FIELD[i].STANCE == 0 or self.BATTLE_FIELD[i].STANCE == 1: #表攻撃か表守備
				print("{}:{} ATK{} DEF{}".format(i,self.BATTLE_FIELD[i].name,self.BATTLE_FIELD[i].ATK,self.BATTLE_FIELD[i].DEF))
			else:
				print("{}:裏守備 ATK??? DEF???".format(i))
			
	def reset_card(self):
		indexes = self.get_existcard_indexes()
		for i in indexes:
			self.BATTLE_FIELD[i].ATTACKED = False

	def is_field_empty(self):
		return len(self.get_existcard_indexes()) == 0

	def is_there_card_can_attack(self):
		for b in self.BATTLE_FIELD:
			if (not b is self.NOTHING) and (not b.ATTACKED):
				return True
		return False

	def is_field_full(self):
		return len(self.get_existcard_indexes()) == 5

	def get_card_can_attack_op_indexes(self):
		indexes = []
		for j in range(5):
			if (self.BATTLE_FIELD[j] != self.NOTHING) and not(self.BATTLE_FIELD[j].ATTACKED):
				indexes.append(j)
		return indexes

	def get_existcard_indexes(self):
		indexes = []
		for j in range(5):
			if self.BATTLE_FIELD[j] != self.NOTHING:
				indexes.append(j)
		return indexes

	def get_most_nonpower_card_index(self):
		indexes = self.get_existcard_indexes()
		min_ = 50000
		retval = -1
		for i in indexes:
			if self.BATTLE_FIELD[i].ATK < min_:
				min_ = self.BATTLE_FIELD[i].ATK
				retval = i
		return retval

class game:
	global LIFE
	global FIELD
	global OPERATE
	global OPPONENT_DECK
	global OPPONENT_HAND_CARDS
	def __init__(self,My,Op):
		self.LIFE = [8000,8000]
		self.FIELD = [game_field(),game_field()]
		self.OPERATE = [My,Op]
		self.first_turn = True

	def check_and_show_life(self):
		if (self.LIFE[0] < 0):
			print("YOU LOSE...")
			exit(0)
		if (self.LIFE[1] < 0):
			print("YOU WIN!")
			exit(0)
		print("ME:{} / OP:{}".format(self.LIFE[0],self.LIFE[1]))

	def run(self):
		T = False
		while(True):
			self.turn(T)
			T = not(T)


	def turn(self,TURN):
		index__,card__ = self.OPERATE[TURN].PUT_PHASE(self.FIELD[TURN])
		if index__ != None:
			self.FIELD[TURN].put_card(index__,card__)
			print("-----OP------")
			self.FIELD[True].show_game_field()
			print("-----ME------")
			self.FIELD[False].show_game_field()
			print("\n\n")

		while(not(self.first_turn) and self.FIELD[TURN].is_there_card_can_attack()):
			turnCid,opCid = self.OPERATE[TURN].BATTLE_PHASE(self.FIELD[TURN],self.FIELD[not(TURN)],)
			if turnCid == None:
				break
			self.FIELD[TURN].BATTLE_FIELD[turnCid].ATTACKED = True
			self.FIELD[TURN].BATTLE_FIELD[turnCid].STANCE = 0
			if self.FIELD[not(TURN)].is_field_empty():
				self.FIELD[TURN].BATTLE_FIELD[turnCid].STANCE = 0
				self.LIFE[not(TURN)]-=self.FIELD[TURN].BATTLE_FIELD[turnCid].ATK #相手ライフから攻撃カードの攻撃力引く
			else:
				if self.FIELD[not(TURN)].BATTLE_FIELD[opCid].STANCE >= 1:
					diff = self.FIELD[not(TURN)].BATTLE_FIELD[opCid].DEF - self.FIELD[TURN].BATTLE_FIELD[turnCid].ATK
					self.FIELD[not(TURN)].BATTLE_FIELD[opCid].STANCE = 1
					if diff < 0:
						self.FIELD[not(TURN)].remove_card(opCid) #モンスター削除
					if diff > 0:
						self.LIFE[TURN] = self.LIFE[TURN] - diff #自分ライフから攻撃差分引く
				else:
					self.FIELD[TURN].BATTLE_FIELD[turnCid].STANCE = 0
					diff = self.FIELD[not(TURN)].BATTLE_FIELD[opCid].ATK - self.FIELD[TURN].BATTLE_FIELD[turnCid].ATK
					if diff < 0:
						self.LIFE[not(TURN)] = self.LIFE[not(TURN)] + diff #相手ライフから攻撃差分引く
						self.FIELD[not(TURN)].remove_card(opCid) #モンスター削除
					if diff > 0:
						self.LIFE[TURN] = self.LIFE[TURN] - diff #自分ライフから攻撃差分引く
						self.FIELD[TURN].remove_card(turnCid) #モンスター削除
					if diff == 0:
						self.FIELD[not(TURN)].remove_card(opCid) #モンスター削除
						self.FIELD[TURN].remove_card(turnCid) #モンスター削除
			self.check_and_show_life()

			print("-----OP------")
			self.FIELD[True].show_game_field()
			print("-----ME------")
			self.FIELD[False].show_game_field()
			print("\n\n")


		self.first_turn = False
		self.check_and_show_life()

class MyOPE:
	def __init__(self):
		pass

	def PUT_PHASE(self,FIELD):
		if input("召喚した？>") != "y":
			return None,None

		if not(FIELD.is_field_full()):
			FIELD_index = FIELD.BATTLE_FIELD.index(False)
		else:
			FIELD_index = int(input("何番目に置くか選択してくれ(0~4)>"))
		
		ATK = int(input("ストレングス>"))
		st = int(input("表攻撃(0),裏守備(2)？>"))	
		return FIELD_index,card("召喚カード",ATK,ATK,stance=st)

	def BATTLE_PHASE(self,MY_FIELD,OP_FIELD):
		xorint = input("攻撃するカードの番号を選択してください(しない場合はx)>")
		if xorint == "x":
			return None,None
		my_card_index = int(xorint)
		if OP_FIELD.is_field_empty(): 
			return my_card_index,0
		else:
			op_card_index = int(input("攻撃する相手のカードの番号を選択してください>"))
			return my_card_index,op_card_index

class OpOPE:
	def __init__(self,DECK):		
		self.deck = []
		for d in DECK:
			self.deck.append(card(d[0],int(d[1]),int(d[2])))
		self.hand_cards = []
		for i in range(5):
			self.hand_cards.append(self.deck.pop(0))

	def PUT_PHASE(self,FIELD):
		rnd = random.randint(0,4)
		card = self.hand_cards.pop(rnd)
		self.hand_cards.append(self.deck.pop(0))

		if not(FIELD.is_field_full()):
			FIELD_index = FIELD.BATTLE_FIELD.index(False)
		else:
			FIELD_index = random.randint(0,4)
		if card.ATK > card.DEF:
			card.STANCE = 0
		else:
			card.STANCE = 2		

		return FIELD_index,card

	def BATTLE_PHASE(self,MY_FIELD,OP_FIELD):
		indexes = MY_FIELD.get_card_can_attack_op_indexes()
		for i in indexes:
			if OP_FIELD.is_field_empty():
				return i,0
			if MY_FIELD.BATTLE_FIELD[i].ATK > OP_FIELD.BATTLE_FIELD[OP_FIELD.get_most_nonpower_card_index()].ATK:
				return i,OP_FIELD.get_most_nonpower_card_index()
		return None,None



from csv import reader
deck_list = []
with open('./deck.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    deck_list = list(csv_reader)
    random.shuffle(deck_list)

MY = MyOPE()
OP = OpOPE(deck_list)
g = game(MY,OP)
g.run()
