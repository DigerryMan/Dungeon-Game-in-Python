# ALL MOBS ROOM

"""
# - indestructable block (Wall)
D - destructable block 
C - possible chest spawn
E - possible enemy spawn
. - empty space
_ - empty space 
Other letters - mobs (for now)
"""


"""STARTING_ROOM = [
  '################################',
  '#.......B.B......B.............#',
  '#................B.B...........#',
  '#.......B....B......B..........#',
  '#......B...B...B..B............#',
  '#........................F.....#',
  '#.......L......................#',
  '#....................F.........#',
  '#.......P......................#',
  '#.........................E....#',
  '#.......M......................#',
  '#........................E.....#',
  '#B..BB..A......................#',
  '#.BB..B........................#',
  '#......B.......................#',
  '#SB.B..B.......................#',
  '#.B...BB......................B#',
  '################################'
]

STARTING_ROOM = [
  '################################',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..........................C...#',
  '#..............................#',
  '#.......................D......#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '################################'
]


SHOP_ROOM = [
  '################################',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#...........s..s..s............#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '################################'
]

BOSS_ROOM = [
  '################################',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#...........................BBB#',
  '################################'
]

ROOM_1 = [
  '################################',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#.........B....................#',
  '#.........B....................#',
  '#.........B...............BBB..#',
  '#.........B...BBBBB............#',
  '#..............................#',
  '#.........E....................#',
  '#...BBB........................#',
  '#..............................#',
  '#..............................#',
  '################################'
]

ROOM_2 = [
  '################################',
  '#.....E........................#',
  '#..............................#',
  '#.........BBBBBBBBBB...........#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#..............................#',
  '#.........B....................#',
  '#.........B....................#',
  '#.........B...............BBB..#',
  '#.........B...BBBBB............#',
  '#..............................#',
  '#..............................#',
  '#...BBB........................#',
  '#..............................#',
  '#..............................#',
  '################################'
]


EASY_ROOM_1 = [
  '################################',
  '#.............|..|.............#',
  '#.....E..E....|..|...E..E......#',
  '#......BB......__.....BB.......#',
  '#......BB.............BB.......#',
  '#..............................#',
  '#...........DDDDDDDD...........#',
  '#__.........DE....ED.........__#',
  '#..|........D..CC..D........|..#',
  '#..|........D..CC..D........|..#',
  '#__.........DE....ED.........__#',
  '#...........DDDDDDDD...........#',
  '#..............................#',
  '#......BB.............BB.......#',
  '#......BB......__.....BB.......#',
  '#.....E..E....|..|...E..E......#',
  '#.............|..|.............#',
  '################################'
]

EASY_ROOM_2 = [
  '################################',
  '#EE...........|..|...........EE#',
  '#.............|..|.............#',
  '#..............__..............#',
  '#..............................#',
  '#..............................#',
  '#........BBBBBBBBBBBBBB........#',
  '#__......BBBBBBBBBBBBBB......__#',
  '#..|.....BBBBBBBBBBBBBB.....|..#',
  '#..|.....BBBBBBBBBBBBBB.....|..#',
  '#__......BBBBBBBBBBBBBB......__#',
  '#........BBBBBBBBBBBBBB........#',
  '#..............................#',
  '#..............................#',
  '#..............__..............#',
  '#.............|..|.............#',
  '#EE...........|..|...........EE#',
  '################################']

EASY_ROOM_3 = [
  '################################',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '#.........B....__....B.........#',
  '#..........B........B..........#',
  '#...........B..EE..B...........#',
  '#............B.EE.B............#',
  '#__...........BEEB...........__#',
  '#..|...........BB...........|..#',
  '#..|...........BB...........|..#',
  '#__...........BEEB...........__#',
  '#............B.EE.B............#',
  '#...........B..EE..B...........#',
  '#..........B........B..........#',
  '#.........B....__....B.........#',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '################################']

EASY_ROOM_4 = [
  '################################',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '#.........BBB..__..BBB.........#',
  '#........B...B....B...B........#',
  '#.......B.....BBBB.....B.......#',
  '#.......B.....EEEE.....B.......#',
  '#__......B....ECCE....B......__#',
  '#..|......B...ECCE...B......|..#',
  '#..|.......B..EEEE..B.......|..#',
  '#__.........B......B.........__#',
  '#............B....B............#',
  '#.............B..B.............#',
  '#..............DD..............#',
  '#..............__..............#',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '################################']

MEDIUM_ROOM_1 = [
  '################################',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '#.....EE.......__.......EE.....#',
  '#.............B..B.............#',
  '#.............B..B.............#',
  '#.............B..B.............#',
  '#__BB..BB.....B..B.....BB..BB__#',
  '#..|........................|..#',
  '#..|........................|..#',
  '#__BB..BB.....B..B.....BB..BB__#',
  '#.............B..B.............#',
  '#.............B..B.............#',
  '#.............B..B.............#',
  '#.....EE.......__.......EE.....#',
  '#.............|..|.............#',
  '#.............|..|.............#',
  '################################'
]




MEDIUM_ROOM_2 = [
  '################################',
  '#EE...........|..|...........EE#',
  '#EE...........|..|...........EE#',
  '#..............__..............#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..............BB..............#',
  '#__............BB............__#',
  '#..|...BB..............BB...|..#',
  '#..|...BB..............BB...|..#',
  '#__............BB............__#',
  '#..............BB..............#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..............__..............#',
  '#EE...........|..|...........EE#',
  '#EE...........|..|...........EE#',
  '################################'
]

HARD_ROOM_1 = [
  '################################',
  '#BBBBBBBBBBBBB|..|BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB|..|BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB.__.BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB.EE.BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB....BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB....BBBBBBBBBBBBB#',
  '#__.......................E..__#',
  '#..|...........CC.....E...E.|..#',
  '#..|...........CC.....E...E.|..#',
  '#__.......................E..__#',
  '#BBBBBBBBBBBBB....BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB....BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB.EE.BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB.__.BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB|..|BBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBB|..|BBBBBBBBBBBBB#',
  '################################']


HARD_ROOM_2 = [
  '################################',
  '#BBBBBBBBBBBBBB..BBBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBBB..BBBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBBB__BBBBBBBBBBBBBB#',
  '#BBBBBBB..............EEBBBBBBB#',
  '#BBBBBB.................EBBBBBB#',
  '#BBBBB...................EBBBBB#',
  '#BBBB........BBBBBB......EEBBBB#',
  '#..|.........B....B.........|..#',
  '#..|.........B....B.........|..#',
  '#BBBB........BBBBBB......EEBBBB#',
  '#BBBBB...................EBBBBB#',
  '#BBBBBB.................EBBBBBB#',
  '#BBBBBBB..............EEBBBBBBB#',
  '#BBBBBBBBBBBBBB__BBBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBBB..BBBBBBBBBBBBBB#',
  '#BBBBBBBBBBBBBB..BBBBBBBBBBBBBB#',
  '################################']"""





NEW_ROOM = [
  '################',
  '#..............#',
  '#.....BBBB.....#',
  '#.B..........B.#',
  '#.B....C.....B.#',
  '#.B..........B.#',
  '#.....BBBB.....#',
  '#..............#',
  '################']


STARTING_ROOM = [
  '################',
  '#..............#',
  '#.BBBBBBBBBB...#',
  '#..........C...#',
  '#...B..........#',
  '#..............#',
  '#.....BBBB.....#',
  '#..............#',
  '################']



SHOP_ROOM = [
  '################',
  '#..............#',
  '#....C.........#',
  '#..............#',
  '#...s..s..s....#',
  '#..............#',
  '#..............#',
  '#..............#',
  '################']

BOSS_ROOM = [
  '################',
  '#..............#',
  '#...C..........#',
  '#..............#',
  '#.......D......#',
  '#..............#',
  '#..............#',
  '#..............#',
  '################']



#rooms = [ROOM_1, ROOM_2]
#rooms = [EASY_ROOM_1, EASY_ROOM_2, EASY_ROOM_3, EASY_ROOM_4, MEDIUM_ROOM_1, MEDIUM_ROOM_2, HARD_ROOM_1, HARD_ROOM_2]
rooms = [NEW_ROOM]

special_rooms = {
  "start": STARTING_ROOM,
  "shop": SHOP_ROOM,
  "boss": BOSS_ROOM
}