"""
sst.py =-- Super Star Trek in Python
"""
import math

PHASEFAC	= 2.0
GALSIZE 	= 8
NINHAB  	= GALSIZE * GALSIZE / 2
MAXUNINHAB	= 10
PLNETMAB	= NINHAB + MAXUNINHAB
QUADSIZE	= 10
BASEMAX 	= 5
FULLCREW	= 428	 # BSD Trek was 387, that's wrong
MAXKLGAME	= 127
MAXKLQUAD	= 9
FOREVER 	= 1e30

# Feature vakues
IHR = 'R',
IHK = 'K',
IHC = 'C',
IHS = 'S',
IHSTAR = '*',
IHP = 'P',
IHW = '@',
IHB = 'B',
IHBLANK = ' ',
IHDOT = '.',
IHQUEST = '?',
IHE = 'E',
IHF = 'F',
IHT = 'T',
IHWEB = '#',
IHMATER0 = '-',
IHMATER1 = 'o',
IHMATER2 = '0',

class coord:
    def __init(self, x=None, y=None):
        self.x = x
        self.y = y
    def invalidate(self):
        self.x = self.y = None
    def is_valid(self):
        return self.x != None and self.y != None
    def __eq__(self, other):
        return self.x == other.y and self.x == other.y
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class planet:
    def __init(self):
        self.w = coord()
        self.name = None
        self.crystals = None	# "absent", "present", or "mined"
        self.known = "unknown"	# Other values: "known" and "shuttle down"

class quadrant:
    def __init__(self):
        self.stars = None
        self.planet = None
        self.starbase = None
        self.klingons = None
        self.romulans = None
        self.supernova = None
        self.charted = None
        self.status = "secure"	# Other valuues: "distressed", "enslaved"

class page:
    "A chart page.  The starchart is a 2D array of these."
    def __init__(self):
	self.stars = None	# Will hold a number
	self.starbase = None	# Will hold a bool
	self.klingons = None	# Will hold a number

class snapshot:
    "State of the universe.  The galaxy is a 2D array of these."
    def __init__(self):
        self.crew = None	# crew complement
	self.remkl = None	# remaining klingons
	self.remcom = None	# remaining commanders
	self.nscrem = None	# remaining super commanders
	self.rembase = None	# remaining bases
	self.starkl = None	# destroyed stars
	self.basekl = None	# destroyed bases
	self.nromrem = None	# Romulans remaining
	self.nplankl = None	# destroyed uninhabited planets
	self.nworldkl = None	# destroyed inhabited planets
        self.plnets = [];	# List of planets known
        self.date = None	# stardate
	self.remres = None	# remaining resources
	self. remtime = None	# remaining time
        self.bases = [] 	# Base quadrant coordinates
        self.kcmdr = [] 	# Commander quadrant coordinates
        self.kscmdr = None	# Supercommander quadrant coordinates
        self.galaxy = {}	# Dictionary of quadrant objects
        self.chart = {}		# Dictionary of page objects

def damaged(dev):
    return game.damage[dev] != 0.0

class event:
    def __init__(self):
        self.date = None	# The only mandatory attribute

class game:
    def __init__(self):
        self.options = []		# List of option strings
        self.state = snapshot()		# State of the universe
        self.snapsht = snapshot()	# For backwards timetravel
        self.quad = {}			# contents of our quadrant
        self.kpower = {}		# enemy energy levels
        self.kdist = {}			# enemy distances
        self.kavgd = {}			# average distances
        self.damage = {}		# damage encountered
        self.future = []		# future events
        self.passwd = None		# Self Destruct password
        # Coordinate members start here
	self.ks = {}			# enemy sector locations
	self.quadrant = None		# where we are
        self.sector = None
	self.tholian = None		# coordinates of Tholian
	self.base = None		# position of base in current quadrant
	self.battle = None		# base coordinates being attacked
	self.plnet = None		# location of planet in quadrant
	self.probec = None		# current probe quadrant
        # Flag members start here
	self.gamewon = None		# Finished!
	self.ididit = None		# action taken -- allows enemy to attack
	self.alive = None		# we are alive (not killed)
	self.justin = None		# just entered quadrant
	self.shldup = None		# shields are up
	self.shldchg = None		# shield changing (affects efficiency)
	self.comhere = None		# commander here
	self.ishere = None		# super-commander in quadrant
	self.iscate = None		# super commander is here
	self.ientesc = None		# attempted escape from supercommander
	self.ithere = None		# Tholian is here 
	self.resting = None		# rest time
	self.icraft = None		# Kirk in Galileo
	self.landed = None		# party on planet or on ship
	self.alldone = None		# game is now finished
	self.neutz = None		# Romulan Neutral Zone
	self.isarmed = None		# probe is armed
	self.inorbit = None		# orbiting a planet
	self.imine = None		# mining
	self.icrystl = None		# dilithium crystals aboard
	self.iseenit = None		# seen base attack report
	self.thawed = None		# thawed game
        # String members start here
        self.condition = None		# green, yellow, red, docked, dead,
        self.iscraft = None		# onship, offship, removed
        self.skill = None		# levels: none, novice, fair, good,
        				# expert, emeritus
        # Integer nembers sart here
	self.inkling = None		# initial number of klingons
	self.inbase = None		# initial number of bases
	self.incom = None		# initial number of commanders
	self.inscom = None		# initial number of commanders
	self.inrom = None		# initial number of commanders
	self.instar = None		# initial stars
	self.intorps = None		# initial/max torpedoes
	self.torps = None		# number of torpedoes
	self.ship = None		# ship type -- 'E' is Enterprise
	self.abandoned = None		# count of crew abandoned in space
	self.length = None		# length of game
	self.klhere = None		# klingons here
	self.casual = None		# causalties
	self.nhelp = None		# calls for help
	self.nkinks = None		# count of energy-barrier crossings
	self.iplnet = None		# planet # in quadrant
	self.inplan = None		# initial planets
	self.nenhere = None		# number of enemies in quadrant
	self.irhere = None		# Romulans in quadrant
	self.isatb = None		# =1 if super commander is attacking base
	self.tourn = None		# tournament number
	self.proben = None		# number of moves for probe
	self.nprobes = None		# number of probes available
        # Float members start here
	self.inresor = None		# initial resources
	self.intime = None		# initial time
	self.inenrg = None		# initial/max energy
	self.inshld = None		# initial/max shield
	self.inlsr = None		# initial life support resources
	self.indate = None		# initial date
	self.energy = None		# energy level
	self.shield = None		# shield level
	self.warpfac = None		# warp speed
	self.wfacsq = None		# squared warp factor
	self.lsupres = None		# life support reserves
	self.dist = None		# movement distance
	self.direc = None		# movement direction
	self.optime = None		# time taken by current operation
	self.docfac = None		# repair factor when docking (constant?)
	self.damfac = None		# damage factor
	self.lastchart = None		# time star chart was last updated
	self.cryprob = None		# probability that crystal will work
	self.probex = None		# location of probe
	self.probey = None		#
	self.probeinx = None		# probe x,y increment
	self.probeiny = None		#
	self.height = None		# height of orbit around planet

