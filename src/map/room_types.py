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


"""
STARTING_ROOM = [
  '################################',
  '#.......B.B......B.............#',
  '#................B.B...........#',
  '#.......B....B......B..........#',
  '#......B...B...B..B............#',
  '#..............................#',
  '#.......L......................#',
  '#....................F.........#',
  '#.......P......................#',
  '#..............................#',
  '#.......M......................#',
  '#........................E.....#',
  '#B..BB..A......................#',
  '#.BB..B........................#',
  '#......B.......................#',
  '#SB.B..B.......................#',
  '#.B...BB......................B#',
  '################################'
]

"""
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
  '#..............................#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#__............BB............__#',
  '#..|...BB..............BB...|..#',
  '#..|...BB..............BB...|..#',
  '#__............BB............__#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..............................#',
  '#..BB..BB..BB..BB..BB..BB..BB..#',
  '#..............__..............#',
  '#EE...........|..|...........EE#',
  '#EE...........|..|...........EE#',
  '################################'
]

#rooms = [ROOM_1, ROOM_2]
rooms = [EASY_ROOM_1, MEDIUM_ROOM_1, MEDIUM_ROOM_2]

special_rooms = {
  "start": STARTING_ROOM,
  "shop": SHOP_ROOM,
  "boss": BOSS_ROOM
}