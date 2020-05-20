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

################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
###############################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
#
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"

################################################################################
##############                BASIC VARIABLES                  #################
################################################################################
bot = commands.Bot(command_prefix=("."))
#who dis?
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
def function_failure_message():
    import inspect
    return "something wierd happened in: " + inspect.currentframe().f_code.co_name

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
@commands.check(dev_check)
async def lookup(ctx, arg1, arg2):
    Element_lookup.validate_user_input(arg1, arg2)
    # once the data is parsed, you have to format!
    #this line sends the final output to the channel the user is asking from
    await ctx.send(Element_lookup.format_and_print_output(output_container))

###############################################################################
class Element_lookup(commands.Cog):
    def __init__(self, bot):
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
            output_container = function_failure_message()


###############################################################################
    async def validate_user_input(self, ctx, *, element_id_user_input, specifics_requested):
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
                        get_physical_properties(element_id_user_input)
                    elif specifics_requested.lower()  == "chemical":
                        get_chemical_properties(element_id_user_input)
                    elif specifics_requested.lower()  == "nuclear":
                        get_nuclear_properties(element_id_user_input)
                    elif specifics_requested.lower()  == "ionization":
                        get_ionization_energy(element_id_user_input)
                    elif specifics_requested.lower()  == "isotopes":
                        get_isotopes(element_id_user_input)
                    elif specifics_requested.lower()  == "oxistates":
                        get_oxistates(element_id_user_input)
                        # input given by user was NOT found in the validation data
                else:
                    user_input_was_wrong("specifics")
                    format_and_print_output(output_container)
        else:
            user_input_was_wrong("element")
            format_and_print_output(output_container)
###############################################################################
    async def format_and_print_output(container_of_output : list):
        '''
        Makes a pretty formatted message as a return value
            This is something the creator of the bot needs to modify to suit
            Thier community.
        '''
        output_string = ""
        for each in container_of_output:
            # I don't know what I am doing here, I have not worked with discord
            # code before so I cannot really do much more than concatenate
            # them all together into a new string and return that so that is
            # what I am doing
            output_string += each
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
    async def compare_element_list(self, ctx, *, data_type : str, less_greater: str):
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
    async def get_basic_information(self, ctx, element_id_user_input):
        '''
        Returns some basic information about the element requested
        takes either a name,atomic number, or symbol
        '''
        try:
            element_object = mendeleev.element(element_id_user_input)
            output_container.append("Sources: " + element_object.sources  + "/n")
            output_container.append("Uses: " + element_object.uses        + "/n")
        except :
            print(Exception)
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
        output_container.append("Hardness: "      + element_object.hardness      + "/n")
        output_container.append("Softness: "      + element_object.softness      + "/n")
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
        output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat   + "/n")
        output_container.append("Electronegativity: "    + element_object.electronegativity  + "/n")
        output_container.append("Covalent Radius: "      + element_object.covalent_radius    + "/n")
        output_container.append("Polarizability: "       + element_object.dipole_polarizability  + "/n")
###############################################################################
    async def get_nuclear_properties(self, ctx, element_id_user_input):
        '''
        Returns Nuclear properties of the element requested
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Neutrons" + element_object.neutrons  + "/n")
        output_container.append("Protons"  + element_object.protons   + "/n")
###############################################################################
    async def get_basic_element_properties(self, ctx, element_id_user_input):
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

bot.run("NzA2NzIyMjE0MzMzOTA2OTk1.XsT4dw.N9z8Z6WMZ2tSK3md2p26GjlK_UM")
