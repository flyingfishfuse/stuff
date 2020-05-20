#!/usr/bin/python3
import re
import asyncio
import discord
import mendeleev
import wikipedia
#from bs4 import BeautifulSoup
from discord.ext import commands
###############################################################################
# Chemical element resource database from wikipedia for discord bot           #
###############################################################################
##    Search by element number, symbol,
##    list resources available
##    show basic info if no specificity in query

#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"

full_data         = False
input_container   = []
output_container  = []

data_list         = wikipedia.page(title='List_of_data_references_for_chemical_elements')
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

specifics_list: = ["physical" , "chemical", "ionization"]
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

###############################################################################

class Element_lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("loaded properties_lookup")
        generate_element_name_list()

    async def user_input_was_wrong(self, ctx,element_id_user_input, specifics_requested):
        '''
        You can put something funny here!
        '''
        pass

    async def validate_user_input(self, ctx, element_id_user_input, specifics_requested):
        '''
        checks if the user is requesting an actual element.
        '''
        # loops over the element and symbol lists and checks if the atomic number
        # requested is within the range of known elements
        if element_id_user_input in range(1-118) or \
            any(user_input == element_id_user_input for user_input in element_list) or \
            any(user_input == element_id_user_input for user_input in symbol_list):
        # Element identification the user provided was in the list of elements
            if specifics_requested.lower()      == "physical":
                get_physical_properties()
            else if specifics_requested.lower() == "chemical":
                get_chemical_properties()
            else if specifics_requested.lower() == "ionization":
                get_ionization_energy()
        else:
            user_input_was_wrong()

    def generate_element_name_list():
        if validate_user_input == True :
            return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
            for numberr in range(1,118):
                element_object = return_element_by_id(each)
                element_list.append(element_object.name)

    async def list_resources(self, ctx, *,):
        #listy_list = []
        #resource_soup = BeautifulSoup(requests.get(data_pages_list).text,'lxml')
        #content = resource_soup.find_all('div' , {'class' : 'mw-content-ltr'})
        #for each in content.find_all('a'):
        #    output_container.append(each)

    def format_and_print_output(output_container):
        '''
        '''

        pass

    async def get_ionization_energy(self, ctx, element_id_user_input):
        '''
        Returns physical properties of the element requested
        takes either a name,atomic number, or symbol
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Ionization Energies: " + element_object.ionenergies  + "/n")

    async def get_physical_properties(self, ctx, element_id_user_input):
        '''
        Returns physical properties of the element requested
        takes either a name,atomic number, or symbol
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Hardness: "      + element_object.hardness  + "/n")
        output_container.append("Boiling Point:"  + element_object.boiling_point  + "/n")

    async def get_chemical_properties(self, ctx, element_id_user_input):
        '''
        Returns Chemical properties of the element requested
        takes either a name,atomic number, or symbol
        '''
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Electron Affinity: "    + element_object.electron_affinity  + "/n")
        output_container.append("Heat Of Formation: "    + element_object.heat_of_formation  + "/n")
        output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat  + "/n")
        output_container.append("Electronegativity: "    + element_object.electronegativity + "/n")
        output_container.append("Covalent Radius: "      + element_object.covalent_radius  + "/n")
        output_container.append("Polarizability"         + element_object.dipole_polarizability  + "/n")

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
