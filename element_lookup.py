#!/usr/bin/python3
import os
import re
import asyncio
import discord
import mendeleev
import wikipedia
from itertools import cycle
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks

###############################################################################
# Chemical element resource database from wikipedia for discord bot           #
###############################################################################
##    Search by element number, symbol,
##    list resources available
##    show basic info if no specificity in query

#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"

bot = commands.Bot(command_prefix=("."))
devs = [446959856318939137, 589968097369128966]
cog_directory_files = os.listdir("./cogs")
full_data           = False
input_container     = []
output_container    = []
data_list           = wikipedia.page(title='List_of_data_references_for_chemical_elements')

#this is the  message sent by the bot if the user input did not pass validation
user_is_a_doofus_message = "Stop being a doofus and feed the data I expect!"

#TODO: TYPE UP HELP MESSAGE
help_message = "Type something here please"

element_list      = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', \
    'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', \
    'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', \
    'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', \
    'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', \
    'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton', \
    'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', \
    'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', \
    'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', 'Cesium', \
    'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', \
    'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', \
    'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', \
    'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', \
    'Platinum', 'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', \
    'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', \
    'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium',\
    'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', \
    'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', \
    'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', \
    'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', \
    'Tennessine']

symbol_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', \
    'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', \
    'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', \
    'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', \
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', \
    'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', \
    'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', \
    'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', \
    'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts']

specifics_list: = ["physical" , "chemical", "ionization", "isotopes", "oxistates"]

################################################################################
##############                      BOT CORE                   #################
################################################################################
#load the cogs into the bot
for filename in cog_directory:
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

#LOAD EXTENSION
@bot.command()
@commands.check(dev_check)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Loaded !")

#UNLOAD EXTENSION
@bot.command()
@commands.check(dev_check)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")

#RELOAD EXTENSION
@bot.command()
@commands.check(dev_check)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Reloaded !")


@bot.event
async def on_ready():
    print("Element_properties_lookup_tool")
    await bot.change_presence(activity=discord.Game(name="THIS IS BETA !"))

#HELP COMMAND
@bot.command()
async def help(ctx):
    await ctx.send(help_message)

#FIRST COMMAND
@bot.command()
@commands.check(dev_check)
async def lookup(ctx, arg1, arg2):
    # right here we define behavior for the command
    # we are only ALLOWING two arguments:
    # the element identification, and level of data requested
    # instantiate the class and pass the data the user provided to the
    # validation function that will call everything else and parse the arguments
    # Once the arguments are parsed, the algorhithm is applied, the output is
    # formatted, and the user is sent a reply!
    Element_lookup.validate_user_input(arg1, arg2)
    # once the data is parsed, you have to format!
    #this line sends the final output to the channel the user is asking from
    await ctx.send(Element_lookup.format_and_print_output(output_container))

###############################################################################
class Element_lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("loaded properties_lookup")
        generate_element_name_list()

################################################################################
##############              INTERNAL  FUNCTIONS                #################
################################################################################
    async def user_input_was_wrong(self, ctx, *, element_id_user_input, specifics_requested):
        '''
        You can put something funny here!
        '''
        output_container = user_is_a_doofus_message
        pass


###############################################################################
    async def validate_user_input(self, ctx, *, element_id_user_input, specifics_requested):
        '''
        checks if the user is requesting an actual element and set of data.
        '''
        # loops over the element and symbol lists and checks if the data
        # requested is within the range of known elements
        #checks atomic number
        if element_id_user_input in range(1-118) or \
        #checks element name
            any(user_input == element_id_user_input for user_input in element_list) or \
        # checks symbol
            any(user_input == element_id_user_input for user_input in symbol_list):
        # Element identification the user provided was in the list of elements
            if specifics_requested.lower()      == "physical":
                get_physical_properties(eleme)
            else if specifics_requested.lower() == "chemical":
                get_chemical_properties()
            else if specifics_requested.lower() == "ionization":
                get_ionization_energy()
            else if specifics_requested.lower() == "isotopes":
                get_isotopes()
            else if specifics_requested.lower() == "oxistates":
                get_oxistates()
        # input given by user was NOT found in the validation data
        else:
            user_input_was_wrong()

###############################################################################
    async def list_resources(self, ctx, *,):
        #listy_list = []
        #resource_soup = BeautifulSoup(requests.get(data_pages_list).text,'lxml')
        #content = resource_soup.find_all('div' , {'class' : 'mw-content-ltr'})
        #for each in content.find_all('a'):
        #    output_container.append(each)
    pass

###############################################################################
    async def format_and_print_output(output_container):
        '''
        '''

        pass
################################################################################
##############          COMMANDS AND USER FUNCTIONS            #################
################################################################################
    async def get_basic_information(self, ctx, element_id_user_input):
        '''
        Returns some basic information about the element requested
        takes either a name,atomic number, or symbol
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Sources: " + element_object.sources  + "/n")
        output_container.append("Uses: " + element_object.uses        + "/n")

###############################################################################
    async def get_isotopes(self, ctx, element_id_user_input):
        '''
        Returns Isotopes of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Isotopes: " + element_object.isotopes + "/n")

###############################################################################
    async def get_ionization_energy(self, ctx, element_id_user_input):
        '''
        Returns Ionization energies of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Ionization Energies: " + element_object.ionenergies  + "/n")

###############################################################################
    async def get_physical_properties(self, ctx, element_id_user_input):
        '''
        Returns physical properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Hardness: "      + element_object.hardness  + "/n")
        output_container.append("Softness: "      + element_object.softness
        output_container.append("Boiling Point:"  + element_object.boiling_point + "/n")
        output_container.append("Melting Point:"  + element_object.melting_point + "/n")
        output_container.append("Specific Heat:"  + element_object.specific_heat + "/n")
        output_container.append("Thermal Conductivity:"  + element_object.thermal_conductivity + "/n")

###############################################################################
    async def get_chemical_properties(self, ctx, element_id_user_input):
        '''
        Returns Chemical properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Electron Affinity: "    + element_object.electron_affinity  + "/n")
        output_container.append("Heat Of Formation: "    + element_object.heat_of_formation  + "/n")
        output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat  + "/n")
        output_container.append("Electronegativity: "    + element_object.electronegativity + "/n")
        output_container.append("Covalent Radius: "      + element_object.covalent_radius  + "/n")
        output_container.append("Polarizability: "       + element_object.dipole_polarizability  + "/n")

###############################################################################
    async def get_nuclear_properties(self, ctx, element_id_user_input):
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Neutrons"         + element_object.neutrons + "/n")
        output_container.append("Protons"         + element_object.protons + "/n")

###############################################################################
    async def get_basic_element_properties(self, ctx, element_id_user_input):
        '''
        takes either a name,atomic number, or symbol
        '''
        #table_headers = resource_soup.find_all('th')
        #data_table = soup.find('table',{'class':'wikitable sortable'})

        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Element: "       + element_object.name + "/n")
        output_container.append("Atomic Weight: " + element_object.atomic_weight + "/n")
        output_container.append("CAS Number: "    + element_object.cas  + "/n")
        output_container.append("Mass:"           + element_object.mass + "/n")


###############################################################################
########    RANDOM CODE SNIPPETS  #################
###############################################################################
## links = My_table.findAll('a')
## output_container.append(+ element_object.  + "/n")
## return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
## output_container.append("" + element_object.  + "/n")
##
### return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
### for each in range(1,118):
###     asdf = return_element_by_id(each)
###     print(asdf.name)
#    def generate_element_name_list():
#        if validate_user_input == True :
#            return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#            for numberr in range(1,118):
#                element_object = return_element_by_id(each)
#                element_list.append(element_object.name)
###############################################################################

bot.run("NzA2NzIyMjE0MzMzOTA2OTk1.XsT4dw.N9z8Z6WMZ2tSK3md2p26GjlK_UM")
