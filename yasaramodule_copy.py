# **********************************************************
# *                                                        *
# *                    Y  A  S  A  R  A                    *
# *                                                        *
# * Yet Another Scientific Artificial Reality Application  *
# *                                                        *
# **********************************************************
# *         Watching Nature@Work - www.yasara.org          *
# **********************************************************
# *            (C) 1993 - 2011 by Elmar Krieger            *
# **********************************************************
# *       yasaramodule.py - The YASARA Python module       *
# *          License for this Python module: BSD           *
# **********************************************************

# IMPORTANT: Do not copy this module anywhere outside the yasara/pym directory,
# it needs to be updated together with YASARA. Instead, copy the module loader
# yasara/pym/yasara.py to a place where Python can find it, then use 'import yasara'
# in your Python script. If you move the YASARA directory somewhere else, you
# have to adapt the path in all copies of yasara/pym/yasara.py you made.

"""
<H1> Scripts - Use YASARA as a Python module

<H2> Windows users can obtain Python from www.python.org

If you are a Linux or MacOS user, the versatile scripting language Python is
already present. If you are running Windows, you normally have to download Python
from <www.python.org>. Alternatively, YASARA comes with its own embedded Python to run its plugins,
which you can find at yasara\\epy\\win\\pythonw.exe

If you are new to Python, you can {find a tutorial here<https://docs.python.org/3/tutorial/>}.

<H2> Copy and import yasara/pym/yasara.py

There are currently four ways of running YASARA automatically:
*) {Yanaconda macros<Macros2>}, the easiest solution.
*) {Python plugins<Plugins2>}, that are activated by clicking on a menu entry and then perform certain tasks.
*) {YASARA command files<RYfoa>}, a simple way to let other applications execute YASARA commands.
*) The YASARA Python module, which you can simply import into your Python scripts, as described here.

To use YASARA from your Python scripts, perform the following installation steps:
1) Make sure that YASARA has been run at least once.
*) Copy the YASARA module loader yasara/pym/yasara.py (Linux), yasara\\pym\\yasara.py (Windows) or YASARA.app/yasara/pym/yasara.py (MacOS)
to the directory where you keep your Python scripts. If you have administrator privileges, you can also
copy it directly to the place where Python collects its modules (e.g. /usr/lib/pythonX.Y in Linux)
*) Import the YASARA module in your script as shown in the example below,
which loads the PDB file 1crn:
<P>
from yasara import *

LoadPDB("1crn")
<P>
You can also resort to the following alternative, which requires more typing and
is therefore not used here (if you choose this option, you have to prepend 'yasara.'
to all variable names and function calls shown throughout the rest of this chapter).
<P>
import yasara

yasara.LoadPDB("1crn")
<P>

<H2> There is a Python function wrapper for most YASARA commands

The syntax of YASARA commands is optimized for a minimum number of key-strokes,
which is not compatible with Python's own syntax. The YASARA Python module therefore contains
Python function wrappers for most YASARA commands.

Example: The YASARA command to choose a new 3D font..
<P>
Font Arial,Height=2,Spacing=1.5,Color=Yellow,Depth=5,DepthCol=Red
<P>
..has the following equivalent in the Python module:
<P>
Font("Arial",height=2,spacing=1.5,color="Yellow",depth=5,depthcol="Red")
<P>

Note that argument names are lowercase in Python, because in contrast to Yanaconda,
Python's variable names are case-sensitive, and the capitalization is often ambiguous
and hard to remember, raising the error rate.

The documentation page of each YASARA command lists the prototype of the corresponding
Python function, e.g. the <Font> command (look at the 'Python:' row in the table at the
top of each page).

A few YASARA commands support more than one format with different argument types.
This is not possible in Python, the command thus has to be wrapped by different
Python functions. The names of these Python functions differ at the end, using
either an increasing number or the name of the first argument. More details
{are available here<YcwmfmtdPf>}.

You can of course also access the return values of YASARA commands:
<P>
# Load a PDB file and color it red
obj = LoadYOb("1crn")
ColorObj(obj,"Red")
<P>
More details about return values {can be found here<Pfrenasvoal>}.

It should also be noted that calling a YASARA command from Python is slower
than using a Python method, since it involves communication between Python
and YASARA. So calls to YASARA commands should be taken out of loops when
possible:
<P>
# Load a PDB file
LoadPDB("1crn")
# Switch off the console to avoid screen updates
Console("off")
# Print atom names the slow way
for i in range(info.atoms):
  name = NameAtom(i+1)[0]
  print "Atom %d has name %s"%(i+1,name)
# Print atom names the fast way
namelist = NameAtom("all")
for i in range(len(namelist)):
  print "Atom %d has name %s"%(i+1,namelist[i])
<P>

If all fails, you can still use the 'run' function to execute any command,
also those without a Python wrapper (mostly WHAT IF commands in the Twinset):
<P>
# Load 1crn, avoiding the Python wrapper 'LoadPDB("1crn")'
run("LoadPDB 1crn")
# Enter WHATIF's GRAFIC menu
run("WHATIF")
run("GRAFIC")
# Show a wire frame
run("SHOTOT 1 Crambin")
# Go back to YASARA
run("YASARA")
# List all objects without the Python wrapper 'ListObj("all")'
run("ListObj all")
<P>

<H2> Python functions return either nothing, a single value or a list

In the {Yanaconda macro language<Macros2>} you can choose between a single return value
and a list {by appending parentheses to the variable name<CtYcmaopl>}. This
is obviously not possible in Python. Instead those functions that are
guaranteed to never return more than one value simply return this value,
while functions possibly returning more than one value always return a list.

Examples:

<P>
# This function never returns a result:
Clear()

# This function always returns a single result, the number of the object loaded:
obj = LoadYOb("crambin")

# This function may return many results (if the PDB file contains an NMR bundle with many MODELs)
objlist = LoadPDB("3gb1")
# Or if you know that the PDB file contains only a single MODEL/object (note the slice [0]):
obj = LoadPDB("1crn")[0]
<P>

To find out what exactly a function returns, simply check the prototype on the documentation
page, e.g. <LoadPDB> and <LoadYOb>.

Some YASARA commands normally give useful output (like an alignment), but this feature is disabled
by default when the command is run from a Python script. To enable output, simply log it to a dummy
file, which forces YASARA to create and show the output:
<P>
# Log output of next command to a dummy file, which will not be read
LogAs("dummy.txt")
# Align two objects and show the resulting alignment on screen
AlignObj(1,2,method="GlobalSeq",parameter=0,results=4)
<P>

<H2> YASARA specific data is available in 'info'

Assuming you used 'from yasara import *', the following variables are defined:

<T>
<P>info.mode<P>            | YASARA mode, 'gra' for graphics and 'txt' for text
<P>info.dir<P>             | YASARA's installation directory
<P>info.licenseshown<P>    | Set to 0 if you do not want to show the license screen in text mode
<P>info.opsys<P>           | The current operating system, "Linux", "MacOS" or "Windows"
<P>info.version<P>         | The YASARA version string X.Y.Z
<P>info.serialnumber<P>    | YASARA's serial number
<P>info.stage<P>           | The YASARA stage View, Model, Dynamics or Structure
<P>info.owner.firstname<P> | Your first name
<P>info.owner.lastname<P>  | Your last name
<P>info.owner.email<P>     | Your e-mail address
<P>info.atoms<P>           | The number of atoms in YASARA's <soup>
<P>info.objects<P>         | The number of active objects in YASARA's <soup>
<P>info.firstobj<P>        | The number of the first active object
<P>info.lastobj<P>         | The number of the last active object
<P>info.leftbutton<P>      | 1 if the left mouse button is pressed in YASARA's window
<P>info.middlebutton<P>    | 1 if the middle mouse button is pressed in YASARA's window
<P>info.rightbutton<P>     | 1 if the right mouse button is pressed in YASARA's window
<P>info.energyunit<P>      | YASARA's current {energy unit<EnergyUnit>}
<P>info.pluginrequest<P>   | Last Python plugin request, can be used to combine Python modules and plugins
<P>info.speedmax<P>        | The speed of the fastest atom during a simulation in m/s
<T>

Note that `some of these variables can change at any time`, and must therefore be re-obtained
from YASARA every time they are used. This requires communication between the module and
YASARA, which can slow things down considerably. It is therefore
suggested to work with a copy. The following example avoids using 'info.objects' inside
a loop that writes an RMSD matrix:

<P>
from yasara import *
id='1adn'
selected='CA Res 8-69'
LoadPDB(id)
rmsdmtx=SupAtom(selected,selected,flip='Yes')
file=open('supresult.txt','w')
# Make copy here
objects=info.objects
for i in range(objects*objects):
  file.write("%6.3f, "%rmsdmtx[i]);
  if ((i+1)%objects==0): file.write('\n')
file.close()
<P>

<H2> YASARA commands with multiple formats map to different Python functions

Since Yanaconda {is a reinterpreted language<Yiarl>}, YASARA commands can accept
arguments in a rather flexible way. In Python on the other hand, the number and
order of function arguments must not change. If a YASARA command supports
more than one format, it thus has to be wrapped by different Python functions.
The names of these Python functions differ at the end, using either an increasing
number or the name of the first argument.

Example for an increasing number:

<P>
# In Yanaconda:
# Format 1: Show an arrow between atoms 123 and 456
ShowArrow Start=AtAtom,123,End=AtAtom,456,Radius=0.5,Color=Red
# Format 2: Show an arrow between points 1/2/3 and 4/5/6
ShowArrow Start=Point,X=1,Y=2,Z=3,End=Point,X=4,Y=5,Y=6,Radius=0.5,Color=Red

# In Python:
ShowArrow(start="AtAtom",selection1=123,end="AtAtom",selection2=456,radius=0.5,color="Red")
ShowArrow2(start="Point",x=1,y=2,z=3,end="Point",x2=4,y2=5,z2=6,radius=0.5,color="Red")
<P>

Note above that argument names in Python are case-sensitive and expected to be
all lowercase. They may also not be repeated, that's why the coordinates of the
second point are x2/y2/z2.

Example for using the name of the first argument:

<P>
# In Yanaconda:
# Format 1: Define a 20x30x40 A cell with angles 80/90/70 degrees:
Cell X=20,Y=30,Z=40,Alpha=80,Beta=90,Gamma=70
# Format 2: Define cell automatically to enclose everything with a 10 A extension:
Cell Auto,Extension=10
# Format 3: Define cell like the crystallographic cell of object 1crn:
Cell Crystal,1crn

# In Python:
Cell(x=20,y=30,z=40,alpha=80,beta=90,gamma=70)
CellAuto(extension=10)
CellCrystal("1crn")
<P>

Again, to find out details about the function variants available in Python, check out
the Python prototypes on the documentation page, e.g. <ShowArrow> and <Cell>.

<H2> A subset of the YASARA soup can be obtained as a pdb_file instance

YASARA comes with a Python PDB file interface that can be found at
yasara/plg/pdb_file.py. In addition, you can easily obtain any part of the YASARA <soup>
as an instance of such a PDB file interface. This means that you can
use the same piece of Python code to analyze a PDB file loaded from disk
and the YASARA <soup>.

The following examples list all Calpha atoms in the PDB file 1crn.pdb:

*) Using the Python PDB file interface without YASARA:
<P>
import pdb_file

pdb=pdb_file.interface("1crn.pdb")
for i in range(pdb.atoms):
  if (pdb.atom[i].name=="CA"): print(pdb.atom[i])
<P>

*) Using the YASARA Python module:
<P>
from yasara import *

LoadPDB("1crn")
pdb=Atom("CA")
print(pdb)
<P>

The instance 'pdb' stores the data in the following way:

<T>
  <P>Instance.crdsys<P>                    | 1 if the atom coordinates use a left-handed system (YASARA's default), and -1 otherwise (PDB file default).
  <P>Instance.atoms<P>                     | the number of atoms
  <P>Instance.atom[i]<P>                   | the ith atom
  <P>Instance.atom[i].element<P>           | the chemical element number of the ith atom
  <P>Instance.atom[i].name<P>              | the name of the ith atom with spaces stripped
  <P>Instance.atom[i].name4<P>             | the name of the ith atom as present in the PDB file, with all spaces
  <P>Instance.atom[i].num<P>               | the YASARA number of the ith atom (only present in the YASARA Python module)
  <P>Instance.atom[i].altloc<P>            | the alternate location indicator of the ith atom, None if empty
  <P>Instance.atom[i].pos.x/.y/.z<P>       | the position of the ith atom
  <P>Instance.atom[i].pos.c[j]<P>          | the jth 'c'omponent of the position vector of atom i
  <P>Instance.atom[i].occupancy<P>         | the occupancy of the ith atom
  <P>Instance.atom[i].bfactor<P>           | the B-factor of the ith atom
  <P>Instance.atom[i].resname<P>           | the name of the residue the ith atom belongs to
  <P>Instance.atom[i].resnum<P>            | the number of the residue the ith atom belongs to
  <P>Instance.atom[i].molname<P>           | the name of the molecule the ith atom belongs to
  <P>Instance.atom[i].segname<P>           | the name of the segment the ith atom belongs to
  <P>Instance.residues<P>                  | the number of residues
  <P>Instance.residue[i]<P>                | the ith residue
  <P>Instance.residue[i].name<P>           | the name of the ith residue
  <P>Instance.residue[i].num<P>            | the number of the ith residue
  <P>Instance.residue[i].molname<P>        | the name of the molecule the ith residue belongs to
  <P>Instance.residue[i].atoms<P>          | the number of atoms in the ith residue
  <P>Instance.residue[i].atom[j]<P>        | the jth atom in the ith residue with properties described above
  <P>Instance.residue[i].atomnamed["X"]<P> | atom with name "X" in the ith residue with properties described above
  <P>Instance.molecules<P>                 | the number of molecules (=chains)
  <P>Instance.molecule[i]<P>               | the ith molecule (=chain)
  <P>Instance.molecule[i].atoms<P>         | the number of atoms in the ith molecule
  <P>Instance.molecule[i].atom[j]<P>       | the jth atom in the ith molecule with properties described above
  <P>Instance.molecule[i].residues<P>      | the number of residues in the ith molecule
  <P>Instance.molecule[i].residue[j]<P>    | the jth residue in the ith molecule with properties described above
  <P>Instance.objects<P>                   | the number of objects (=NMR MODELs)
  <P>Instance.object[i]<P>                 | the ith object
  <P>Instance.object[i].name<P>            | the YASARA name of the ith object (only present in the YASARA Python module)
  <P>Instance.object[i].num<P>             | the YASARA number of the ith object (only present in the YASARA Python module)
  <P>Instance.object[i].atoms<P>           | the number of atoms in the ith object
  <P>Instance.object[i].atom[j]<P>         | the jth atom in the ith object with properties described above
  <P>Instance.object[i].residues<P>        | the number of residues in the ith object
  <P>Instance.object[i].residue[j]<P>      | the jth residue in the ith object with properties described above
  <P>Instance.object[i].molecules<P>       | the number of molecules in the ith object
  <P>Instance.object[i].molecule[j]<P>     | the jth molecule in the ith object with properties described above
  <P>Instance.object[i].molnamed["X"]<P>   | the molecule named "X" in the ith object with properties described above
<T>

If you obtain the atoms from YASARA, you also get information about covalent bonds and bond orders (excluding
dative bonds to metal ions):
<T>
  <P>Instance.atom[i].bonds<P>             | the number of bonds formed by atom i
  <P>Instance.atom[i].bond[j].order<P>     | the order of bond j formed by atom i, potentially fractional (e.g. 1.5 for ring bonds in benzene)
  <P>Instance.atom[i].bond[j].atomnum<P>   | the YASARA number of the jth atom bound to atom i
  <P>Instance.atom[i].bond[j].atomidx<P>   | the index in Instance.atom of the jth atom bound to atom i, None if the bound atom is not part of Instance.atom
  <P>Instance.atom[i].bond[j].atom<P>      | the jth atom bound to atom i, Instance.atom[Instance.atom[i].bond[j].atomidx], None if not part of Instance.atom
<T>

The following data are currently only available if you load the atoms from disk using
pdb_file.interface:
<T>
  <P>Instance.cell<P>                      | information about the unit cell
  <P>Instance.cell.x/.y/.z<P>              | the cell dimensions
  <P>Instance.cell.alpha/.beta/.gamma<P>   | the cell angles
  <P>Instance.cell/.spacegroup/.z<P>       | the remaining cell parameters
  <P>Instance.resolution<P>                | the X-ray resolution
<T>

The YASARA Python module provides five commands to extract selected
portions of the YASARA <soup> as a PDB file instance: `Atom`, `Residue`, `Molecule`, `Object` and `All`.
The first four {take a selection<Selections>} as the only argument:

<P>
from yasara import *

# Load PDB file 5tim
LoadPDB("5tim")

# Get all atoms in molecule A that contact molecule B
contact=Atom("Mol A with distance<5 from Mol B")
print("There are %d contacts:"%contact.atoms)
print(contact)

# Get all Arg residues that form a salt-bridge with Asp or Glu
bridge=Residue("Arg Atom NE NH? with distance<3.5 from Asp Glu Atom OD? OE?")
print("There are %d salt-bridged arginines"%bridge.residues)
for i in range(bridge.residues):
  print(bridge.residue[i].name,bridge.residue[i].num)

# Get the protein molecules
protein=Molecule("Protein")
print("There are %d protein molecules containing %d atoms"%
      (protein.molecules,protein.atoms))

# Clear the YASARA soup and load an NMR structure bundle
Clear()
LoadPDB("3gb1")

# Get the first model (each model is stored in a separate object)
first=Object(1)
print("The first model contains %d atoms, %d residues and %d molecules"%
      (first.atoms,first.residues,first.molecules))

# Get the entire soup
soup=All()
print("The bundle contains %d models"%soup.objects)
<P>

As a final example, the Python script below calculates the accessible surface area of
molecule B in 5TIM using four different methods, two of which provide the area per heavy atom
(adding the surface areas of the bound hydrogen atoms). Since hydrogen atoms are almost entirely
within the Van der Waals sphere of their heavy atom, they normally do not have to be considered
for surface calculations (the heavy atom only surface is listed first for comparison).
<P>
Clear()
# Load a PDB file
LoadPDB("5tim",download=1)
# Delete non-protein residues
DelRes("!Protein")
# Consider everything for surface calculations
AddEnvAll()
# Get the surface of molecule B, considering heavy atoms only
heavysurf = SurfMol("B",Type="accessible")[0]
# Add the hydrogens
Clean()
# Get the surface of molecule B, considering all atoms
allsurf = SurfMol("B",Type="accessible")[0]
# Get the surface contributions of the individual atoms in molecule B
surflist = SurfMol("B",Type="accessible",unit="Atom")
# Get the chemical element of the atoms in molecule B
elementlist = ElementAtom("Mol B")
# Calculate the 'united surface' (heavy atom plus hydrogens)
# considering the fact that hydrogens follow their heavy atoms.
# If you are not sure about that, use the SwapHyd command first.
allsurf1=0
i=0
while (i<len(elementlist)):
  surf=surflist[i]
  # Add the surface of the following hydrogen atoms
  while (i+1<len(elementlist) and elementlist[i+1]==1):
    i+=1
    surf+=surflist[i]
  print "Method 1: Selected heavy atom %d: %.2f"%(i,surf)
  allsurf1+=surf
  i+=1
# Calculate the 'united surface' a second time, without considering
# the fact that hydrogens follow their heavy atoms. Instead, we
# loop over the bonds formed by the heavy atoms
allsurf2=0
protein=Atom("Mol B")
for i in range(protein.atoms):
  atom=protein.atom[i]
  if (atom.element!=1):
    surf=surflist[i]
    for j in range(atom.bonds):
      if (atom.bond[j].atom.element==1):
        surf+=surflist[atom.bond[j].atomidx]
    print "Method 2: Selected heavy atom %d (%d): %.2f"%(i,atom.num,surf)
    allsurf2+=surf
# Print results
print "Surface considering just heavy atoms:           %.3f A^2"%heavysurf
print "Surface with hydrogens:                         %.3f A^2"%allsurf
print "Surface with hydrogens summed up with method 1: %.3f A^2"%allsurf1
print "Surface with hydrogens summed up with method 2: %.3f A^2"%allsurf2
<P>

<H2> Molecules in PDB format can be sent directly to YASARA

The procedure described in the previous paragraph can also be reversed, i.e. a PDB file
stored in memory either as a simple string or as a pdb_file instance can be built directly
in YASARA:

<P>
# Read a PDB file as a single string
pdb1=open("1crn.pdb").read()
# Read a PDB file as a list of strings
pdb2=open("5tim.pdb").readlines()
# Parse a PDB file
pdb3=pdb_file.interface("3gb1.pdb")
# Build all three in YASARA. The first two assume
# that the PDB file contains only a single model.
obj1=BuildPDB(pdb1)[0]
obj2=BuildPDB(pdb2)[0]
objlist3=BuildPDB(pdb3)
<P>

<H2> The console needs to be switched off for maximum performance

By default, the Python module runs YASARA in interactive graphical mode. This means
that the YASARA window is permanently updated (at least after each YASARA Python function
you call), and that you can even work with YASARA interactively while your Python script
is doing something else.

If your Python script needs to call thousands of YASARA functions in a loop, this
approach soon becomes too slow. The solution is the
same as used by {Yanaconda macros<Mcbsubsotc>} and {Python plugins<Pcbsu>},
switching off the console:

<P>
Console("Off")
<P>

See the <Console> command for more details and note that YASARA will neither redraw the screen
nor proceed a simulation unless you tell it to by {calling the Wait() function<Mcwfastouypab>},
and may thus appear frozen. You can of course any time enable the console
again with yasara.Console("Hidden").

Switching off the console is especially important if you start a simulation with yasara.Sim("on"),
since the simulation would otherwise proceed asynchronously with your Python script, which
is usually not what you want. Instead use yasara.Wait() to let the simulation proceed for
a certain number of steps as mentioned above.

<H2> There is a specific Python function for each experiment

In YASARA Dynamics and YASARA Structure, several <experiment>s are available that
perform complex tasks at the touch of a button. In Yanaconda, experiments expect
their parameters in a separate, indented section:

<P>
# Prepare neutralization experiment
Experiment Neutralization
  # Fill the cell with water at a density of 1.0 g/cm^3
  WaterDensity 1.0
  # Add NaCl counter ions with 0.9%
  NaCl 0.9
  # Protonate ionizable groups according to pH 7.0
  pH 7.0
  # Save pKa predictions as dat/1crn_mutant.pka
  pKaFile 1crn_mutant
  # Finish quickly (final water density will be OK, but not exact)
  Speed Fast
# Start experiment
Experiment On
# Wait till end of experiment
Wait ExpEnd
<P>

In Python, each experiment is wrapped by its own function instead:

<P>
ExperimentNeutralization(waterdensity=1.0,nacl=0.9,ph=7.0,pkafile="1crn_mutant",speed="fast")
Experiment("On")
Wait("ExpEnd")
<P>

<H2> The Python module can run YASARA in graphics or text mode

Normally the Python module runs YASARA in graphics mode, so that you can follow its
work visually on screen. To choose text-only output instead, set info.mode to 'txt'
before you call the first YASARA Python function:

<P>
from yasara import *

# Choose text mode before the first function call
info.mode='txt'
# If you want, disable the display of the license screen
info.licenseshown=0
# First function call, load a PDB file
LoadPDB("1crn")
# List all arginine residues
ListRes("Arg")
# Exit YASARA
Exit()
# Switch to graphics mode
info.mode='gra'
# Load and show a PDB file
LoadPDB("1crn")
<P>

<H2> Python scripts can run Yanaconda macros

If you run YASARA from a Python script, it is often convenient to start one of the existing Yanaconda
macros (e.g. for {docking<Gdoltew>} or {MD simulation<Rastew>}) from the Python script, instead of
translating the Yanaconda code to Python.

The following example shows how this is done, by docking two ligands using the {dock_run macro<Gdoltew>}.
Note that the <ApplyMacro> function waits until the Yanaconda macro finished, so you do not
have to do any waiting or synchronization yourself.

<P>
from yasara import *

# DOCK LIGAND TO RECEPTOR
# =======================
# Apply the dock_run macro to 'macrotarget', the receptor must be present
# as macrotarget_receptor.pdb/.yob or .sce, the ligand as macrotarget_ligand.pdb/.yob/.sdf.
def dock(macrotarget):
  ApplyMacro(os.path.join(info.dir,"mcr/dock_run.mcr"),targets=macrotarget)

# DOCK VARIOUS LIGANDS
info.mode='txt'
targetlist=["testsuite/complexA","testsuite/complexB"]
for target in targetlist:
  print("Docking "+target)
  dock(target)
  print("Finished "+target)
<P>

The example above is the only practical option for running macros that are too complex
to be translated to Python in a reasonable amount of time (e.g. the md_runmembrane macro).
Alteratively you can translate Yanaconda to Python, e.g. the following Python script md_run.py
performs most of the work of the md_run/md_runfast macros (it doesn't continue a
trajectory run before, but always starts from scratch):
<P>
#!/usr/bin/env python
import yasara

# Part 1: Parameter setup
# Please look at yasara/mcr/md_run.mcr for an explanation of these parameters
#
# Location where the trajectory is saved (e.g. for analysis with md_analysis.mcr or for playback with md_play.mcr)
# This is the common beginning for all filenames saved.
target='/myself/mytrajectories/1crn'
# pH at which the simulation should be run
ph=7.4
# The NaCl concentration as a mass fraction, here we use 0.9% NaCl (physiological solution)
nacl='0.9'
# Simulation temperature
temperature='298K'
# Water density in [g/ml], should match the temperature set above
density=0.997
# Pressure control mode for NPT ensemble, either with barostat or desostat (faster)
pressurectrl=["Manometer1D",1,None,None]
pressurectrl=["SolventProbe",None,"HOH",density]
# Duration of the simulation in [picoseconds]
duration=5000
# Extension of the cell on each side around the solute in [A]
extension=10
# Shape of the simulation cell
cellshape='Cube'
# The simulation speed, either 'slow' (2*1 fs timestep), 'normal' (2*1.25 fs timestep) or
# 'fast' (maximize performance with 2*2.5 fs timestep and constraints)
speed='fast'
# Snapshot save interval in [femtoseconds]
if speed=='fast':
  saveinterval=250000
else:
  saveinterval=100000
# Forcefield to use (these are now all YASARA commands, so no '=' used)
yasara.ForceField("AMBER14")
# Cutoff
yasara.Cutoff(8)
# Cell boundary
yasara.Boundary("periodic")
# Use longrange coulomb forces (particle-mesh Ewald)
yasara.Longrange("Coulomb")
# Keep the solute from diffusing around and crossing periodic boundaries. Disable that for simulations of crystals.
yasara.CorrectDrift(1)
# Treat all simulation warnings as errors that stop the Python script
yasara.WarnIsError(1)

# Part 2: Prepare and solvate structure
# Load a protein
yasara.Clear()
yasara.LoadPDB("1crn",download=1)
# Align object with major axes to minimize cell size
yasara.NiceOriAll()
# Delete long peptide bonds that bridge gaps in the structure, which tells CleanAll to add ACE/NME
# capping groups (the structure of the missing residues could also be predicted, see LoadPDB docs).
yasara.DelBond("N","C",lenmin=5)
# Delete waters that are not involved in metal binding, to help the calculation of binding energies
yasara.DelRes("Water with 0 arrows to all")
# Prepare the structure for simulation at the chosen pH
yasara.CleanAll()
yasara.pH(ph)
# Optimize the hydrogen-bonding network (more stable trajectories)
yasara.OptHydAll("YASARA")
# Create the simulation cell
yasara.CellAuto(extension,cellshape)
# Fill the cell with water including pKa prediction and protonation state assignment
yasara.ExperimentNeutralization(density,nacl,ph,target,'fast')
yasara.Experiment("On")
yasara.Wait("ExpEnd")
# Save scene with water for analysis for playback
yasara.SaveSce(target+"_water")

# Part 3: Minimize structure to remove clashes
# Choose timestep and activate constraints
if speed=='fast':
  # Fast simulation speed
  # Constrain bonds to hydrogens
  yasara.FixBond("all","Element H")
  # Constrain certain bond angles involving hydrogens
  yasara.FixHydAngle("all")
  # Choose a multiple timestep of 2*2.5 = 5 fs
  # For structures with severe errors, 2*2 = 4 fs is safer (tslist=2,2)
  tslist=[2,2.5]
else:
  # Slow or normal simulation speed
  # Remove any constraints
  yasara.FreeBond("all","all")
  yasara.FreeAngle("all","all","all")
  if speed=='slow':
    # Choose a multiple timestep of 2*1.00 = 2.0 fs
    tslist=[2,1.0]
  else:
    # Choose a multiple timestep of 2*1.25 = 2.5 fs
    tslist=[2,1.25]
    # With this timestep, atoms may get too fast in very rare circumstances
    yasara.Brake(13000)
# Update the pairlist every 10 (CPU) or 25 (GPU) steps
processorlist=yasara.Processors()
if processorlist[2]:
  yasara.SimSteps(25,25)
else:
  yasara.SimSteps(10,10)
# Calculate total timestep, we want a float, so tslist2 is on the left side
ts=tslist[0]*tslist[1]
# Snapshots are saved every 'savesteps'
savesteps=int(saveinterval/ts)
# Set final simulation parameters
yasara.TimeStep(tslist[0],tslist[1])
yasara.Temp(temperature)
# Perform energy minimization
yasara.Experiment("Minimization")
yasara.Experiment("On")
yasara.Wait("ExpEnd")

# Part 4: Start the simulation
# Set temperature and pressure control
yasara.TempCtrl("Rescale")
yasara.PressureCtrl(*pressurectrl)
# Save snapshots if needed
yasara.SaveSim(target+"00000",savesteps)
# Synchronize Python script and YASARA
yasara.Console("off")
# Start simulation
yasara.Sim("On")

# Part 5: Analyze simulation while it is running
while (1):
  # Get current time in [fs]
  time=yasara.Time()
  # Calculate energy
  energylist=yasara.Energy("all")
  # Get secondary structure fractions
  secstrlist=yasara.SecStr()
  print "At time %f fs, the energy components are "%time,energylist,", the secondary structure fractions are ",secstrlist
  # Wait 10 screen update cycles
  yasara.Wait(10)
  # Finished?
  if time>duration*1000: break

# Finished
yasara.Sim("Off")
<P>

<H2> Python scripts can interact with Python plugins

If you run YASARA from your Python script, you maybe also want to add options to the
user interface that trigger an action in your script.

To achieve this goal, {first create a Python plugin that adds the options to YASARA's user interface<Plugins2>}.
The Python plugin does not have to respond to these actions, this can be done directly
in your Python script:

<P>
from yasara import *
import time

while 1:
  # Sleep a bit (this will become 'Wait("Plugin")' eventually)
  time.sleep(0.2)
  # Get the plugin request string, if any
  request=info.pluginrequest
  # Act upon the request...
  if request!=None:
    print(request)
<P>

In one of the next YASARA releases, this polling will be replaced with Wait:

<P>
from yasara import *

while 1:
  # Wait until a plugin is activated
  Wait("Plugin")
  # Get the plugin request string
  request=info.pluginrequest
  # Act upon the request...
  print(request)
<P>

<H2> A unique YASARA ID can be chosen on clusters

If you are running several Python scripts in parallel on a cluster where process IDs
are not unique, this is likely to cause problems with temporary files, {as explained here<RYocc>}.

The solution is to choose a unique ID at the beginning of your Python script, before
calling the first YASARA function:

<P>
from yasara import *

# Choose text mode and unique ID before the first function call
info.mode='txt'
info.pid=123
# First function call, load a PDB file
LoadPDB("5tim")
<P>

It is then your duty to ensure that you never run two Python scripts with the same
info.pid in parallel, for example by using some job counter as the pid. The problem
with non-unique process IDs of course also affects Python's os.getpid(), so this function
`must not` be used.

If you use Python's `multiprocessing module` to run multiple YASARAs from the same Python
script, you will encounter the error 'The connection to the Python module failed with error code 4',
when a Python process exits. The reason is that the YASARA Python module installs the exit handler
function 'Exit' using atexit.register(Exit). This seems not to work with multiprocessing, so
call yasara.Exit() manually before exiting.
"""

import sys,os,time,disk,socket,atexit,string,struct,pdb_file
from python2to3 import *

#  ======================================================================
#                     C O N T A I N E R   C L A S S
#  ======================================================================

class container:
  """
  The class just provides storage for random data, and permits to access
  the various variables using a dot.
  """
  def __init__(self,type=None,data={}):
    self.type=type
    for varname in data.keys():
      self.__dict__[varname]=data[varname]

  def __setitem__(self,varname,value):
    self.__dict__[varname]=value

  def __getitem__(self,varname):
    return (self.__dict__[varname])

#  ======================================================================
#           Y A S A R A   C O M M U N I C A T I O N   C L A S S
#  ======================================================================

class yasara_communicator:

  # INITIALIZE COMMUNICATION ON A GIVEN PORT
  # ========================================
  def __init__(self):
    # THE MESSAGE IDs AND OTHER PREDEFINED VALUES
    self.REQUESTATOM=1   # Request a selection of atoms
    self.REQUESTRES=2    # Request a selection of residues
    self.REQUESTMOL=4    # Request a selection of molecules
    self.REQUESTOBJ=8    # Request a selection of objects
    self.REQUESTALL=16   # Request entire soup
    self.REQUESTINFO=17  # Request YASARA info
    self.INFO=18         # Returned YASARA info
    self.EXECUTE=19      # Execute a YASARA command
    self.RESULT=20       # Result of a YASARA command
    self.ERROR=21        # Error raised by YASARA
    self.ATOMDATA=22     # Requested YASARA atom data
    self.BUILDPDB=23     # Build PDB file in YASARA
    self.LASTINRES=1     # Flag that atom is last in residue
    self.LASTINMOL=2     # Flag that atom is last in molecule
    self.LASTINOBJ=4     # Flag that atom is last in object
    # FIND AND BLOCK A FREE PORT
    port=socket.IPPORT_USERRESERVED
    while (1):
      # MACOSX PYTHON HAS A BUG THAT REQUIRES RECREATING THE SOCKET
      # AFTER EACH CONNECTION TRY. (MAYBE APPLIES TO bind AS WELL?)
      self.srvsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      # SEE plg/yasara.py WHY THIS IS COMMENTED OUT, WORKAROUND FOR WINDOWS ME BUG
      #self.srvsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
      try:
        self.srvsock.bind(("",port))
        break
      except: port+=1
    self.srvsock.listen(1)
    self.sock=None
    self.port=port

  # ACCEPT A CONNECTION FROM YASARA
  # ===============================
  def accept(self):
    if (self.sock!=None): raise RuntimeError("Connection has already been accepted")
    # accept() IS NOT BLOCKING AS EXPECTED, IT MAY STILL TIME OUT ON SOME PLATFORMS
    (self.sock,ip)=self.srvsock.accept()

  # REPORT BROKEN CONNECTION TO YASARA
  # ==================================
  def reportbrokenconn(self):
    global pid

    pid=None
    raise RuntimeError("Connection to YASARA broken. Either you exited YASARA manually or it encountered a fatal error")

  # SEND DATA TO YASARA
  # ===================
  def send(self,data):
    global pid

    sent=0
    size=len(data)
    while (sent<size):
      # IF THE CONNECTION BREAKS, THIS RETURNS 0 IN LINUX,
      # BUT RAISES AN EXCEPTION (WHICH ONE??) IN SOME WINDOWS VERSIONS
      try: result=self.sock.send(data[sent:])
      except KeyboardInterrupt: raise
      except: self.reportbrokenconn()
      if (result==0): self.reportbrokenconn()
      sent+=result

  # RECEIVE DATA FROM YASARA
  # ========================
  def receive(self,size):
    global pid

    data=binary("")
    while (len(data)<size):
      # IF THE CONNECTION BREAKS, THIS RETURNS 0 IN LINUX,
      # BUT RAISES AN EXCEPTION (WHICH ONE??) IN SOME WINDOWS VERSIONS
      try: chunk=self.sock.recv(size-len(data))
      except KeyboardInterrupt: raise
      except: self.reportbrokenconn()
      if (len(chunk)==0): self.reportbrokenconn()
      data+=chunk
    return(data)

  # SEND A MESSAGE TO YASARA
  # ========================
  def sendmessage(self,messagetype,messagedata=""):
    header=struct.pack('ii',messagetype,len(messagedata))
    # IMPORTANT: THERE SEEMS TO BE A PROBLEM OR BUG IN THE SOCKET IMPLEMENTATION
    # (TESTED ON FEDORA CORE 5+6): IF self.send IS CALLED TWICE, THIS CAUSES AN
    # ETERNAL STALL OF ABOUT 50ms. WE THEREFORE HAVE TO CREATE A NEW COPY OF
    # THE ENTIRE PACKET TO SEND IT ALL AT ONCE
    self.send(header+binary(messagedata))

  # RECEIVE A MESSAGE FROM YASARA
  # =============================
  def receivemessage(self,expectedtype=None):
    (messagetype,datasize)=struct.unpack('ii',self.receive(8))
    data=self.receive(datasize)
    if (messagetype==self.ATOMDATA):
      # RECEIVE PART OF THE YASARA SOUP
      (atoms,crdsys)=struct.unpack('ii',data[:8])
      messagedata=pdb_file.interface()
      messagedata.crdsys=crdsys
      # BUILD A DICTIONARY THAT MAPS YASARA ATOM NUMBERS TO ATOM NUMBER IN THE SOUP PORTION
      atomidx={}
      pos=12
      for i in range(atoms):
        atom=pdb_file.pdb_atom()
        (atom.num,atom.name4,atom.altloc,atom.element,atom.resinscode,flags,
         atom.resname,padding,atom.resnum,atom.molname,atom.segname,atom.pos.x,atom.pos.y,atom.pos.z,
         atom.occupancy,atom.bfactor,atom.property,atom.bonds)=struct.unpack('i4scbcb3sc4s4s4sffffffi',data[pos:pos+56])
        # CONVERT PYTHON3 BYTES TO STRINGS
        atom.name4=text(atom.name4)
        atom.altloc=text(atom.altloc)
        atom.resinscode=text(atom.resinscode)
        atom.resname=text(atom.resname)
        atom.resnum=text(atom.resnum)
        atom.molname=text(atom.molname)
        atom.segname=text(atom.segname)
        pos+=56
        atom.name=atom.name4.strip()
        atom.crdsys=crdsys
        atomidx[atom.num]=i
        # CONVERT RESIDUE NUMBER
        if (atom.resinscode=='\x00'):
          try: atom.resnum=int(atom.resnum)
          except: pass
        else: atom.resnum+=atom.resinscode
        # MOLECULE NAME MAY HAVE TERMINAL ZEROES */
        atom.molname=atom.molname.strip('\x00')
        # USE None FOR EMPTY ALTLOC/SEGNAME
        if (atom.altloc=='\x00'): atom.altloc=None
        if (atom.segname=='\x00\x00\x00\x00'): atom.segname=None
        atom.bond=[]
        if (atom.bonds):
          # GET THE BONDS
          bondlist=struct.unpack('i'*atom.bonds,data[pos:pos+atom.bonds*4])
          pos+=atom.bonds*4
          for j in range(atom.bonds):
            bond=container()
            bond.order=(bondlist[j]>>24)&15
            if (bond.order>3):
              # CONVERT YASARA'S INTERNAL INTEGER BOND ORDERS TO FLOATING POINT NUMBERS
              if (bond.order==4): bond.order=1.5
              elif (bond.order==5): bond.order=1.25
              elif (bond.order==6): bond.order=1.33
              elif (bond.order==7): bond.order=1.66
              elif (bond.order==8): bond.order=1.75
              elif (bond.order==9): bond.order=4
              elif (bond.order==10): bond.order=2.5
            bond.atomnum=bondlist[j]&0xffffff
            atom.bond.append(bond)
        # MARK THE LAST ATOM IN EACH RESIDUE/MOLECULE/OBJECT TO HELP messagedata.update()
        atom.lastinres=flags&self.LASTINRES;
        atom.lastinmol=flags&self.LASTINMOL;
        atom.lastinobj=flags&self.LASTINOBJ;
        messagedata.atom.append(atom)
      # FINALIZE THE BONDS, NOW THAT atomidx IS COMPLETE */
      for i in range(atoms):
        atom=messagedata.atom[i]
        for j in range(atom.bonds):
          atom.bond[j].atomidx=atomidx.get(atom.bond[j].atomnum)
          if (atom.bond[j].atomidx==None): atom.bond[j].atom=None
          else: atom.bond[j].atom=messagedata.atom[atom.bond[j].atomidx]
      # MAYBE THE USER WANTS atomidx TOO
      messagedata.atomidx=atomidx
      # CREATE THE HIGHER LEVEL DATA STRUCTURES
      messagedata.update()
      # ADD THE OBJECT INFO
      objlist=pickle.loads(data[pos:])
      if (messagedata.objects*2!=len(objlist)): raise RuntimeError("Object data did not match atom data")
      for i in range(messagedata.objects):
        messagedata.object[i].num=objlist[i*2]
        messagedata.object[i].name=objlist[i*2+1]
    else:
      # ALL OTHER MESSAGES RETURN A PICKLED LIST
      messagedata=pickle.loads(data)
      if (messagetype==self.ERROR):
        raise RuntimeError("YASARA raised error %d: %s"%(messagedata[0],messagedata[1]))
    if (expectedtype!=None and messagetype!=expectedtype):
      raise RuntimeError("Unexpected message type received")
    if (expectedtype==None): return((messagetype,messagedata))
    else: return(messagedata)

#  ======================================================================
#                    Y A S A R A   I N F O   C L A S S
#  ======================================================================

class yasara_info(container):
  """
  This class stores YASARA data, which may have to be updated upon each access
  """
  def __getattr__(self,item):
    global pid,com,info,yasaradir

    if (pid==None): start()
    if (item=='dir'):
      # THE YASARA FOLDER IS IN sys.path
      for dir in sys.path:
        idx=dir.find("yasara"+os.sep+"pym")
        if (idx!=-1): return(dir[:idx+6])
      return(None)
    # RETRIEVE DATA FROM YASARA
    com.sendmessage(com.REQUESTINFO)
    infolist=com.receivemessage(com.INFO);
    # QUICKLY RETURN VARIABLES THAT CHANGE OVER TIME
    if (item=="atoms"): return(infolist[6])
    if (item=="objects"): return(infolist[7])
    if (item=="firstobj"): return(infolist[8])
    if (item=="lastobj"): return(infolist[9])
    if (item=="leftbutton"): return(infolist[10])
    if (item=="middlebutton"): return(infolist[11])
    if (item=="rightbutton"): return(infolist[12])
    if (item=="energyunit"): return(infolist[13])
    if (item=="speedmax"): return(infolist[14])
    if (item=="pluginrequest"): return(infolist[15])
    # THE FOLLOWING VARIABLES ARE CONSTANTS, STORING THEM IN __dict__
    # MAKES SURE THAT WE DON'T HAVE TO REQUEST THEM AGAIN, SINCE __getattr__
    # IS THEN NOT CALLED ANYMORE.
    self.serialnumber=infolist[0]
    self.version=infolist[1]
    self.stage=infolist[2]
    self.owner=container()
    self.owner.email=infolist[3]
    self.owner.firstname=infolist[4]
    self.owner.lastname=infolist[5]
    return(self.__dict__[item])

  def __getitem__(self,item):
    return(self.__getattr__(item))

  def __repr__(self):
    return("The content of 'info' is dynamically updated and cannot be printed all at once")

#  ======================================================================
#         Y A S A R A   M O D U L E   I N I T I A L I Z A T I O N
#  ======================================================================

# YASARA PROCESS ID AS SOON AS IT HAS BEEN STARTED
pid=None

# THE COMMUNICATION CHANNEL TO YASARA
com=None

# FLAG IF WE REGISTERED THE EXIT FUNCTION
exitregistered=0

# SINCE WE START YASARA ONLY WHEN THE FIRST COMMAND IS RUN, ALL DATA
# FOR THE USER MUST BE STORED IN A CLASS, BECAUSE WE HAVE AN IMPORTING
# MODULE LAYER IN BETWEEN
info=yasara_info()

# MODE FOR RUNNING YASARA: 'gra' (GRAPHICS), 'con' (FANCY CONSOLE) OR 'txt' (TEXT ONLY)
info.mode='gra'
info.pid=None
info.licenseshown=1

# DETERMINE OPERATING SYSTEM
if (os.name.lower()=="nt"): info.opsys="Windows"
else:
  try:
    import platform
    info.opsys=platform.system()
    if (info.opsys=="Darwin"): info.opsys="MacOS"
  except:
    # platform MODULE DOES NOT YET EXIST (EARLY PYTHONS)
    if (os.path.exists("/Applications/Finder")): info.opsys="MacOS"
    else: info.opsys="Linux"

# FIND YASARA DIRECTORY AND EXECUTABLE
for path in sys.path:
  # BROKEN PYTHON MAY ADD A TERMINAL SLASH
  path=path.rstrip(os.sep)
  if (path[-10:]=='yasara'+os.sep+'pym'):
    directory=path[:-4]
    break
else: raise RuntimeError("Could not find YASARA, do not import yasaramodule.py directly")
if (info.opsys=="Linux"):
  # THIS IS FOR INTERAL USE, IN CASE 'yasara' IS BEING RECOMPILED. DON'T DO IT, SINCE
  # USERS MAY ALSO STORE OLD YASARAs AS yasara2, THEN TROUBLE LIES AHEAD...
  #executable=os.path.join(directory,"yasara2")
  #if (not os.path.exists(executable)):
  executable=os.path.join(directory,"yasara")
elif (info.opsys=="Windows"): executable=os.path.join(directory,"YASARA.exe")
else: executable=os.path.join(os.path.dirname(directory),"MacOS/yasara.app")
if (not os.path.exists(executable)): raise RuntimeError("Could not find YASARA at "+executable+", please reinstall")
# IN MODELS@HOME, AN UPDATED YASARA STILL NEEDS TO BE MADE EXECUTABLE. 511 IS 0777, WHICH DOESN'T WORK IN PYTHON 3
try: os.chmod(executable,511)
except: print("Failed to make %s executable"%executable)

#  ======================================================================
#                H E L P E R   F U N C T I O N   G R O U P
#  ======================================================================

# REGISTER EXIT HANDLER
# =====================
def registerexit():
  global exitregistered

  if (not exitregistered):
    # WHEN THE PYTHON MODULE EXITS, YASARA ALSO NEEDS TO CLOSE
    atexit.register(Exit)
    exitregistered=1

# START YASARA
# ============
def start():
  global pid,com,info

  # PREPARE TO ACCEPT CONNECTION TO YASARA
  com=yasara_communicator()
  # START YASARA, PROVIDING com.port AS COMMAND LINE ARGUMENT
  arglist=[executable,"-pym",str(com.port),"-"+info.mode]
  if (info.opsys=="Windows"):
    # QUOTING THE executable IN arglist[0] IS A WORKAROUND FOR A WINDOWS XP BUG THAT
    # SHOWS UP IF executable CONTAINS SPACES. DO THIS HOWEVER ONLY IN WINDOWS,
    # SINCE IT TRIGGERS A MACOSX BUG (RegisterProcess failed (error = -50))
    arglist[0]='"'+arglist[0]+'"'
  if (info.pid!=None):
    # USER REQUESTED TO RUN YASARA WITH A CERTAIN PID IN TEMP FILES ON A CLUSTER,
    # ALSO DISABLE THE THREAD SCHEDULER IN ONE SHOT
    arglist+=["-pid",str(info.pid)]
  if (not info.licenseshown): arglist.append("-nls")
  #print "Starting YASARA "+executable+" with mode "+info.mode
  pid=os.spawnv(os.P_NOWAIT,executable,arglist)
  # WAIT UNTIL YASARA CONNECTS
  com.accept()
  registerexit()

# RESTART YASARA
# ==============
def restart():
  global pid

  print("WARNING - YASARA disappeared unexpectedly, restarting now. Do not close the YASARA window manually, instead terminate this script.")
  os.waitpid(pid,0)
  start()

# EXIT YASARA
# ===========
def Exit():
  global pid,com

  if (pid!=None):
    com.sendmessage(com.EXECUTE,"Exit")
    os.waitpid(pid,0)
    pid=None

# CONNECT TO A YASARA THAT IS ALREADY RUNNING
# ===========================================
# This method is used if the Python module is launched from a Python plugin, so
# we want to connect to the already running YASARA instead of launching a new one.
# Connecting requires the process ID of the already running YASARA, and the name
# of a temporary file where YASARA looks for the communication port, both can be
# found in the original 'yasara.request' string
def connect(request):
  global pid,com

  if (request[:12]!="LaunchModule"):
    print("ERROR - The request passed to the connect method does not start with 'LaunchModule'")
    raise SystemExit
  portfilename=request[12:]
  # OPEN A SOCKET TO COMMUNICATE WITH YASARA, CHOOSE NEXT FREE PORT NUMBER
  com=yasara_communicator()
  # CREATE THE PID/PORT FILE ATOMICALLY BY RENAMING, SO THAT YASARA WON'T
  # ACCIDENTALLY READ A HALF-WRITTEN FILE
  tmpfilename=portfilename+"_tmp"
  open(tmpfilename,"w").write("%d %d"%(os.getpid(),com.port))
  os.rename(tmpfilename,portfilename)
  # WAIT UNTIL YASARA HAS READ THE FILE AND CONNECTS TO OUR SOCKET
  com.accept()
  # REMEMBER YASARA's PID, WHICH IS PART OF THE FILENAME
  pid=int(portfilename[portfilename.rfind('_')+1:])
  registerexit()

# PROCESS A PYTHON MODULE REQUEST IN YASARA
# =========================================
def process(messagetype,messagedata):
  global pid

  if (pid==None): start()
  if (messagetype=="BUILDPDB"): messagetype=com.BUILDPDB
  else: messagetype=com.EXECUTE
  # DO NOT CATCH CONNECTION PROBLEMS, HANDLE THE EXCEPTION NORMALLY
  com.sendmessage(messagetype,messagedata)
  result=com.receivemessage(com.RESULT)
  return(result)

# RUN A COMMAND IN YASARA
# =======================
def run(command):
  if (command.find("\n")==-1): return(process("EXECUTE",command))
  # THIS IS A MULTI-LINE COMMAND, SEND EACH LINE SEPARATELY SO THAT ALL ERRORS CAN BE CAUGHT
  comlist=command.split("\n")
  resultlist=[]
  for com in comlist: resultlist.append(process("EXECUTE",com))
  return(resultlist)

# GET PART OF THE YASARA SOUP
# ===========================
def soup(unit,selection):
  if (pid==None): start()
  com.sendmessage(unit,selection)
  return(com.receivemessage(com.ATOMDATA))

# CLEAN STRING
# ============
def cstr(text,quoted=0):
  text=str(text)
  text=text.replace("\n","\\n")
  text=text.replace("\r","\\r")
  text=text.replace("\t","\\t")
  if (quoted):
    for quote in ['"',"'"]:
      if (text.find(quote)==-1): break
    else:
      quote='"'
      text=text.replace(quote,"'")
    text=quote+text+quote
  return(text)

# CONVERT SELECTION TO STRING
# ===========================
def selstr(selection):
  if (type(selection) in [type(""),type(u""),type(1),type(1.)]): selstr=cstr(selection)
  else:
    if (type(selection)!=type([])): selection=list(selection)
    selstr=""
    for i in range(len(selection)):
      if (i>0 and type(selection[i])==type("") and type(selection[i-1])==type("") and
          ((selection[i][:9]=="Res Atom " and selection[i-1][:9]=="Res Atom ") or
           (selection[i][:9]=="Mol Atom " and selection[i-1][:9]=="Mol Atom "))):
        # WE CAN COMPRESS THE UNIQUE RESIDUE/MOLECULE IDs (SEE DOCS OF List COMMAND)
        selstr+=cstr(selection[i][9:]+" ")
      else: selstr+=cstr(selection[i])+" "
  selstr=selstr.strip()
  if (selstr==""): selstr="none"
  return(selstr)

# DEPRECATED COMMANDS, KEEP PYTHON WRAPPERS FOR BACKWARDS COMPATIBILITY:
# SINCE 2017-02:
def Renumber(first=None): Number(first=None)
def RenumberAll(first=None): NumberAll(first)
def RenumberObj(selection1, first=None): NumberObj(selection1, first)
def RenumberRes(selection1, first=None, inscode=None, increment=None): NumberRes(selection1, first, inscode, increment)
def RenumberAtom(selection1, first=None): NumberAtom(selection1, first)

#  ======================================================================
#         Y A S A R A   C O M M A N D   F U N C T I O N   G R O U P
#  ======================================================================

#  ============ S P E C I A L   Y A S A R A   C O M M A N D S ===========

# GET AN ATOM SELECTION FROM YASARA
# =================================
def Atom(selection):
  return(soup(com.REQUESTATOM,str(selection)))

# GET A RESIDUE SELECTION FROM YASARA
# ===================================
def Residue(selection):
  return(soup(com.REQUESTRES,str(selection)))

# GET A MOLECULE SELECTION FROM YASARA
# ====================================
def Molecule(selection):
  return(soup(com.REQUESTMOL,str(selection)))

# GET AN OBJECT SELECTION FROM YASARA
# ===================================
def Object(selection):
  return(soup(com.REQUESTOBJ,str(selection)))

# GET THE ENTIRE YASARA SOUP
# ==========================
def All():
  return(soup(com.REQUESTALL,""))

# BUILD A PDB FILE IN YASARA
# ==========================
def BuildPDB(pdb):
  if (type(pdb)==type([])): pdb='\n'.join(pdb)
  elif (type(pdb)!=type("")): pdb=str(pdb)
  return(process("BUILDPDB",pdb))

#  ============= N O R M A L   Y A S A R A   C O M M A N D S ============

# SET/GET ACCELERATION OF ATOMS (ALL OR SELECTED)
# ===============================================
def Accel(x=None, y=None, z=None):
  command='Accel '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET ACCELERATION OF ATOMS (ALL)
# ===================================
def AccelAll(x=None, y=None, z=None):
  command='AccelAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET ACCELERATION OF ATOMS (OBJECT)
# ======================================
def AccelObj(selection1, x=None, y=None, z=None):
  command='AccelObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET ACCELERATION OF ATOMS (MOLECULE)
# ========================================
def AccelMol(selection1, x=None, y=None, z=None):
  command='AccelMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET ACCELERATION OF ATOMS (RESIDUE)
# =======================================
def AccelRes(selection1, x=None, y=None, z=None):
  command='AccelRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET ACCELERATION OF ATOMS (ATOM)
# ====================================
def AccelAtom(selection1, x=None, y=None, z=None):
  command='AccelAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# ADD ANGLE TO FORCE FIELD
# ========================
def AddAngle(selection1, selection2, selection3, Min=None, bfc=None):
  command='AddAngle '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (bfc!=None): command+='BFC='+cstr(bfc)+','
  run(command[:-1])

# ADD COVALENT BONDS
# ==================
def AddBond(selection1, selection2, order=None, update=None, lenmax=None):
  command='AddBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (lenmax!=None): command+='LenMax='+cstr(lenmax)+','
  run(command[:-1])

# ADD N/C-TERMINAL CAPPING GROUPS (ALL OR SELECTED)
# =================================================
def AddCap(Type=None, location=None):
  command='AddCap '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (location!=None): command+='Location='+cstr(location)+','
  run(command[:-1])

# ADD N/C-TERMINAL CAPPING GROUPS (ALL)
# =====================================
def AddCapAll(Type=None, location=None):
  command='AddCapAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (location!=None): command+='Location='+cstr(location)+','
  run(command[:-1])

# ADD N/C-TERMINAL CAPPING GROUPS (OBJECT)
# ========================================
def AddCapObj(selection1, Type=None, location=None):
  command='AddCapObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (location!=None): command+='Location='+cstr(location)+','
  run(command[:-1])

# ADD DIHEDRAL TO FORCE FIELD
# ===========================
def AddDihedral(selection1, selection2, selection3, selection4, barrier=None, period=None, phase=None):
  command='AddDihedral '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  if (barrier!=None): command+='Barrier='+cstr(barrier)+','
  if (period!=None): command+='Period='+cstr(period)+','
  if (phase!=None): command+='Phase='+cstr(phase)+','
  run(command[:-1])

# SUM ATOM DISPLACEMENTS TO CALCULATE CROSS-CORRELATION COEFFICIENTS (MOLECULE)
# =============================================================================
def AddDispMol(selection1, selection2):
  command='AddDispMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# SUM ATOM DISPLACEMENTS TO CALCULATE CROSS-CORRELATION COEFFICIENTS (RESIDUE)
# ============================================================================
def AddDispRes(selection1, selection2):
  command='AddDispRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# SUM ATOM DISPLACEMENTS TO CALCULATE CROSS-CORRELATION COEFFICIENTS (ATOM)
# =========================================================================
def AddDispAtom(selection1, selection2):
  command='AddDispAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (ALL OR SELECTED)
# =============================================================
def AddEnv():
  command='AddEnv '
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (ALL)
# =================================================
def AddEnvAll():
  command='AddEnvAll '
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (OBJECT)
# ====================================================
def AddEnvObj(selection1):
  command='AddEnvObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (MOLECULE)
# ======================================================
def AddEnvMol(selection1):
  command='AddEnvMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (RESIDUE)
# =====================================================
def AddEnvRes(selection1):
  command='AddEnvRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# ADD TO ENVIRONMENT FOR SURFACE CALCULATIONS (ATOM)
# ==================================================
def AddEnvAtom(selection1):
  command='AddEnvAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# ADD ELECTROSTATIC FIELD
# =======================
def AddESF(x=None, y=None, z=None):
  command='AddESF '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ADD MISSING HYDROGENS (ALL OR SELECTED)
# =======================================
def AddHyd(number=None, update=None):
  command='AddHyd '
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD MISSING HYDROGENS (ALL)
# ===========================
def AddHydAll(number=None, update=None):
  command='AddHydAll '
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD MISSING HYDROGENS (OBJECT)
# ==============================
def AddHydObj(selection1, number=None, update=None):
  command='AddHydObj '
  command+=selstr(selection1)+','
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD MISSING HYDROGENS (MOLECULE)
# ================================
def AddHydMol(selection1, number=None, update=None):
  command='AddHydMol '
  command+=selstr(selection1)+','
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD MISSING HYDROGENS (RESIDUE)
# ===============================
def AddHydRes(selection1, number=None, update=None):
  command='AddHydRes '
  command+=selstr(selection1)+','
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD MISSING HYDROGENS (ATOM)
# ============================
def AddHydAtom(selection1, number=None, update=None):
  command='AddHydAtom '
  command+=selstr(selection1)+','
  if (number!=None): command+='Number='+cstr(number)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# ADD A KEY-VALUE PAIR TO CALCULATE AVERAGES
# ==========================================
def AddPair(key, value):
  command='AddPair '
  command+='Key='+cstr(key)+','
  command+='Value='+cstr(value)+','
  run(command[:-1])

# ADD ATOM POSITIONS TO CALCULATE AVERAGE, STANDARD DEVIATION AND PRINCIPAL COMPONENTS (MOLECULE)
# ===============================================================================================
def AddPosMol(selection1, selection2):
  command='AddPosMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# ADD ATOM POSITIONS TO CALCULATE AVERAGE, STANDARD DEVIATION AND PRINCIPAL COMPONENTS (RESIDUE)
# ==============================================================================================
def AddPosRes(selection1, selection2):
  command='AddPosRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# ADD ATOM POSITIONS TO CALCULATE AVERAGE, STANDARD DEVIATION AND PRINCIPAL COMPONENTS (ATOM)
# ===========================================================================================
def AddPosAtom(selection1, selection2):
  command='AddPosAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# ADD TERMINAL RESIDUE
# ====================
def AddRes(name, selection1, omega=None, phi=None, psi=None, tau=None, end=None, isomer=None):
  command='AddRes '
  command+='Name='+cstr(name)+','
  command+=selstr(selection1)+','
  if (omega!=None): command+='Omega='+cstr(omega)+','
  if (phi!=None): command+='Phi='+cstr(phi)+','
  if (psi!=None): command+='Psi='+cstr(psi)+','
  if (tau!=None): command+='Tau='+cstr(tau)+','
  if (end!=None): command+='End='+cstr(end)+','
  if (isomer!=None): command+='Isomer='+cstr(isomer)+','
  run(command[:-1])

# ADD TERMINAL RESIDUE
# ====================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def AddRes2(name, selection1, epsilon=None, zeta=None, alpha=None, beta=None, gamma=None, end=None):
  command='AddRes '
  command+='Name='+cstr(name)+','
  command+=selstr(selection1)+','
  if (epsilon!=None): command+='Epsilon='+cstr(epsilon)+','
  if (zeta!=None): command+='Zeta='+cstr(zeta)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  if (end!=None): command+='End='+cstr(end)+','
  run(command[:-1])

# ADD BOND OR POSITION RESTRAINT TO FORCE FIELD
# =============================================
def AddSpring(selection1, selection2, len=None, sfc=None):
  command='AddSpring '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (len!=None): command+='Len='+cstr(len)+','
  if (sfc!=None): command+='SFC='+cstr(sfc)+','
  run(command[:-1])

# ADD CELLS TO TABLE
# ==================
def Tabulate(value):
  command='Tabulate '
  command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# ADD C-TERMINAL OXYGENS (ALL OR SELECTED)
# ========================================
def AddTer():
  command='AddTer '
  run(command[:-1])

# ADD C-TERMINAL OXYGENS (ALL)
# ============================
def AddTerAll():
  command='AddTerAll '
  run(command[:-1])

# ADD C-TERMINAL OXYGENS (OBJECT)
# ===============================
def AddTerObj(selection1):
  command='AddTerObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# ADD OBJECTS TO THE SOUP (ALL OR SELECTED)
# =========================================
def Add():
  command='Add '
  return(run(command[:-1]))

# ADD OBJECTS TO THE SOUP (ALL)
# =============================
def AddAll():
  command='AddAll '
  return(run(command[:-1]))

# ADD OBJECTS TO THE SOUP (OBJECT)
# ================================
def AddObj(selection1):
  command='AddObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# ALIGN MULTIPLE OBJECTS (ALL OR SELECTED)
# ========================================
def AlignMulti(parameter=None):
  command='AlignMulti '
  if (parameter!=None): command+='Parameter='+cstr(parameter)+','
  return(run(command[:-1]))

# ALIGN MULTIPLE OBJECTS (ALL)
# ============================
def AlignMultiAll(parameter=None):
  command='AlignMultiAll '
  if (parameter!=None): command+='Parameter='+cstr(parameter)+','
  return(run(command[:-1]))

# ALIGN MULTIPLE OBJECTS (OBJECT)
# ===============================
def AlignMultiObj(selection1, parameter=None):
  command='AlignMultiObj '
  command+=selstr(selection1)+','
  if (parameter!=None): command+='Parameter='+cstr(parameter)+','
  return(run(command[:-1]))

# SET/GET ALIGNMENT PARAMETERS
# ============================
def AlignPar(dismax=None, anglemax=None, lenmin=None, gapopen=None, gapextend=None, overhang=None):
  command='AlignPar '
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  if (anglemax!=None): command+='AngleMax='+cstr(anglemax)+','
  if (lenmin!=None): command+='LenMin='+cstr(lenmin)+','
  if (gapopen!=None): command+='GapOpen='+cstr(gapopen)+','
  if (gapextend!=None): command+='GapExtend='+cstr(gapextend)+','
  if (overhang!=None): command+='Overhang='+cstr(overhang)+','
  return(run(command[:-1]))

# ALIGN SIMILAR PROTEINS FROM THE PDB
# ===================================
def AlignPDBMol(selection1, method=None, structures=None, coverage=None, seqidmax=None, filename=None, format=None):
  command='AlignPDBMol '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  if (coverage!=None): command+='Coverage='+cstr(coverage)+','
  if (seqidmax!=None): command+='SeqIdMax='+cstr(seqidmax)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# ALIGN ATOMS
# ===========
def AlignAtom(selection1, selection2, method=None, alignmatch=None, resultmatch=None, dismax=None, minimize=None, duplicate=None):
  command='AlignAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (alignmatch!=None): command+='AlignMatch='+cstr(alignmatch)+','
  if (resultmatch!=None): command+='ResultMatch='+cstr(resultmatch)+','
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  if (minimize!=None): command+='Minimize='+cstr(minimize)+','
  if (duplicate!=None): command+='Duplicate='+cstr(duplicate)+','
  return(run(command[:-1]))

# ALIGN OBJECTS AND MOLECULES (OBJECT)
# ====================================
def AlignObj(selection1, selection2, method=None, parameter=None, results=None, copyresnum=None):
  command='AlignObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (parameter!=None): command+='Parameter='+cstr(parameter)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (copyresnum!=None): command+='CopyResNum='+cstr(copyresnum)+','
  return(run(command[:-1]))

# ALIGN OBJECTS AND MOLECULES (MOLECULE)
# ======================================
def AlignMol(selection1, selection2, method=None, parameter=None, results=None, copyresnum=None):
  command='AlignMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (parameter!=None): command+='Parameter='+cstr(parameter)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (copyresnum!=None): command+='CopyResNum='+cstr(copyresnum)+','
  return(run(command[:-1]))

# SET/GET ANGLE BETWEEN ATOMS
# ===========================
def Angle(selection1, selection2, selection3, bound=None, set=None):
  command='Angle '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  if (bound!=None): command+='bound='+cstr(bound)+','
  if (set!=None): command+='set='+cstr(set)+','
  return(run(command[:-1]))

# GET ANGLE BETWEEN TWO VECTORS
# =============================
def AngleVec(x1=None, y1=None, z1=None, x2=None, y2=None, z2=None):
  command='AngleVec '
  if (x1!=None): command+='X1='+cstr(x1)+','
  if (y1!=None): command+='Y1='+cstr(y1)+','
  if (z1!=None): command+='Z1='+cstr(z1)+','
  if (x2!=None): command+='X2='+cstr(x2)+','
  if (y2!=None): command+='Y2='+cstr(y2)+','
  if (z2!=None): command+='Z2='+cstr(z2)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# ANIMATE APPEARANCE AND DISAPPEARANCE OF IMAGES
# ==============================================
def AnimateImage(selection1, enter=None, rest=None, leave=None, steps=None):
  command='AnimateImage '
  command+=selstr(selection1)+','
  if (enter!=None): command+='Enter='+cstr(enter)+','
  if (rest!=None): command+='Rest='+cstr(rest)+','
  if (leave!=None): command+='Leave='+cstr(leave)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  run(command[:-1])

# ANIMATE WINDOWS
# ===============
def AnimateWin(Type):
  command='AnimateWin '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SET SIMULATED ANNEALING STEPS
# =============================
def AnnealSteps(number):
  command='AnnealSteps '
  command+='Number='+cstr(number)+','
  run(command[:-1])

# SWITCH ANTIALIASING ON/OFF
# ==========================
def Antialias(level):
  command='Antialias '
  command+='Level='+cstr(level)+','
  run(command[:-1])

# APPLY MACRO TO MULTIPLE TARGETS OR FILES
# ========================================
def ApplyMacro(filename, targets, remove=None, newextension=None):
  command='ApplyMacro '
  command+='Filename='+cstr(filename)+','
  command+='Targets='+cstr(targets)+','
  if (remove!=None): command+='Remove='+cstr(remove)+','
  if (newextension!=None): command+='NewExtension='+cstr(newextension)+','
  run(command[:-1])

# SWITCH PLASMA INSIDE ATOMS ON/OFF
# =================================
def AtomPlasma(flag):
  command='AtomPlasma '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# SET SIZE OF ATOMS
# =================
def AtomSize(radius):
  command='AtomSize '
  command+='Radius='+cstr(radius)+','
  run(command[:-1])

# SWITCH ELEMENT SYMBOL INSIDE ATOMS ON/OFF
# =========================================
def AtomSymbol(flag):
  command='AtomSymbol '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# SET TEXTURE STYLE OF ATOMS
# ==========================
def AtomTexture(Type):
  command='AtomTexture '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# MOVE IMAGES AUTOMATICALLY
# =========================
def AutoMoveImage(selection1, x=None, y=None, width=None, height=None, alpha=None, steps=None, cycle=None, zoom3d=None):
  command='AutoMoveImage '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (cycle!=None): command+='Cycle='+cstr(cycle)+','
  if (zoom3d!=None): command+='Zoom3D='+cstr(zoom3d)+','
  run(command[:-1])

# POSITION AND ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL OR SELECTED)
# ===============================================================================================
def AutoPosOri(x, y, z, alpha, beta, gamma, steps=None, wait=None):
  command='AutoPosOri '
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# POSITION AND ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL)
# ===================================================================================
def AutoPosOriAll(x, y, z, alpha, beta, gamma, steps=None, wait=None):
  command='AutoPosOriAll '
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# POSITION AND ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (OBJECT)
# ======================================================================================
def AutoPosOriObj(selection1, x, y, z, alpha, beta, gamma, steps=None, wait=None):
  command='AutoPosOriObj '
  command+=selstr(selection1)+','
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# POSITION OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL OR SELECTED)
# ====================================================================================
def AutoPos(x=None, y=None, z=None, steps=None, wait=None, shape=None, shapepar=None):
  command='AutoPos '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  if (shape!=None): command+='Shape='+cstr(shape)+','
  if (shapepar!=None): command+='ShapePar='+cstr(shapepar)+','
  run(command[:-1])

# POSITION OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL)
# ========================================================================
def AutoPosAll(x=None, y=None, z=None, steps=None, wait=None, shape=None, shapepar=None):
  command='AutoPosAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  if (shape!=None): command+='Shape='+cstr(shape)+','
  if (shapepar!=None): command+='ShapePar='+cstr(shapepar)+','
  run(command[:-1])

# POSITION OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (OBJECT)
# ===========================================================================
def AutoPosObj(selection1, x=None, y=None, z=None, steps=None, wait=None, shape=None, shapepar=None):
  command='AutoPosObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  if (shape!=None): command+='Shape='+cstr(shape)+','
  if (shapepar!=None): command+='ShapePar='+cstr(shapepar)+','
  run(command[:-1])

# MOVE OBJECTS OR SCENE AUTOMATICALLY (ALL OR SELECTED)
# =====================================================
def AutoMove(x=None, y=None, z=None):
  command='AutoMove '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE OBJECTS OR SCENE AUTOMATICALLY (ALL)
# =========================================
def AutoMoveAll(x=None, y=None, z=None):
  command='AutoMoveAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE OBJECTS OR SCENE AUTOMATICALLY (OBJECT)
# ============================================
def AutoMoveObj(selection1, x=None, y=None, z=None):
  command='AutoMoveObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL OR SELECTED)
# ==================================================================================
def AutoOri(alpha, beta, gamma, steps=None, wait=None):
  command='AutoOri '
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (ALL)
# ======================================================================
def AutoOriAll(alpha, beta, gamma, steps=None, wait=None):
  command='AutoOriAll '
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ORIENT OBJECTS OR SCENE AUTOMATICALLY IN A GIVEN NUMBER OF STEPS (OBJECT)
# =========================================================================
def AutoOriObj(selection1, alpha, beta, gamma, steps=None, wait=None):
  command='AutoOriObj '
  command+=selstr(selection1)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ROTATE OBJECTS OR SCENE AUTOMATICALLY (ALL OR SELECTED)
# =======================================================
def AutoRotate(x=None, y=None, z=None):
  command='AutoRotate '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE OBJECTS OR SCENE AUTOMATICALLY (ALL)
# ===========================================
def AutoRotateAll(x=None, y=None, z=None):
  command='AutoRotateAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE OBJECTS OR SCENE AUTOMATICALLY (OBJECT)
# ==============================================
def AutoRotateObj(selection1, x=None, y=None, z=None):
  command='AutoRotateObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# AVERAGE KEY-VALUE PAIRS COLLECTED BEFORE
# ========================================
def AveragePair(snapshots, splitkey):
  command='AveragePair '
  command+='Snapshots='+cstr(snapshots)+','
  command+='SplitKey='+cstr(splitkey)+','
  return(run(command[:-1]))

# AVERAGE ATOM POSITIONS (MOLECULE)
# =================================
def AveragePosMol(selection1):
  command='AveragePosMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# AVERAGE ATOM POSITIONS (RESIDUE)
# ================================
def AveragePosRes(selection1):
  command='AveragePosRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# AVERAGE ATOM POSITIONS (ATOM)
# =============================
def AveragePosAtom(selection1):
  command='AveragePosAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SET BALL AND STICK RADII IN BALLS&STICKS
# ========================================
def BallStickRadius(ball=None, stick=None):
  command='BallStickRadius '
  if (ball!=None): command+='Ball='+cstr(ball)+','
  if (stick!=None): command+='Stick='+cstr(stick)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (ALL OR SELECTED)
# =============================================
def BallStick():
  command='BallStick '
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (ALL)
# =================================
def BallStickAll():
  command='BallStickAll '
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (OBJECT)
# ====================================
def BallStickObj(selection1):
  command='BallStickObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (MOLECULE)
# ======================================
def BallStickMol(selection1):
  command='BallStickMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (RESIDUE)
# =====================================
def BallStickRes(selection1):
  command='BallStickRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS&STICKS (ATOM)
# ==================================
def BallStickAtom(selection1):
  command='BallStickAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS (ALL OR SELECTED)
# ======================================
def Ball():
  command='Ball '
  run(command[:-1])

# STYLE ATOMS AS BALLS (ALL)
# ==========================
def BallAll():
  command='BallAll '
  run(command[:-1])

# STYLE ATOMS AS BALLS (OBJECT)
# =============================
def BallObj(selection1):
  command='BallObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS (MOLECULE)
# ===============================
def BallMol(selection1):
  command='BallMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS (RESIDUE)
# ==============================
def BallRes(selection1):
  command='BallRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS BALLS (ATOM)
# ===========================
def BallAtom(selection1):
  command='BallAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (ALL OR SELECTED)
# ==============================================================
def Bend(radius, dimensions=None, angle=None):
  command='Bend '
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (ALL)
# ==================================================
def BendAll(radius, dimensions=None, angle=None):
  command='BendAll '
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (OBJECT)
# =====================================================
def BendObj(selection1, radius, dimensions=None, angle=None):
  command='BendObj '
  command+=selstr(selection1)+','
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (MOLECULE)
# =======================================================
def BendMol(selection1, radius, dimensions=None, angle=None):
  command='BendMol '
  command+=selstr(selection1)+','
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (RESIDUE)
# ======================================================
def BendRes(selection1, radius, dimensions=None, angle=None):
  command='BendRes '
  command+=selstr(selection1)+','
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# BEND ATOMS OR MESH ONTO A CYLINDER OR SPHERE (ATOM)
# ===================================================
def BendAtom(selection1, radius, dimensions=None, angle=None):
  command='BendAtom '
  command+=selstr(selection1)+','
  command+='Radius='+cstr(radius)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (angle!=None): command+='Angle='+cstr(angle)+','
  run(command[:-1])

# CALCULATE BINDING ENERGIES
# ==========================
def BindEnergyObj(selection1):
  command='BindEnergyObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (ALL OR SELECTED)
# ======================================
def BFactor(value=None):
  command='BFactor '
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (ALL)
# ==========================
def BFactorAll(value=None):
  command='BFactorAll '
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (OBJECT)
# =============================
def BFactorObj(selection1, value=None):
  command='BFactorObj '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (MOLECULE)
# ===============================
def BFactorMol(selection1, value=None):
  command='BFactorMol '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (RESIDUE)
# ==============================
def BFactorRes(selection1, value=None):
  command='BFactorRes '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE B-FACTOR (ATOM)
# ===========================
def BFactorAtom(selection1, value=None):
  command='BFactorAtom '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SORT DISTANCES INTO BINS TO CALCULATE THE RADIAL DISTRIBUTION FUNCTION
# ======================================================================
def BinDistance(selection1, selection2, bins=None, binwidth=None):
  command='BinDistance '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (bins!=None): command+='Bins='+cstr(bins)+','
  if (binwidth!=None): command+='BinWidth='+cstr(binwidth)+','
  run(command[:-1])

# BLAST PROTEIN SEQUENCE (ALL OR SELECTED)
# ========================================
def BLAST(database=None, passes=None, evalue=None, hits=None, order=None, filename=None, format=None):
  command='BLAST '
  if (database!=None): command+='Database='+cstr(database)+','
  if (passes!=None): command+='Passes='+cstr(passes)+','
  if (evalue!=None): command+='EValue='+cstr(evalue)+','
  if (hits!=None): command+='Hits='+cstr(hits)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# BLAST PROTEIN SEQUENCE (ALL)
# ============================
def BLASTAll(database=None, passes=None, evalue=None, hits=None, order=None, filename=None, format=None):
  command='BLASTAll '
  if (database!=None): command+='Database='+cstr(database)+','
  if (passes!=None): command+='Passes='+cstr(passes)+','
  if (evalue!=None): command+='EValue='+cstr(evalue)+','
  if (hits!=None): command+='Hits='+cstr(hits)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# BLAST PROTEIN SEQUENCE (OBJECT)
# ===============================
def BLASTObj(selection1, database=None, passes=None, evalue=None, hits=None, order=None, filename=None, format=None):
  command='BLASTObj '
  command+=selstr(selection1)+','
  if (database!=None): command+='Database='+cstr(database)+','
  if (passes!=None): command+='Passes='+cstr(passes)+','
  if (evalue!=None): command+='EValue='+cstr(evalue)+','
  if (hits!=None): command+='Hits='+cstr(hits)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# BLAST PROTEIN SEQUENCE (MOLECULE)
# =================================
def BLASTMol(selection1, database=None, passes=None, evalue=None, hits=None, order=None, filename=None, format=None):
  command='BLASTMol '
  command+=selstr(selection1)+','
  if (database!=None): command+='Database='+cstr(database)+','
  if (passes!=None): command+='Passes='+cstr(passes)+','
  if (evalue!=None): command+='EValue='+cstr(evalue)+','
  if (hits!=None): command+='Hits='+cstr(hits)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# BLAST PROTEIN SEQUENCE (RESIDUE)
# ================================
def BLASTRes(selection1, database=None, passes=None, evalue=None, hits=None, order=None, filename=None, format=None):
  command='BLASTRes '
  command+=selstr(selection1)+','
  if (database!=None): command+='Database='+cstr(database)+','
  if (passes!=None): command+='Passes='+cstr(passes)+','
  if (evalue!=None): command+='EValue='+cstr(evalue)+','
  if (hits!=None): command+='Hits='+cstr(hits)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# BOUND VALUE TO INTERVAL
# =======================
def Bound(value, Min=None, Max=None):
  command='Bound '
  command+='Value='+cstr(value)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (Max!=None): command+='Max='+cstr(Max)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET/GET CELL BOUNDARY
# =====================
def Boundary(Type=None):
  command='Boundary '
  if (Type!=None): command+='Type='+cstr(Type)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SIMULATION BRAKE
# ================
def Brake(speed):
  command='Brake '
  if (type(speed)==type('') and speed.lower()=='off'): command+=' off,'
  else:
    command+='Speed='+cstr(speed)+','
  run(command[:-1])

# BUILD A BRIDGE BETWEEN TWO ATOMS
# ================================
def BridgeAtom(selection1, selection2, name):
  command='BridgeAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET WEB BROWSER
# ===============
def Browser(com):
  command='Browser '
  command+='Command='+cstr(com)+','
  run(command[:-1])

# BUILD SINGLE ATOM
# =================
def BuildAtom(element, copies=None, selection1=None):
  command='BuildAtom '
  command+='Element='+cstr(element)+','
  if (copies!=None): command+='Copies='+cstr(copies)+','
  if (selection1!=None): command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD PET GENOME WITH NUCLEIC ACID BINDING PROTEINS
# ===================================================
def BuildGenome(Type, filename, selection1):
  command='BuildGenome '
  command+='Type='+cstr(Type)+','
  command+='Filename='+cstr(filename)+','
  command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD A GRID OF ATOMS
# =====================
def BuildGrid(element=None, x=None, y=None, z=None, spacing=None):
  command='BuildGrid '
  if (element!=None): command+='Element='+cstr(element)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (spacing!=None): command+='Spacing='+cstr(spacing)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD FUNCTIONAL GROUP
# ======================
def BuildGroup(name):
  command='BuildGroup '
  command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# BUILD CENTRAL OR TERMINAL LOOP
# ==============================
def BuildLoop(selection1, sequence, selection2, structures=None, mutate=None, bumpsum=None, secstr=None, bridgecys=None):
  command='BuildLoop '
  command+=selstr(selection1)+','
  command+='Sequence='+cstr(sequence)+','
  command+=selstr(selection2)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  if (mutate!=None): command+='Mutate='+cstr(mutate)+','
  if (bumpsum!=None): command+='Bumpsum='+cstr(bumpsum)+','
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  if (bridgecys!=None): command+='BridgeCys='+cstr(bridgecys)+','
  return(run(command[:-1]))

# BUILD PEPTIDE OR NUCLEIC ACID CHAIN
# ===================================
def BuildMol(filename=None, sequence=None, Type=None):
  command='BuildMol '
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (sequence!=None): command+='Sequence='+cstr(sequence)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD SINGLE RESIDUE
# ====================
def BuildRes(name, psi=None, tau=None, center=None, isomer=None, useph=None):
  command='BuildRes '
  command+='Name='+cstr(name)+','
  if (psi!=None): command+='Psi='+cstr(psi)+','
  if (tau!=None): command+='Tau='+cstr(tau)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (isomer!=None): command+='Isomer='+cstr(isomer)+','
  if (useph!=None): command+='UsepH='+cstr(useph)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD SINGLE RESIDUE
# ====================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def BuildRes2(name, alpha=None, beta=None, gamma=None, center=None):
  command='BuildRes '
  command+='Name='+cstr(name)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  if (center!=None): command+='Center='+cstr(center)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD MOLECULE FROM SMILES STRING
# =================================
def BuildSMILES(string, sort=None):
  command='BuildSMILES '
  command+='String='+cstr(string)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# BUILD SYMMETRY RELATED RESIDUES
# ===============================
def BuildSymRes(selection1):
  command='BuildSymRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# CALCULATE CAVITY VOLUMES (ALL OR SELECTED)
# ==========================================
def CaviVol(Type=None):
  command='CaviVol '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE CAVITY VOLUMES (ALL)
# ==============================
def CaviVolAll(Type=None):
  command='CaviVolAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE CAVITY VOLUMES (OBJECT)
# =================================
def CaviVolObj(selection1, Type=None):
  command='CaviVolObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE CAVITY VOLUMES (MOLECULE)
# ===================================
def CaviVolMol(selection1, Type=None):
  command='CaviVolMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE CAVITY VOLUMES (RESIDUE)
# ==================================
def CaviVolRes(selection1, Type=None):
  command='CaviVolRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE CAVITY VOLUMES (ATOM)
# ===============================
def CaviVolAtom(selection1, Type=None):
  command='CaviVolAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CHANGE WORKING DIRECTORY
# ========================
def CD(noname1, onstartup=None):
  command='CD '
  command+=cstr(noname1)+','
  if (onstartup!=None): command+='OnStartUp='+cstr(onstartup)+','
  run(command[:-1])

# SET/GET SIMULATION CELL DIMENSIONS
# ==================================
def Cell(x=None, y=None, z=None, alpha=None, beta=None, gamma=None, center=None):
  command='Cell '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  if (center!=None): command+='Center='+cstr(center)+','
  return(run(command[:-1]))

# SET/GET SIMULATION CELL DIMENSIONS
# ==================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def CellAuto(extension=None, shape=None, selection1=None):
  command='Cell Auto,'
  if (extension!=None): command+='Extension='+cstr(extension)+','
  if (shape!=None): command+='Shape='+cstr(shape)+','
  if (selection1!=None): command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET/GET SIMULATION CELL DIMENSIONS
# ==================================
# THIS IS ALTERNATIVE 3, WITH DIFFERENT PARAMETERS
def CellCrystal(selection1):
  command='Cell Crystal,'
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# GET SIMULATION CELL EDGE VECTORS
# ================================
def CellEdges():
  command='CellEdges '
  return(run(command[:-1]))

# CENTER ATOMS OR POLYGON MESHES (ALL OR SELECTED)
# ================================================
def Center(coordsys=None):
  command='Center '
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# CENTER ATOMS OR POLYGON MESHES (ALL)
# ====================================
def CenterAll(coordsys=None):
  command='CenterAll '
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# CENTER ATOMS OR POLYGON MESHES (OBJECT)
# =======================================
def CenterObj(selection1, coordsys=None):
  command='CenterObj '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# CENTER ATOMS OR POLYGON MESHES (MOLECULE)
# =========================================
def CenterMol(selection1, coordsys=None):
  command='CenterMol '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# CENTER ATOMS OR POLYGON MESHES (RESIDUE)
# ========================================
def CenterRes(selection1, coordsys=None):
  command='CenterRes '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# CENTER ATOMS OR POLYGON MESHES (ATOM)
# =====================================
def CenterAtom(selection1, coordsys=None):
  command='CenterAtom '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  run(command[:-1])

# SET/GET THE SUMMED UP CHARGE (ALL OR SELECTED)
# ==============================================
def Charge(e=None):
  command='Charge '
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# SET/GET THE SUMMED UP CHARGE (ALL)
# ==================================
def ChargeAll(e=None):
  command='ChargeAll '
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# SET/GET THE SUMMED UP CHARGE (OBJECT)
# =====================================
def ChargeObj(selection1, e=None):
  command='ChargeObj '
  command+=selstr(selection1)+','
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# SET/GET THE SUMMED UP CHARGE (MOLECULE)
# =======================================
def ChargeMol(selection1, e=None):
  command='ChargeMol '
  command+=selstr(selection1)+','
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# SET/GET THE SUMMED UP CHARGE (RESIDUE)
# ======================================
def ChargeRes(selection1, e=None):
  command='ChargeRes '
  command+=selstr(selection1)+','
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# SET/GET THE SUMMED UP CHARGE (ATOM)
# ===================================
def ChargeAtom(selection1, e=None):
  command='ChargeAtom '
  command+=selstr(selection1)+','
  if (e!=None): command+='e='+cstr(e)+','
  return(run(command[:-1]))

# CHECK STRUCTURE QUALITY (ALL OR SELECTED)
# =========================================
def Check(Type, filename=None):
  command='Check '
  command+='Type='+cstr(Type)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# CHECK STRUCTURE QUALITY (ALL)
# =============================
def CheckAll(Type, filename=None):
  command='CheckAll '
  command+='Type='+cstr(Type)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# CHECK STRUCTURE QUALITY (OBJECT)
# ================================
def CheckObj(selection1, Type, filename=None):
  command='CheckObj '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# CHECK STRUCTURE QUALITY (RESIDUE)
# =================================
def CheckRes(selection1, Type, filename=None):
  command='CheckRes '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# CHECK STRUCTURE QUALITY (ATOM)
# ==============================
def CheckAtom(selection1, Type, filename=None):
  command='CheckAtom '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# CLASSIFY RESTRAINTS (ALL OR SELECTED)
# =====================================
def ClassRest(Class, component, number, newclass):
  command='ClassRest '
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLASSIFY RESTRAINTS (ALL)
# =========================
def ClassRestAll(Class, component, number, newclass):
  command='ClassRestAll '
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLASSIFY RESTRAINTS (OBJECT)
# ============================
def ClassRestObj(selection1, Class, component, number, newclass):
  command='ClassRestObj '
  command+=selstr(selection1)+','
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLASSIFY RESTRAINTS (MOLECULE)
# ==============================
def ClassRestMol(selection1, Class, component, number, newclass):
  command='ClassRestMol '
  command+=selstr(selection1)+','
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLASSIFY RESTRAINTS (RESIDUE)
# =============================
def ClassRestRes(selection1, Class, component, number, newclass):
  command='ClassRestRes '
  command+=selstr(selection1)+','
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLASSIFY RESTRAINTS (ATOM)
# ==========================
def ClassRestAtom(selection1, Class, component, number, newclass):
  command='ClassRestAtom '
  command+=selstr(selection1)+','
  command+='Class='+cstr(Class)+','
  command+='Component='+cstr(component)+','
  command+='Number='+cstr(number)+','
  command+='NewClass='+cstr(newclass)+','
  run(command[:-1])

# CLEAN OBJECTS FOR MOLECULAR DYNAMICS SIMULATION (ALL OR SELECTED)
# =================================================================
def Clean(skip=None):
  command='Clean '
  if (skip!=None): command+='Skip='+cstr(skip)+','
  run(command[:-1])

# CLEAN OBJECTS FOR MOLECULAR DYNAMICS SIMULATION (ALL)
# =====================================================
def CleanAll(skip=None):
  command='CleanAll '
  if (skip!=None): command+='Skip='+cstr(skip)+','
  run(command[:-1])

# CLEAN OBJECTS FOR MOLECULAR DYNAMICS SIMULATION (OBJECT)
# ========================================================
def CleanObj(selection1, skip=None):
  command='CleanObj '
  command+=selstr(selection1)+','
  if (skip!=None): command+='Skip='+cstr(skip)+','
  run(command[:-1])

# CLEAR SCENE
# ===========
def Clear():
  command='Clear '
  run(command[:-1])

# COLOR BONDS
# ===========
def ColorBonds(color):
  command='ColorBonds '
  command+='Color='+cstr(color)+','
  run(command[:-1])

# COLOR BACKGROUND
# ================
def ColorBG(topleft, bottomleft=None, topright=None, bottomright=None):
  command='ColorBG '
  command+='TopLeft='+cstr(topleft)+','
  if (bottomleft!=None): command+='BottomLeft='+cstr(bottomleft)+','
  if (topright!=None): command+='TopRight='+cstr(topright)+','
  if (bottomright!=None): command+='BottomRight='+cstr(bottomright)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (ALL OR SELECTED)
# ======================================================================
def ColorFar(Type, first, second=None):
  command='ColorFar '
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (ALL)
# ==========================================================
def ColorFarAll(Type, first, second=None):
  command='ColorFarAll '
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (OBJECT)
# =============================================================
def ColorFarObj(selection1, Type, first, second=None):
  command='ColorFarObj '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (MOLECULE)
# ===============================================================
def ColorFarMol(selection1, Type, first, second=None):
  command='ColorFarMol '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (RESIDUE)
# ==============================================================
def ColorFarRes(selection1, Type, first, second=None):
  command='ColorFarRes '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# SET OVERALL OBJECT INSTANCE COLORS AT A FAR DISTANCE (ATOM)
# ===========================================================
def ColorFarAtom(selection1, Type, first, second=None):
  command='ColorFarAtom '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  command+='First='+cstr(first)+','
  if (second!=None): command+='Second='+cstr(second)+','
  run(command[:-1])

# COLOR FOG
# =========
def ColorFog(color):
  command='ColorFog '
  command+='Color='+cstr(color)+','
  run(command[:-1])

# COLOR HYDROGEN BONDS
# ====================
def ColorHBo(color=None, alpha=None, inherit=None):
  command='ColorHBo '
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (inherit!=None): command+='Inherit='+cstr(inherit)+','
  run(command[:-1])

# COLOR HEAD-UP DISPLAY
# =====================
def ColorHUD(color):
  command='ColorHUD '
  command+='Color='+cstr(color)+','
  run(command[:-1])

# COLOR POLYGON MESH
# ==================
def ColorMesh(selection1, color=None):
  command='ColorMesh '
  command+=selstr(selection1)+','
  if (color!=None): command+='Color='+cstr(color)+','
  run(command[:-1])

# SET/GET DEFAULT COLOR PARAMETERS
# ================================
def ColorPar(scheme, name=None, color=None, value=None):
  command='ColorPar '
  command+='Scheme='+cstr(scheme)+','
  if (name!=None): command+='Name='+cstr(name)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# COLOR SURFACE (ALL OR SELECTED)
# ===============================
def ColorSurf(Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ColorSurf '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# COLOR SURFACE (ALL)
# ===================
def ColorSurfAll(Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ColorSurfAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# COLOR SURFACE (OBJECT)
# ======================
def ColorSurfObj(selection1, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ColorSurfObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ALL OR SELECTED)
# =====================================
def Color(first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='Color '
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ALL OR SELECTED)
# =====================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorFile(filename=None):
  command='Color File,'
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ALL)
# =========================
def ColorAll(first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='ColorAll '
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ALL)
# =========================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorAllFile(filename=None):
  command='ColorAll File,'
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (OBJECT)
# ============================
def ColorObj(selection1, first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='ColorObj '
  command+=selstr(selection1)+','
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (OBJECT)
# ============================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorObjFile(noname1=None, filename=None):
  command='ColorObj File,'
  if (noname1!=None): command+=cstr(noname1)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (MOLECULE)
# ==============================
def ColorMol(selection1, first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='ColorMol '
  command+=selstr(selection1)+','
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (MOLECULE)
# ==============================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorMolFile(noname1=None, filename=None):
  command='ColorMol File,'
  if (noname1!=None): command+=cstr(noname1)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (RESIDUE)
# =============================
def ColorRes(selection1, first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='ColorRes '
  command+=selstr(selection1)+','
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (RESIDUE)
# =============================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorResFile(noname1=None, filename=None):
  command='ColorRes File,'
  if (noname1!=None): command+=cstr(noname1)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ATOM)
# ==========================
def ColorAtom(selection1, first=None, second=None, segments=None, mapcons=None, filename=None, consmin=None):
  command='ColorAtom '
  command+=selstr(selection1)+','
  if (first!=None): command+='first='+cstr(first)+','
  if (second!=None): command+='second='+cstr(second)+','
  if (segments!=None): command+='Segments='+cstr(segments)+','
  if (mapcons!=None): command+='MapCons='+cstr(mapcons)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (consmin!=None): command+='ConsMin='+cstr(consmin)+','
  return(run(command[:-1]))

# SET/GET ATOM COLORS (ATOM)
# ==========================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ColorAtomFile(noname1=None, filename=None):
  command='ColorAtom File,'
  if (noname1!=None): command+=cstr(noname1)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# COMPARE BONDS
# =============
def CompareBond(selection1, selection2, selection3, selection4, checkmol=None):
  command='CompareBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  if (checkmol!=None): command+='CheckMol='+cstr(checkmol)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COMPARE ATOMS AND RESIDUES (RESIDUE)
# ====================================
def CompareRes(selection1, selection2, checkmol=None):
  command='CompareRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (checkmol!=None): command+='CheckMol='+cstr(checkmol)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COMPARE ATOMS AND RESIDUES (ATOM)
# =================================
def CompareAtom(selection1, selection2, checkmol=None):
  command='CompareAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (checkmol!=None): command+='CheckMol='+cstr(checkmol)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET/GET COMPOUND NAMES OF MOLECULES
# ===================================
def CompoundMol(selection1, name=None):
  command='CompoundMol '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET CONSOLE MODE
# ====================
def Console(flag=None):
  command='Console '
  if (flag!=None): command+='Flag='+cstr(flag)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET CONSOLE PARAMETERS
# ======================
def ConsolePar(font=None, height=None, antialias=None):
  command='ConsolePar '
  if (font!=None): command+='Font='+cstr(font)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (antialias!=None): command+='Antialias='+cstr(antialias)+','
  run(command[:-1])

# SET/GET COORDINATE SYSTEM
# =========================
def CoordSys(handed=None, show=None):
  command='CoordSys '
  if (handed!=None): command+='handed='+cstr(handed)+','
  if (show!=None): command+='Show='+cstr(show)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CALCULATE CONTACT SURFACE AREAS (OBJECT)
# ========================================
def ConSurfObj(selection1, selection2, cutoff=None, subtract=None, Type=None, unit=None):
  command='ConSurfObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE CONTACT SURFACE AREAS (MOLECULE)
# ==========================================
def ConSurfMol(selection1, selection2, cutoff=None, subtract=None, Type=None, unit=None):
  command='ConSurfMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE CONTACT SURFACE AREAS (RESIDUE)
# =========================================
def ConSurfRes(selection1, selection2, cutoff=None, subtract=None, Type=None, unit=None):
  command='ConSurfRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE CONTACT SURFACE AREAS (ATOM)
# ======================================
def ConSurfAtom(selection1, selection2, cutoff=None, subtract=None, Type=None, unit=None):
  command='ConSurfAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# COPY FILE
# =========
def CopyFile(srcfilename=None, dstfilename=None, append=None):
  command='CopyFile '
  if (srcfilename!=None): command+='SrcFilename='+cstr(srcfilename)+','
  if (dstfilename!=None): command+='DstFilename='+cstr(dstfilename)+','
  if (append!=None): command+='append='+cstr(append)+','
  run(command[:-1])

# COPY ATOM OR VERTEX POSITIONS BETWEEN OBJECTS
# =============================================
def CopyPosObj(selection1, selection2):
  command='CopyPosObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# COPY VISUALIZATION STYLE BETWEEN OBJECTS
# ========================================
def CopyStyleObj(selection1, selection2, match=None):
  command='CopyStyleObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  run(command[:-1])

# CORRECT CIS-PEPTIDE BONDS DURING A SIMULATION
# =============================================
def CorrectCis(Type, old=None, proline=None):
  command='CorrectCis '
  command+='Type='+cstr(Type)+','
  if (old!=None): command+='Old='+cstr(old)+','
  if (proline!=None): command+='Proline='+cstr(proline)+','
  run(command[:-1])

# CORRECT NAMING CONVENTIONS DURING A SIMULATION
# ==============================================
def CorrectConv(flag):
  command='CorrectConv '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# CORRECT SOLUTE DRIFT DURING A SIMULATION
# ========================================
def CorrectDrift(flag):
  command='CorrectDrift '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# CORRECT WRONG ISOMERS DURING A SIMULATION
# =========================================
def CorrectIso(Type, old=None):
  command='CorrectIso '
  command+='Type='+cstr(Type)+','
  if (old!=None): command+='Old='+cstr(old)+','
  run(command[:-1])

# CORRECT KNOTS AND OTHER ENTANGLEMENTS DURING A SIMULATION
# =========================================================
def CorrectKnots(flag):
  command='CorrectKnots '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# COUNT BONDS
# ===========
def CountBond(selection1, selection2, Type=None):
  command='CountBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COUNT CONTACTS (OBJECT)
# =======================
def CountConObj(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, unit=None):
  command='CountConObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# COUNT CONTACTS (MOLECULE)
# =========================
def CountConMol(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, unit=None):
  command='CountConMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# COUNT CONTACTS (RESIDUE)
# ========================
def CountConRes(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, unit=None):
  command='CountConRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# COUNT CONTACTS (ATOM)
# =====================
def CountConAtom(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, unit=None):
  command='CountConAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# COUNT SELECTED UNITS (OBJECT)
# =============================
def CountObj(selection1):
  command='CountObj '
  command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COUNT SELECTED UNITS (MOLECULE)
# ===============================
def CountMol(selection1):
  command='CountMol '
  command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COUNT SELECTED UNITS (RESIDUE)
# ==============================
def CountRes(selection1):
  command='CountRes '
  command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COUNT SELECTED UNITS (ATOM)
# ===========================
def CountAtom(selection1):
  command='CountAtom '
  command+=selstr(selection1)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# COUPLE OBJECT MOVEMENT TO ANOTHER OBJECT (ALL OR SELECTED)
# ==========================================================
def Couple(selection1):
  command='Couple '
  command+=selstr(selection1)+','
  run(command[:-1])

# COUPLE OBJECT MOVEMENT TO ANOTHER OBJECT (ALL)
# ==============================================
def CoupleAll(selection1):
  command='CoupleAll '
  command+=selstr(selection1)+','
  run(command[:-1])

# COUPLE OBJECT MOVEMENT TO ANOTHER OBJECT (OBJECT)
# =================================================
def CoupleObj(selection1, selection2):
  command='CoupleObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# CRYSTALLIZE OBJECTS TO FILL THE UNIT CELL (ALL OR SELECTED)
# ===========================================================
def Crystallize(center=None):
  command='Crystallize '
  if (center!=None): command+='Center='+cstr(center)+','
  return(run(command[:-1]))

# CRYSTALLIZE OBJECTS TO FILL THE UNIT CELL (ALL)
# ===============================================
def CrystallizeAll(center=None):
  command='CrystallizeAll '
  if (center!=None): command+='Center='+cstr(center)+','
  return(run(command[:-1]))

# CRYSTALLIZE OBJECTS TO FILL THE UNIT CELL (OBJECT)
# ==================================================
def CrystallizeObj(selection1, center=None):
  command='CrystallizeObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  return(run(command[:-1]))

# SET FORCE CUTOFF DISTANCE
# =========================
def Cutoff(distance):
  command='Cutoff '
  command+='Distance='+cstr(distance)+','
  return(run(command[:-1]))

# CUT OBJECTS OPEN (ALL OR SELECTED)
# ==================================
def Cut(secstr=None, atoms=None, cell=None):
  command='Cut '
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  if (atoms!=None): command+='Atoms='+cstr(atoms)+','
  if (cell!=None): command+='Cell='+cstr(cell)+','
  return(run(command[:-1]))

# CUT OBJECTS OPEN (ALL)
# ======================
def CutAll(secstr=None, atoms=None, cell=None):
  command='CutAll '
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  if (atoms!=None): command+='Atoms='+cstr(atoms)+','
  if (cell!=None): command+='Cell='+cstr(cell)+','
  return(run(command[:-1]))

# CUT OBJECTS OPEN (OBJECT)
# =========================
def CutObj(selection1, secstr=None, atoms=None, cell=None):
  command='CutObj '
  command+=selstr(selection1)+','
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  if (atoms!=None): command+='Atoms='+cstr(atoms)+','
  if (cell!=None): command+='Cell='+cstr(cell)+','
  return(run(command[:-1]))

# CALCULATE CYSTEINE BRIDGE ENERGIES
# ==================================
def CysEnergyRes(selection1, selection2):
  command='CysEnergyRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  return(run(command[:-1]))

# CALCULATE DYNAMIC CROSS-CORRELATION MATRIX
# ==========================================
def DCCM():
  command='DCCM '
  return(run(command[:-1]))

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (ALL OR SELECTED)
# ==================================================================================
def Deflate(formulacol=None):
  command='Deflate '
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (ALL)
# ======================================================================
def DeflateAll(formulacol=None):
  command='DeflateAll '
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (OBJECT)
# =========================================================================
def DeflateObj(selection1, formulacol=None):
  command='DeflateObj '
  command+=selstr(selection1)+','
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (MOLECULE)
# ===========================================================================
def DeflateMol(selection1, formulacol=None):
  command='DeflateMol '
  command+=selstr(selection1)+','
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (RESIDUE)
# ==========================================================================
def DeflateRes(selection1, formulacol=None):
  command='DeflateRes '
  command+=selstr(selection1)+','
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# CONVERT 3D TO 2D COORDINATES, CREATING A FLAT STRUCTURAL FORMULA (ATOM)
# =======================================================================
def DeflateAtom(selection1, formulacol=None):
  command='DeflateAtom '
  command+=selstr(selection1)+','
  if (formulacol!=None): command+='FormulaCol='+cstr(formulacol)+','
  run(command[:-1])

# DEFORM A POLYGON MESH USING SINE FUNCTIONS
# ==========================================
def DeformMesh(selection1, function=None, ampx=None, ampy=None, ampz=None, lenx=None, leny=None, lenz=None):
  command='DeformMesh '
  command+=selstr(selection1)+','
  if (function!=None): command+='Function='+cstr(function)+','
  if (ampx!=None): command+='AmpX='+cstr(ampx)+','
  if (ampy!=None): command+='AmpY='+cstr(ampy)+','
  if (ampz!=None): command+='AmpZ='+cstr(ampz)+','
  if (lenx!=None): command+='LenX='+cstr(lenx)+','
  if (leny!=None): command+='LenY='+cstr(leny)+','
  if (lenz!=None): command+='LenZ='+cstr(lenz)+','
  run(command[:-1])

# GET DEGREES OF FREEDOM
# ======================
def DegFreedom():
  command='DegFreedom '
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# DELETE COVALENT BONDS
# =====================
def DelBond(selection1, selection2, lenmin=None):
  command='DelBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (lenmin!=None): command+='LenMin='+cstr(lenmin)+','
  run(command[:-1])

# DELETE FILE
# ===========
def DelFile(filename):
  command='DelFile '
  command+='Filename='+cstr(filename)+','
  run(command[:-1])

# DELETE ALL HYDROGENS (ALL OR SELECTED)
# ======================================
def DelHyd():
  command='DelHyd '
  run(command[:-1])

# DELETE ALL HYDROGENS (ALL)
# ==========================
def DelHydAll():
  command='DelHydAll '
  run(command[:-1])

# DELETE ALL HYDROGENS (OBJECT)
# =============================
def DelHydObj(selection1):
  command='DelHydObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE IMAGES
# =============
def DelImage(selection1):
  command='DelImage '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE RESTRAINTS (ALL OR SELECTED)
# ===================================
def DelRest(Class=None, component=None, number=None):
  command='DelRest '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE RESTRAINTS (ALL)
# =======================
def DelRestAll(Class=None, component=None, number=None):
  command='DelRestAll '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE RESTRAINTS (OBJECT)
# ==========================
def DelRestObj(selection1, Class=None, component=None, number=None):
  command='DelRestObj '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE RESTRAINTS (MOLECULE)
# ============================
def DelRestMol(selection1, Class=None, component=None, number=None):
  command='DelRestMol '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE RESTRAINTS (RESIDUE)
# ===========================
def DelRestRes(selection1, Class=None, component=None, number=None):
  command='DelRestRes '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE RESTRAINTS (ATOM)
# ========================
def DelRestAtom(selection1, Class=None, component=None, number=None):
  command='DelRestAtom '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# DELETE TABLES
# =============
def DelTab(selection1):
  command='DelTab '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE VIEW
# ===========
def DelView(selection1):
  command='DelView '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE ALL WATER MOLECULES (ALL OR SELECTED)
# ============================================
def DelWater():
  command='DelWater '
  run(command[:-1])

# DELETE ALL WATER MOLECULES (ALL)
# ================================
def DelWaterAll():
  command='DelWaterAll '
  run(command[:-1])

# DELETE ALL WATER MOLECULES (OBJECT)
# ===================================
def DelWaterObj(selection1):
  command='DelWaterObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE YANACONDA VARIABLE
# =========================
def DelVar(name, renumber=None, matchnum=None):
  command='DelVar '
  command+='Name='+cstr(name)+','
  if (renumber!=None): command+='Renumber='+cstr(renumber)+','
  if (matchnum!=None): command+='MatchNum='+cstr(matchnum)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (ALL OR SELECTED)
# ==========================================
def Del(center=None):
  command='Del '
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (ALL)
# ==============================
def DelAll(center=None):
  command='DelAll '
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (OBJECT)
# =================================
def DelObj(selection1, center=None):
  command='DelObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (MOLECULE)
# ===================================
def DelMol(selection1, center=None):
  command='DelMol '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (RESIDUE)
# ==================================
def DelRes(selection1, center=None):
  command='DelRes '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE ATOMS AND OBJECTS (ATOM)
# ===============================
def DelAtom(selection1, center=None):
  command='DelAtom '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# SET/GET DIHEDRAL ANGLE BETWEEN ATOMS
# ====================================
def Dihedral(selection1, selection2, selection3, selection4, bound=None, set=None):
  command='Dihedral '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  if (bound!=None): command+='bound='+cstr(bound)+','
  if (set!=None): command+='set='+cstr(set)+','
  return(run(command[:-1]))

# CALCULATE ELECTRIC DIPOLE MOMENTS (OBJECT)
# ==========================================
def DipoleObj(selection1):
  command='DipoleObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE ELECTRIC DIPOLE MOMENTS (MOLECULE)
# ============================================
def DipoleMol(selection1):
  command='DipoleMol '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE ELECTRIC DIPOLE MOMENTS (RESIDUE)
# ===========================================
def DipoleRes(selection1):
  command='DipoleRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE ELECTRIC DIPOLE MOMENTS (ATOM)
# ========================================
def DipoleAtom(selection1):
  command='DipoleAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET/GET DISTANCE BETWEEN ATOMS
# ==============================
def Distance(selection1, selection2, bound=None, set=None):
  command='Distance '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (bound!=None): command+='bound='+cstr(bound)+','
  if (set!=None): command+='set='+cstr(set)+','
  return(run(command[:-1]))

# DOWNLOAD FILE FROM INTERNET
# ===========================
def Download(url, filename, replace=None):
  command='Download '
  command+='URL='+cstr(url)+','
  command+='Filename='+cstr(filename)+','
  if (replace!=None): command+='Replace='+cstr(replace)+','
  run(command[:-1])

# DRAW A LINE
# ===========
def DrawLine(startx, starty, endx=None, endy=None, color=None, width=None, round=None):
  command='DrawLine '
  command+='StartX='+cstr(startx)+','
  command+='StartY='+cstr(starty)+','
  if (endx!=None): command+='EndX='+cstr(endx)+','
  if (endy!=None): command+='EndY='+cstr(endy)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (round!=None): command+='Round='+cstr(round)+','
  run(command[:-1])

# DUPLICATE VIEW
# ==============
def DuplicateView(selection1, name, hud=None):
  command='DuplicateView '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  if (hud!=None): command+='HUD='+cstr(hud)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# DUPLICATE OBJECTS (ALL OR SELECTED)
# ===================================
def Duplicate():
  command='Duplicate '
  return(run(command[:-1]))

# DUPLICATE OBJECTS (ALL)
# =======================
def DuplicateAll():
  command='DuplicateAll '
  return(run(command[:-1]))

# DUPLICATE OBJECTS (OBJECT)
# ==========================
def DuplicateObj(selection1):
  command='DuplicateObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# DUPLICATE OBJECTS (MOLECULE)
# ============================
def DuplicateMol(selection1):
  command='DuplicateMol '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# DUPLICATE OBJECTS (RESIDUE)
# ===========================
def DuplicateRes(selection1):
  command='DuplicateRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# DUPLICATE OBJECTS (ATOM)
# ========================
def DuplicateAtom(selection1):
  command='DuplicateAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# GET CHEMICAL ELEMENT
# ====================
def ElementAtom(selection1):
  command='ElementAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET ENERGY UNIT
# ===============
def EnergyUnit(name):
  command='EnergyUnit '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# CALCULATE FORCE FIELD ENERGIES (ALL OR SELECTED)
# ================================================
def Energy(component, *arglist2):
  command='Energy '
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# CALCULATE FORCE FIELD ENERGIES (ALL)
# ====================================
def EnergyAll(component, *arglist2):
  command='EnergyAll '
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# CALCULATE FORCE FIELD ENERGIES (OBJECT)
# =======================================
def EnergyObj(selection1, component, *arglist2):
  command='EnergyObj '
  command+=selstr(selection1)+','
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# CALCULATE FORCE FIELD ENERGIES (MOLECULE)
# =========================================
def EnergyMol(selection1, component, *arglist2):
  command='EnergyMol '
  command+=selstr(selection1)+','
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# CALCULATE FORCE FIELD ENERGIES (RESIDUE)
# ========================================
def EnergyRes(selection1, component, *arglist2):
  command='EnergyRes '
  command+=selstr(selection1)+','
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# CALCULATE FORCE FIELD ENERGIES (ATOM)
# =====================================
def EnergyAtom(selection1, component, *arglist2):
  command='EnergyAtom '
  command+=selstr(selection1)+','
  command+='Component='+cstr(component)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# EXPAND PET OBJECTS (ALL OR SELECTED)
# ====================================
def Expand(scalepos=None, instance=None):
  command='Expand '
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  run(command[:-1])

# EXPAND PET OBJECTS (ALL)
# ========================
def ExpandAll(scalepos=None, instance=None):
  command='ExpandAll '
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  run(command[:-1])

# EXPAND PET OBJECTS (OBJECT)
# ===========================
def ExpandObj(selection1, scalepos=None, instance=None):
  command='ExpandObj '
  command+=selstr(selection1)+','
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
def Experiment(noname1):
  command='Experiment '
  command+=cstr(noname1)+','
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ExperimentMinimization(convergence=None):
  command='Experiment Minimization\n'
  if (convergence!=None): command+='  convergence '+cstr(convergence)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 3, WITH DIFFERENT PARAMETERS
def ExperimentNeutralization(waterdensity=None, nacl=None, ph=None, pkafile=None, speed=None, ions=None):
  command='Experiment Neutralization\n'
  if (waterdensity!=None): command+='  waterdensity '+cstr(waterdensity)+'\n'
  if (nacl!=None): command+='  nacl '+cstr(nacl)+'\n'
  if (ph!=None): command+='  ph '+cstr(ph)+'\n'
  if (pkafile!=None): command+='  pkafile '+cstr(pkafile)+'\n'
  if (speed!=None): command+='  speed '+cstr(speed)+'\n'
  if (ions!=None): command+='  ions '+cstr(ions)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 4, WITH DIFFERENT PARAMETERS
def ExperimentMorphing(startobj=None, endobj=None, structures=None, structurefile=None, morphforce=None):
  command='Experiment Morphing\n'
  if (startobj!=None): command+='  startobj '+cstr(startobj)+'\n'
  if (endobj!=None): command+='  endobj '+cstr(endobj)+'\n'
  if (structures!=None): command+='  structures '+cstr(structures)+'\n'
  if (structurefile!=None): command+='  structurefile '+cstr(structurefile)+'\n'
  if (morphforce!=None): command+='  morphforce '+cstr(morphforce)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 5, WITH DIFFERENT PARAMETERS
def ExperimentDocking(method=None, ligandobj=None, receptorobj=None, runs=None, clusterrmsd=None, resultfile=None, tmpfileid=None, gridparlist=None, dockparlist=None, setuponly=None, clustermembers=None):
  command='Experiment Docking\n'
  if (method!=None): command+='  method '+cstr(method)+'\n'
  if (ligandobj!=None): command+='  ligandobj '+cstr(ligandobj)+'\n'
  if (receptorobj!=None): command+='  receptorobj '+cstr(receptorobj)+'\n'
  if (runs!=None): command+='  runs '+cstr(runs)+'\n'
  if (clusterrmsd!=None): command+='  clusterrmsd '+cstr(clusterrmsd)+'\n'
  if (resultfile!=None): command+='  resultfile '+cstr(resultfile)+'\n'
  if (tmpfileid!=None): command+='  tmpfileid '+cstr(tmpfileid)+'\n'
  if (gridparlist!=None): 
    if (type(gridparlist)!=type([])): gridparlist=[gridparlist]
    for value in gridparlist:
      command+='  gridpar '+cstr(value)+'\n'
  if (dockparlist!=None): 
    if (type(dockparlist)!=type([])): dockparlist=[dockparlist]
    for value in dockparlist:
      command+='  dockpar '+cstr(value)+'\n'
  if (setuponly!=None): command+='  setuponly '+cstr(setuponly)+'\n'
  if (clustermembers!=None): command+='  clustermembers '+cstr(clustermembers)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 6, WITH DIFFERENT PARAMETERS
def ExperimentHomologyModeling(sequencefile=None, psiblasts=None, evalue=None, oligostate=None, templates=None, alignments=None, alignfile=None, templateobj=None, loopsamples=None, speed=None, animation=None, resultfile=None, termextension=None, residues=None, structprofile=None, fixmodelres=None, looplenmax=None, report=None):
  command='Experiment HomologyModeling\n'
  if (sequencefile!=None): command+='  sequencefile '+cstr(sequencefile)+'\n'
  if (psiblasts!=None): command+='  psiblasts '+cstr(psiblasts)+'\n'
  if (evalue!=None): command+='  evalue '+cstr(evalue)+'\n'
  if (oligostate!=None): command+='  oligostate '+cstr(oligostate)+'\n'
  if (templates!=None): command+='  templates '+cstr(templates)+'\n'
  if (alignments!=None): command+='  alignments '+cstr(alignments)+'\n'
  if (alignfile!=None): command+='  alignfile '+cstr(alignfile)+'\n'
  if (templateobj!=None): command+='  templateobj '+cstr(templateobj)+'\n'
  if (loopsamples!=None): command+='  loopsamples '+cstr(loopsamples)+'\n'
  if (speed!=None): command+='  speed '+cstr(speed)+'\n'
  if (animation!=None): command+='  animation '+cstr(animation)+'\n'
  if (resultfile!=None): command+='  resultfile '+cstr(resultfile)+'\n'
  if (termextension!=None): command+='  termextension '+cstr(termextension)+'\n'
  if (residues!=None): command+='  residues '+cstr(residues)+'\n'
  if (structprofile!=None): command+='  structprofile '+cstr(structprofile)+'\n'
  if (fixmodelres!=None): command+='  fixmodelres '+cstr(fixmodelres)+'\n'
  if (looplenmax!=None): command+='  looplenmax '+cstr(looplenmax)+'\n'
  if (report!=None): command+='  report '+cstr(report)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 7, WITH DIFFERENT PARAMETERS
def ExperimentProteinModeling(sequencefile=None, foldmethod=None, psiblasts=None, evalue=None, oligostate=None, templates=None, alignments=None, alignfile=None, templateobj=None, loopsamples=None, speed=None, animation=None, resultfile=None, termextension=None, residues=None, structprofile=None, fixmodelres=None, looplenmax=None, report=None):
  command='Experiment ProteinModeling\n'
  if (sequencefile!=None): command+='  sequencefile '+cstr(sequencefile)+'\n'
  if (foldmethod!=None): command+='  foldmethod '+cstr(foldmethod)+'\n'
  if (psiblasts!=None): command+='  psiblasts '+cstr(psiblasts)+'\n'
  if (evalue!=None): command+='  evalue '+cstr(evalue)+'\n'
  if (oligostate!=None): command+='  oligostate '+cstr(oligostate)+'\n'
  if (templates!=None): command+='  templates '+cstr(templates)+'\n'
  if (alignments!=None): command+='  alignments '+cstr(alignments)+'\n'
  if (alignfile!=None): command+='  alignfile '+cstr(alignfile)+'\n'
  if (templateobj!=None): command+='  templateobj '+cstr(templateobj)+'\n'
  if (loopsamples!=None): command+='  loopsamples '+cstr(loopsamples)+'\n'
  if (speed!=None): command+='  speed '+cstr(speed)+'\n'
  if (animation!=None): command+='  animation '+cstr(animation)+'\n'
  if (resultfile!=None): command+='  resultfile '+cstr(resultfile)+'\n'
  if (termextension!=None): command+='  termextension '+cstr(termextension)+'\n'
  if (residues!=None): command+='  residues '+cstr(residues)+'\n'
  if (structprofile!=None): command+='  structprofile '+cstr(structprofile)+'\n'
  if (fixmodelres!=None): command+='  fixmodelres '+cstr(fixmodelres)+'\n'
  if (looplenmax!=None): command+='  looplenmax '+cstr(looplenmax)+'\n'
  if (report!=None): command+='  report '+cstr(report)+'\n'
  run(command[:-1])

# CHOOSE AND CONTROL EXPERIMENTS
# ==============================
# THIS IS ALTERNATIVE 8, WITH DIFFERENT PARAMETERS
def ExperimentNMRFolding(startobj=None, restrainfile=None, structures=None, structurefile=None):
  command='Experiment NMRFolding\n'
  if (startobj!=None): command+='  startobj '+cstr(startobj)+'\n'
  if (restrainfile!=None): command+='  restrainfile '+cstr(restrainfile)+'\n'
  if (structures!=None): command+='  structures '+cstr(structures)+'\n'
  if (structurefile!=None): command+='  structurefile '+cstr(structurefile)+'\n'
  run(command[:-1])

# GET FILE SIZE
# =============
def FileSize(filename):
  command='FileSize '
  command+='Filename='+cstr(filename)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# GET FILE MODIFICATION TIME
# ==========================
def FileTime(filename):
  command='FileTime '
  command+='Filename='+cstr(filename)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# FILL SIMULATION CELL WITH OBJECT
# ================================
def FillCellObj(selection1, copies, density, bumpsum, randomori, dismin, location, compartment, radius, x, y, z, location2, compartment2, selection2):
  command='FillCellObj '
  command+=selstr(selection1)+','
  command+='Copies='+cstr(copies)+','
  command+='Density='+cstr(density)+','
  command+='BumpSum='+cstr(bumpsum)+','
  command+='RandomOri='+cstr(randomori)+','
  command+='DisMin='+cstr(dismin)+','
  command+='Location='+cstr(location)+','
  command+='Compartment='+cstr(compartment)+','
  command+='Radius='+cstr(radius)+','
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='Location='+cstr(location2)+','
  command+='Compartment='+cstr(compartment2)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# FILL SIMULATION CELL WITH WATER
# ===============================
def FillCellWater(density=None, probe=None, bumpsum=None, dismax=None):
  command='FillCellWater '
  if (density!=None): command+='Density='+cstr(density)+','
  if (probe!=None): command+='Probe='+cstr(probe)+','
  if (bumpsum!=None): command+='BumpSum='+cstr(bumpsum)+','
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# FILL OR CLEAR RECTANGULAR AREA
# ==============================
def FillRect(x=None, y=None, width=None, height=None, color=None):
  command='FillRect '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  run(command[:-1])

# GET FIRST ATOM OR RESIDUE FACING EACH CAVITY AND THE CAVITY VOLUME (RESIDUE)
# ============================================================================
def FirstCaviRes(selection1, Type=None):
  command='FirstCaviRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# GET FIRST ATOM OR RESIDUE FACING EACH CAVITY AND THE CAVITY VOLUME (ATOM)
# =========================================================================
def FirstCaviAtom(selection1, Type=None):
  command='FirstCaviAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# GET FIRST ATOM OR RESIDUE FACING EACH SURFACE AND THE SURFACE AREA (RESIDUE)
# ============================================================================
def FirstSurfRes(selection1, Type=None):
  command='FirstSurfRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# GET FIRST ATOM OR RESIDUE FACING EACH SURFACE AND THE SURFACE AREA (ATOM)
# =========================================================================
def FirstSurfAtom(selection1, Type=None):
  command='FirstSurfAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CONSTRAIN BOND LENGTH DURING SIMULATION
# =======================================
def FixBond(selection1, selection2):
  command='FixBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# CONSTRAIN BOND ANGLE DURING SIMULATION
# ======================================
def FixAngle(selection1, selection2, selection3):
  command='FixAngle '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  run(command[:-1])

# CONSTRAIN CRITICAL HYDROGEN BOND ANGLES DURING SIMULATION
# =========================================================
def FixHydAngle(selection1):
  command='FixHydAngle '
  command+=selstr(selection1)+','
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (ALL OR SELECTED)
# =============================================
def Fix():
  command='Fix '
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (ALL)
# =================================
def FixAll():
  command='FixAll '
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (OBJECT)
# ====================================
def FixObj(selection1):
  command='FixObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (MOLECULE)
# ======================================
def FixMol(selection1):
  command='FixMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (RESIDUE)
# =====================================
def FixRes(selection1):
  command='FixRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# FIX ATOMS DURING SIMULATION (ATOM)
# ==================================
def FixAtom(selection1):
  command='FixAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# FLIP TABLE AXES
# ===============
def FlipTab(selection1, firstdim, seconddim=None):
  command='FlipTab '
  command+=selstr(selection1)+','
  command+='FirstDim='+cstr(firstdim)+','
  if (seconddim!=None): command+='SecondDim='+cstr(seconddim)+','
  run(command[:-1])

# SET FOG DENSITY
# ===============
def Fog(density, Range, dismin, dismax):
  command='Fog '
  command+='Density='+cstr(density)+','
  command+='Range='+cstr(Range)+','
  command+='DisMin='+cstr(dismin)+','
  command+='DisMax='+cstr(dismax)+','
  run(command[:-1])

# PREDICT OLIGOMERIC PROTEIN COMPLEX WITH DNA/RNA AND LIGANDS FROM ITS SEQUENCES WITH AI
# ======================================================================================
def FoldObj(filename, sequence, method, selection1):
  command='FoldObj '
  command+='Filename='+cstr(filename)+','
  command+='Sequence='+cstr(sequence)+','
  command+='Method='+cstr(method)+','
  command+=selstr(selection1)+','
  run(command[:-1])

# PREDICT MONOMERIC PROTEIN STRUCTURE DIRECTLY FROM ITS SEQUENCE WITH AI
# ======================================================================
def FoldMol(filename, sequence, method=None):
  command='FoldMol '
  command+='Filename='+cstr(filename)+','
  command+='Sequence='+cstr(sequence)+','
  if (method!=None): command+='Method='+cstr(method)+','
  run(command[:-1])

# SET FONT FOR 3D LETTERS
# =======================
def Font(name=None, height=None, color=None, alpha=None, spacing=None, depth=None, depthcol=None, depthalpha=None):
  command='Font '
  if (name!=None): command+='Name='+cstr(name)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (spacing!=None): command+='Spacing='+cstr(spacing)+','
  if (depth!=None): command+='Depth='+cstr(depth)+','
  if (depthcol!=None): command+='DepthCol='+cstr(depthcol)+','
  if (depthalpha!=None): command+='DepthAlpha='+cstr(depthalpha)+','
  run(command[:-1])

# SWITCH FONT FOG ON/OFF
# ======================
def FontFog(flag):
  command='FontFog '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# SET/GET FORCE FIELD
# ===================
def ForceField(name=None, method=None, setpar=None):
  command='ForceField '
  if (name!=None): command+='Name='+cstr(name)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (setpar!=None): command+='SetPar='+cstr(setpar)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET/GET FORCE ON ATOMS (ALL OR SELECTED)
# ========================================
def Force(x=None, y=None, z=None):
  command='Force '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET FORCE ON ATOMS (ALL)
# ============================
def ForceAll(x=None, y=None, z=None):
  command='ForceAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET FORCE ON ATOMS (OBJECT)
# ===============================
def ForceObj(selection1, x=None, y=None, z=None):
  command='ForceObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET FORCE ON ATOMS (MOLECULE)
# =================================
def ForceMol(selection1, x=None, y=None, z=None):
  command='ForceMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET FORCE ON ATOMS (RESIDUE)
# ================================
def ForceRes(selection1, x=None, y=None, z=None):
  command='ForceRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET FORCE ON ATOMS (ATOM)
# =============================
def ForceAtom(selection1, x=None, y=None, z=None):
  command='ForceAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# FORMAT RESIDUE OUTPUT
# =====================
def FormatRes(output):
  command='FormatRes '
  command+='Output='+cstr(output)+','
  run(command[:-1])

# CALCULATE FORMATION ENERGIES (ALL OR SELECTED)
# ==============================================
def FormEnergy():
  command='FormEnergy '
  return(run(command[:-1]))

# CALCULATE FORMATION ENERGIES (ALL)
# ==================================
def FormEnergyAll():
  command='FormEnergyAll '
  return(run(command[:-1]))

# CALCULATE FORMATION ENERGIES (OBJECT)
# =====================================
def FormEnergyObj(selection1):
  command='FormEnergyObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE FORMATION ENERGIES (MOLECULE)
# =======================================
def FormEnergyMol(selection1):
  command='FormEnergyMol '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE FORMATION ENERGIES (RESIDUE)
# ======================================
def FormEnergyRes(selection1):
  command='FormEnergyRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE FORMATION ENERGIES (ATOM)
# ===================================
def FormEnergyAtom(selection1):
  command='FormEnergyAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET SCREEN UPDATE FREQUENCY
# ===========================
def FramesPerSec(number, redrawidle=None):
  command='FramesPerSec '
  command+='Number='+cstr(number)+','
  if (redrawidle!=None): command+='RedrawIdle='+cstr(redrawidle)+','
  run(command[:-1])

# REMOVE BOND LENGTH CONSTRAINT DURING SIMULATION
# ===============================================
def FreeBond(selection1, selection2):
  command='FreeBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# FREE BOND ANGLE DURING SIMULATION
# =================================
def FreeAngle(selection1, selection2, selection3):
  command='FreeAngle '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (ALL OR SELECTED)
# ==============================================
def Free():
  command='Free '
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (ALL)
# ==================================
def FreeAll():
  command='FreeAll '
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (OBJECT)
# =====================================
def FreeObj(selection1):
  command='FreeObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (MOLECULE)
# =======================================
def FreeMol(selection1):
  command='FreeMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (RESIDUE)
# ======================================
def FreeRes(selection1):
  command='FreeRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# FREE ATOMS DURING SIMULATION (ATOM)
# ===================================
def FreeAtom(selection1):
  command='FreeAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SWITCH FULLSCREEN MODE ON/OFF
# =============================
def FullScreen(flag):
  command='FullScreen '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# CALCULATE GLOBAL DISTANCE TEST (OBJECT)
# =======================================
def GDTObj(selection1, selection2, cutoff=None, match=None):
  command='GDTObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (match!=None): command+='Match='+cstr(match)+','
  return(run(command[:-1]))

# CALCULATE GLOBAL DISTANCE TEST (MOLECULE)
# =========================================
def GDTMol(selection1, selection2, cutoff=None, match=None):
  command='GDTMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (match!=None): command+='Match='+cstr(match)+','
  return(run(command[:-1]))

# CALCULATE GLOBAL DISTANCE TEST (RESIDUE)
# ========================================
def GDTRes(selection1, selection2, cutoff=None, match=None):
  command='GDTRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (match!=None): command+='Match='+cstr(match)+','
  return(run(command[:-1]))

# CALCULATE GLOBAL DISTANCE TEST (ATOM)
# =====================================
def GDTAtom(selection1, selection2, cutoff=None, match=None):
  command='GDTAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (match!=None): command+='Match='+cstr(match)+','
  return(run(command[:-1]))

# GRAB NEXT OBJECT FOR MOUSE MOVEMENT
# ===================================
def GrabNext():
  command='GrabNext '
  run(command[:-1])

# GRAB PREVIOUS OBJECT FOR MOUSE MOVEMENT
# =======================================
def GrabPrev():
  command='GrabPrev '
  run(command[:-1])

# GRAB OBJECT OR SCENE FOR MOUSE MOVEMENT (ALL OR SELECTED)
# =========================================================
def Grab():
  command='Grab '
  run(command[:-1])

# GRAB OBJECT OR SCENE FOR MOUSE MOVEMENT (ALL)
# =============================================
def GrabAll():
  command='GrabAll '
  run(command[:-1])

# GRAB OBJECT OR SCENE FOR MOUSE MOVEMENT (OBJECT)
# ================================================
def GrabObj(selection1):
  command='GrabObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# CALCULATE ANGLE BETWEEN TWO ATOM GROUPS
# =======================================
def GroupAngle(selection1, selection2, Range=None):
  command='GroupAngle '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Range!=None): command+='Range='+cstr(Range)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CALCULATE BOUNDING BOX AROUND ATOM GROUP
# ========================================
def GroupBox(selection1, Type=None, coordsys=None):
  command='GroupBox '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  return(run(command[:-1]))

# CALCULATE GEOMETRIC CENTER OR CENTER OF MASS
# ============================================
def GroupCenter(selection1, coordsys=None, Type=None):
  command='GroupCenter '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE DIHEDRAL ANGLE BETWEEN TWO ATOM GROUPS
# ================================================
def GroupDihedral(selection1, selection2):
  command='GroupDihedral '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CALCULATE DISTANCE BETWEEN TWO ATOM GROUPS
# ==========================================
def GroupDistance(selection1, selection2, center=None):
  command='GroupDistance '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (center!=None): command+='Center='+cstr(center)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CALCULATE OPTIMAL LINE THROUGH ATOM GROUP
# =========================================
def GroupLine(selection1, coordsys=None):
  command='GroupLine '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  return(run(command[:-1]))

# CALCULATE OPTIMAL PLANE THROUGH ATOM GROUP
# ==========================================
def GroupPlane(selection1, coordsys=None):
  command='GroupPlane '
  command+=selstr(selection1)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  return(run(command[:-1]))

# ADD ATOMS TO GROUP (ALL OR SELECTED)
# ====================================
def Group(name):
  command='Group '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# ADD ATOMS TO GROUP (ALL)
# ========================
def GroupAll(name):
  command='GroupAll '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# ADD ATOMS TO GROUP (OBJECT)
# ===========================
def GroupObj(selection1, name):
  command='GroupObj '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# ADD ATOMS TO GROUP (MOLECULE)
# =============================
def GroupMol(selection1, name):
  command='GroupMol '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# ADD ATOMS TO GROUP (RESIDUE)
# ============================
def GroupRes(selection1, name):
  command='GroupRes '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# ADD ATOMS TO GROUP (ATOM)
# =========================
def GroupAtom(selection1, name):
  command='GroupAtom '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# HIDE ARROWS (ALL OR SELECTED)
# =============================
def HideArrow():
  command='HideArrow '
  run(command[:-1])

# HIDE ARROWS (ALL)
# =================
def HideArrowAll():
  command='HideArrowAll '
  run(command[:-1])

# HIDE ARROWS (OBJECT)
# ====================
def HideArrowObj(selection1):
  command='HideArrowObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ARROWS (MOLECULE)
# ======================
def HideArrowMol(selection1):
  command='HideArrowMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ARROWS (RESIDUE)
# =====================
def HideArrowRes(selection1):
  command='HideArrowRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ARROWS (ATOM)
# ==================
def HideArrowAtom(selection1):
  command='HideArrowAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE HYDROGEN BONDS (ALL OR SELECTED)
# =====================================
def HideHBo():
  command='HideHBo '
  run(command[:-1])

# HIDE HYDROGEN BONDS (ALL)
# =========================
def HideHBoAll():
  command='HideHBoAll '
  run(command[:-1])

# HIDE HYDROGEN BONDS (OBJECT)
# ============================
def HideHBoObj(selection1):
  command='HideHBoObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE HYDROGEN BONDS (MOLECULE)
# ==============================
def HideHBoMol(selection1):
  command='HideHBoMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE HYDROGEN BONDS (RESIDUE)
# =============================
def HideHBoRes(selection1):
  command='HideHBoRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE HYDROGEN BONDS (ATOM)
# ==========================
def HideHBoAtom(selection1):
  command='HideHBoAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE IN HEAD-UP DISPLAY (MOLECULE)
# ==================================
def HideHUDMol(selection1):
  command='HideHUDMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE IN HEAD-UP DISPLAY (RESIDUE)
# =================================
def HideHUDRes(selection1):
  command='HideHUDRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE IN HEAD-UP DISPLAY (ATOM)
# ==============================
def HideHUDAtom(selection1):
  command='HideHUDAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE IMAGES
# ===========
def HideImage(selection1):
  command='HideImage '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE TEXT MESSAGE AT THE BOTTOM
# ===============================
def HideMessage():
  command='HideMessage '
  run(command[:-1])

# HIDE POLYGONS (ALL OR SELECTED)
# ===============================
def HidePolygon():
  command='HidePolygon '
  run(command[:-1])

# HIDE POLYGONS (ALL)
# ===================
def HidePolygonAll():
  command='HidePolygonAll '
  run(command[:-1])

# HIDE POLYGONS (OBJECT)
# ======================
def HidePolygonObj(selection1):
  command='HidePolygonObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE POLYGONS (MOLECULE)
# ========================
def HidePolygonMol(selection1):
  command='HidePolygonMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE POLYGONS (RESIDUE)
# =======================
def HidePolygonRes(selection1):
  command='HidePolygonRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE POLYGONS (ATOM)
# ====================
def HidePolygonAtom(selection1):
  command='HidePolygonAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE RESTRAINTS (ALL OR SELECTED)
# =================================
def HideRest(Class=None):
  command='HideRest '
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE RESTRAINTS (ALL)
# =====================
def HideRestAll(Class=None):
  command='HideRestAll '
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE RESTRAINTS (OBJECT)
# ========================
def HideRestObj(selection1, Class=None):
  command='HideRestObj '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE RESTRAINTS (MOLECULE)
# ==========================
def HideRestMol(selection1, Class=None):
  command='HideRestMol '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE RESTRAINTS (RESIDUE)
# =========================
def HideRestRes(selection1, Class=None):
  command='HideRestRes '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE RESTRAINTS (ATOM)
# ======================
def HideRestAtom(selection1, Class=None):
  command='HideRestAtom '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# HIDE SECONDARY STRUCTURE (ALL OR SELECTED)
# ==========================================
def HideSecStr(showatoms=None):
  command='HideSecStr '
  if (showatoms!=None): command+='ShowAtoms='+cstr(showatoms)+','
  run(command[:-1])

# HIDE SECONDARY STRUCTURE (ALL)
# ==============================
def HideSecStrAll(showatoms=None):
  command='HideSecStrAll '
  if (showatoms!=None): command+='ShowAtoms='+cstr(showatoms)+','
  run(command[:-1])

# HIDE SECONDARY STRUCTURE (OBJECT)
# =================================
def HideSecStrObj(selection1, showatoms=None):
  command='HideSecStrObj '
  command+=selstr(selection1)+','
  if (showatoms!=None): command+='ShowAtoms='+cstr(showatoms)+','
  run(command[:-1])

# HIDE SECONDARY STRUCTURE (MOLECULE)
# ===================================
def HideSecStrMol(selection1, showatoms=None):
  command='HideSecStrMol '
  command+=selstr(selection1)+','
  if (showatoms!=None): command+='ShowAtoms='+cstr(showatoms)+','
  run(command[:-1])

# HIDE SECONDARY STRUCTURE (RESIDUE)
# ==================================
def HideSecStrRes(selection1, showatoms=None):
  command='HideSecStrRes '
  command+=selstr(selection1)+','
  if (showatoms!=None): command+='ShowAtoms='+cstr(showatoms)+','
  run(command[:-1])

# HIDE SURFACE (ALL OR SELECTED)
# ==============================
def HideSurf(Type=None):
  command='HideSurf '
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE SURFACE (ALL)
# ==================
def HideSurfAll(Type=None):
  command='HideSurfAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE SURFACE (OBJECT)
# =====================
def HideSurfObj(selection1, Type=None):
  command='HideSurfObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE SURFACE (MOLECULE)
# =======================
def HideSurfMol(selection1, Type=None):
  command='HideSurfMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE SURFACE (RESIDUE)
# ======================
def HideSurfRes(selection1, Type=None):
  command='HideSurfRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE SURFACE (ATOM)
# ===================
def HideSurfAtom(selection1, Type=None):
  command='HideSurfAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# HIDE TRACE THROUGH ATOMS
# ========================
def HideTrace(selection1):
  command='HideTrace '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ATOMS (ALL OR SELECTED)
# ============================
def Hide():
  command='Hide '
  run(command[:-1])

# HIDE ATOMS (ALL)
# ================
def HideAll():
  command='HideAll '
  run(command[:-1])

# HIDE ATOMS (OBJECT)
# ===================
def HideObj(selection1):
  command='HideObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ATOMS (MOLECULE)
# =====================
def HideMol(selection1):
  command='HideMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ATOMS (RESIDUE)
# ====================
def HideRes(selection1):
  command='HideRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# HIDE ATOMS (ATOM)
# =================
def HideAtom(selection1):
  command='HideAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SWITCH HEAD-UP DISPLAY
# ======================
def HUD(show=None, antialias=None, fontsize=None):
  command='HUD '
  if (show!=None): command+='Show='+cstr(show)+','
  if (antialias!=None): command+='Antialias='+cstr(antialias)+','
  if (fontsize!=None): command+='FontSize='+cstr(fontsize)+','
  run(command[:-1])

# SWITCH IMAGE FOG ON/OFF
# =======================
def ImageFog(flag):
  command='ImageFog '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (ALL OR SELECTED)
# =========================================================================
def Inflate():
  command='Inflate '
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (ALL)
# =============================================================
def InflateAll():
  command='InflateAll '
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (OBJECT)
# ================================================================
def InflateObj(selection1):
  command='InflateObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (MOLECULE)
# ==================================================================
def InflateMol(selection1):
  command='InflateMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (RESIDUE)
# =================================================================
def InflateRes(selection1):
  command='InflateRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# GENERATE 3D COORDINATES FOR FLAT OR DISTORTED MOLECULES (ATOM)
# ==============================================================
def InflateAtom(selection1):
  command='InflateAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# INSTALL ACCESSORY PROGRAM
# =========================
def Install(program, code):
  command='Install '
  command+='Program='+cstr(program)+','
  command+='Code='+cstr(code)+','
  run(command[:-1])

# CREATE OBJECT INSTANCES FOR VISUALIZATION (ALL OR SELECTED)
# ===========================================================
def Instance(copies=None, group=None, x=None, y=None, z=None, rx=None, ry=None, rz=None):
  command='Instance '
  if (copies!=None): command+='Copies='+cstr(copies)+','
  if (group!=None): command+='Group='+cstr(group)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (rx!=None): command+='RX='+cstr(rx)+','
  if (ry!=None): command+='RY='+cstr(ry)+','
  if (rz!=None): command+='RZ='+cstr(rz)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE OBJECT INSTANCES FOR VISUALIZATION (ALL)
# ===============================================
def InstanceAll(copies=None, group=None, x=None, y=None, z=None, rx=None, ry=None, rz=None):
  command='InstanceAll '
  if (copies!=None): command+='Copies='+cstr(copies)+','
  if (group!=None): command+='Group='+cstr(group)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (rx!=None): command+='RX='+cstr(rx)+','
  if (ry!=None): command+='RY='+cstr(ry)+','
  if (rz!=None): command+='RZ='+cstr(rz)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE OBJECT INSTANCES FOR VISUALIZATION (OBJECT)
# ==================================================
def InstanceObj(selection1, copies=None, group=None, x=None, y=None, z=None, rx=None, ry=None, rz=None):
  command='InstanceObj '
  command+=selstr(selection1)+','
  if (copies!=None): command+='Copies='+cstr(copies)+','
  if (group!=None): command+='Group='+cstr(group)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (rx!=None): command+='RX='+cstr(rx)+','
  if (ry!=None): command+='RY='+cstr(ry)+','
  if (rz!=None): command+='RZ='+cstr(rz)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET FORCE FIELD TERMS
# =====================
def Interactions(Type):
  command='Interactions '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# PERFORM COLLISION DETECTION TO FIND INTERSECTING OBJECTS
# ========================================================
def IntersectObj(selection1, radiusscale1, selection2, radiusscale2=None):
  command='IntersectObj '
  command+=selstr(selection1)+','
  command+='RadiusScale1='+cstr(radiusscale1)+','
  command+=selstr(selection2)+','
  if (radiusscale2!=None): command+='RadiusScale2='+cstr(radiusscale2)+','
  return(run(command[:-1]))

# JOIN OBJECTS TO ONE FINAL OBJECT
# ================================
def JoinObj(selection1, selection2, center=None):
  command='JoinObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# DELETE SPLIT POINTS (MOLECULE)
# ==============================
def JoinMol(selection1):
  command='JoinMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE SPLIT POINTS (RESIDUE)
# =============================
def JoinRes(selection1):
  command='JoinRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE SPLIT POINTS (ATOM)
# ==========================
def JoinAtom(selection1):
  command='JoinAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# CONFIGURE VIRTUAL ON-SCREEN KEYBOARD
# ====================================
def Keyboard(state, layout, size, keysize, alpha, gapalpha, feedback, inputscale):
  command='Keyboard '
  command+='State='+cstr(state)+','
  command+='Layout='+cstr(layout)+','
  command+='Size='+cstr(size)+','
  command+='KeySize='+cstr(keysize)+','
  command+='Alpha='+cstr(alpha)+','
  command+='GapAlpha='+cstr(gapalpha)+','
  command+='Feedback='+cstr(feedback)+','
  command+='InputScale='+cstr(inputscale)+','
  run(command[:-1])

# REMOVE FRACTIONAL BOND ORDERS
# =============================
def KekulizeBond(selection1, selection2):
  command='KekulizeBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# CALCULATE KINETIC ENERGY (ALL OR SELECTED)
# ==========================================
def KinEnergy(currenttime=None):
  command='KinEnergy '
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# CALCULATE KINETIC ENERGY (ALL)
# ==============================
def KinEnergyAll(currenttime=None):
  command='KinEnergyAll '
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# CALCULATE KINETIC ENERGY (OBJECT)
# =================================
def KinEnergyObj(selection1, currenttime=None):
  command='KinEnergyObj '
  command+=selstr(selection1)+','
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# CALCULATE KINETIC ENERGY (MOLECULE)
# ===================================
def KinEnergyMol(selection1, currenttime=None):
  command='KinEnergyMol '
  command+=selstr(selection1)+','
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# CALCULATE KINETIC ENERGY (RESIDUE)
# ==================================
def KinEnergyRes(selection1, currenttime=None):
  command='KinEnergyRes '
  command+=selstr(selection1)+','
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# CALCULATE KINETIC ENERGY (ATOM)
# ===============================
def KinEnergyAtom(selection1, currenttime=None):
  command='KinEnergyAtom '
  command+=selstr(selection1)+','
  if (currenttime!=None): command+='CurrentTime='+cstr(currenttime)+','
  return(run(command[:-1]))

# LABEL ATOM DISTANCES
# ====================
def LabelDis(selection1, selection2, format=None, height=None, color=None, x=None, y=None, z=None, bound=None, radius=None):
  command='LabelDis '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (bound!=None): command+='Bound='+cstr(bound)+','
  if (radius!=None): command+='Radius='+cstr(radius)+','
  run(command[:-1])

# SET LABEL PARAMETERS
# ====================
def LabelPar(font, height=None, color=None, ontop=None, shrink=None, fog=None):
  command='LabelPar '
  command+='Font='+cstr(font)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (ontop!=None): command+='OnTop='+cstr(ontop)+','
  if (shrink!=None): command+='Shrink='+cstr(shrink)+','
  if (fog!=None): command+='Fog='+cstr(fog)+','
  run(command[:-1])

# ADD LABELS (ALL OR SELECTED)
# ============================
def Label(format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='Label '
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (ALL)
# ================
def LabelAll(format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelAll '
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (OBJECT)
# ===================
def LabelObj(selection1, format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelObj '
  command+=selstr(selection1)+','
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (MOLECULE)
# =====================
def LabelMol(selection1, format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelMol '
  command+=selstr(selection1)+','
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (SEGMENT)
# ====================
def LabelSeg(selection1, format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelSeg '
  command+=selstr(selection1)+','
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (RESIDUE)
# ====================
def LabelRes(selection1, format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelRes '
  command+=selstr(selection1)+','
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# ADD LABELS (ATOM)
# =================
def LabelAtom(selection1, format, height=None, color=None, x=None, y=None, z=None, convert=None):
  command='LabelAtom '
  command+=selstr(selection1)+','
  command+='Format='+cstr(format)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# CONFIGURE THE LIGHT SOURCE
# ==========================
def LightSource(alpha=None, gamma=None, ambience=None, ambience2=None, shadow=None, shadowspeed=None, ambiencefps=None, softshadowfps=None, hardshadowfps=None, cellshadow=None):
  command='LightSource '
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  if (ambience!=None): command+='Ambience='+cstr(ambience)+','
  if (ambience2!=None): command+='Ambience2='+cstr(ambience2)+','
  if (shadow!=None): command+='Shadow='+cstr(shadow)+','
  if (shadowspeed!=None): command+='ShadowSpeed='+cstr(shadowspeed)+','
  if (ambiencefps!=None): command+='AmbienceFPS='+cstr(ambiencefps)+','
  if (softshadowfps!=None): command+='SoftShadowFPS='+cstr(softshadowfps)+','
  if (hardshadowfps!=None): command+='HardShadowFPS='+cstr(hardshadowfps)+','
  if (cellshadow!=None): command+='CellShadow='+cstr(cellshadow)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (ALL OR SELECTED)
# =======================================
def Light(direction):
  command='Light '
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (ALL)
# ===========================
def LightAll(direction):
  command='LightAll '
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (OBJECT)
# ==============================
def LightObj(selection1, direction):
  command='LightObj '
  command+=selstr(selection1)+','
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (MOLECULE)
# ================================
def LightMol(selection1, direction):
  command='LightMol '
  command+=selstr(selection1)+','
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (RESIDUE)
# ===============================
def LightRes(selection1, direction):
  command='LightRes '
  command+=selstr(selection1)+','
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# SET PER-ATOM LIGHTING (ATOM)
# ============================
def LightAtom(selection1, direction):
  command='LightAtom '
  command+=selstr(selection1)+','
  command+='Direction='+cstr(direction)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (ALL OR SELECTED)
# ==========================================
def Link(deviation=None, Type=None):
  command='Link '
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (ALL)
# ==============================
def LinkAll(deviation=None, Type=None):
  command='LinkAll '
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (OBJECT)
# =================================
def LinkObj(selection1, deviation=None, Type=None):
  command='LinkObj '
  command+=selstr(selection1)+','
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (MOLECULE)
# ===================================
def LinkMol(selection1, deviation=None, Type=None):
  command='LinkMol '
  command+=selstr(selection1)+','
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (RESIDUE)
# ==================================
def LinkRes(selection1, deviation=None, Type=None):
  command='LinkRes '
  command+=selstr(selection1)+','
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# FIND BONDS AUTOMATICALLY (ATOM)
# ===============================
def LinkAtom(selection1, deviation=None, Type=None):
  command='LinkAtom '
  command+=selstr(selection1)+','
  if (deviation!=None): command+='Deviation='+cstr(deviation)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  run(command[:-1])

# LIST CONTACTS (OBJECT)
# ======================
def ListConObj(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, sort=None, results=None):
  command='ListConObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# LIST CONTACTS (MOLECULE)
# ========================
def ListConMol(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, sort=None, results=None):
  command='ListConMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# LIST CONTACTS (RESIDUE)
# =======================
def ListConRes(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, sort=None, results=None):
  command='ListConRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# LIST CONTACTS (ATOM)
# ====================
def ListConAtom(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None, sort=None, results=None):
  command='ListConAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# LIST DIRECTORY CONTENT
# ======================
def ListDir(filename):
  command='ListDir '
  command+='Filename='+cstr(filename)+','
  return(run(command[:-1]))

# LIST HYDROGEN BONDS (OBJECT)
# ============================
def ListHBoObj(selection1, selection2, Min=None, results=None, format=None):
  command='ListHBoObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST HYDROGEN BONDS (MOLECULE)
# ==============================
def ListHBoMol(selection1, selection2, Min=None, results=None, format=None):
  command='ListHBoMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST HYDROGEN BONDS (RESIDUE)
# =============================
def ListHBoRes(selection1, selection2, Min=None, results=None, format=None):
  command='ListHBoRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST HYDROGEN BONDS (ATOM)
# ==========================
def ListHBoAtom(selection1, selection2, Min=None, results=None, format=None):
  command='ListHBoAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST INTERACTIONS (OBJECT)
# ==========================
def ListIntObj(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, sort=None, results=None, format=None):
  command='ListIntObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST INTERACTIONS (MOLECULE)
# ============================
def ListIntMol(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, sort=None, results=None, format=None):
  command='ListIntMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST INTERACTIONS (RESIDUE)
# ===========================
def ListIntRes(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, sort=None, results=None, format=None):
  command='ListIntRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LIST INTERACTIONS (ATOM)
# ========================
def ListIntAtom(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, sort=None, results=None, format=None):
  command='ListIntAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# LOAD IMAGE FROM BMP FILE
# ========================
def LoadBmp(filename, transcol=None):
  command='LoadBmp '
  command+='Filename='+cstr(filename)+','
  if (transcol!=None): command+='TransCol='+cstr(transcol)+','
  run(command[:-1])

# LOAD CIF OR MMCIF FILE
# ======================
def LoadCIF(filename, center=None, correct=None, model=None, missres=None, transfer=None):
  command='LoadCIF '
  command+='Filename='+cstr(filename)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (correct!=None): command+='Correct='+cstr(correct)+','
  if (model!=None): command+='Model='+cstr(model)+','
  if (missres!=None): command+='MissRes='+cstr(missres)+','
  if (transfer!=None): command+='Transfer='+cstr(transfer)+','
  return(run(command[:-1]))

# LOAD POLYGON MESH IN COLLADA FORMAT
# ===================================
def LoadDAE(filename, color=None, alpha=None, open=None):
  command='LoadDAE '
  command+='Filename='+cstr(filename)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (open!=None): command+='Open='+cstr(open)+','
  return(run(command[:-1]))

# LOAD AND VISUALIZE ELECTROSTATIC POTENTIAL
# ==========================================
def LoadESP(filename, style, Min=None, Max=None):
  command='LoadESP '
  command+='Filename='+cstr(filename)+','
  command+='Style='+cstr(style)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (Max!=None): command+='Max='+cstr(Max)+','
  run(command[:-1])

# LOAD AND VISUALIZE ELECTROSTATIC POTENTIAL
# ==========================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def LoadESP2(filename, style, level=None):
  command='LoadESP '
  command+='Filename='+cstr(filename)+','
  command+='Style='+cstr(style)+','
  if (level!=None): command+='Level='+cstr(level)+','
  run(command[:-1])

# LOAD IMAGE FROM JPG FILE
# ========================
def LoadJPG(filename):
  command='LoadJPG '
  command+='Filename='+cstr(filename)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN MDCRD FORMAT (ALL OR SELECTED)
# ==========================================================
def LoadMDCrd(filename, snapshot=None, assignsec=None, readcell=None):
  command='LoadMDCrd '
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  if (readcell!=None): command+='readCell='+cstr(readcell)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN MDCRD FORMAT (ALL)
# ==============================================
def LoadMDCrdAll(filename, snapshot=None, assignsec=None, readcell=None):
  command='LoadMDCrdAll '
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  if (readcell!=None): command+='readCell='+cstr(readcell)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN MDCRD FORMAT (OBJECT)
# =================================================
def LoadMDCrdObj(selection1, filename, snapshot=None, assignsec=None, readcell=None):
  command='LoadMDCrdObj '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  if (readcell!=None): command+='readCell='+cstr(readcell)+','
  run(command[:-1])

# STREAM MOVIE FROM MPEG4 FILE
# ============================
def LoadMPG(filename, loop=None, startframe=None, fps=None):
  command='LoadMPG '
  command+='Filename='+cstr(filename)+','
  if (loop!=None): command+='Loop='+cstr(loop)+','
  if (startframe!=None): command+='StartFrame='+cstr(startframe)+','
  if (fps!=None): command+='FPS='+cstr(fps)+','
  run(command[:-1])

# LOAD DISTANCE, DIHEDRAL AND RDC RESTRAINTS IN NMR EXCHANGE FORMAT
# =================================================================
def LoadNEF(filename, selection1, Class, nameformat):
  command='LoadNEF '
  command+='Filename='+cstr(filename)+','
  command+=selstr(selection1)+','
  command+='Class='+cstr(Class)+','
  command+='NameFormat='+cstr(nameformat)+','
  run(command[:-1])

# LOAD PROTEIN DATA BANK FILE
# ===========================
def LoadPDB(filename, center=None, correct=None, model=None, download=None, seqres=None, contour=None, transfer=None):
  command='LoadPDB '
  command+='Filename='+cstr(filename)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (correct!=None): command+='Correct='+cstr(correct)+','
  if (model!=None): command+='Model='+cstr(model)+','
  if (download!=None): command+='Download='+cstr(download)+','
  if (seqres!=None): command+='SeqRes='+cstr(seqres)+','
  if (contour!=None): command+='Contour='+cstr(contour)+','
  if (transfer!=None): command+='Transfer='+cstr(transfer)+','
  return(run(command[:-1]))

# LOAD IMAGE FROM PNG FILE
# ========================
def LoadPNG(filename, transcol=None):
  command='LoadPNG '
  command+='Filename='+cstr(filename)+','
  if (transcol!=None): command+='TransCol='+cstr(transcol)+','
  run(command[:-1])

# LOAD AMBER PREP TOPOLOGY
# ========================
def LoadPrep(filename, name=None):
  command='LoadPrep '
  command+='Filename='+cstr(filename)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# LOAD COMPLETE SCENE
# ===================
def LoadSce(filename, settings=None):
  command='LoadSce '
  command+='Filename='+cstr(filename)+','
  if (settings!=None): command+='Settings='+cstr(settings)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN SIM FORMAT
# ======================================
def LoadSim(filename, assignsec=None):
  command='LoadSim '
  command+='Filename='+cstr(filename)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  run(command[:-1])

# LOAD TABLE WITH ONE, TWO OR THREE DIMENSIONS
# ============================================
def LoadTab(filename, dimensions=None, columns=None, rows=None, pages=None):
  command='LoadTab '
  command+='Filename='+cstr(filename)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (columns!=None): command+='Columns='+cstr(columns)+','
  if (rows!=None): command+='Rows='+cstr(rows)+','
  if (pages!=None): command+='Pages='+cstr(pages)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# LOAD DISTANCE, DIHEDRAL AND RDC RESTRAINTS IN XPLOR FORMAT
# ==========================================================
def LoadTbl(filename, selection1, Class=None, nameformat=None):
  command='LoadTbl '
  command+='Filename='+cstr(filename)+','
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (nameformat!=None): command+='NameFormat='+cstr(nameformat)+','
  run(command[:-1])

# LOAD POLYGON MESH IN WAVEFRONT OBJECT FORMAT
# ============================================
def LoadWOb(filename, color=None, alpha=None, open=None, selection1=None):
  command='LoadWOb '
  command+='Filename='+cstr(filename)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (open!=None): command+='Open='+cstr(open)+','
  if (selection1!=None): command+=selstr(selection1)+','
  return(run(command[:-1]))

# LOAD SIMULATION SNAPSHOT IN XTC FORMAT (ALL OR SELECTED)
# ========================================================
def LoadXTC(filename, snapshot=None, assignsec=None):
  command='LoadXTC '
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN XTC FORMAT (ALL)
# ============================================
def LoadXTCAll(filename, snapshot=None, assignsec=None):
  command='LoadXTCAll '
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  run(command[:-1])

# LOAD SIMULATION SNAPSHOT IN XTC FORMAT (OBJECT)
# ===============================================
def LoadXTCObj(selection1, filename, snapshot=None, assignsec=None):
  command='LoadXTCObj '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (snapshot!=None): command+='Snapshot='+cstr(snapshot)+','
  if (assignsec!=None): command+='assignSec='+cstr(assignsec)+','
  run(command[:-1])

# LOAD YASARA OBJECT
# ==================
def LoadYOb(filename, transfer=None):
  command='LoadYOb '
  command+='Filename='+cstr(filename)+','
  if (transfer!=None): command+='Transfer='+cstr(transfer)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# LOAD FILE IN ANY FORMAT
# =======================
def Load(filename):
  command='Load '
  command+='Filename='+cstr(filename)+','
  run(command[:-1])

# IMPORT FILE WITH OPENBABEL
# ==========================
def Load(format, filename, center=None, resonate=None, model=None, transfer=None):
  command='Load '
  command=command[:-1]+cstr(format)+' '
  command+='Filename='+cstr(filename)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (resonate!=None): command+='Resonate='+cstr(resonate)+','
  if (model!=None): command+='Model='+cstr(model)+','
  if (transfer!=None): command+='Transfer='+cstr(transfer)+','
  return(run(command[:-1]))

# LOG OUTPUT OF NEXT COMMAND
# ==========================
def LogAs(filename, append=None):
  command='LogAs '
  command+='Filename='+cstr(filename)+','
  if (append!=None): command+='append='+cstr(append)+','
  run(command[:-1])

# LOG OUTPUT OF NEXT COMMAND
# ==========================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def LogAs2(filename, append, noname1):
  command='LogAs '
  command+='Filename='+cstr(filename)+','
  command+='append='+cstr(append)+','
  command+=cstr(noname1)+','
  run(command[:-1])

# LIST BONDS
# ==========
def ListBond(selection1, selection2, results=None, lenmin=None):
  command='ListBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (results!=None): command+='Results='+cstr(results)+','
  if (lenmin!=None): command+='LenMin='+cstr(lenmin)+','
  return(run(command[:-1]))

# LIST FLOATING ASSIGNMENTS (ALL OR SELECTED)
# ===========================================
def ListFloat(Type=None, format=None):
  command='ListFloat '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (format!=None): command+='Format='+cstr(format)+','
  run(command[:-1])

# LIST FLOATING ASSIGNMENTS (ALL)
# ===============================
def ListFloatAll(Type=None, format=None):
  command='ListFloatAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (format!=None): command+='Format='+cstr(format)+','
  run(command[:-1])

# LIST FLOATING ASSIGNMENTS (OBJECT)
# ==================================
def ListFloatObj(selection1, Type=None, format=None):
  command='ListFloatObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (format!=None): command+='Format='+cstr(format)+','
  run(command[:-1])

# LIST IMAGES
# ===========
def ListImage(selection1):
  command='ListImage '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (ALL OR SELECTED)
# ==============================================
def ListRest(Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRest '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (ALL)
# ==================================
def ListRestAll(Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRestAll '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (OBJECT)
# =====================================
def ListRestObj(selection1, Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRestObj '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (MOLECULE)
# =======================================
def ListRestMol(selection1, Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRestMol '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (RESIDUE)
# ======================================
def ListRestRes(selection1, Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRestRes '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST RESTRAINTS AND ENERGIES (ATOM)
# ===================================
def ListRestAtom(selection1, Class=None, component=None, format=None, sort=None, dismin=None, dihmin=None, rdcmin=None, objectsmin=None):
  command='ListRestAtom '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (sort!=None): command+='Sort='+cstr(sort)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (dihmin!=None): command+='DihMin='+cstr(dihmin)+','
  if (rdcmin!=None): command+='RDCMin='+cstr(rdcmin)+','
  if (objectsmin!=None): command+='ObjectsMin='+cstr(objectsmin)+','
  return(run(command[:-1]))

# LIST ATOMS MATCHING SMARTS STRING
# =================================
def ListSMARTS(string, selection1=None):
  command='ListSMARTS '
  command+='String='+cstr(string)+','
  if (selection1!=None): command+=selstr(selection1)+','
  return(run(command[:-1]))

# LIST ATOMS MATCHING SMILES STRING
# =================================
def ListSMILES(string, selection1=None):
  command='ListSMILES '
  command+='String='+cstr(string)+','
  if (selection1!=None): command+=selstr(selection1)+','
  return(run(command[:-1]))

# LIST SELECTION (OBJECT)
# =======================
def ListObj(selection1, format=None, compress=None):
  command='ListObj '
  command+=selstr(selection1)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (compress!=None): command+='Compress='+cstr(compress)+','
  return(run(command[:-1]))

# LIST SELECTION (MOLECULE)
# =========================
def ListMol(selection1, format=None, compress=None):
  command='ListMol '
  command+=selstr(selection1)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (compress!=None): command+='Compress='+cstr(compress)+','
  return(run(command[:-1]))

# LIST SELECTION (RESIDUE)
# ========================
def ListRes(selection1, format=None, compress=None):
  command='ListRes '
  command+=selstr(selection1)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (compress!=None): command+='Compress='+cstr(compress)+','
  return(run(command[:-1]))

# LIST SELECTION (ATOM)
# =====================
def ListAtom(selection1, format=None, compress=None):
  command='ListAtom '
  command+=selstr(selection1)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (compress!=None): command+='Compress='+cstr(compress)+','
  return(run(command[:-1]))

# SET LONG RANGE INTERACTIONS
# ===========================
def Longrange(Type):
  command='Longrange '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SET MACRO TARGET
# ================
def MacroTarget(filename=None, remove=None):
  command='MacroTarget '
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (remove!=None): command+='Remove='+cstr(remove)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE EMPTY IMAGE
# ==================
def MakeImage(name, width=None, height=None, topcol=None, bottomcol=None):
  command='MakeImage '
  command+='Name='+cstr(name)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (topcol!=None): command+='TopCol='+cstr(topcol)+','
  if (bottomcol!=None): command+='BottomCol='+cstr(bottomcol)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE OBJECT WITH ATTACHED IMAGE
# =================================
def MakeImageObj(name, selection1, width=None, height=None, depth=None):
  command='MakeImageObj '
  command+='Name='+cstr(name)+','
  command+=selstr(selection1)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (depth!=None): command+='Depth='+cstr(depth)+','
  return(run(command[:-1]))

# MAKE A TABLE
# ============
def MakeTab(name, dimensions=None, columns=None, rows=None, pages=None):
  command='MakeTab '
  command+='Name='+cstr(name)+','
  if (dimensions!=None): command+='Dimensions='+cstr(dimensions)+','
  if (columns!=None): command+='Columns='+cstr(columns)+','
  if (rows!=None): command+='Rows='+cstr(rows)+','
  if (pages!=None): command+='Pages='+cstr(pages)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# MAKE TEXT OBJECT TO PRINT 3D LETTERS
# ====================================
def MakeTextObj(name=None, width=None, height=None):
  command='MakeTextObj '
  if (name!=None): command+='Name='+cstr(name)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE AN EMPTY SECONDARY WINDOW
# ================================
def MakeWin(width=None, height=None, screen=None, fullscreen=None, topcol=None, bottomcol=None):
  command='MakeWin '
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (screen!=None): command+='Screen='+cstr(screen)+','
  if (fullscreen!=None): command+='FullScreen='+cstr(fullscreen)+','
  if (topcol!=None): command+='TopCol='+cstr(topcol)+','
  if (bottomcol!=None): command+='BottomCol='+cstr(bottomcol)+','
  run(command[:-1])

# SET/GET ATOMS MARKED WITH FIREFLIES
# ===================================
def MarkAtom(selection1=None, selection2=None, selection3=None, selection4=None, zoom=None):
  command='MarkAtom '
  if (selection1!=None): command+=selstr(selection1)+','
  if (selection2!=None): command+=selstr(selection2)+','
  if (selection3!=None): command+=selstr(selection3)+','
  if (selection4!=None): command+=selstr(selection4)+','
  if (zoom!=None): command+='Zoom='+cstr(zoom)+','
  return(run(command[:-1]))

# SET/GET ATOMS MARKED WITH FIREFLIES
# ===================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def MarkAtomNone():
  command='MarkAtom None,'
  return(run(command[:-1]))

# CALCULATE MASS (ALL OR SELECTED)
# ================================
def Mass():
  command='Mass '
  return(run(command[:-1]))

# CALCULATE MASS (ALL)
# ====================
def MassAll():
  command='MassAll '
  return(run(command[:-1]))

# CALCULATE MASS (OBJECT)
# =======================
def MassObj(selection1):
  command='MassObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE MASS (MOLECULE)
# =========================
def MassMol(selection1):
  command='MassMol '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE MASS (RESIDUE)
# ========================
def MassRes(selection1):
  command='MassRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# CALCULATE MASS (ATOM)
# =====================
def MassAtom(selection1):
  command='MassAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SET MEMORY USAGE AND EXIT
# =========================
def Memory(size):
  command='Memory '
  command+='Size='+cstr(size)+','
  run(command[:-1])

# SWITCH MENU ON/OFF
# ==================
def Menu(flag):
  command='Menu '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# MONOMERIZE OBJECTS, KEEPING THE TRANSFORMATIONS TO OLIGOMERIZE AGAIN LATER (ALL OR SELECTED)
# ============================================================================================
def Monomerize(center=None):
  command='Monomerize '
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# MONOMERIZE OBJECTS, KEEPING THE TRANSFORMATIONS TO OLIGOMERIZE AGAIN LATER (ALL)
# ================================================================================
def MonomerizeAll(center=None):
  command='MonomerizeAll '
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# MONOMERIZE OBJECTS, KEEPING THE TRANSFORMATIONS TO OLIGOMERIZE AGAIN LATER (OBJECT)
# ===================================================================================
def MonomerizeObj(selection1, center=None):
  command='MonomerizeObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  run(command[:-1])

# MOVE POLYGON MESH
# =================
def MoveMesh(selection1, x=None, y=None, z=None):
  command='MoveMesh '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (ALL OR SELECTED)
# ==================================================
def Move(x=None, y=None, z=None):
  command='Move '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (ALL)
# ======================================
def MoveAll(x=None, y=None, z=None):
  command='MoveAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (OBJECT)
# =========================================
def MoveObj(selection1, x=None, y=None, z=None):
  command='MoveObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (MOLECULE)
# ===========================================
def MoveMol(selection1, x=None, y=None, z=None):
  command='MoveMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (RESIDUE)
# ==========================================
def MoveRes(selection1, x=None, y=None, z=None):
  command='MoveRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# MOVE ATOMS, OBJECTS OR THE SCENE (ATOM)
# =======================================
def MoveAtom(selection1, x=None, y=None, z=None):
  command='MoveAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SET ENERGY MINIMIZATION STEP
# ============================
def MinStep(size):
  command='MinStep '
  command+='Size='+cstr(size)+','
  run(command[:-1])

# CONVERT RESIDUE NAMES FROM 1- TO 3-LETTER CODE
# ==============================================
def Name3(sequence):
  command='Name3 '
  command+='Sequence='+cstr(sequence)+','
  return(run(command[:-1]))

# RENAME FILE
# ===========
def RenameFile(srcfilename=None, dstfilename=None, overwrite=None):
  command='RenameFile '
  if (srcfilename!=None): command+='SrcFilename='+cstr(srcfilename)+','
  if (dstfilename!=None): command+='DstFilename='+cstr(dstfilename)+','
  if (overwrite!=None): command+='Overwrite='+cstr(overwrite)+','
  run(command[:-1])

# SET/GET NAMES OF OBJECTS, SEGMENTS, MOLECULES, RESIDUES AND ATOMS (OBJECT)
# ==========================================================================
def NameObj(selection1, name=None):
  command='NameObj '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET NAMES OF OBJECTS, SEGMENTS, MOLECULES, RESIDUES AND ATOMS (MOLECULE)
# ============================================================================
def NameMol(selection1, name=None):
  command='NameMol '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET NAMES OF OBJECTS, SEGMENTS, MOLECULES, RESIDUES AND ATOMS (SEGMENT)
# ===========================================================================
def NameSeg(selection1, name=None):
  command='NameSeg '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET NAMES OF OBJECTS, SEGMENTS, MOLECULES, RESIDUES AND ATOMS (RESIDUE)
# ===========================================================================
def NameRes(selection1, name=None):
  command='NameRes '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET NAMES OF OBJECTS, SEGMENTS, MOLECULES, RESIDUES AND ATOMS (ATOM)
# ========================================================================
def NameAtom(selection1, name=None):
  command='NameAtom '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# ORIENT OBJECTS NICELY (ALL OR SELECTED)
# =======================================
def NiceOri(axis1=None, axis2=None):
  command='NiceOri '
  if (axis1!=None): command+='Axis1='+cstr(axis1)+','
  if (axis2!=None): command+='Axis2='+cstr(axis2)+','
  run(command[:-1])

# ORIENT OBJECTS NICELY (ALL)
# ===========================
def NiceOriAll(axis1=None, axis2=None):
  command='NiceOriAll '
  if (axis1!=None): command+='Axis1='+cstr(axis1)+','
  if (axis2!=None): command+='Axis2='+cstr(axis2)+','
  run(command[:-1])

# ORIENT OBJECTS NICELY (OBJECT)
# ==============================
def NiceOriObj(selection1, axis1=None, axis2=None):
  command='NiceOriObj '
  command+=selstr(selection1)+','
  if (axis1!=None): command+='Axis1='+cstr(axis1)+','
  if (axis2!=None): command+='Axis2='+cstr(axis2)+','
  run(command[:-1])

# SET/GET THE OCCUPANCY (ALL OR SELECTED)
# =======================================
def Occup(value=None):
  command='Occup '
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE OCCUPANCY (ALL)
# ===========================
def OccupAll(value=None):
  command='OccupAll '
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE OCCUPANCY (OBJECT)
# ==============================
def OccupObj(selection1, value=None):
  command='OccupObj '
  command+=selstr(selection1)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE OCCUPANCY (MOLECULE)
# ================================
def OccupMol(selection1, value=None):
  command='OccupMol '
  command+=selstr(selection1)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE OCCUPANCY (RESIDUE)
# ===============================
def OccupRes(selection1, value=None):
  command='OccupRes '
  command+=selstr(selection1)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE OCCUPANCY (ATOM)
# ============================
def OccupAtom(selection1, value=None):
  command='OccupAtom '
  command+=selstr(selection1)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# OLIGOMERIZE OBJECTS TO GENERATE THE BIOLOGICALLY ACTIVE FORM (ALL OR SELECTED)
# ==============================================================================
def Oligomerize(center=None, instance=None):
  command='Oligomerize '
  if (center!=None): command+='Center='+cstr(center)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  return(run(command[:-1]))

# OLIGOMERIZE OBJECTS TO GENERATE THE BIOLOGICALLY ACTIVE FORM (ALL)
# ==================================================================
def OligomerizeAll(center=None, instance=None):
  command='OligomerizeAll '
  if (center!=None): command+='Center='+cstr(center)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  return(run(command[:-1]))

# OLIGOMERIZE OBJECTS TO GENERATE THE BIOLOGICALLY ACTIVE FORM (OBJECT)
# =====================================================================
def OligomerizeObj(selection1, center=None, instance=None):
  command='OligomerizeObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (instance!=None): command+='Instance='+cstr(instance)+','
  return(run(command[:-1]))

# OPTIMIZE HYDROGEN BONDING NETWORK (ALL OR SELECTED)
# ===================================================
def OptHyd(method):
  command='OptHyd '
  command+='Method='+cstr(method)+','
  run(command[:-1])

# OPTIMIZE HYDROGEN BONDING NETWORK (ALL)
# =======================================
def OptHydAll(method):
  command='OptHydAll '
  command+='Method='+cstr(method)+','
  run(command[:-1])

# OPTIMIZE HYDROGEN BONDING NETWORK (OBJECT)
# ==========================================
def OptHydObj(selection1, method):
  command='OptHydObj '
  command+=selstr(selection1)+','
  command+='Method='+cstr(method)+','
  run(command[:-1])

# OPTIMIZE CENTRAL OR TERMINAL LOOP
# =================================
def OptimizeLoop(selection1, selection2, samples=None, secstr=None):
  command='OptimizeLoop '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (samples!=None): command+='Samples='+cstr(samples)+','
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# OPTIMIZE MOLECULAR GEOMETRY (ALL OR SELECTED)
# =============================================
def Optimize(method=None, structures=None):
  command='Optimize '
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  return(run(command[:-1]))

# OPTIMIZE MOLECULAR GEOMETRY (ALL)
# =================================
def OptimizeAll(method=None, structures=None):
  command='OptimizeAll '
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  return(run(command[:-1]))

# OPTIMIZE MOLECULAR GEOMETRY (OBJECT)
# ====================================
def OptimizeObj(selection1, method=None, structures=None):
  command='OptimizeObj '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  return(run(command[:-1]))

# OPTIMIZE MOLECULAR GEOMETRY (MOLECULE)
# ======================================
def OptimizeMol(selection1, method=None, structures=None):
  command='OptimizeMol '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  return(run(command[:-1]))

# OPTIMIZE MOLECULAR GEOMETRY (RESIDUE)
# =====================================
def OptimizeRes(selection1, method=None, structures=None):
  command='OptimizeRes '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  return(run(command[:-1]))

# GET VECTOR ORIENTATION
# ======================
def OriVec(x1=None, y1=None, z1=None, x2=None, y2=None, z2=None):
  command='OriVec '
  if (x1!=None): command+='X1='+cstr(x1)+','
  if (y1!=None): command+='Y1='+cstr(y1)+','
  if (z1!=None): command+='Z1='+cstr(z1)+','
  if (x2!=None): command+='X2='+cstr(x2)+','
  if (y2!=None): command+='Y2='+cstr(y2)+','
  if (z2!=None): command+='Z2='+cstr(z2)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE ORIENTATION (ALL OR SELECTED)
# =====================================================
def Ori(alpha=None, beta=None, gamma=None):
  command='Ori '
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE ORIENTATION (ALL)
# =========================================
def OriAll(alpha=None, beta=None, gamma=None):
  command='OriAll '
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE ORIENTATION (OBJECT)
# ============================================
def OriObj(selection1, alpha=None, beta=None, gamma=None):
  command='OriObj '
  command+=selstr(selection1)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# CALCULATE OVERLAP VOLUMES (OBJECT)
# ==================================
def OverlapObj(selection1, selection2, Type=None):
  command='OverlapObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE OVERLAP VOLUMES (MOLECULE)
# ====================================
def OverlapMol(selection1, selection2, Type=None):
  command='OverlapMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE OVERLAP VOLUMES (RESIDUE)
# ===================================
def OverlapRes(selection1, selection2, Type=None):
  command='OverlapRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE OVERLAP VOLUMES (ATOM)
# ================================
def OverlapAtom(selection1, selection2, Type=None):
  command='OverlapAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET PERMISSIONS OF THE YASARA INSTALL DIRECTORY
# ===============================================
def PermitAccess():
  command='PermitAccess '
  run(command[:-1])

# CALCULATE ATOM POSITIONS FROM PCA COMPONENTS (OBJECT)
# =====================================================
def PCAPosObj(selection1, unit, selection2, value, value2):
  command='PCAPosObj '
  command+=selstr(selection1)+','
  command+='Unit='+cstr(unit)+','
  command+=selstr(selection2)+','
  command+='Value='+cstr(value)+','
  command+='Value='+cstr(value2)+','
  run(command[:-1])

# CALCULATE ATOM POSITIONS FROM PCA COMPONENTS (MOLECULE)
# =======================================================
def PCAPosMol(selection1, unit, selection2, value, value2):
  command='PCAPosMol '
  command+=selstr(selection1)+','
  command+='Unit='+cstr(unit)+','
  command+=selstr(selection2)+','
  command+='Value='+cstr(value)+','
  command+='Value='+cstr(value2)+','
  run(command[:-1])

# CALCULATE ATOM POSITIONS FROM PCA COMPONENTS (RESIDUE)
# ======================================================
def PCAPosRes(selection1, unit, selection2, value, value2):
  command='PCAPosRes '
  command+=selstr(selection1)+','
  command+='Unit='+cstr(unit)+','
  command+=selstr(selection2)+','
  command+='Value='+cstr(value)+','
  command+='Value='+cstr(value2)+','
  run(command[:-1])

# CALCULATE ATOM POSITIONS FROM PCA COMPONENTS (ATOM)
# ===================================================
def PCAPosAtom(selection1, unit, selection2, value, value2):
  command='PCAPosAtom '
  command+=selstr(selection1)+','
  command+='Unit='+cstr(unit)+','
  command+=selstr(selection2)+','
  command+='Value='+cstr(value)+','
  command+='Value='+cstr(value2)+','
  run(command[:-1])

# PERFORM PRINCIPAL COMPONENT ANALYSIS (MOLECULE)
# ===============================================
def PCAMol(selection1, component=None, weighted=None):
  command='PCAMol '
  command+=selstr(selection1)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (weighted!=None): command+='Weighted='+cstr(weighted)+','
  return(run(command[:-1]))

# PERFORM PRINCIPAL COMPONENT ANALYSIS (RESIDUE)
# ==============================================
def PCARes(selection1, component=None, weighted=None):
  command='PCARes '
  command+=selstr(selection1)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (weighted!=None): command+='Weighted='+cstr(weighted)+','
  return(run(command[:-1]))

# PERFORM PRINCIPAL COMPONENT ANALYSIS (ATOM)
# ===========================================
def PCAAtom(selection1, component=None, weighted=None):
  command='PCAAtom '
  command+=selstr(selection1)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (weighted!=None): command+='Weighted='+cstr(weighted)+','
  return(run(command[:-1]))

# SET/GET DEFAULT PH
# ==================
def pH(value=None, update=None):
  command='pH '
  if (value!=None): command+='Value='+cstr(value)+','
  if (update!=None): command+='Update='+cstr(update)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET/GET RESIDUE PKA
# ===================
def pKaRes(selection1, value=None):
  command='pKaRes '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# PLAY BACK MACRO
# ===============
def PlayMacro(filename, label, onstartup=None):
  command='PlayMacro '
  command+='Filename='+cstr(filename)+','
  command+='Label='+cstr(label)+','
  if (onstartup!=None): command+='OnStartup='+cstr(onstartup)+','
  run(command[:-1])

# SET STYLE OF MOUSE POINTER
# ==========================
def PointerStyle(Type=None, software=None):
  command='PointerStyle '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (software!=None): command+='Software='+cstr(software)+','
  run(command[:-1])

# SET POINT AND LINE RADIUS AND PLASTICITY IN WIRE FRAMES
# =======================================================
def PointPar(radius=None, plastic=None):
  command='PointPar '
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (plastic!=None): command+='plastic='+cstr(plastic)+','
  run(command[:-1])

# SET/GET POLYGON SMOOTHNESS AND REFLECTIVITY
# ===========================================
def PolygonPar(smoothness=None, reflection=None):
  command='PolygonPar '
  if (smoothness!=None): command+='Smoothness='+cstr(smoothness)+','
  if (reflection!=None): command+='Reflection='+cstr(reflection)+','
  return(run(command[:-1]))

# POLYMERIZE OBJECTS
# ==================
def Polymerize(selection1, selection2, copies=None, dihedral=None):
  command='Polymerize '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (copies!=None): command+='Copies='+cstr(copies)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  run(command[:-1])

# POSITION AND JUSTIFY TEXT
# =========================
def PosText(x=None, y=None, justify=None):
  command='PosText '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (justify!=None): command+='justify='+cstr(justify)+','
  run(command[:-1])

# SET/GET ATOM POSITIONS (MOLECULE)
# =================================
def PosMol(selection1, x=None, y=None, z=None, coordsys=None, mean=None):
  command='PosMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  if (mean!=None): command+='Mean='+cstr(mean)+','
  return(run(command[:-1]))

# SET/GET ATOM POSITIONS (RESIDUE)
# ================================
def PosRes(selection1, x=None, y=None, z=None, coordsys=None, mean=None):
  command='PosRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  if (mean!=None): command+='Mean='+cstr(mean)+','
  return(run(command[:-1]))

# SET/GET ATOM POSITIONS (ATOM)
# =============================
def PosAtom(selection1, x=None, y=None, z=None, coordsys=None, mean=None):
  command='PosAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (coordsys!=None): command+='CoordSys='+cstr(coordsys)+','
  if (mean!=None): command+='Mean='+cstr(mean)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION AND ORIENTATION (ALL OR SELECTED)
# ==================================================================
def PosOri(x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
  command='PosOri '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION AND ORIENTATION (ALL)
# ======================================================
def PosOriAll(x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
  command='PosOriAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION AND ORIENTATION (OBJECT)
# =========================================================
def PosOriObj(selection1, x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
  command='PosOriObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION (ALL OR SELECTED)
# ==================================================
def Pos(x=None, y=None, z=None):
  command='Pos '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION (ALL)
# ======================================
def PosAll(x=None, y=None, z=None):
  command='PosAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET OBJECT OR SCENE POSITION (OBJECT)
# =========================================
def PosObj(selection1, x=None, y=None, z=None):
  command='PosObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# PREDICT SECONDARY STRUCTURE (ALL OR SELECTED)
# =============================================
def PredSecStr(method=None):
  command='PredSecStr '
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# PREDICT SECONDARY STRUCTURE (ALL)
# =================================
def PredSecStrAll(method=None):
  command='PredSecStrAll '
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# PREDICT SECONDARY STRUCTURE (OBJECT)
# ====================================
def PredSecStrObj(selection1, method=None):
  command='PredSecStrObj '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# PREDICT SECONDARY STRUCTURE (MOLECULE)
# ======================================
def PredSecStrMol(selection1, method=None):
  command='PredSecStrMol '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# PREDICT SECONDARY STRUCTURE (RESIDUE)
# =====================================
def PredSecStrRes(selection1, method=None):
  command='PredSecStrRes '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# SET PRESSURE CONTROL
# ====================
def PressureCtrl(Type, pressure=None, name=None, density=None, axis=None):
  command='PressureCtrl '
  command+='Type='+cstr(Type)+','
  if (pressure!=None): command+='Pressure='+cstr(pressure)+','
  if (name!=None): command+='Name='+cstr(name)+','
  if (density!=None): command+='Density='+cstr(density)+','
  if (axis!=None): command+='Axis='+cstr(axis)+','
  run(command[:-1])

# PRINT TEXT
# ==========
def Print(text, convert=None):
  command='Print '
  command+='Text='+cstr(text,1)+','
  if (convert!=None): command+='Convert='+cstr(convert)+','
  run(command[:-1])

# PRINT TO CONSOLE
# ================
def PrintCon():
  command='PrintCon '
  run(command[:-1])

# PRINT TO HEAD-UP DISPLAY
# ========================
def PrintHUD():
  command='PrintHUD '
  run(command[:-1])

# PRINT TO IMAGE
# ==============
def PrintImage(selection1):
  command='PrintImage '
  command+=selstr(selection1)+','
  run(command[:-1])

# PRINT TO TEXT OBJECT
# ====================
def PrintObj(selection1):
  command='PrintObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# PRINT TO SECONDARY WINDOW
# =========================
def PrintWin():
  command='PrintWin '
  run(command[:-1])

# SET/GET NUMBER OF PROCESSORS TO USE
# ===================================
def Processors(cputhreads=None, gpu=None, bindthreads=None):
  command='Processors '
  if (cputhreads!=None): command+='CPUThreads='+cstr(cputhreads)+','
  if (gpu!=None): command+='GPU='+cstr(gpu)+','
  if (bindthreads!=None): command+='BindThreads='+cstr(bindthreads)+','
  return(run(command[:-1]))

# SET PERSPECTIVE OR PARALLEL PROJECTION
# ======================================
def Projection(Type):
  command='Projection '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SET/GET THE PROPERTY VALUE (ALL OR SELECTED)
# ============================================
def Prop(value=None):
  command='Prop '
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE PROPERTY VALUE (ALL)
# ================================
def PropAll(value=None):
  command='PropAll '
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE PROPERTY VALUE (OBJECT)
# ===================================
def PropObj(selection1, value=None):
  command='PropObj '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE PROPERTY VALUE (MOLECULE)
# =====================================
def PropMol(selection1, value=None):
  command='PropMol '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE PROPERTY VALUE (RESIDUE)
# ====================================
def PropRes(selection1, value=None):
  command='PropRes '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET THE PROPERTY VALUE (ATOM)
# =================================
def PropAtom(selection1, value=None):
  command='PropAtom '
  command+=selstr(selection1)+','
  if (value!=None): command+='value='+cstr(value)+','
  return(run(command[:-1]))

# PRINT WORKING DIRECTORY
# =======================
def PWD():
  command='PWD '
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET QUANTUM MECHANICS METHOD
# ============================
def QuantumMechanics(method):
  command='QuantumMechanics '
  command+='Method='+cstr(method)+','
  run(command[:-1])

# CALCULATE THE RADIUS (ALL OR SELECTED)
# ======================================
def Radius(center=None, Type=None):
  command='Radius '
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE THE RADIUS (ALL)
# ==========================
def RadiusAll(center=None, Type=None):
  command='RadiusAll '
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE THE RADIUS (OBJECT)
# =============================
def RadiusObj(selection1, center=None, Type=None):
  command='RadiusObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE THE RADIUS (MOLECULE)
# ===============================
def RadiusMol(selection1, center=None, Type=None):
  command='RadiusMol '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE THE RADIUS (RESIDUE)
# ==============================
def RadiusRes(selection1, center=None, Type=None):
  command='RadiusRes '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE THE RADIUS (ATOM)
# ===========================
def RadiusAtom(selection1, center=None, Type=None):
  command='RadiusAtom '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# DISPLAY ERROR MESSAGE
# =====================
def RaiseError(text=None):
  command='RaiseError '
  if (text!=None): command+='Text='+cstr(text,1)+','
  run(command[:-1])

# SET RANDOM NUMBER SEED
# ======================
def RandomSeed(number):
  command='RandomSeed '
  command+='Number='+cstr(number)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CREATE RAYTRACED SCREENSHOT USING POVRAY
# ========================================
def RayTrace(filename, x=None, y=None, zoom=None, atoms=None, labelshadow=None, secalpha=None, display=None, outline=None, background=None):
  command='RayTrace '
  command+='Filename='+cstr(filename)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (zoom!=None): command+='zoom='+cstr(zoom)+','
  if (atoms!=None): command+='Atoms='+cstr(atoms)+','
  if (labelshadow!=None): command+='LabelShadow='+cstr(labelshadow)+','
  if (secalpha!=None): command+='SecAlpha='+cstr(secalpha)+','
  if (display!=None): command+='Display='+cstr(display)+','
  if (outline!=None): command+='Outline='+cstr(outline)+','
  if (background!=None): command+='Background='+cstr(background)+','
  run(command[:-1])

# CALCULATE RADIAL DISTRIBUTION FUNCTION
# ======================================
def RDF(normbins=None):
  command='RDF '
  if (normbins!=None): command+='NormBins='+cstr(normbins)+','
  return(run(command[:-1]))

# RECORD ALL CONSOLE OUTPUT IN A LOG FILE
# =======================================
def RecordLog(filename, append=None):
  command='RecordLog '
  command+='Filename='+cstr(filename)+','
  if (append!=None): command+='append='+cstr(append)+','
  run(command[:-1])

# REGULARIZE COVALENT GEOMETRY (ALL OR SELECTED)
# ==============================================
def Regularize(sigmas=None):
  command='Regularize '
  if (sigmas!=None): command+='Sigmas='+cstr(sigmas)+','
  run(command[:-1])

# REGULARIZE COVALENT GEOMETRY (ALL)
# ==================================
def RegularizeAll(sigmas=None):
  command='RegularizeAll '
  if (sigmas!=None): command+='Sigmas='+cstr(sigmas)+','
  run(command[:-1])

# REGULARIZE COVALENT GEOMETRY (OBJECT)
# =====================================
def RegularizeObj(selection1, sigmas=None):
  command='RegularizeObj '
  command+=selstr(selection1)+','
  if (sigmas!=None): command+='Sigmas='+cstr(sigmas)+','
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (ALL OR SELECTED)
# ==================================================================
def RemoveEnv():
  command='RemoveEnv '
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (ALL)
# ======================================================
def RemoveEnvAll():
  command='RemoveEnvAll '
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (OBJECT)
# =========================================================
def RemoveEnvObj(selection1):
  command='RemoveEnvObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (MOLECULE)
# ===========================================================
def RemoveEnvMol(selection1):
  command='RemoveEnvMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (RESIDUE)
# ==========================================================
def RemoveEnvRes(selection1):
  command='RemoveEnvRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# REMOVE FROM ENVIRONMENT FOR SURFACE CALCULATIONS (ATOM)
# =======================================================
def RemoveEnvAtom(selection1):
  command='RemoveEnvAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# RECREATE A POLYGON MESH WITH MOSTLY EQUILATERAL TRIANGLES
# =========================================================
def ReMesh(selection1, len=None):
  command='ReMesh '
  command+=selstr(selection1)+','
  if (len!=None): command+='Len='+cstr(len)+','
  run(command[:-1])

# REMOVE OBJECTS FROM THE SOUP (ALL OR SELECTED)
# ==============================================
def Remove():
  command='Remove '
  run(command[:-1])

# REMOVE OBJECTS FROM THE SOUP (ALL)
# ==================================
def RemoveAll():
  command='RemoveAll '
  run(command[:-1])

# REMOVE OBJECTS FROM THE SOUP (OBJECT)
# =====================================
def RemoveObj(selection1):
  command='RemoveObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# SET/GET RENDERING LIBRARY AND GPU
# =================================
def Renderer(library=None, gpu=None):
  command='Renderer '
  if (library!=None): command+='Library='+cstr(library)+','
  if (gpu!=None): command+='GPU='+cstr(gpu)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# NUMBER OBJECTS (ALL OR SELECTED)
# ================================
def Number(first=None):
  command='Number '
  if (first!=None): command+='first='+cstr(first)+','
  run(command[:-1])

# NUMBER OBJECTS (ALL)
# ====================
def NumberAll(first=None):
  command='NumberAll '
  if (first!=None): command+='first='+cstr(first)+','
  run(command[:-1])

# NUMBER OBJECTS (OBJECT)
# =======================
def NumberObj(selection1, first=None):
  command='NumberObj '
  command+=selstr(selection1)+','
  if (first!=None): command+='first='+cstr(first)+','
  run(command[:-1])

# NUMBER RESIDUES
# ===============
def NumberRes(selection1, first=None, inscode=None, increment=None):
  command='NumberRes '
  command+=selstr(selection1)+','
  if (first!=None): command+='First='+cstr(first)+','
  if (inscode!=None): command+='InsCode='+cstr(inscode)+','
  if (increment!=None): command+='Increment='+cstr(increment)+','
  run(command[:-1])

# NUMBER ATOMS
# ============
def NumberAtom(selection1, first=None):
  command='NumberAtom '
  command+=selstr(selection1)+','
  if (first!=None): command+='First='+cstr(first)+','
  run(command[:-1])

# SET/GET KEY-VALUE PAIRS OF OBJECT (ALL OR SELECTED)
# ===================================================
def Pair(key=None, value=None):
  command='Pair '
  if (key!=None): command+='Key='+cstr(key)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET KEY-VALUE PAIRS OF OBJECT (ALL)
# =======================================
def PairAll(key=None, value=None):
  command='PairAll '
  if (key!=None): command+='Key='+cstr(key)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET KEY-VALUE PAIRS OF OBJECT (OBJECT)
# ==========================================
def PairObj(selection1, key=None, value=None):
  command='PairObj '
  command+=selstr(selection1)+','
  if (key!=None): command+='Key='+cstr(key)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# REPLACE RESIDUES
# ================
def ReplaceRes(selection1, selection2, superpose=None, addbonds=None, renumberres=None, renamemol=None):
  command='ReplaceRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (superpose!=None): command+='Superpose='+cstr(superpose)+','
  if (addbonds!=None): command+='AddBonds='+cstr(addbonds)+','
  if (renumberres!=None): command+='RenumberRes='+cstr(renumberres)+','
  if (renamemol!=None): command+='RenameMol='+cstr(renamemol)+','
  run(command[:-1])

# SET/GET OBJECT X-RAY RESOLUTION (ALL OR SELECTED)
# =================================================
def Resolution(value=None):
  command='Resolution '
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET OBJECT X-RAY RESOLUTION (ALL)
# =====================================
def ResolutionAll(value=None):
  command='ResolutionAll '
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# SET/GET OBJECT X-RAY RESOLUTION (OBJECT)
# ========================================
def ResolutionObj(selection1, value=None):
  command='ResolutionObj '
  command+=selstr(selection1)+','
  if (value!=None): command+='Value='+cstr(value)+','
  return(run(command[:-1]))

# INTRODUCE FRACTIONAL BOND ORDERS
# ================================
def ResonateBond(selection1, selection2):
  command='ResonateBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# CALCULATE RESTRAINT ENERGIES (ALL OR SELECTED)
# ==============================================
def RestEnergy(component=None):
  command='RestEnergy '
  if (component!=None): command+='Component='+cstr(component)+','
  return(run(command[:-1]))

# CALCULATE RESTRAINT ENERGIES (ALL)
# ==================================
def RestEnergyAll(component=None):
  command='RestEnergyAll '
  if (component!=None): command+='Component='+cstr(component)+','
  return(run(command[:-1]))

# CALCULATE RESTRAINT ENERGIES (OBJECT)
# =====================================
def RestEnergyObj(selection1, component=None):
  command='RestEnergyObj '
  command+=selstr(selection1)+','
  if (component!=None): command+='Component='+cstr(component)+','
  return(run(command[:-1]))

# GET RESTRAINT VIOLATION STATISTICS (ALL OR SELECTED)
# ====================================================
def RestViol():
  command='RestViol '
  return(run(command[:-1]))

# GET RESTRAINT VIOLATION STATISTICS (ALL)
# ========================================
def RestViolAll():
  command='RestViolAll '
  return(run(command[:-1]))

# GET RESTRAINT VIOLATION STATISTICS (OBJECT)
# ===========================================
def RestViolObj(selection1):
  command='RestViolObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# RESTRAIN DISTANCE
# =================
def RestrainDis(selection1, selection2, Class, d, dminus, dplus):
  command='RestrainDis '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Class='+cstr(Class)+','
  command+='d='+cstr(d)+','
  command+='dminus='+cstr(dminus)+','
  command+='dplus='+cstr(dplus)+','
  run(command[:-1])

# RESTRAIN DIHEDRAL ANGLE
# =======================
def RestrainDih(selection1, selection2, selection3, selection4, Class, c, equil, delta, exponent=None):
  command='RestrainDih '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  command+='Class='+cstr(Class)+','
  command+='C='+cstr(c)+','
  command+='Equil='+cstr(equil)+','
  command+='Delta='+cstr(delta)+','
  if (exponent!=None): command+='Exponent='+cstr(exponent)+','
  run(command[:-1])

# SET/GET RESTRAINING PARAMETERS
# ==============================
def RestrainPar(average=None, ceil=None, dismin=None, monomers=None, joindis=None, floatgroups=None, showamb=None, periodic=None):
  command='RestrainPar '
  if (average!=None): command+='Average='+cstr(average)+','
  if (ceil!=None): command+='Ceil='+cstr(ceil)+','
  if (dismin!=None): command+='DisMin='+cstr(dismin)+','
  if (monomers!=None): command+='Monomers='+cstr(monomers)+','
  if (joindis!=None): command+='JoinDis='+cstr(joindis)+','
  if (floatgroups!=None): command+='FloatGroups='+cstr(floatgroups)+','
  if (showamb!=None): command+='ShowAmb='+cstr(showamb)+','
  if (periodic!=None): command+='Periodic='+cstr(periodic)+','
  return(run(command[:-1]))

# SET/GET RESTRAINING POTENTIAL FUNCTIONS
# =======================================
def RestrainPot(name=None, sqconstant=None, sqoffset=None, sqexponent=None, rswitch=None, soexponent=None, asymptote=None, gamma=None, rdcforceconst=None, rdcerrorscale=None, update=None):
  command='RestrainPot '
  if (name!=None): command+='Name='+cstr(name)+','
  if (sqconstant!=None): command+='SqConstant='+cstr(sqconstant)+','
  if (sqoffset!=None): command+='SqOffset='+cstr(sqoffset)+','
  if (sqexponent!=None): command+='SqExponent='+cstr(sqexponent)+','
  if (rswitch!=None): command+='rSwitch='+cstr(rswitch)+','
  if (soexponent!=None): command+='SoExponent='+cstr(soexponent)+','
  if (asymptote!=None): command+='Asymptote='+cstr(asymptote)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  if (rdcforceconst!=None): command+='RDCForceConst='+cstr(rdcforceconst)+','
  if (rdcerrorscale!=None): command+='RDCErrorScale='+cstr(rdcerrorscale)+','
  if (update!=None): command+='Update='+cstr(update)+','
  return(run(command[:-1]))

# CALCULATE ROOT MEAN SQUARE FLUCTUATIONS AND B-FACTORS (MOLECULE)
# ================================================================
def RMSFMol(selection1, unit=None):
  command='RMSFMol '
  command+=selstr(selection1)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ROOT MEAN SQUARE FLUCTUATIONS AND B-FACTORS (RESIDUE)
# ===============================================================
def RMSFRes(selection1, unit=None):
  command='RMSFRes '
  command+=selstr(selection1)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ROOT MEAN SQUARE FLUCTUATIONS AND B-FACTORS (ATOM)
# ============================================================
def RMSFAtom(selection1, unit=None):
  command='RMSFAtom '
  command+=selstr(selection1)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE RMSDS (OBJECT)
# ========================
def RMSDObj(selection1, selection2, match=None, flip=None, unit=None):
  command='RMSDObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE RMSDS (MOLECULE)
# ==========================
def RMSDMol(selection1, selection2, match=None, flip=None, unit=None):
  command='RMSDMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE RMSDS (RESIDUE)
# =========================
def RMSDRes(selection1, selection2, match=None, flip=None, unit=None):
  command='RMSDRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE RMSDS (ATOM)
# ======================
def RMSDAtom(selection1, selection2, match=None, flip=None, unit=None):
  command='RMSDAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# ROTATE ATOMS, OBJECTS OR THE SCENE (ALL OR SELECTED)
# ====================================================
def Rotate(x=None, y=None, z=None):
  command='Rotate '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS, OBJECTS OR THE SCENE (ALL)
# ========================================
def RotateAll(x=None, y=None, z=None):
  command='RotateAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS, OBJECTS OR THE SCENE (OBJECT)
# ===========================================
def RotateObj(selection1, x=None, y=None, z=None):
  command='RotateObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS, OBJECTS OR THE SCENE (MOLECULE)
# =============================================
def RotateMol(selection1, x=None, y=None, z=None):
  command='RotateMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS, OBJECTS OR THE SCENE (RESIDUE)
# ============================================
def RotateRes(selection1, x=None, y=None, z=None):
  command='RotateRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS, OBJECTS OR THE SCENE (ATOM)
# =========================================
def RotateAtom(selection1, x=None, y=None, z=None):
  command='RotateAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (ALL OR SELECTED)
# =====================================================
def RotAxis(px, py, pz, dx, dy, dz, angle):
  command='RotAxis '
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (ALL)
# =========================================
def RotAxisAll(px, py, pz, dx, dy, dz, angle):
  command='RotAxisAll '
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (OBJECT)
# ============================================
def RotAxisObj(selection1, px, py, pz, dx, dy, dz, angle):
  command='RotAxisObj '
  command+=selstr(selection1)+','
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (MOLECULE)
# ==============================================
def RotAxisMol(selection1, px, py, pz, dx, dy, dz, angle):
  command='RotAxisMol '
  command+=selstr(selection1)+','
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (RESIDUE)
# =============================================
def RotAxisRes(selection1, px, py, pz, dx, dy, dz, angle):
  command='RotAxisRes '
  command+=selstr(selection1)+','
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# ROTATE ATOMS ABOUT A SPECIFIED AXIS (ATOM)
# ==========================================
def RotAxisAtom(selection1, px, py, pz, dx, dy, dz, angle):
  command='RotAxisAtom '
  command+=selstr(selection1)+','
  command+='PX='+cstr(px)+','
  command+='PY='+cstr(py)+','
  command+='PZ='+cstr(pz)+','
  command+='DX='+cstr(dx)+','
  command+='DY='+cstr(dy)+','
  command+='DZ='+cstr(dz)+','
  command+='Angle='+cstr(angle)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (ALL OR SELECTED)
# ==================================================
def RunMOPAC(keywords):
  command='RunMOPAC '
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (ALL)
# ======================================
def RunMOPACAll(keywords):
  command='RunMOPACAll '
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (OBJECT)
# =========================================
def RunMOPACObj(selection1, keywords):
  command='RunMOPACObj '
  command+=selstr(selection1)+','
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (MOLECULE)
# ===========================================
def RunMOPACMol(selection1, keywords):
  command='RunMOPACMol '
  command+=selstr(selection1)+','
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (RESIDUE)
# ==========================================
def RunMOPACRes(selection1, keywords):
  command='RunMOPACRes '
  command+=selstr(selection1)+','
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# RUN MOPAC FOR CUSTOM CALCULATION (ATOM)
# =======================================
def RunMOPACAtom(selection1, keywords):
  command='RunMOPACAtom '
  command+=selstr(selection1)+','
  command+='Keywords='+cstr(keywords)+','
  run(command[:-1])

# SAMPLE DIHEDRAL ANGLES
# ======================
def SampleDih(selection1, method=None, structures=None, dihedrals=None, bumpsum=None, scaffold=None, devmax=None, devbins=None):
  command='SampleDih '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  if (dihedrals!=None): command+='Dihedrals='+cstr(dihedrals)+','
  if (bumpsum!=None): command+='Bumpsum='+cstr(bumpsum)+','
  if (scaffold!=None): command+='Scaffold='+cstr(scaffold)+','
  if (devmax!=None): command+='DevMax='+cstr(devmax)+','
  if (devbins!=None): command+='DevBins='+cstr(devbins)+','
  return(run(command[:-1]))

# SAMPLE CENTRAL OR TERMINAL LOOP
# ===============================
def SampleLoop(selection1, selection2, structures=None, bumpsum=None, secstr=None, bridgecys=None):
  command='SampleLoop '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  if (bumpsum!=None): command+='Bumpsum='+cstr(bumpsum)+','
  if (secstr!=None): command+='SecStr='+cstr(secstr)+','
  if (bridgecys!=None): command+='BridgeCys='+cstr(bridgecys)+','
  return(run(command[:-1]))

# SAVE ALIGNMENT BETWEEN OBJECTS
# ==============================
def SaveAli(selection1, selection2, method=None, filename=None, format=None):
  command='SaveAli '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (filename!=None): command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  return(run(command[:-1]))

# SAVE SCREENSHOT AS UNCOMPRESSED WINDOWS BITMAP
# ==============================================
def SaveBmp(filename, menu=None, depthmap=None):
  command='SaveBmp '
  command+='Filename='+cstr(filename)+','
  if (menu!=None): command+='Menu='+cstr(menu)+','
  if (depthmap!=None): command+='DepthMap='+cstr(depthmap)+','
  run(command[:-1])

# SAVE CIF OR MMCIF FILE
# ======================
def SaveCIF(selection1, filename, format=None, transform=None):
  command='SaveCIF '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (transform!=None): command+='Transform='+cstr(transform)+','
  run(command[:-1])

# SAVE ELECTROSTATIC POTENTIAL MAP
# ================================
def SaveESP(filename, method=None, format=None):
  command='SaveESP '
  command+='Filename='+cstr(filename)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (format!=None): command+='Format='+cstr(format)+','
  run(command[:-1])

# SAVE A MACRO TO RESTORE THE CURRENT STATE
# =========================================
def SaveMacro(filename, component):
  command='SaveMacro '
  command+='Filename='+cstr(filename)+','
  command+='Component='+cstr(component)+','
  run(command[:-1])

# SAVE SIMULATION SNAPSHOTS IN MDCRD FORMAT
# =========================================
def SaveMDCrd(filename, steps=None, selection1=None):
  command='SaveMDCrd '
  if (type(filename)==type('') and filename.lower()=='off'): command+=' off,'
  else:
    command+='Filename='+cstr(filename)+','
    if (steps!=None): command+='Steps='+cstr(steps)+','
    if (selection1!=None): command+=selstr(selection1)+','
  run(command[:-1])

# SAVE MPEG4 VIDEO
# ================
def SaveMPG(filename, x=None, y=None, fps=None, quality=None, skip=None, raytrace=None, menu=None, justmacro=None, frames=None):
  command='SaveMPG '
  if (type(filename)==type('') and filename.lower()=='off'): command+=' off,'
  else:
    command+='Filename='+cstr(filename)+','
    if (x!=None): command+='X='+cstr(x)+','
    if (y!=None): command+='Y='+cstr(y)+','
    if (fps!=None): command+='FPS='+cstr(fps)+','
    if (quality!=None): command+='Quality='+cstr(quality)+','
    if (skip!=None): command+='Skip='+cstr(skip)+','
    if (raytrace!=None): command+='RayTrace='+cstr(raytrace)+','
    if (menu!=None): command+='Menu='+cstr(menu)+','
    if (justmacro!=None): command+='justMacro='+cstr(justmacro)+','
    if (frames!=None): command+='Frames='+cstr(frames)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SAVE DISTANCE, DIHEDRAL AND RDC RESTRAINTS IN NMR EXCHANGE FORMAT
# =================================================================
def SaveNEF(selection1, filename, component=None):
  command='SaveNEF '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (component!=None): command+='Component='+cstr(component)+','
  run(command[:-1])

# SAVE PROTEIN DATA BANK FILE
# ===========================
def SavePDB(selection1, filename, format=None, transform=None, usecif=None, bondorders=None):
  command='SavePDB '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (format!=None): command+='Format='+cstr(format)+','
  if (transform!=None): command+='Transform='+cstr(transform)+','
  if (usecif!=None): command+='UseCIF='+cstr(usecif)+','
  if (bondorders!=None): command+='BondOrders='+cstr(bondorders)+','
  run(command[:-1])

# SAVE PLOT
# =========
def SavePlot(filename, selection1, width, height, title, Type, xcolumn, ycolumn, ycolumns, xlabel, ylabel, legendpos, graphname, *arglist2):
  command='SavePlot '
  command+='Filename='+cstr(filename)+','
  command+=selstr(selection1)+','
  command+='Width='+cstr(width)+','
  command+='Height='+cstr(height)+','
  command+='Title='+cstr(title)+','
  command+='Type='+cstr(Type)+','
  command+='XColumn='+cstr(xcolumn)+','
  command+='YColumn='+cstr(ycolumn)+','
  command+='YColumns='+cstr(ycolumns)+','
  command+='XLabel='+cstr(xlabel)+','
  command+='YLabel='+cstr(ylabel)+','
  command+='LegendPos='+cstr(legendpos)+','
  command+='Graphname='+cstr(graphname)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  run(command[:-1])

# SAVE SCREENSHOT AS COMPRESSED PNG BITMAP
# ========================================
def SavePNG(filename, menu=None, depthmap=None):
  command='SavePNG '
  command+='Filename='+cstr(filename)+','
  if (menu!=None): command+='Menu='+cstr(menu)+','
  if (depthmap!=None): command+='DepthMap='+cstr(depthmap)+','
  run(command[:-1])

# SAVE POVRAY SCENE DESCRIPTION
# =============================
def SavePOV(filename, zoom=None, atoms=None, labelshadow=None, secalpha=None, background=None):
  command='SavePOV '
  command+='Filename='+cstr(filename)+','
  if (zoom!=None): command+='Zoom='+cstr(zoom)+','
  if (atoms!=None): command+='Atoms='+cstr(atoms)+','
  if (labelshadow!=None): command+='LabelShadow='+cstr(labelshadow)+','
  if (secalpha!=None): command+='SecAlpha='+cstr(secalpha)+','
  if (background!=None): command+='Background='+cstr(background)+','
  run(command[:-1])

# SAVE AMBER PREP TOPOLOGY (ALL OR SELECTED)
# ==========================================
def SavePrep(filename, hydnumbers=None, reorder=None, propcharges=None):
  command='SavePrep '
  command+='Filename='+cstr(filename)+','
  if (hydnumbers!=None): command+='HydNumbers='+cstr(hydnumbers)+','
  if (reorder!=None): command+='Reorder='+cstr(reorder)+','
  if (propcharges!=None): command+='PropCharges='+cstr(propcharges)+','
  run(command[:-1])

# SAVE AMBER PREP TOPOLOGY (ALL)
# ==============================
def SavePrepAll(filename, hydnumbers=None, reorder=None, propcharges=None):
  command='SavePrepAll '
  command+='Filename='+cstr(filename)+','
  if (hydnumbers!=None): command+='HydNumbers='+cstr(hydnumbers)+','
  if (reorder!=None): command+='Reorder='+cstr(reorder)+','
  if (propcharges!=None): command+='PropCharges='+cstr(propcharges)+','
  run(command[:-1])

# SAVE AMBER PREP TOPOLOGY (OBJECT)
# =================================
def SavePrepObj(selection1, filename, hydnumbers=None, reorder=None, propcharges=None):
  command='SavePrepObj '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (hydnumbers!=None): command+='HydNumbers='+cstr(hydnumbers)+','
  if (reorder!=None): command+='Reorder='+cstr(reorder)+','
  if (propcharges!=None): command+='PropCharges='+cstr(propcharges)+','
  run(command[:-1])

# SAVE AMBER PREP TOPOLOGY (MOLECULE)
# ===================================
def SavePrepMol(selection1, filename, hydnumbers=None, reorder=None, propcharges=None):
  command='SavePrepMol '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (hydnumbers!=None): command+='HydNumbers='+cstr(hydnumbers)+','
  if (reorder!=None): command+='Reorder='+cstr(reorder)+','
  if (propcharges!=None): command+='PropCharges='+cstr(propcharges)+','
  run(command[:-1])

# SAVE AMBER PREP TOPOLOGY (RESIDUE)
# ==================================
def SavePrepRes(selection1, filename, hydnumbers=None, reorder=None, propcharges=None):
  command='SavePrepRes '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (hydnumbers!=None): command+='HydNumbers='+cstr(hydnumbers)+','
  if (reorder!=None): command+='Reorder='+cstr(reorder)+','
  if (propcharges!=None): command+='PropCharges='+cstr(propcharges)+','
  run(command[:-1])

# SAVE COMPLETE SCENE
# ===================
def SaveSce(filename):
  command='SaveSce '
  command+='Filename='+cstr(filename)+','
  run(command[:-1])

# SAVE RESIDUE SEQUENCE (OBJECT)
# ==============================
def SaveSeqObj(selection1, filename, join=None):
  command='SaveSeqObj '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (join!=None): command+='Join='+cstr(join)+','
  run(command[:-1])

# SAVE RESIDUE SEQUENCE (MOLECULE)
# ================================
def SaveSeqMol(selection1, filename, join=None):
  command='SaveSeqMol '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (join!=None): command+='Join='+cstr(join)+','
  run(command[:-1])

# SAVE RESIDUE SEQUENCE (RESIDUE)
# ===============================
def SaveSeqRes(selection1, filename, join=None):
  command='SaveSeqRes '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (join!=None): command+='Join='+cstr(join)+','
  run(command[:-1])

# SAVE SIMULATION SNAPSHOTS IN SIM FORMAT
# =======================================
def SaveSim(filename, steps=None, number=None):
  command='SaveSim '
  if (type(filename)==type('') and filename.lower()=='off'): command+=' off,'
  else:
    command+='Filename='+cstr(filename)+','
    if (steps!=None): command+='Steps='+cstr(steps)+','
    if (number!=None): command+='Number='+cstr(number)+','
  run(command[:-1])

# SAVE FORMATTED TABLE
# ====================
def SaveTab(selection1, filename, format, columns, numformat, header):
  command='SaveTab '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  command+='Format='+cstr(format)+','
  command+='Columns='+cstr(columns)+','
  command+='NumFormat='+cstr(numformat)+','
  command+='Header='+cstr(header)+','
  run(command[:-1])

# SAVE DISTANCE, DIHEDRAL AND RDC RESTRAINTS IN XPLOR FORMAT
# ==========================================================
def SaveTbl(selection1, filename, component=None, nameformat=None):
  command='SaveTbl '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (component!=None): command+='Component='+cstr(component)+','
  if (nameformat!=None): command+='NameFormat='+cstr(nameformat)+','
  run(command[:-1])

# SAVE ALIAS/WAVEFRONT OBJECT
# ===========================
def SaveWOb(selection1, filename, interpolcol=None, level=None, ballzoom=None):
  command='SaveWOb '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (interpolcol!=None): command+='InterpolCol='+cstr(interpolcol)+','
  if (level!=None): command+='Level='+cstr(level)+','
  if (ballzoom!=None): command+='BallZoom='+cstr(ballzoom)+','
  run(command[:-1])

# SAVE SIMULATION SNAPSHOTS IN XTC FORMAT
# =======================================
def SaveXTC(filename, steps=None, selection1=None):
  command='SaveXTC '
  if (type(filename)==type('') and filename.lower()=='off'): command+=' off,'
  else:
    command+='Filename='+cstr(filename)+','
    if (steps!=None): command+='Steps='+cstr(steps)+','
    if (selection1!=None): command+=selstr(selection1)+','
  run(command[:-1])

# SAVE YASARA OBJECT
# ==================
def SaveYOb(selection1, filename, transform=None):
  command='SaveYOb '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (transform!=None): command+='Transform='+cstr(transform)+','
  run(command[:-1])

# EXPORT FILE WITH OPENBABEL
# ==========================
def Save(format, selection1, filename, nameformat=None, transform=None, dativebonds=None):
  command='Save '
  command=command[:-1]+cstr(format)+' '
  command+=selstr(selection1)+','
  command+='Filename='+cstr(filename)+','
  if (nameformat!=None): command+='NameFormat='+cstr(nameformat)+','
  if (transform!=None): command+='Transform='+cstr(transform)+','
  if (dativebonds!=None): command+='DativeBonds='+cstr(dativebonds)+','
  run(command[:-1])

# SET/GET FORCE SCALING FACTORS
# =============================
def ScaleForce(component=None, factor=None):
  command='ScaleForce '
  if (component!=None): command+='Component='+cstr(component)+','
  if (factor!=None): command+='Factor='+cstr(factor)+','
  return(run(command[:-1]))

# SCALE RESTRAINTS (ALL OR SELECTED)
# ==================================
def ScaleRest(Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRest '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE RESTRAINTS (ALL)
# ======================
def ScaleRestAll(Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRestAll '
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE RESTRAINTS (OBJECT)
# =========================
def ScaleRestObj(selection1, Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRestObj '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE RESTRAINTS (MOLECULE)
# ===========================
def ScaleRestMol(selection1, Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRestMol '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE RESTRAINTS (RESIDUE)
# ==========================
def ScaleRestRes(selection1, Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRestRes '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE RESTRAINTS (ATOM)
# =======================
def ScaleRestAtom(selection1, Class=None, distance=None, dihedral=None, rdc=None):
  command='ScaleRestAtom '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  if (distance!=None): command+='Distance='+cstr(distance)+','
  if (dihedral!=None): command+='Dihedral='+cstr(dihedral)+','
  if (rdc!=None): command+='RDC='+cstr(rdc)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (ALL OR SELECTED)
# =========================================================
def Scale(x=None, y=None, z=None):
  command='Scale '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (ALL)
# =============================================
def ScaleAll(x=None, y=None, z=None):
  command='ScaleAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (OBJECT)
# ================================================
def ScaleObj(selection1, x=None, y=None, z=None):
  command='ScaleObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (MOLECULE)
# ==================================================
def ScaleMol(selection1, x=None, y=None, z=None):
  command='ScaleMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (RESIDUE)
# =================================================
def ScaleRes(selection1, x=None, y=None, z=None):
  command='ScaleRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# SCALE ATOM POSITIONS AND POLYGON MESHES (ATOM)
# ==============================================
def ScaleAtom(selection1, x=None, y=None, z=None):
  command='ScaleAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  run(command[:-1])

# FIX YASARA WINDOW ON A CERTAIN SCREEN
# =====================================
def Screen(number):
  command='Screen '
  command+='Number='+cstr(number)+','
  run(command[:-1])

# SET/GET WINDOW AND FULLSCREEN SIZE
# ==================================
def ScreenSize(x=None, y=None, scale=None):
  command='ScreenSize '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (scale!=None): command+='Scale='+cstr(scale)+','
  return(run(command[:-1]))

# SET SECONDARY STRUCTURE DISPLAY PARAMETERS
# ==========================================
def SecStrPar(strandwidth, strandheight, strandslope, arrowheight, strandperf, helixwidth, helixheight, helixslope, helixperf, helixsection, tuberadius, tubeellip, gaps, coltrans):
  command='SecStrPar '
  command+='StrandWidth='+cstr(strandwidth)+','
  command+='StrandHeight='+cstr(strandheight)+','
  command+='StrandSlope='+cstr(strandslope)+','
  command+='ArrowHeight='+cstr(arrowheight)+','
  command+='StrandPerf='+cstr(strandperf)+','
  command+='HelixWidth='+cstr(helixwidth)+','
  command+='HelixHeight='+cstr(helixheight)+','
  command+='HelixSlope='+cstr(helixslope)+','
  command+='HelixPerf='+cstr(helixperf)+','
  command+='HelixSection='+cstr(helixsection)+','
  command+='TubeRadius='+cstr(tuberadius)+','
  command+='TubeEllip='+cstr(tubeellip)+','
  command+='Gaps='+cstr(gaps)+','
  command+='ColTrans='+cstr(coltrans)+','
  run(command[:-1])

# SET/GET SECONDARY STRUCTURE (ALL OR SELECTED)
# =============================================
def SecStr(Type=None):
  command='SecStr '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET/GET SECONDARY STRUCTURE (ALL)
# =================================
def SecStrAll(Type=None):
  command='SecStrAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET/GET SECONDARY STRUCTURE (OBJECT)
# ====================================
def SecStrObj(selection1, Type=None):
  command='SecStrObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET/GET SECONDARY STRUCTURE (MOLECULE)
# ======================================
def SecStrMol(selection1, Type=None):
  command='SecStrMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET/GET SECONDARY STRUCTURE (RESIDUE)
# =====================================
def SecStrRes(selection1, Type=None):
  command='SecStrRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (ALL OR SELECTED)
# ==========================================
def Seg(name=None):
  command='Seg '
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (ALL)
# ==============================
def SegAll(name=None):
  command='SegAll '
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (OBJECT)
# =================================
def SegObj(selection1, name=None):
  command='SegObj '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (MOLECULE)
# ===================================
def SegMol(selection1, name=None):
  command='SegMol '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (RESIDUE)
# ==================================
def SegRes(selection1, name=None):
  command='SegRes '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# SET/GET THE SEGMENT NAME (ATOM)
# ===============================
def SegAtom(selection1, name=None):
  command='SegAtom '
  command+=selstr(selection1)+','
  if (name!=None): command+='Name='+cstr(name)+','
  return(run(command[:-1]))

# INTERACTIVELY SELECT ATOMS WITHIN AN ARBITRARY AREA (OBJECT)
# ============================================================
def SelectAreaObj():
  command='SelectAreaObj '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN AN ARBITRARY AREA (MOLECULE)
# ==============================================================
def SelectAreaMol():
  command='SelectAreaMol '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN AN ARBITRARY AREA (RESIDUE)
# =============================================================
def SelectAreaRes():
  command='SelectAreaRes '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN AN ARBITRARY AREA (ATOM)
# ==========================================================
def SelectAreaAtom():
  command='SelectAreaAtom '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A RECTANGULAR BOX (OBJECT)
# ============================================================
def SelectBoxObj():
  command='SelectBoxObj '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A RECTANGULAR BOX (MOLECULE)
# ==============================================================
def SelectBoxMol():
  command='SelectBoxMol '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A RECTANGULAR BOX (RESIDUE)
# =============================================================
def SelectBoxRes():
  command='SelectBoxRes '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A RECTANGULAR BOX (ATOM)
# ==========================================================
def SelectBoxAtom():
  command='SelectBoxAtom '
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A SPHERE AROUND OTHER ATOMS (OBJECT)
# ======================================================================
def SelectSphereObj(selection1):
  command='SelectSphereObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A SPHERE AROUND OTHER ATOMS (MOLECULE)
# ========================================================================
def SelectSphereMol(selection1):
  command='SelectSphereMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A SPHERE AROUND OTHER ATOMS (RESIDUE)
# =======================================================================
def SelectSphereRes(selection1):
  command='SelectSphereRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# INTERACTIVELY SELECT ATOMS WITHIN A SPHERE AROUND OTHER ATOMS (ATOM)
# ====================================================================
def SelectSphereAtom(selection1):
  command='SelectSphereAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SELECT TABLE TO ADD CELLS
# =========================
def SelectTab(selection1, column=None, row=None, page=None):
  command='SelectTab '
  command+=selstr(selection1)+','
  if (column!=None): command+='Column='+cstr(column)+','
  if (row!=None): command+='Row='+cstr(row)+','
  if (page!=None): command+='Page='+cstr(page)+','
  run(command[:-1])

# SELECT ATOMS (ALL OR SELECTED)
# ==============================
def Select(mode=None):
  command='Select '
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SELECT ATOMS (ALL)
# ==================
def SelectAll(mode=None):
  command='SelectAll '
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SELECT ATOMS (OBJECT)
# =====================
def SelectObj(selection1, mode=None):
  command='SelectObj '
  command+=selstr(selection1)+','
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SELECT ATOMS (MOLECULE)
# =======================
def SelectMol(selection1, mode=None):
  command='SelectMol '
  command+=selstr(selection1)+','
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SELECT ATOMS (RESIDUE)
# ======================
def SelectRes(selection1, mode=None):
  command='SelectRes '
  command+=selstr(selection1)+','
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SELECT ATOMS (ATOM)
# ===================
def SelectAtom(selection1, mode=None):
  command='SelectAtom '
  command+=selstr(selection1)+','
  if (mode!=None): command+='Mode='+cstr(mode)+','
  run(command[:-1])

# SWITCH SEQUENCE SELECTOR ON/OFF
# ===============================
def SeqSelector(flag):
  command='SeqSelector '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# GET RESIDUE SEQUENCE (ALL OR SELECTED)
# ======================================
def Sequence(join=None):
  command='Sequence '
  if (join!=None): command+='Join='+cstr(join)+','
  return(run(command[:-1]))

# GET RESIDUE SEQUENCE (ALL)
# ==========================
def SequenceAll(join=None):
  command='SequenceAll '
  if (join!=None): command+='Join='+cstr(join)+','
  return(run(command[:-1]))

# GET RESIDUE SEQUENCE (OBJECT)
# =============================
def SequenceObj(selection1, join=None):
  command='SequenceObj '
  command+=selstr(selection1)+','
  if (join!=None): command+='Join='+cstr(join)+','
  return(run(command[:-1]))

# GET RESIDUE SEQUENCE (MOLECULE)
# ===============================
def SequenceMol(selection1, join=None):
  command='SequenceMol '
  command+=selstr(selection1)+','
  if (join!=None): command+='Join='+cstr(join)+','
  return(run(command[:-1]))

# GET RESIDUE SEQUENCE (RESIDUE)
# ==============================
def SequenceRes(selection1, join=None):
  command='SequenceRes '
  command+=selstr(selection1)+','
  if (join!=None): command+='Join='+cstr(join)+','
  return(run(command[:-1]))

# SHIFT ATOM COLORS (ALL OR SELECTED)
# ===================================
def ShiftColor(color, shift=None):
  command='ShiftColor '
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHIFT ATOM COLORS (ALL)
# =======================
def ShiftColorAll(color, shift=None):
  command='ShiftColorAll '
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHIFT ATOM COLORS (OBJECT)
# ==========================
def ShiftColorObj(selection1, color, shift=None):
  command='ShiftColorObj '
  command+=selstr(selection1)+','
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHIFT ATOM COLORS (MOLECULE)
# ============================
def ShiftColorMol(selection1, color, shift=None):
  command='ShiftColorMol '
  command+=selstr(selection1)+','
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHIFT ATOM COLORS (RESIDUE)
# ===========================
def ShiftColorRes(selection1, color, shift=None):
  command='ShiftColorRes '
  command+=selstr(selection1)+','
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHIFT ATOM COLORS (ATOM)
# ========================
def ShiftColorAtom(selection1, color, shift=None):
  command='ShiftColorAtom '
  command+=selstr(selection1)+','
  command+='color='+cstr(color)+','
  if (shift!=None): command+='Shift='+cstr(shift)+','
  run(command[:-1])

# SHOW ARROWS BETWEEN ATOMS OR POINTS
# ===================================
def ShowArrow(start, selection1, end, selection2, radius=None, heads=None, color=None, dismax=None, visualize=None):
  command='ShowArrow '
  command+='Start='+cstr(start)+','
  command+=selstr(selection1)+','
  command+='End='+cstr(end)+','
  command+=selstr(selection2)+','
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (heads!=None): command+='Heads='+cstr(heads)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  if (visualize!=None): command+='Visualize='+cstr(visualize)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW ARROWS BETWEEN ATOMS OR POINTS
# ===================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ShowArrow2(start, x, y, z, end, x2=None, y2=None, z2=None, radius=None, heads=None, color=None):
  command='ShowArrow '
  command+='Start='+cstr(start)+','
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='End='+cstr(end)+','
  if (x2!=None): command+='X='+cstr(x2)+','
  if (y2!=None): command+='Y='+cstr(y2)+','
  if (z2!=None): command+='Z='+cstr(z2)+','
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (heads!=None): command+='Heads='+cstr(heads)+','
  if (color!=None): command+='Color='+cstr(color)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW ARROWS BETWEEN ATOMS OR POINTS
# ===================================
# THIS IS ALTERNATIVE 3, WITH DIFFERENT PARAMETERS
def ShowArrow3(start, selection1, x, y, z, end, selection2, x2=None, y2=None, z2=None, radius=None, heads=None, color=None, dismax=None):
  command='ShowArrow '
  command+='Start='+cstr(start)+','
  command+=selstr(selection1)+','
  command+='X='+cstr(x)+','
  command+='Y='+cstr(y)+','
  command+='Z='+cstr(z)+','
  command+='End='+cstr(end)+','
  command+=selstr(selection2)+','
  if (x2!=None): command+='X='+cstr(x2)+','
  if (y2!=None): command+='Y='+cstr(y2)+','
  if (z2!=None): command+='Z='+cstr(z2)+','
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (heads!=None): command+='Heads='+cstr(heads)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW ARROWS BETWEEN ATOMS OR POINTS
# ===================================
# THIS IS ALTERNATIVE 4, WITH DIFFERENT PARAMETERS
def ShowArrow4(start, selection1, dis, end, selection2, dis2=None, radius=None, heads=None, color=None, dismax=None):
  command='ShowArrow '
  command+='Start='+cstr(start)+','
  command+=selstr(selection1)+','
  command+='Dis='+cstr(dis)+','
  command+='End='+cstr(end)+','
  command+=selstr(selection2)+','
  if (dis2!=None): command+='Dis='+cstr(dis2)+','
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (heads!=None): command+='Heads='+cstr(heads)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (dismax!=None): command+='DisMax='+cstr(dismax)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW A RECTANGULAR BOX
# ======================
def ShowBox(width=None, height=None, depth=None, leftcol=None, rightcol=None, bottomcol=None, topcol=None, frontcol=None, backcol=None):
  command='ShowBox '
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (depth!=None): command+='Depth='+cstr(depth)+','
  if (leftcol!=None): command+='LeftCol='+cstr(leftcol)+','
  if (rightcol!=None): command+='RightCol='+cstr(rightcol)+','
  if (bottomcol!=None): command+='BottomCol='+cstr(bottomcol)+','
  if (topcol!=None): command+='TopCol='+cstr(topcol)+','
  if (frontcol!=None): command+='FrontCol='+cstr(frontcol)+','
  if (backcol!=None): command+='BackCol='+cstr(backcol)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW CLICKABLE BUTTON
# =====================
def ShowButton(text, x=None, y=None, width=None, height=None, border=None, color=None, action=None):
  command='ShowButton '
  command+='Text='+cstr(text,1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (border!=None): command+='Border='+cstr(border)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (action!=None): command+='Action='+cstr(action)+','
  run(command[:-1])

# SHOW CAVITIES (ALL OR SELECTED)
# ===============================
def ShowCavi(Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCavi '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CAVITIES (ALL)
# ===================
def ShowCaviAll(Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCaviAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CAVITIES (OBJECT)
# ======================
def ShowCaviObj(selection1, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCaviObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CAVITIES (MOLECULE)
# ========================
def ShowCaviMol(selection1, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCaviMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CAVITIES (RESIDUE)
# =======================
def ShowCaviRes(selection1, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCaviRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CAVITIES (ATOM)
# ====================
def ShowCaviAtom(selection1, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowCaviAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW A CONE, CYLINDER, PYRAMID OR PRISM
# =======================================
def ShowCone(bottomradius=None, topradius=None, height=None, edges=None, bottomcol=None, topcol=None, sidecol=None, alpha=None, smooth=None):
  command='ShowCone '
  if (bottomradius!=None): command+='BottomRadius='+cstr(bottomradius)+','
  if (topradius!=None): command+='TopRadius='+cstr(topradius)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (edges!=None): command+='Edges='+cstr(edges)+','
  if (bottomcol!=None): command+='BottomCol='+cstr(bottomcol)+','
  if (topcol!=None): command+='TopCol='+cstr(topcol)+','
  if (sidecol!=None): command+='SideCol='+cstr(sidecol)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (smooth!=None): command+='Smooth='+cstr(smooth)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW CONTACT SURFACE (OBJECT)
# =============================
def ShowConSurfObj(selection1, selection2, cutoff=None, subtract=None, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowConSurfObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CONTACT SURFACE (MOLECULE)
# ===============================
def ShowConSurfMol(selection1, selection2, cutoff=None, subtract=None, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowConSurfMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CONTACT SURFACE (RESIDUE)
# ==============================
def ShowConSurfRes(selection1, selection2, cutoff=None, subtract=None, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowConSurfRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CONTACT SURFACE (ATOM)
# ===========================
def ShowConSurfAtom(selection1, selection2, cutoff=None, subtract=None, Type=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowConSurfAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW CONTACTS (OBJECT)
# ======================
def ShowConObj(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None):
  command='ShowConObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW CONTACTS (MOLECULE)
# ========================
def ShowConMol(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None):
  command='ShowConMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW CONTACTS (RESIDUE)
# =======================
def ShowConRes(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None):
  command='ShowConRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW CONTACTS (ATOM)
# ====================
def ShowConAtom(selection1, selection2, cutoff=None, subtract=None, energy=None, exclude=None, occluded=None):
  command='ShowConAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (subtract!=None): command+='Subtract='+cstr(subtract)+','
  if (energy!=None): command+='Energy='+cstr(energy)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW ELECTROSTATIC POTENTIAL
# ============================
# THIS IS ALTERNATIVE 1, WITH DIFFERENT PARAMETERS
def ShowESPPoints(method=None, resolution=None, Min=None, Max=None):
  command='ShowESP Points,'
  if (method!=None): command+='Method='+cstr(method)+','
  if (resolution!=None): command+='Resolution='+cstr(resolution)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (Max!=None): command+='Max='+cstr(Max)+','
  run(command[:-1])

# SHOW ELECTROSTATIC POTENTIAL
# ============================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ShowESPDensity(method=None, resolution=None, Min=None, Max=None):
  command='ShowESP Density,'
  if (method!=None): command+='Method='+cstr(method)+','
  if (resolution!=None): command+='Resolution='+cstr(resolution)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (Max!=None): command+='Max='+cstr(Max)+','
  run(command[:-1])

# SHOW ELECTROSTATIC POTENTIAL
# ============================
# THIS IS ALTERNATIVE 3, WITH DIFFERENT PARAMETERS
def ShowESPContour(method=None, resolution=None, level=None):
  command='ShowESP Contour,'
  if (method!=None): command+='Method='+cstr(method)+','
  if (resolution!=None): command+='Resolution='+cstr(resolution)+','
  if (level!=None): command+='Level='+cstr(level)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (ALL OR SELECTED)
# =====================================
def ShowHBo(extend=None):
  command='ShowHBo '
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (ALL)
# =========================
def ShowHBoAll(extend=None):
  command='ShowHBoAll '
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (OBJECT)
# ============================
def ShowHBoObj(selection1, extend=None):
  command='ShowHBoObj '
  command+=selstr(selection1)+','
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (MOLECULE)
# ==============================
def ShowHBoMol(selection1, extend=None):
  command='ShowHBoMol '
  command+=selstr(selection1)+','
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (RESIDUE)
# =============================
def ShowHBoRes(selection1, extend=None):
  command='ShowHBoRes '
  command+=selstr(selection1)+','
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW HYDROGEN BONDS (ATOM)
# ==========================
def ShowHBoAtom(selection1, extend=None):
  command='ShowHBoAtom '
  command+=selstr(selection1)+','
  if (extend!=None): command+='Extend='+cstr(extend)+','
  run(command[:-1])

# SHOW IN HEAD-UP DISPLAY (MOLECULE)
# ==================================
def ShowHUDMol(selection1):
  command='ShowHUDMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW IN HEAD-UP DISPLAY (RESIDUE)
# =================================
def ShowHUDRes(selection1):
  command='ShowHUDRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW IN HEAD-UP DISPLAY (ATOM)
# ==============================
def ShowHUDAtom(selection1):
  command='ShowHUDAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW IMAGES
# ===========
def ShowImage(selection1, x=None, y=None, width=None, height=None, alpha=None, priority=None):
  command='ShowImage '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (priority!=None): command+='Priority='+cstr(priority)+','
  run(command[:-1])

# SHOW INTERACTIONS (OBJECT)
# ==========================
def ShowIntObj(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, delold=None):
  command='ShowIntObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (delold!=None): command+='DelOld='+cstr(delold)+','
  return(run(command[:-1]))

# SHOW INTERACTIONS (MOLECULE)
# ============================
def ShowIntMol(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, delold=None):
  command='ShowIntMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (delold!=None): command+='DelOld='+cstr(delold)+','
  return(run(command[:-1]))

# SHOW INTERACTIONS (RESIDUE)
# ===========================
def ShowIntRes(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, delold=None):
  command='ShowIntRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (delold!=None): command+='DelOld='+cstr(delold)+','
  return(run(command[:-1]))

# SHOW INTERACTIONS (ATOM)
# ========================
def ShowIntAtom(selection1, selection2, Type, cutoff=None, exclude=None, occluded=None, delold=None):
  command='ShowIntAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+='Type='+cstr(Type)+','
  if (cutoff!=None): command+='Cutoff='+cstr(cutoff)+','
  if (exclude!=None): command+='Exclude='+cstr(exclude)+','
  if (occluded!=None): command+='Occluded='+cstr(occluded)+','
  if (delold!=None): command+='DelOld='+cstr(delold)+','
  return(run(command[:-1]))

# SHOW ION BINDING SITES (ALL OR SELECTED)
# ========================================
def ShowIonSites(ion):
  command='ShowIonSites '
  command+='Ion='+cstr(ion)+','
  return(run(command[:-1]))

# SHOW ION BINDING SITES (ALL)
# ============================
def ShowIonSitesAll(ion):
  command='ShowIonSitesAll '
  command+='Ion='+cstr(ion)+','
  return(run(command[:-1]))

# SHOW ION BINDING SITES (OBJECT)
# ===============================
def ShowIonSitesObj(selection1, ion):
  command='ShowIonSitesObj '
  command+=selstr(selection1)+','
  command+='Ion='+cstr(ion)+','
  return(run(command[:-1]))

# SHOW KNOWLEDGE-BASED POTENTIAL
# ==============================
def ShowKBP(selection1, selection2, name=None, Type=None, size=None):
  command='ShowKBP '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (name!=None): command+='Name='+cstr(name)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (size!=None): command+='Size='+cstr(size)+','
  return(run(command[:-1]))

# SHOW TEXT MESSAGE AT THE BOTTOM
# ===============================
def ShowMessage(text):
  command='ShowMessage '
  command+='Text='+cstr(text,1)+','
  run(command[:-1])

# SHOW RESTRAINTS (ALL OR SELECTED)
# =================================
def ShowRest(Class=None):
  command='ShowRest '
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW RESTRAINTS (ALL)
# =====================
def ShowRestAll(Class=None):
  command='ShowRestAll '
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW RESTRAINTS (OBJECT)
# ========================
def ShowRestObj(selection1, Class=None):
  command='ShowRestObj '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW RESTRAINTS (MOLECULE)
# ==========================
def ShowRestMol(selection1, Class=None):
  command='ShowRestMol '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW RESTRAINTS (RESIDUE)
# =========================
def ShowRestRes(selection1, Class=None):
  command='ShowRestRes '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW RESTRAINTS (ATOM)
# ======================
def ShowRestAtom(selection1, Class=None):
  command='ShowRestAtom '
  command+=selstr(selection1)+','
  if (Class!=None): command+='Class='+cstr(Class)+','
  run(command[:-1])

# SHOW SIDE-CHAIN ROTAMERS (ALL OR SELECTED)
# ==========================================
def ShowRota():
  command='ShowRota '
  return(run(command[:-1]))

# SHOW SIDE-CHAIN ROTAMERS (ALL)
# ==============================
def ShowRotaAll():
  command='ShowRotaAll '
  return(run(command[:-1]))

# SHOW SIDE-CHAIN ROTAMERS (OBJECT)
# =================================
def ShowRotaObj(selection1):
  command='ShowRotaObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SHOW SIDE-CHAIN ROTAMERS (MOLECULE)
# ===================================
def ShowRotaMol(selection1):
  command='ShowRotaMol '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SHOW SIDE-CHAIN ROTAMERS (RESIDUE)
# ==================================
def ShowRotaRes(selection1):
  command='ShowRotaRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SHOW SECONDARY STRUCTURE (ALL OR SELECTED)
# ==========================================
def ShowSecStr(style=None, hideatoms=None):
  command='ShowSecStr '
  if (style!=None): command+='Style='+cstr(style)+','
  if (hideatoms!=None): command+='HideAtoms='+cstr(hideatoms)+','
  run(command[:-1])

# SHOW SECONDARY STRUCTURE (ALL)
# ==============================
def ShowSecStrAll(style=None, hideatoms=None):
  command='ShowSecStrAll '
  if (style!=None): command+='Style='+cstr(style)+','
  if (hideatoms!=None): command+='HideAtoms='+cstr(hideatoms)+','
  run(command[:-1])

# SHOW SECONDARY STRUCTURE (OBJECT)
# =================================
def ShowSecStrObj(selection1, style=None, hideatoms=None):
  command='ShowSecStrObj '
  command+=selstr(selection1)+','
  if (style!=None): command+='Style='+cstr(style)+','
  if (hideatoms!=None): command+='HideAtoms='+cstr(hideatoms)+','
  run(command[:-1])

# SHOW SECONDARY STRUCTURE (MOLECULE)
# ===================================
def ShowSecStrMol(selection1, style=None, hideatoms=None):
  command='ShowSecStrMol '
  command+=selstr(selection1)+','
  if (style!=None): command+='Style='+cstr(style)+','
  if (hideatoms!=None): command+='HideAtoms='+cstr(hideatoms)+','
  run(command[:-1])

# SHOW SECONDARY STRUCTURE (RESIDUE)
# ==================================
def ShowSecStrRes(selection1, style=None, hideatoms=None):
  command='ShowSecStrRes '
  command+=selstr(selection1)+','
  if (style!=None): command+='Style='+cstr(style)+','
  if (hideatoms!=None): command+='HideAtoms='+cstr(hideatoms)+','
  run(command[:-1])

# CREATE A SIMULATION CELL OBJECT TO VISUALIZE NEIGHBORING CELLS
# ==============================================================
def ShowCell(x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
  command='ShowCell '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (beta!=None): command+='Beta='+cstr(beta)+','
  if (gamma!=None): command+='Gamma='+cstr(gamma)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW SIMULATION NEIGHBOR SEARCH GRID
# ====================================
def ShowGrid(Type=None, center=None, color=None):
  command='ShowGrid '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (color!=None): command+='Color='+cstr(color)+','
  return(run(command[:-1]))

# SHOW A SPHERE OR ELLIPSOID
# ==========================
def ShowSphere(radius=None, color=None, alpha=None, level=None, scaley=None, scalez=None):
  command='ShowSphere '
  if (radius!=None): command+='Radius='+cstr(radius)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (level!=None): command+='Level='+cstr(level)+','
  if (scaley!=None): command+='ScaleY='+cstr(scaley)+','
  if (scalez!=None): command+='ScaleZ='+cstr(scalez)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW A RECTANGULAR PLANE
# ========================
def ShowPlane(width=None, height=None, trianglelen=None, color=None, alpha=None, specular=None):
  command='ShowPlane '
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (trianglelen!=None): command+='TriangleLen='+cstr(trianglelen)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW POLYGON BETWEEN ATOMS OR POINTS
# ====================================
# THIS IS ALTERNATIVE 1, WITH DIFFERENT PARAMETERS
def ShowPolygonAtoms(color, alpha, vertices, selection1, selection2, selection3, selection4=None, selection5=None, selection6=None, selection7=None, selection8=None):
  command='ShowPolygon Atoms,'
  command+='Color='+cstr(color)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Vertices='+cstr(vertices)+','
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  if (selection4!=None): command+=selstr(selection4)+','
  if (selection5!=None): command+=selstr(selection5)+','
  if (selection6!=None): command+=selstr(selection6)+','
  if (selection7!=None): command+=selstr(selection7)+','
  if (selection8!=None): command+=selstr(selection8)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW POLYGON BETWEEN ATOMS OR POINTS
# ====================================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def ShowPolygonPoints(color, alpha, vertices, x1, y1, z1, x2=None, y2=None, z2=None, x3=None, y3=None, z3=None, x4=None, y4=None, z4=None, x5=None, y5=None, z5=None, x6=None, y6=None, z6=None, x7=None, y7=None, z7=None, x8=None, y8=None, z8=None):
  command='ShowPolygon Points,'
  command+='Color='+cstr(color)+','
  command+='Alpha='+cstr(alpha)+','
  command+='Vertices='+cstr(vertices)+','
  command+='X1='+cstr(x1)+','
  command+='Y1='+cstr(y1)+','
  command+='Z1='+cstr(z1)+','
  if (x2!=None): command+='X2='+cstr(x2)+','
  if (y2!=None): command+='Y2='+cstr(y2)+','
  if (z2!=None): command+='Z2='+cstr(z2)+','
  if (x3!=None): command+='X3='+cstr(x3)+','
  if (y3!=None): command+='Y3='+cstr(y3)+','
  if (z3!=None): command+='Z3='+cstr(z3)+','
  if (x4!=None): command+='X4='+cstr(x4)+','
  if (y4!=None): command+='Y4='+cstr(y4)+','
  if (z4!=None): command+='Z4='+cstr(z4)+','
  if (x5!=None): command+='X5='+cstr(x5)+','
  if (y5!=None): command+='Y5='+cstr(y5)+','
  if (z5!=None): command+='Z5='+cstr(z5)+','
  if (x6!=None): command+='X6='+cstr(x6)+','
  if (y6!=None): command+='Y6='+cstr(y6)+','
  if (z6!=None): command+='Z6='+cstr(z6)+','
  if (x7!=None): command+='X7='+cstr(x7)+','
  if (y7!=None): command+='Y7='+cstr(y7)+','
  if (z7!=None): command+='Z7='+cstr(z7)+','
  if (x8!=None): command+='X8='+cstr(x8)+','
  if (y8!=None): command+='Y8='+cstr(y8)+','
  if (z8!=None): command+='Z8='+cstr(z8)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW POLYGON INSIDE RING (ALL OR SELECTED)
# ==========================================
def ShowRing(color=None, alpha=None):
  command='ShowRing '
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW POLYGON INSIDE RING (ALL)
# ==============================
def ShowRingAll(color=None, alpha=None):
  command='ShowRingAll '
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW POLYGON INSIDE RING (OBJECT)
# =================================
def ShowRingObj(selection1, color=None, alpha=None):
  command='ShowRingObj '
  command+=selstr(selection1)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW POLYGON INSIDE RING (MOLECULE)
# ===================================
def ShowRingMol(selection1, color=None, alpha=None):
  command='ShowRingMol '
  command+=selstr(selection1)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW POLYGON INSIDE RING (RESIDUE)
# ==================================
def ShowRingRes(selection1, color=None, alpha=None):
  command='ShowRingRes '
  command+=selstr(selection1)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW POLYGON INSIDE RING (ATOM)
# ===============================
def ShowRingAtom(selection1, color=None, alpha=None):
  command='ShowRingAtom '
  command+=selstr(selection1)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  run(command[:-1])

# SHOW A SPHERICAL ENVIRONMENT
# ============================
def ShowSkySphere(filename):
  command='ShowSkySphere '
  command+='Filename='+cstr(filename)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW SURFACE (ALL OR SELECTED)
# ==============================
def ShowSurf(Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurf '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW SURFACE (ALL)
# ==================
def ShowSurfAll(Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurfAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW SURFACE (OBJECT)
# =====================
def ShowSurfObj(selection1, Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurfObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW SURFACE (MOLECULE)
# =======================
def ShowSurfMol(selection1, Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurfMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW SURFACE (RESIDUE)
# ======================
def ShowSurfRes(selection1, Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurfRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW SURFACE (ATOM)
# ===================
def ShowSurfAtom(selection1, Type=None, update=None, outcol=None, outalpha=None, incol=None, inalpha=None, specular=None):
  command='ShowSurfAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (outcol!=None): command+='OutCol='+cstr(outcol)+','
  if (outalpha!=None): command+='OutAlpha='+cstr(outalpha)+','
  if (incol!=None): command+='InCol='+cstr(incol)+','
  if (inalpha!=None): command+='InAlpha='+cstr(inalpha)+','
  if (specular!=None): command+='Specular='+cstr(specular)+','
  return(run(command[:-1]))

# SHOW TABLE DATA AS 3D OBJECT
# ============================
def ShowTab(selection1, width=None, Range=None, Min=None, mincol=None, Max=None, maxcol=None, style=None, center=None):
  command='ShowTab '
  command+=selstr(selection1)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (Range!=None): command+='Range='+cstr(Range)+','
  if (Min!=None): command+='Min='+cstr(Min)+','
  if (mincol!=None): command+='MinCol='+cstr(mincol)+','
  if (Max!=None): command+='Max='+cstr(Max)+','
  if (maxcol!=None): command+='MaxCol='+cstr(maxcol)+','
  if (style!=None): command+='Style='+cstr(style)+','
  if (center!=None): command+='Center='+cstr(center)+','
  return(run(command[:-1]))

# SHOW A TORUS
# ============
def ShowTorus(largeradius=None, largeedges=None, smallradius=None, smalledges=None, color=None, alpha=None):
  command='ShowTorus '
  if (largeradius!=None): command+='LargeRadius='+cstr(largeradius)+','
  if (largeedges!=None): command+='LargeEdges='+cstr(largeedges)+','
  if (smallradius!=None): command+='SmallRadius='+cstr(smallradius)+','
  if (smalledges!=None): command+='SmallEdges='+cstr(smalledges)+','
  if (color!=None): command+='Color='+cstr(color)+','
  if (alpha!=None): command+='Alpha='+cstr(alpha)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SHOW TRACE THROUGH ATOMS
# ========================
def ShowTrace(selection1):
  command='ShowTrace '
  command+=selstr(selection1)+','
  run(command[:-1])

# OPEN A FILE IN THE WEB BROWSER
# ==============================
def ShowURL(name):
  command='ShowURL '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# SHOW VIEW
# =========
def ShowView(selection1):
  command='ShowView '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW A USER INTERFACE WINDOW AND OBTAIN THE INPUT MADE
# ======================================================
def ShowWin(Type, title, *arglist2):
  command='ShowWin '
  command+='Type='+cstr(Type)+','
  command+='Title='+cstr(title)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  return(run(command[:-1]))

# SHOW POLYGON MESH AS WIRE FRAME (ALL OR SELECTED)
# =================================================
def ShowWire(update=None, mesh=None, side=None):
  command='ShowWire '
  if (update!=None): command+='Update='+cstr(update)+','
  if (mesh!=None): command+='Mesh='+cstr(mesh)+','
  if (side!=None): command+='Side='+cstr(side)+','
  return(run(command[:-1]))

# SHOW POLYGON MESH AS WIRE FRAME (ALL)
# =====================================
def ShowWireAll(update=None, mesh=None, side=None):
  command='ShowWireAll '
  if (update!=None): command+='Update='+cstr(update)+','
  if (mesh!=None): command+='Mesh='+cstr(mesh)+','
  if (side!=None): command+='Side='+cstr(side)+','
  return(run(command[:-1]))

# SHOW POLYGON MESH AS WIRE FRAME (OBJECT)
# ========================================
def ShowWireObj(selection1, update=None, mesh=None, side=None):
  command='ShowWireObj '
  command+=selstr(selection1)+','
  if (update!=None): command+='Update='+cstr(update)+','
  if (mesh!=None): command+='Mesh='+cstr(mesh)+','
  if (side!=None): command+='Side='+cstr(side)+','
  return(run(command[:-1]))

# SHOW ATOMS (ALL OR SELECTED)
# ============================
def Show():
  command='Show '
  run(command[:-1])

# SHOW ATOMS (ALL)
# ================
def ShowAll():
  command='ShowAll '
  run(command[:-1])

# SHOW ATOMS (OBJECT)
# ===================
def ShowObj(selection1):
  command='ShowObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW ATOMS (MOLECULE)
# =====================
def ShowMol(selection1):
  command='ShowMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW ATOMS (RESIDUE)
# ====================
def ShowRes(selection1):
  command='ShowRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHOW ATOMS (ATOM)
# =================
def ShowAtom(selection1):
  command='ShowAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SHRINK OBJECT TO COARSE-GRAINED PET VERSION (ALL OR SELECTED)
# =============================================================
def Shrink(scalepos=None, element=None, fixdomains=None):
  command='Shrink '
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (element!=None): command+='Element='+cstr(element)+','
  if (fixdomains!=None): command+='FixDomains='+cstr(fixdomains)+','
  run(command[:-1])

# SHRINK OBJECT TO COARSE-GRAINED PET VERSION (ALL)
# =================================================
def ShrinkAll(scalepos=None, element=None, fixdomains=None):
  command='ShrinkAll '
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (element!=None): command+='Element='+cstr(element)+','
  if (fixdomains!=None): command+='FixDomains='+cstr(fixdomains)+','
  run(command[:-1])

# SHRINK OBJECT TO COARSE-GRAINED PET VERSION (OBJECT)
# ====================================================
def ShrinkObj(selection1, scalepos=None, element=None, fixdomains=None):
  command='ShrinkObj '
  command+=selstr(selection1)+','
  if (scalepos!=None): command+='ScalePos='+cstr(scalepos)+','
  if (element!=None): command+='Element='+cstr(element)+','
  if (fixdomains!=None): command+='FixDomains='+cstr(fixdomains)+','
  run(command[:-1])

# SET/GET SIMULATION STATE
# ========================
def Sim(control=None, In=None):
  command='Sim '
  if (control!=None): command+='Control='+cstr(control)+','
  if (In!=None): command+='in='+cstr(In)+','
  return(run(command[:-1]))

# SET SIMULATION SPEED
# ====================
def SimSpeed(Type):
  command='SimSpeed '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SET/GET NUMBER OF SIMULATION STEPS PER SCREEN AND PAIRLIST UPDATE
# =================================================================
def SimSteps(screen=None, pairlist=None):
  command='SimSteps '
  if (screen!=None): command+='Screen='+cstr(screen)+','
  if (pairlist!=None): command+='Pairlist='+cstr(pairlist)+','
  return(run(command[:-1]))

# GET SOLVENT DENSITY IN SIMULATION CELL
# ======================================
def SolvDensity(name=None):
  command='SolvDensity '
  if (name!=None): command+='Name='+cstr(name)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# CALCULATE SOLVATION ENERGY (ALL OR SELECTED)
# ============================================
def SolvEnergy(method=None):
  command='SolvEnergy '
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# CALCULATE SOLVATION ENERGY (ALL)
# ================================
def SolvEnergyAll(method=None):
  command='SolvEnergyAll '
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# CALCULATE SOLVATION ENERGY (OBJECT)
# ===================================
def SolvEnergyObj(selection1, method=None):
  command='SolvEnergyObj '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# CALCULATE SOLVATION ENERGY (MOLECULE)
# =====================================
def SolvEnergyMol(selection1, method=None):
  command='SolvEnergyMol '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# CALCULATE SOLVATION ENERGY (RESIDUE)
# ====================================
def SolvEnergyRes(selection1, method=None):
  command='SolvEnergyRes '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# CALCULATE SOLVATION ENERGY (ATOM)
# =================================
def SolvEnergyAtom(selection1, method=None):
  command='SolvEnergyAtom '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# SET/GET SOLVATION PARAMETERS
# ============================
def SolvPar(esolute=None, esolvent=None, resolution=None, ioncon=None):
  command='SolvPar '
  if (esolute!=None): command+='eSolute='+cstr(esolute)+','
  if (esolvent!=None): command+='eSolvent='+cstr(esolvent)+','
  if (resolution!=None): command+='Resolution='+cstr(resolution)+','
  if (ioncon!=None): command+='IonCon='+cstr(ioncon)+','
  return(run(command[:-1]))

# ASSIGN COMMAND TO SPACEBALL BUTTON
# ==================================
def SpaceballButton(number, com):
  command='SpaceballButton '
  command+='Number='+cstr(number)+','
  command+='Command='+cstr(com)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET SPACEBALL PARAMETERS
# ========================
def SpaceballPar(mode=None, movescale=None, rotatescale=None):
  command='SpaceballPar '
  if (mode!=None): command+='Mode='+cstr(mode)+','
  if (movescale!=None): command+='MoveScale='+cstr(movescale)+','
  if (rotatescale!=None): command+='RotateScale='+cstr(rotatescale)+','
  run(command[:-1])

# DETERMINE FIRST AND LAST UNIT SPANNING A SELECTION (OBJECT)
# ===========================================================
def SpanObj(selection1):
  command='SpanObj '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# DETERMINE FIRST AND LAST UNIT SPANNING A SELECTION (RESIDUE)
# ============================================================
def SpanRes(selection1):
  command='SpanRes '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# DETERMINE FIRST AND LAST UNIT SPANNING A SELECTION (ATOM)
# =========================================================
def SpanAtom(selection1):
  command='SpanAtom '
  command+=selstr(selection1)+','
  return(run(command[:-1]))

# SPEED UP MOVEMENTS WHEN GRAPHICS ARE SLOW
# =========================================
def SpeedUp(status=None):
  command='SpeedUp '
  if (status!=None): command+='Status='+cstr(status)+','
  run(command[:-1])

# SET/GET SPEED AND VELOCITY OF ATOMS (ALL OR SELECTED)
# =====================================================
def Speed(x=None, y=None, z=None):
  command='Speed '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET SPEED AND VELOCITY OF ATOMS (ALL)
# =========================================
def SpeedAll(x=None, y=None, z=None):
  command='SpeedAll '
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET SPEED AND VELOCITY OF ATOMS (OBJECT)
# ============================================
def SpeedObj(selection1, x=None, y=None, z=None):
  command='SpeedObj '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET SPEED AND VELOCITY OF ATOMS (MOLECULE)
# ==============================================
def SpeedMol(selection1, x=None, y=None, z=None):
  command='SpeedMol '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET SPEED AND VELOCITY OF ATOMS (RESIDUE)
# =============================================
def SpeedRes(selection1, x=None, y=None, z=None):
  command='SpeedRes '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SET/GET SPEED AND VELOCITY OF ATOMS (ATOM)
# ==========================================
def SpeedAtom(selection1, x=None, y=None, z=None):
  command='SpeedAtom '
  command+=selstr(selection1)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# SPLIT OBJECTS AT SPLIT POINTS (ALL OR SELECTED)
# ===============================================
def Split(center=None, selection1=None, keep=None):
  command='Split '
  if (center!=None): command+='Center='+cstr(center)+','
  if (selection1!=None): command+=selstr(selection1)+','
  if (keep!=None): command+='Keep='+cstr(keep)+','
  return(run(command[:-1]))

# SPLIT OBJECTS AT SPLIT POINTS (ALL)
# ===================================
def SplitAll(center=None, selection1=None, keep=None):
  command='SplitAll '
  if (center!=None): command+='Center='+cstr(center)+','
  if (selection1!=None): command+=selstr(selection1)+','
  if (keep!=None): command+='Keep='+cstr(keep)+','
  return(run(command[:-1]))

# SPLIT OBJECTS AT SPLIT POINTS (OBJECT)
# ======================================
def SplitObj(selection1, center=None, selection2=None, keep=None):
  command='SplitObj '
  command+=selstr(selection1)+','
  if (center!=None): command+='Center='+cstr(center)+','
  if (selection2!=None): command+=selstr(selection2)+','
  if (keep!=None): command+='Keep='+cstr(keep)+','
  return(run(command[:-1]))

# INTRODUCE SPLIT POINTS (MOLECULE)
# =================================
def SplitMol(selection1):
  command='SplitMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# INTRODUCE SPLIT POINTS (RESIDUE)
# ================================
def SplitRes(selection1):
  command='SplitRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# INTRODUCE SPLIT POINTS (ATOM)
# =============================
def SplitAtom(selection1):
  command='SplitAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SET STEREO MODE
# ===============
def Stereo(mode):
  command='Stereo '
  command+='Mode='+cstr(mode)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET STEREO PARAMETERS
# =====================
def StereoPar(eyedis=None, protru=None):
  command='StereoPar '
  if (eyedis!=None): command+='EyeDis='+cstr(eyedis)+','
  if (protru!=None): command+='ProTru='+cstr(protru)+','
  run(command[:-1])

# SET STICK RADIUS
# ================
def StickRadius(percent):
  command='StickRadius '
  command+='percent='+cstr(percent)+','
  run(command[:-1])

# STYLE ATOMS AS STICKS (ALL OR SELECTED)
# =======================================
def Stick():
  command='Stick '
  run(command[:-1])

# STYLE ATOMS AS STICKS (ALL)
# ===========================
def StickAll():
  command='StickAll '
  run(command[:-1])

# STYLE ATOMS AS STICKS (OBJECT)
# ==============================
def StickObj(selection1):
  command='StickObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS STICKS (MOLECULE)
# ================================
def StickMol(selection1):
  command='StickMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS STICKS (RESIDUE)
# ===============================
def StickRes(selection1):
  command='StickRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# STYLE ATOMS AS STICKS (ATOM)
# ============================
def StickAtom(selection1):
  command='StickAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# STOP LOG RECORDER
# =================
def StopLog():
  command='StopLog '
  run(command[:-1])

# STOP RUNNING PLUGIN
# ===================
def StopPlugin():
  command='StopPlugin '
  run(command[:-1])

# SET/GET GENERAL SCENE STYLE
# ===========================
def Style(backbone=None, sidechain=None, hetgroup=None, save=None):
  command='Style '
  if (backbone!=None): command+='Backbone='+cstr(backbone)+','
  if (sidechain!=None): command+='Sidechain='+cstr(sidechain)+','
  if (hetgroup!=None): command+='Hetgroup='+cstr(hetgroup)+','
  if (save!=None): command+='Save='+cstr(save)+','
  return(run(command[:-1]))

# STYLE WINDOWS
# =============
def StyleWin(Type):
  command='StyleWin '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SUPERPOSE MULTIPLE OBJECTS (OBJECT)
# ===================================
def SupMultiObj(selection1, method=None, match=None, flip=None, unit=None):
  command='SupMultiObj '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE MULTIPLE OBJECTS (MOLECULE)
# =====================================
def SupMultiMol(selection1, method=None, match=None, flip=None, unit=None):
  command='SupMultiMol '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE MULTIPLE OBJECTS (RESIDUE)
# ====================================
def SupMultiRes(selection1, method=None, match=None, flip=None, unit=None):
  command='SupMultiRes '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE MULTIPLE OBJECTS (ATOM)
# =================================
def SupMultiAtom(selection1, method=None, match=None, flip=None, unit=None):
  command='SupMultiAtom '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE OBJECTS ON ORDERED UNITS (MOLECULE)
# =============================================
def SupOrderedMol(selection1, selection2, selection3, selection4, selection5, selection6, *arglist2):
  command='SupOrderedMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  command+=selstr(selection5)+','
  command+=selstr(selection6)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SUPERPOSE OBJECTS ON ORDERED UNITS (RESIDUE)
# ============================================
def SupOrderedRes(selection1, selection2, selection3, selection4, selection5, selection6, *arglist2):
  command='SupOrderedRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  command+=selstr(selection5)+','
  command+=selstr(selection6)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SUPERPOSE OBJECTS ON ORDERED UNITS (ATOM)
# =========================================
def SupOrderedAtom(selection1, selection2, selection3, selection4, selection5, selection6, *arglist2):
  command='SupOrderedAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  command+=selstr(selection3)+','
  command+=selstr(selection4)+','
  command+=selstr(selection5)+','
  command+=selstr(selection6)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SUPERPOSE OBJECTS (OBJECT)
# ==========================
def SupObj(selection1, selection2, match=None, flip=None, unit=None):
  command='SupObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE OBJECTS (MOLECULE)
# ============================
def SupMol(selection1, selection2, match=None, flip=None, unit=None):
  command='SupMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE OBJECTS (RESIDUE)
# ===========================
def SupRes(selection1, selection2, match=None, flip=None, unit=None):
  command='SupRes '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SUPERPOSE OBJECTS (ATOM)
# ========================
def SupAtom(selection1, selection2, match=None, flip=None, unit=None):
  command='SupAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (match!=None): command+='Match='+cstr(match)+','
  if (flip!=None): command+='Flip='+cstr(flip)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# SET/GET SURFACE PARAMETERS
# ==========================
def SurfPar(probe=None, resolution=None, molecular=None, espmax=None, smoothcut=None, radii=None, unite=None):
  command='SurfPar '
  if (probe!=None): command+='Probe='+cstr(probe)+','
  if (resolution!=None): command+='Resolution='+cstr(resolution)+','
  if (molecular!=None): command+='Molecular='+cstr(molecular)+','
  if (espmax!=None): command+='ESPMax='+cstr(espmax)+','
  if (smoothcut!=None): command+='SmoothCut='+cstr(smoothcut)+','
  if (radii!=None): command+='Radii='+cstr(radii)+','
  if (unite!=None): command+='Unite='+cstr(unite)+','
  return(run(command[:-1]))

# CALCULATE DISTANCE FROM SURFACE (OBJECT)
# ========================================
def SurfDisObj(selection1, Type, results=None):
  command='SurfDisObj '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# CALCULATE DISTANCE FROM SURFACE (MOLECULE)
# ==========================================
def SurfDisMol(selection1, Type, results=None):
  command='SurfDisMol '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# CALCULATE DISTANCE FROM SURFACE (RESIDUE)
# =========================================
def SurfDisRes(selection1, Type, results=None):
  command='SurfDisRes '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# CALCULATE DISTANCE FROM SURFACE (ATOM)
# ======================================
def SurfDisAtom(selection1, Type, results=None):
  command='SurfDisAtom '
  command+=selstr(selection1)+','
  command+='Type='+cstr(Type)+','
  if (results!=None): command+='Results='+cstr(results)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (ALL OR SELECTED)
# ============================================================
def SurfESP(Type=None, method=None, unit=None):
  command='SurfESP '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (ALL)
# ================================================
def SurfESPAll(Type=None, method=None, unit=None):
  command='SurfESPAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (OBJECT)
# ===================================================
def SurfESPObj(selection1, Type=None, method=None, unit=None):
  command='SurfESPObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (MOLECULE)
# =====================================================
def SurfESPMol(selection1, Type=None, method=None, unit=None):
  command='SurfESPMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (RESIDUE)
# ====================================================
def SurfESPRes(selection1, Type=None, method=None, unit=None):
  command='SurfESPRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE ELECTROSTATIC SURFACE POTENTIALS (ATOM)
# =================================================
def SurfESPAtom(selection1, Type=None, method=None, unit=None):
  command='SurfESPAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (method!=None): command+='Method='+cstr(method)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (ALL OR SELECTED)
# =========================================
def Surf(Type=None, unit=None):
  command='Surf '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (ALL)
# =============================
def SurfAll(Type=None, unit=None):
  command='SurfAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (OBJECT)
# ================================
def SurfObj(selection1, Type=None, unit=None):
  command='SurfObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (MOLECULE)
# ==================================
def SurfMol(selection1, Type=None, unit=None):
  command='SurfMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (RESIDUE)
# =================================
def SurfRes(selection1, Type=None, unit=None):
  command='SurfRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CALCULATE SURFACE AREAS (ATOM)
# ==============================
def SurfAtom(selection1, Type=None, unit=None):
  command='SurfAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  return(run(command[:-1]))

# CHANGE CHEMICAL ELEMENT OR ADD FUNCTIONAL GROUP
# ===============================================
def SwapAtom(selection1, element, updatebonds=None, updatehyd=None, rename=None, attachpoint=None):
  command='SwapAtom '
  command+=selstr(selection1)+','
  command+='Element='+cstr(element)+','
  if (updatebonds!=None): command+='UpdateBonds='+cstr(updatebonds)+','
  if (updatehyd!=None): command+='UpdateHyd='+cstr(updatehyd)+','
  if (rename!=None): command+='Rename='+cstr(rename)+','
  if (attachpoint!=None): command+='AttachPoint='+cstr(attachpoint)+','
  return(run(command[:-1]))

# SWAP ORDER OF COVALENT BONDS
# ============================
def SwapBond(selection1, selection2, order=None, update=None):
  command='SwapBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (order!=None): command+='Order='+cstr(order)+','
  if (update!=None): command+='Update='+cstr(update)+','
  run(command[:-1])

# SWAP HYDROGEN ORDERING IN RESIDUES (ALL OR SELECTED)
# ====================================================
def SwapHyd(order):
  command='SwapHyd '
  command+='Order='+cstr(order)+','
  run(command[:-1])

# SWAP HYDROGEN ORDERING IN RESIDUES (ALL)
# ========================================
def SwapHydAll(order):
  command='SwapHydAll '
  command+='Order='+cstr(order)+','
  run(command[:-1])

# SWAP HYDROGEN ORDERING IN RESIDUES (OBJECT)
# ===========================================
def SwapHydObj(selection1, order):
  command='SwapHydObj '
  command+=selstr(selection1)+','
  command+='Order='+cstr(order)+','
  run(command[:-1])

# SWAP IMAGES
# ===========
def SwapImage(selection1, selection2):
  command='SwapImage '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# SWAP TWO OBJECTS IN THE LIST
# ============================
def SwapObj(selection1, selection2):
  command='SwapObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  run(command[:-1])

# SWAP ATOM POSITIONS
# ===================
def SwapPosAtom(selection1, selection2, bound=None):
  command='SwapPosAtom '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (bound!=None): command+='Bound='+cstr(bound)+','
  run(command[:-1])

# SWAP RESIDUE SIDE-CHAINS
# ========================
def SwapRes(selection1, new, isomer=None):
  command='SwapRes '
  command+=selstr(selection1)+','
  command+='new='+cstr(new)+','
  if (isomer!=None): command+='Isomer='+cstr(isomer)+','
  run(command[:-1])

# SET/GET OBJECT VISIBILITIES (ALL OR SELECTED)
# =============================================
def Switch(visibility=None, wait=None):
  command='Switch '
  if (visibility!=None): command+='Visibility='+cstr(visibility)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  return(run(command[:-1]))

# SET/GET OBJECT VISIBILITIES (ALL)
# =================================
def SwitchAll(visibility=None, wait=None):
  command='SwitchAll '
  if (visibility!=None): command+='Visibility='+cstr(visibility)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  return(run(command[:-1]))

# SET/GET OBJECT VISIBILITIES (OBJECT)
# ====================================
def SwitchObj(selection1, visibility=None, wait=None):
  command='SwitchObj '
  command+=selstr(selection1)+','
  if (visibility!=None): command+='Visibility='+cstr(visibility)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  return(run(command[:-1]))

# GET SYSTEM TIME
# ===============
def SystemTime():
  command='SystemTime '
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET/GET TABLE CELLS
# ===================
def Tab(selection1, column=None, row=None, page=None, set=None, numformat=None):
  command='Tab '
  command+=selstr(selection1)+','
  if (column!=None): command+='Column='+cstr(column)+','
  if (row!=None): command+='Row='+cstr(row)+','
  if (page!=None): command+='Page='+cstr(page)+','
  if (set!=None): command+='Set='+cstr(set)+','
  if (numformat!=None): command+='NumFormat='+cstr(numformat)+','
  return(run(command[:-1]))

# SET/GET SIMULATION TEMPERATURE
# ==============================
def Temp(degrees=None, reassign=None):
  command='Temp '
  if (degrees!=None): command+='degrees='+cstr(degrees)+','
  if (reassign!=None): command+='Reassign='+cstr(reassign)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET TEMPERATURE CONTROL
# =======================
def TempCtrl(Type):
  command='TempCtrl '
  command+='Type='+cstr(Type)+','
  run(command[:-1])

# SET/GET SIMULATION TIME
# =======================
def Time(fs=None):
  command='Time '
  if (fs!=None): command+='FS='+cstr(fs)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# SET SIMULATION TIMESTEP
# =======================
def TimeStep(inter=None, intra=None):
  command='TimeStep '
  if (inter!=None): command+='Inter='+cstr(inter)+','
  if (intra!=None): command+='Intra='+cstr(intra)+','
  run(command[:-1])

# TRANSFER OBJECTS INTO ANOTHER COORDINATE SYSTEM (ALL OR SELECTED)
# =================================================================
def Transfer(selection1, local=None):
  command='Transfer '
  command+=selstr(selection1)+','
  if (local!=None): command+='Local='+cstr(local)+','
  run(command[:-1])

# TRANSFER OBJECTS INTO ANOTHER COORDINATE SYSTEM (ALL)
# =====================================================
def TransferAll(selection1, local=None):
  command='TransferAll '
  command+=selstr(selection1)+','
  if (local!=None): command+='Local='+cstr(local)+','
  run(command[:-1])

# TRANSFER OBJECTS INTO ANOTHER COORDINATE SYSTEM (OBJECT)
# ========================================================
def TransferObj(selection1, selection2, local=None):
  command='TransferObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (local!=None): command+='Local='+cstr(local)+','
  run(command[:-1])

# GET PREVIOUSLY APPLIED TRANSFORMATIONS
# ======================================
def Transformation(Type=None, number=None):
  command='Transformation '
  if (Type!=None): command+='Type='+cstr(Type)+','
  if (number!=None): command+='Number='+cstr(number)+','
  return(run(command[:-1]))

# TRANSFORM OBJECTS (ALL OR SELECTED)
# ===================================
def Transform(keeppos=None):
  command='Transform '
  if (keeppos!=None): command+='KeepPos='+cstr(keeppos)+','
  run(command[:-1])

# TRANSFORM OBJECTS (ALL)
# =======================
def TransformAll(keeppos=None):
  command='TransformAll '
  if (keeppos!=None): command+='KeepPos='+cstr(keeppos)+','
  run(command[:-1])

# TRANSFORM OBJECTS (OBJECT)
# ==========================
def TransformObj(selection1, keeppos=None):
  command='TransformObj '
  command+=selstr(selection1)+','
  if (keeppos!=None): command+='KeepPos='+cstr(keeppos)+','
  run(command[:-1])

# TWIST OBJECTS TO IMPROVE STRUCTURAL ALIGNMENT (OBJECT)
# ======================================================
def TwistObj(selection1, selection2, strength=None, structures=None):
  command='TwistObj '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (strength!=None): command+='Strength='+cstr(strength)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  run(command[:-1])

# TWIST OBJECTS TO IMPROVE STRUCTURAL ALIGNMENT (MOLECULE)
# ========================================================
def TwistMol(selection1, selection2, strength=None, structures=None):
  command='TwistMol '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (strength!=None): command+='Strength='+cstr(strength)+','
  if (structures!=None): command+='Structures='+cstr(structures)+','
  run(command[:-1])

# GET THE ATOM TYPE
# =================
def TypeAtom(selection1, method=None):
  command='TypeAtom '
  command+=selstr(selection1)+','
  if (method!=None): command+='Method='+cstr(method)+','
  return(run(command[:-1]))

# ASSIGN BOND ORDERS AUTOMATICALLY
# ================================
def TypeBond(selection1, selection2, usetopo=None, kekulize=None, hydmissing=None):
  command='TypeBond '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (usetopo!=None): command+='useTopo='+cstr(usetopo)+','
  if (kekulize!=None): command+='Kekulize='+cstr(kekulize)+','
  if (hydmissing!=None): command+='HydMissing='+cstr(hydmissing)+','
  run(command[:-1])

# UNCOUPLE OBJECT MOVEMENT FROM ANOTHER OBJECT (ALL OR SELECTED)
# ==============================================================
def Uncouple():
  command='Uncouple '
  run(command[:-1])

# UNCOUPLE OBJECT MOVEMENT FROM ANOTHER OBJECT (ALL)
# ==================================================
def UncoupleAll():
  command='UncoupleAll '
  run(command[:-1])

# UNCOUPLE OBJECT MOVEMENT FROM ANOTHER OBJECT (OBJECT)
# =====================================================
def UncoupleObj(selection1):
  command='UncoupleObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# SET NUMBER OF UNDO LEVELS
# =========================
def UndoLevels(number):
  command='UndoLevels '
  command+='Number='+cstr(number)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (ALL OR SELECTED)
# =========================================
def Ungroup(name):
  command='Ungroup '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (ALL)
# =============================
def UngroupAll(name):
  command='UngroupAll '
  command+='Name='+cstr(name)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (OBJECT)
# ================================
def UngroupObj(selection1, name):
  command='UngroupObj '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (MOLECULE)
# ==================================
def UngroupMol(selection1, name):
  command='UngroupMol '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (RESIDUE)
# =================================
def UngroupRes(selection1, name):
  command='UngroupRes '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# REMOVE ATOMS FROM GROUP (ATOM)
# ==============================
def UngroupAtom(selection1, name):
  command='UngroupAtom '
  command+=selstr(selection1)+','
  command+='Name='+cstr(name)+','
  run(command[:-1])

# DELETE DISTANCES LABELS
# =======================
def UnlabelDis(selection1, selection2, bound=None):
  command='UnlabelDis '
  command+=selstr(selection1)+','
  command+=selstr(selection2)+','
  if (bound!=None): command+='bound='+cstr(bound)+','
  run(command[:-1])

# DELETE LABELS (ALL OR SELECTED)
# ===============================
def Unlabel():
  command='Unlabel '
  run(command[:-1])

# DELETE LABELS (ALL)
# ===================
def UnlabelAll():
  command='UnlabelAll '
  run(command[:-1])

# DELETE LABELS (OBJECT)
# ======================
def UnlabelObj(selection1):
  command='UnlabelObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE LABELS (MOLECULE)
# ========================
def UnlabelMol(selection1):
  command='UnlabelMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE LABELS (SEGMENT)
# =======================
def UnlabelSeg(selection1):
  command='UnlabelSeg '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE LABELS (RESIDUE)
# =======================
def UnlabelRes(selection1):
  command='UnlabelRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# DELETE LABELS (ATOM)
# ====================
def UnlabelAtom(selection1):
  command='UnlabelAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# LET ANIMATED IMAGE DISAPPEAR
# ============================
def UnrestImage(selection1):
  command='UnrestImage '
  command+=selstr(selection1)+','
  run(command[:-1])

# UNSELECT ATOMS (ALL OR SELECTED)
# ================================
def Unselect():
  command='Unselect '
  run(command[:-1])

# UNSELECT ATOMS (ALL)
# ====================
def UnselectAll():
  command='UnselectAll '
  run(command[:-1])

# UNSELECT ATOMS (OBJECT)
# =======================
def UnselectObj(selection1):
  command='UnselectObj '
  command+=selstr(selection1)+','
  run(command[:-1])

# UNSELECT ATOMS (MOLECULE)
# =========================
def UnselectMol(selection1):
  command='UnselectMol '
  command+=selstr(selection1)+','
  run(command[:-1])

# UNSELECT ATOMS (RESIDUE)
# ========================
def UnselectRes(selection1):
  command='UnselectRes '
  command+=selstr(selection1)+','
  run(command[:-1])

# UNSELECT ATOMS (ATOM)
# =====================
def UnselectAtom(selection1):
  command='UnselectAtom '
  command+=selstr(selection1)+','
  run(command[:-1])

# SET USER INPUT
# ==============
def UserInput(status=None):
  command='UserInput '
  if (status!=None): command+='Status='+cstr(status)+','
  run(command[:-1])

# GET ORIENTATION VECTORS
# =======================
def VecOri(alpha, beta, gamma):
  command='VecOri '
  command+='Alpha='+cstr(alpha)+','
  command+='Beta='+cstr(beta)+','
  command+='Gamma='+cstr(gamma)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (ALL OR SELECTED)
# ===================================
def Volume(Type=None):
  command='Volume '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (ALL)
# =======================
def VolumeAll(Type=None):
  command='VolumeAll '
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (OBJECT)
# ==========================
def VolumeObj(selection1, Type=None):
  command='VolumeObj '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (MOLECULE)
# ============================
def VolumeMol(selection1, Type=None):
  command='VolumeMol '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (RESIDUE)
# ===========================
def VolumeRes(selection1, Type=None):
  command='VolumeRes '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# CALCULATE VOLUMES (ATOM)
# ========================
def VolumeAtom(selection1, Type=None):
  command='VolumeAtom '
  command+=selstr(selection1)+','
  if (Type!=None): command+='Type='+cstr(Type)+','
  return(run(command[:-1]))

# GET SIZE, ORIENTATION AND POSTION OF THE VR PLAY AREA
# =====================================================
def VRArea():
  command='VRArea '
  return(run(command[:-1]))

# SET/GET VIRTUAL REALITY PARAMETERS
# ==================================
def VRPar(controllers=None, beamangle=None, ctrlshiftz=None, ctrlscalez=None, guiscale=None, scrscale=None, scrshifty=None, updatewin=None, camleftx=None, camlefty=None, camrightx=None, camrighty=None, scrcorner=None, x=None, y=None, z=None):
  command='VRPar '
  if (controllers!=None): command+='Controllers='+cstr(controllers)+','
  if (beamangle!=None): command+='BeamAngle='+cstr(beamangle)+','
  if (ctrlshiftz!=None): command+='CtrlShiftZ='+cstr(ctrlshiftz)+','
  if (ctrlscalez!=None): command+='CtrlScaleZ='+cstr(ctrlscalez)+','
  if (guiscale!=None): command+='GUIScale='+cstr(guiscale)+','
  if (scrscale!=None): command+='ScrScale='+cstr(scrscale)+','
  if (scrshifty!=None): command+='ScrShiftY='+cstr(scrshifty)+','
  if (updatewin!=None): command+='UpdateWin='+cstr(updatewin)+','
  if (camleftx!=None): command+='CamLeftX='+cstr(camleftx)+','
  if (camlefty!=None): command+='CamLeftY='+cstr(camlefty)+','
  if (camrightx!=None): command+='CamRightX='+cstr(camrightx)+','
  if (camrighty!=None): command+='CamRightY='+cstr(camrighty)+','
  if (scrcorner!=None): command+='ScrCorner='+cstr(scrcorner)+','
  if (x!=None): command+='X='+cstr(x)+','
  if (y!=None): command+='Y='+cstr(y)+','
  if (z!=None): command+='Z='+cstr(z)+','
  return(run(command[:-1]))

# WAIT FOR CERTAIN TIME PERIOD OR CONDITION
# =========================================
def Wait(steps, unit=None):
  command='Wait '
  command+=cstr(steps)+','
  if (unit!=None): command+='Unit='+cstr(unit)+','
  result=run(command[:-1])
  if (result!=None and len(result)): return(result[0])
  return(None)

# TREAT WARNINGS AS ERRORS
# ========================
def WarnIsError(flag):
  command='WarnIsError '
  command+='Flag='+cstr(flag)+','
  run(command[:-1])

# SET TIMEOUT FOR INTERNET CONNECTIONS
# ====================================
def WebTimeout(seconds=None):
  command='WebTimeout '
  if (seconds!=None): command+='Seconds='+cstr(seconds)+','
  run(command[:-1])

# SET WINDOW FONT
# ===============
def WinFont(location, name=None, height=None):
  command='WinFont '
  command+='Location='+cstr(location)+','
  if (name!=None): command+='Name='+cstr(name)+','
  if (height!=None): command+='Height='+cstr(height)+','
  run(command[:-1])

# SET WINDOW BACKGROUND TEXTURE
# =============================
def WinTexture(number):
  command='WinTexture '
  command+='Number='+cstr(number)+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 1, WITH DIFFERENT PARAMETERS
def WriteReportTitle(filename, text):
  command='WriteReport Title,'
  command+='Filename='+cstr(filename)+','
  command+='Text='+cstr(text,1)+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 2, WITH DIFFERENT PARAMETERS
def WriteReportHeading(level, text):
  command='WriteReport Heading,'
  command+='Level='+cstr(level)+','
  command+='Text='+cstr(text,1)+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 3, WITH DIFFERENT PARAMETERS
def WriteReportParagraph(text):
  command='WriteReport Paragraph,'
  command+='Text='+cstr(text,1)+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 4, WITH DIFFERENT PARAMETERS
def WriteReportTable(selection1, caption=None, numformat=None, rowsmax=None, infocolumn=None, datacolumn=None, datacolumns=None, *arglist2):
  command='WriteReport Table,'
  command+=selstr(selection1)+','
  if (caption!=None): command+='Caption='+cstr(caption)+','
  if (numformat!=None): command+='NumFormat='+cstr(numformat)+','
  if (rowsmax!=None): command+='RowsMax='+cstr(rowsmax)+','
  if (infocolumn!=None): command+='InfoColumn='+cstr(infocolumn)+','
  if (datacolumn!=None): command+='DataColumn='+cstr(datacolumn)+','
  if (datacolumns!=None): command+='DataColumns='+cstr(datacolumns)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 5, WITH DIFFERENT PARAMETERS
def WriteReportPlot(caption, selection1, width, height, title, Type, xcolumn, ycolumn, ycolumns, xlabel, ylabel, legendpos, graphname, *arglist2):
  command='WriteReport Plot,'
  command+='Caption='+cstr(caption)+','
  command+=selstr(selection1)+','
  command+='Width='+cstr(width)+','
  command+='Height='+cstr(height)+','
  command+='Title='+cstr(title)+','
  command+='Type='+cstr(Type)+','
  command+='XColumn='+cstr(xcolumn)+','
  command+='YColumn='+cstr(ycolumn)+','
  command+='YColumns='+cstr(ycolumns)+','
  command+='XLabel='+cstr(xlabel)+','
  command+='YLabel='+cstr(ylabel)+','
  command+='LegendPos='+cstr(legendpos)+','
  command+='GraphName='+cstr(graphname)+','
  # ANY NUMBER OF VARIABLE ARGUMENTS CAN FOLLOW
  for arglist in arglist2:
    if (type(arglist)!=type([])): arglist=[arglist]
    for arg in arglist:
      command+=cstr(arg,quoted=(type(arg)!=type(1) and type(arg)!=type(1.)))+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 6, WITH DIFFERENT PARAMETERS
def WriteReportImage(filename, style=None, caption=None, width=None, height=None, name=None, delete=None):
  command='WriteReport Image,'
  command+='Filename='+cstr(filename)+','
  if (style!=None): command+='Style='+cstr(style)+','
  if (caption!=None): command+='Caption='+cstr(caption)+','
  if (width!=None): command+='Width='+cstr(width)+','
  if (height!=None): command+='Height='+cstr(height)+','
  if (name!=None): command+='Name='+cstr(name)+','
  if (delete!=None): command+='Delete='+cstr(delete)+','
  run(command[:-1])

# WRITE HTML REPORT
# =================
# THIS IS ALTERNATIVE 7, WITH DIFFERENT PARAMETERS
def WriteReportEnd():
  command='WriteReport End,'
  run(command[:-1])

# ZOOM IN ON ATOMS (ALL OR SELECTED)
# ==================================
def Zoom(steps=None, wait=None):
  command='Zoom '
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ZOOM IN ON ATOMS (ALL)
# ======================
def ZoomAll(steps=None, wait=None):
  command='ZoomAll '
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ZOOM IN ON ATOMS (OBJECT)
# =========================
def ZoomObj(selection1, steps=None, wait=None):
  command='ZoomObj '
  command+=selstr(selection1)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ZOOM IN ON ATOMS (MOLECULE)
# ===========================
def ZoomMol(selection1, steps=None, wait=None):
  command='ZoomMol '
  command+=selstr(selection1)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ZOOM IN ON ATOMS (RESIDUE)
# ==========================
def ZoomRes(selection1, steps=None, wait=None):
  command='ZoomRes '
  command+=selstr(selection1)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

# ZOOM IN ON ATOMS (ATOM)
# =======================
def ZoomAtom(selection1, steps=None, wait=None):
  command='ZoomAtom '
  command+=selstr(selection1)+','
  if (steps!=None): command+='Steps='+cstr(steps)+','
  if (wait!=None): command+='Wait='+cstr(wait)+','
  run(command[:-1])

