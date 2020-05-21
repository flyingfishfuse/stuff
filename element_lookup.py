#!/usr/bin/python3
import os
import re
import asyncio
import discord
import mendeleev
import wikipedia
import math, cmath
from itertools import cycle
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord_key import discord_bot_token

################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
###############################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
##stuff:
# https://www.thecrazyprogrammer.com/2018/05/wikipedia-api-python-tutorial.html
# https://pypi.org/project/mendeleev/
# https://wikipedia.readthedocs.io/en/latest/code.html#module-wikipedia
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#context
# https://mendeleev.readthedocs.io/en/stable/notebooks/01_intro_to_mendeleev.html#Getting-list-of-elements

#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"

################################################################################
##############                BASIC VARIABLES                  #################
################################################################################
bot = commands.Bot(command_prefix=("."))
#who dis?
bot_permissions = 92160
devs = [446959856318939137, 589968097369128966]
cog_directory_files = os.listdir("./cogs")
load_cogs = False
#not used yet
input_container     = []
#used yet
output_container    = []
#TODO: give this as an option eventually.
#data_list           = wikipedia.page(title='List_of_data_references_for_chemical_elements')

#this is the  message sent by the bot if the user input did not pass validation
user_is_a_doofus_element_message = "Stop being a doofus and feed the data on elements that I expect!"
#this is the  message sent by the bot if the user input did not pass validation
user_is_a_doofus_specific_message = "Stop being a doofus and feed the data on specifics that I expect!"
#TODO: TYPE UP HELP MESSAGE
help_message = "Put the element's name, symbol, or atomic number followed by either: physical, chemical, nuclear, ionization, isotopes, oxistates"
#shamelessly stolen from stackoverflow
def function_failure_message(exception_message):
    import inspect
    return "something wierd happened in: " + inspect.currentframe().f_code.co_name + \
        "/n" + exception_message



element_list = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', \
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

specifics_list = ["physical" , "chemical", "nuclear", "ionization", "isotopes", "oxistates"]

yotta = 1000000000000000000000000#
zetta = 1000000000000000000000  #
exa =  1000000000000000000      #
peta = 1000000000000000        #
tera = 1000000000000         #
giga = 1000000000          #
mega = 1000000          #
kilo = 1000          #
hecto = 100       #
deca = 10       #
deci = 0.1     #
centi = 0.01      #
milli = 0.001       #
micro = 0.00001       #
nano = 0.00000001        #
pico = 0.000000000001      #
femto = 0.000000000000001    #
atto = 0.000000000000000001    #
zepto = 0.000000000000000000001 #
yocto = 0.000000000000000000000001

pi = 3.14159
Vbe= 0.7 # volts

################################################################################
##############                      BOT CORE                   #################
################################################################################
#load the cogs into the bot
if load_cogs == True:
    for filename in cog_directory_files:
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

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@bot.event
async def on_ready():
    print("Element_properties_lookup_tool")
    await bot.change_presence(activity=discord.Game(name="THIS IS BETA !"))

#HELP COMMAND
@bot.command()
async def usage(ctx):
    await ctx.send(help_message)

#FIRST COMMAND
# right here we define behavior for the command
#   we are only ALLOWING two arguments:
#     the element identification
#     level of data requested
# instantiate the class and pass the data the user provided to the validation
#   function that will call everything else and parse the arguments. Once the
#   arguments are parsed, the algorhithm is applied, the output is formatted,
#   and the user is sent a reply@bot.command()
@bot.command()
async def lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(arg1, arg2)
    # once the data is parsed, you have to format!
    #this line sends the final output to the channel the user is asking from
    #await ctx.send(Element_lookup.format_and_print_output(output_container))

###############################################################################
class Element_lookup(commands.Cog):
    def __init__(self, ctx, bot):
        self.bot = bot
        print("loaded properties_lookup")
        #generate_element_name_list()

################################################################################
##############              INTERNAL  FUNCTIONS                #################
################################################################################
    async def user_input_was_wrong(type_of_pebkac_failure):
        '''
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        '''
        if type_of_pebkac_failure == "element":
            output_container = user_is_a_doofus_element_message
        elif type_of_pebkac_failure == "specifics":
            output_container = user_is_a_doofus_specifics_message
        else:
            output_container = await function_failure_message()


###############################################################################
    async def validate_user_input(element_id_user_input, specifics_requested):
        '''
        checks if the user is requesting an actual element and set of data.
        '''
        #lets do some preliminary checks for special things to let other people
        # add special behavior, this is a social networking bot after
        #if element_id_user_input
        # loops over the element and symbol lists and checks if the data
        # requested is within the range of known elements
        #checks atomic number
        if element_id_user_input in range(1-118) or \
            any(user_input == element_id_user_input for user_input in element_list) or \
            any(user_input == element_id_user_input for user_input in symbol_list):
            # Element identification the user provided was in the list of elements
            # now we have to check the second input
                if any(user_input == specifics_requested for user_input in specifics_list):
                    # second variable was validated sucessfully so now we
                    #do the thing
                    if specifics_requested.lower()    == "physical":
                        await Element_lookup.get_physical_properties(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                    elif specifics_requested.lower()  == "chemical":
                        await Element_lookup.get_chemical_properties(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                    elif specifics_requested.lower()  == "nuclear":
                        await Element_lookup.get_nuclear_properties(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                    elif specifics_requested.lower()  == "ionization":
                        await Element_lookup.get_ionization_energy(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                    elif specifics_requested.lower()  == "isotopes":
                        await Element_lookup.get_isotopes(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                    elif specifics_requested.lower()  == "oxistates":
                        await Element_lookup.get_oxistates(element_id_user_input)
                        await Element_lookup.format_and_print_output(output_container)
                        # input given by user was NOT found in the validation data
                else:
                    await Element_lookup.user_input_was_wrong("specifics")
                    await Element_lookup.format_and_print_output(output_container)
        else:
            await Element_lookup.user_input_was_wrong("element")
            await Element_lookup.format_and_print_output(output_container)
###############################################################################
    async def format_and_print_output(container_of_output : list):
        '''
        Makes a pretty formatted message as a return value
            This is something the creator of the bot needs to modify to suit
            Thier community.
        '''
        output_string = ""
        for each in container_of_output:
            output_string + container_of_output
            # I don't know what I am doing here, I have not worked with discord
            # code before so I cannot really do much more than concatenate
            # them all together into a new string and return that so that is
            # what I am doing
        return output_string
################################################################################
##############          COMMANDS AND USER FUNCTIONS            #################
################################################################################
# command is {prefix}{compare_element_list}{"affinity" OR "electronegativity"}{"less" OR "greater"}
############################
# alpha FUNCTIONS
###########################
# these needs to be integrated to the main script
# This function compares ALL the elements to the one you provide
# you can extend the functionality by copying the relevant code
    async def compare_element_list(data_type : str, less_greater: str):
        element_data_list = []
        return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
        element_to_compare   = return_element_by_id(element_id_user_input)
        for each in range(1,118):
            element_object = return_element_by_id(each)
            # CHANGE ELEMENT_OBJECT.NAME to ELEMENT_OBJECT.SOMETHING_ELSE
            # That is all you need to do, then add the new functionality to the
            # help and list
            if data_type == "affinity":
                if less_greater == "less":
                    if element_object.electron_affinity < element_to_compare.electron_affinity:
                        element_list.append(element_object.electron_affinity)
                elif less_greater == "greater":
                    if element_object.electron_affinity > element_to_compare.electron_affinity:
                        element_list.append(element_object.electron_affinity)
            elif data_type == "electronegativity":
                if less_greater == "less":
                    if element_object.electronegativity < element_to_compare.electronegativity:
                        element_list.append(element_object.electronegativity)
                elif less_greater == "greater":
                    if element_object.electronegativity > element_to_compare.electronegativity:
                        element_list.append(element_object.electronegativity)

############################
# beta FUNCTIONS
###########################
#these are already integrated into the core code of the script
# they are not finished, but functional
    async def get_basic_information(element_id_user_input):
        '''
        Returns some basic information about the element requested
        takes either a name,atomic number, or symbol
        '''
        try:
            element_object = mendeleev.element(element_id_user_input)
            output_container.append("Description: " + element_object.description  + "/n")
            output_container.append("Sources: " + element_object.sources  + "/n")

        except :
            print(Exception)
###############################################################################
    async def get_history(element_id_user_input):
        '''
        Returns some historical information about the element requested
        takes either a name,atomic number, or symbol
        '''
        try:
            element_object = mendeleev.element(element_id_user_input)
            output_container.append("Uses: " + element_object.uses        + "/n")
            output_container.append("Abundance in Crust" + element_object.abundance_crust + "/n")
            output_container.append("Abundance in Sea" + element_object.abundance_sea + "/n")
            output_container.append("Discoveries: " + element_object.discoveries  + "/n")
            output_container.append("Discovery Location: " + element_object.discovery_location  + "/n")
            output_container.append("Discovery Year: " + element_object.discovery_year        + "/n")
                    # name_origin
        except :
            print(Exception)

###############################################################################
    async def get_isotopes(element_id_user_input):
        '''
        Returns Isotopes of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Isotopes: " + element_object.isotopes + "/n")
###############################################################################
    async def get_ionization_energy(element_id_user_input):
        '''
        Returns Ionization energies of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Ionization Energies: " + element_object.ionenergies  + "/n")
###############################################################################
    async def get_physical_properties(element_id_user_input):
        '''
        Returns physical properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Hardness: "      + element_object.hardness      + "/n")
        output_container.append("Softness: "      + element_object.softness      + "/n")
        output_container.append("Boiling Point:"  + element_object.boiling_point + "/n")
        output_container.append("Melting Point:"  + element_object.melting_point + "/n")
        output_container.append("Specific Heat:"  + element_object.specific_heat + "/n")
        output_container.append("Thermal Conductivity:"  + element_object.thermal_conductivity + "/n")
###############################################################################
    async def get_chemical_properties(element_id_user_input):
        '''
        Returns Chemical properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Electron Affinity: "    + element_object.electron_affinity  + "/n")
        output_container.append("Heat Of Formation: "    + element_object.heat_of_formation  + "/n")
        output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat   + "/n")
        output_container.append("Electronegativity: "    + element_object.electronegativity  + "/n")
        output_container.append("Covalent Radius: "      + element_object.covalent_radius    + "/n")
        output_container.append("Polarizability: "       + element_object.dipole_polarizability  + "/n")
###############################################################################
    async def get_nuclear_properties(element_id_user_input):
        '''
        Returns Nuclear properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Neutrons" + element_object.neutrons  + "/n")
        output_container.append("Protons"  + element_object.protons   + "/n")
                # atomic_radius
                # atomic_weight
        # is_radioactive

###############################################################################
    async def get_basic_element_properties(element_id_user_input):
        '''
        takes either a name,atomic number, or symbol
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Element: "       + element_object.name          + "/n")
        output_container.append("Atomic Weight: " + element_object.atomic_weight + "/n")
        output_container.append("CAS Number: "    + element_object.cas           + "/n")
        output_container.append("Mass:"           + element_object.mass          + "/n")


###############################################################################
########    RANDOM CODE SNIPPETS  #################
###############################################################################
## links = My_table.findAll('a')
## output_container.append(+ element_object.  + "/n")
## return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
## output_container.append("" + element_object.  + "/n")
##
#
# table_headers = resource_soup.find_all('th')
# data_table = soup.find('table',{'class':'wikitable sortable'})
#
################################################################################
### This is how you get lists of data for ALL the elements at once:
##
### return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
### for each in range(1,118):
###     asdf = return_element_by_id(each)
###     print(asdf.name)
#    def generate_element_name_list():
#       return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#           for numberr in range(1,118):
#               element_object = return_element_by_id(each)
# CHANGE ELEMENT_OBJECT.NAME to ELEMENT_OBJECT.SOMETHING_ELSE
#               element_list.append(element_object.name)
################################################################################
#    async def list_resources(self, ctx, *,):
#        listy_list = []
#        resource_soup = BeautifulSoup(requests.get(data_pages_list).text,'lxml')
#        content = resource_soup.find_all('div' , {'class' : 'mw-content-ltr'})
#        for each in content.find_all('a'):
#            output_container.append(each)
#    pass
###############################################################################

bot.run(token=discord_bot_token, bot=True)
