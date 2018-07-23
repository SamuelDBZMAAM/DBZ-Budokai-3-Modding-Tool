##Started on 01/05/18 and was finished on --/--/---- (DD/MM/YYYY)
##Created by Samuel O'Brien (AKA SamuelDBZModsAnimationsAndMore, SamuelDBZMAAM, TrueXenoSama69, any other name I go by in the future)
##Purpose of program:
##To adjust, remove and replace certain lines in Dragon Ball Budokai Series' files
##Thank you to the kind people over at Programming Discussions Discord for giving me a hand with this: https://discord.gg/9zT7NHP
##BLACK TEXT BOX VERSION (BTB) current version 0.02


##To do -
#Create a UI that is helpful and appealing
#Use functions/sub-programs that can change B4 01 00 00 B4 01 to other --COMPLETE
#Use functions/sub-programs that can remove AMGs from the list
#Use functions/sub-programs that reshade model parts                   --COMPLETE
#Use functions/sub-programs that can add AMGs to the list
#Use functions/sub-programs that can add textures to the AMT
#Borderless models                                                     --COMPLETE
# -- MAYBE -- Model and Animation swaps
#Edit aura files
#Edit moveset files
#Edit SLES files
#Editing AMGs to have multiple model parts and axis
#Have hand and face swaps for B3 and B1


##FEATURES FOR NEXT UPDATE
#B3 to B1 porting                          - DONE
#Custom Shader for B1 to B3 and B4 editing - DONE 
#AMT Editing
#Aura Editing
#Give option to show the stats or not
#AMB editing


##Notes -
#Tkinter for the UI (maybe for a UI friendly release)
#Either put the hex into text or read as hex to edit
#MUST read the AMO0 and AMT as separate (with the AMB as an exception)
#MUST read AMGs as separate (if adding model parts to AMG)
#"Replace All" and "Replace Singular" options
#Manual Axis input for labelling the model selected (or automatic if applicable)
#


##Parts of code to keep
#print(struct.unpack("I", f.read(4))[0])
#print(f.read(-integer-).hex())
#f.write(0x40) -writes 0 0x40 times
#f.write(b'\x40') -writes 0x40 1 time
#import struct
#
#Basically fix the input for a hex value for the shader
#
#Goes back 2 lines befoer the one you've searched for
#head_offsets.append(((f.tell() - 48)))
#print(hex(f.tell() - 48))
#
#bytes(hex(shader), ("utf-8")) -----------THIS PIECE MAKES YOUR LIFE MUCH EASIER AND CONVERTS STUFF TO HEX
#
#shader_number = int(input("Give me the number of the shader you want (do not use '9'): "))
#shader_number = chr(shader_number)
#shader_number = bytes(shader_number, ("utf-8"))
#
#
#f.seek(0,2) - to go to the end of a file
#f.tell() - to find the length of a file
#just x = f.tell() after the f.seek(0,2) to get the length

import struct
#struct.pack("<I", int(21324142))
# < = little endian, > = big endian

#s.encode('utf-16LE')
#s.encode('utf-16BE')



#the function to convert the 46 to a 47 to create a borderless model (and vice versa)
def borderless(f):
    #User input on whther the removal or addition of borders is required
    choice = input("Remove or Add a border? (r/a): ")
    #makes whatever was input by the user all in lowercase
    choice = choice.lower()
    #from that input, it only takes the 1st letter of that string
    choice = choice[0:1]
    #If remove (which is "r") is selected, it proceeds with removing the border (turning all values from 46 to 47)
    if choice == "r":
        #sets the variable "chunk" to be one line of hex (16)
        chunk = f.read(16)
        #creates an array in which offsets will be stored
        offsets = []
        #counter for how many offsets were stored
        counter = 0
        #a while loop that exists for as long as a chunk (16 lines of hex) is NOT equal to a b"" (byte)
        while chunk != b"":
            #if chunk[0] (which is the first hex value in the 16 lines) is equal to 01 and chunk[8] (9th value within the 16) is equal to 46 then
            if chunk[0]== 0x1 and chunk[8] == 0x46:
                #it adds the offset of that line which holds the 01 00 00 .... 46 00 00 .... line 
                offsets.append(((f.tell() - 16)))
                #It also prints it too, I could change this in later updates to be enabled/disabled
                print(hex(f.tell() - 16))
                #adds + 1 to the counter for stats at the end (could also change this later)
                counter += 1
            #for some reason this has to be in place, I think, I don't know, just leave it lol
            chunk = f.read(16)
        #a for loop that goes through the offsets array, and then for each one it will do
        for i in offsets:
            #it goes to that offset and then goes to the 9th value
            f.seek(i+8)
            #it the writes over it, changing the value below it (46), into a 47
            f.write(b"\x47")
            #I had to repeat it since it would not change the end value, there will be a way to fix that but I'm too lazy lol
            f.seek(i+8)
            f.write(b"\x47")
        #simple printing statment that just shows the amount of values changed 
        print("Replaced", counter, "of 46 values with 47")
        print("")
        #closes the file to save space if proceeding to perform other operations with different (or the same) file
        f.close()
        
    #If add is selected, it also proceeds
    #this is the same code as above although with slight tweaks with 47 being changed with 46 and vice versa (only to be used if you had no borders on one model
    #and wanted to add them back on)
    if choice == "a":
        chunk = f.read(16)
        offsets = []
        counter = 0
        while chunk != b"":
            if chunk[0]== 0x1 and chunk[8] == 0x47:
                offsets.append(((f.tell() - 16)))
                print(hex(f.tell() - 16))
                counter += 1
            chunk = f.read(16)
        #print(offsets)
        for i in offsets:
            f.seek(i+8)
            f.write(b"\x46")
            f.seek(i+8)
            f.write(b"\x46")
        print("Replaced", counter, "of 47 values with 46")
        print("")
        f.close()

    
#for correcting B4 01 00 00 B4 01 00 00 (texture) 00 00 00 FF FF FF FF parts with it's shadable variant
def b4_edit(f):
    chunk = f.read(16)
    offsets = []
    counter = 0
    #this is the input from the user to determine the shader value the user wants (if the user inputs "5", the number in hex will be "5", so beware!)
    #this value starts off as an integer
    shader_number = int(input("Give me the number of the shader you want: "))
    #keeps this number as an int for a later print statement
    shader = shader_number
    #converts the integer to a "chr"....whatever the hell THAT is (I found this out by mistake but whatever it is, I'm keeping it lmaos
    shader_number = chr(shader_number)
    #I then convert this value into bytes, in which we see as hex which will be the shader number input over the first FF in the 4 FFs
    shader_number = bytes(shader_number, ("utf-8"))
    while chunk != b"":
        if chunk[0]== 0xB4 and chunk[12] == 0xFF:
            offsets.append(((f.tell() - 16)))
            print(hex(f.tell() - 16))
            counter += 1
        chunk = f.read(16)
    #for each offset, it will go to it and then write over each line 
    for i in offsets:
        #this goes to the first 01 in B4 01 00 00
        f.seek(i+1)
        #replaces it with 62
        f.write(b"\x62")
        #this goes to the second B4 in B4 01 00 00
        f.seek(i+4)
        #this then replaces it with BD
        f.write(b"\xBD")
        #the 01 after
        f.seek(i+5)
        #then replace with 29
        f.write(b"\x29")
        #where the first FF is
        f.seek(i+12)
        #replace with the shader number
        f.write(shader_number)
        f.seek(i+13)
        #it the writes over the rest of the FFs with 00s
        f.write(b"\x00")
        f.seek(i+14)
        f.write(b"\x00")
        f.seek(i+15)
        f.write(b"\x00")
    #print statement which shows how many B4 01s were replaced and given what shader
    print("Replaced", counter, "FFs with 0" + str(shader) + " 00 00 00 as shader number")
    print("")
    f.close()
        
        
#to convert Budokai 1 model into Budokai 3 format
def b1_edit(f):
    chunk = f.read(16)
    offsets = []
    counter = 0
    shader_number = int(input("Give me the number of the shader you want: "))
    shader = shader_number
    shader_number = chr(shader_number)
    shader_number = bytes(shader_number, ("utf-8"))
    #this while loop differs since it contains 2 if statements, all this means is that in order to append to the "offsets" array, it will need to look for 2 things
    while chunk != b"":
        #BD 11 00 00 BD 01 00 00 model parts
        if chunk[0]== 0xBD and chunk[1] == 0x11:
            offsets.append(((f.tell() - 16)))
            print(hex(f.tell() - 16))
            counter += 1
        #and BD 01 00 00 BD 01 00 00 parts
        if chunk[0]== 0xBD and chunk[1] == 0x01:
            offsets.append(((f.tell() - 16)))
            print(hex(f.tell() - 16))
            counter += 1
        chunk = f.read(16)
    #once more, it reads from the offsets and replaces what is needed to be replaced 
    for i in offsets:
        f.seek(i+0)
        f.write(b"\xB5")
        f.seek(i+1)
        f.write(b"\x01")
        f.seek(i+4)
        f.write(b"\xBD")
        f.seek(i+5)
        f.write(b"\x29")
        f.seek(i+12)
        f.write(shader_number)
        f.seek(i+13)
        f.write(b"\x00")
        f.seek(i+14)
        f.write(b"\x00")
        f.seek(i+15)
        f.write(b"\x00")
        f.seek(i+32) #00 00 80 3F parts
        f.write(b"\x00")
        f.seek(i+33)
        f.write(b"\x00")
        f.seek(i+34)
        f.write(b"\x80")
        f.seek(i+35)
        f.write(b"\x3f")
        f.seek(i+36)
        f.write(b"\x00")
        f.seek(i+37)
        f.write(b"\x00")
        f.seek(i+38)
        f.write(b"\x80")
        f.seek(i+39)
        f.write(b"\x3f")
        f.seek(i+40)
        f.write(b"\x00")
        f.seek(i+41)
        f.write(b"\x00")
        f.seek(i+42)
        f.write(b"\x80")
        f.seek(i+43)
        f.write(b"\x3f")
        f.seek(i+44)
        f.write(b"\x00")
        f.seek(i+45)
        f.write(b"\x00")
        f.seek(i+46)
        f.write(b"\x80")
        f.seek(i+47)
        f.write(b"\x3f")
        f.seek(i+48) #Next line
        f.write(b"\x00")
        f.seek(i+49)
        f.write(b"\x00")
        f.seek(i+50)
        f.write(b"\x80")
        f.seek(i+51)
        f.write(b"\x3f")
        f.seek(i+52)
        f.write(b"\x00")
        f.seek(i+53)
        f.write(b"\x00")
        f.seek(i+54)
        f.write(b"\x80")
        f.seek(i+55)
        f.write(b"\x3f")
        f.seek(i+56)
        f.write(b"\x00")
        f.seek(i+57)
        f.write(b"\x00")
        f.seek(i+58)
        f.write(b"\x80")
        f.seek(i+59)
        f.write(b"\x3f")
        f.seek(i+60)
        f.write(b"\x00")
        f.seek(i+61)
        f.write(b"\x00")
        f.seek(i+62)
        f.write(b"\x80")
        f.seek(i+63)
        f.write(b"\x3f")

    #basic print statement
    print(str(counter) + " model parts of Budokai 1 model converted to Budokai 3 with shader as 0" + str(shader) + " 00 00 00")
    print("")
    f.close()



#For converting Budokai 3 to Budokai 1, it is essentially the reverse of above
def b3_edit(f):
    chunk = f.read(16)
    offsets = []
    counter = 0
    while chunk != b"":
        if chunk[0]== 0xB5 and chunk[1] == 0x01:
            offsets.append(((f.tell() - 16)))
            print(hex(f.tell() - 16))
            counter += 1
        chunk = f.read(16)
    #print(offsets)
    for i in offsets:
        f.seek(i+0)
        f.write(b"\x35")
        f.seek(i+1)
        f.write(b"\x62")
        f.seek(i+4)
        f.write(b"\x35")
        f.seek(i+5)
        f.write(b"\x62")
        f.seek(i+12)
        f.write(b"\xFF")
        f.seek(i+13)
        f.write(b"\xFF")
        f.seek(i+14)
        f.write(b"\xFF")
        f.seek(i+15)
        f.write(b"\xFF")
        f.seek(i+32) #00 00 80 3F parts
        f.write(b"\xCD")
        f.seek(i+33)
        f.write(b"\xCC")
        f.seek(i+34)
        f.write(b"\x4C")
        f.seek(i+35)
        f.write(b"\x3f")
        f.seek(i+36)
        f.write(b"\xCD")
        f.seek(i+37)
        f.write(b"\xCC")
        f.seek(i+38)
        f.write(b"\x4C")
        f.seek(i+39)
        f.write(b"\x3f")
        f.seek(i+40)
        f.write(b"\x66")
        f.seek(i+41)
        f.write(b"\x66")
        f.seek(i+42)
        f.write(b"\x66")
        f.seek(i+43)
        f.write(b"\x3f")
        f.seek(i+44)
        f.write(b"\x00")
        f.seek(i+45)
        f.write(b"\x00")
        f.seek(i+46)
        f.write(b"\x80")
        f.seek(i+47)
        f.write(b"\x3f")
        f.seek(i+48) #Next line
        f.write(b"\x00")
        f.seek(i+49)
        f.write(b"\x00")
        f.seek(i+50)
        f.write(b"\x00")
        f.seek(i+51)
        f.write(b"\x43")
        f.seek(i+52)
        f.write(b"\x00")
        f.seek(i+53)
        f.write(b"\x00")
        f.seek(i+54)
        f.write(b"\x00")
        f.seek(i+55)
        f.write(b"\x43")
        f.seek(i+56)
        f.write(b"\x00")
        f.seek(i+57)
        f.write(b"\x00")
        f.seek(i+58)
        f.write(b"\x00")
        f.seek(i+59)
        f.write(b"\x43")
        f.seek(i+60)
        f.write(b"\x00")
        f.seek(i+61)
        f.write(b"\x00")
        f.seek(i+62)
        f.write(b"\x00")
        f.seek(i+63)
        f.write(b"\x43")
        
    print("Budokai 3 model converted to Budokai 1")
    print("")
    f.close()

#Old AMT editing code
def amt_edit(f):
    head = open("FILES/tex_head.bin", "r+b")
    tex1 = open("FILES/tex_1.bin", "r+b")
    tex2 = open("FILES/tex_2.bin", "r+b")
    chunk = f.read(16)
    chunk_head = head.read(16)
    chunk_tex1 = tex1.read(16)
    chunk_tex2 = tex2.read(16)
    counter = 0
    head_offsets = []
    head_values = []



    #this looks for the end line of each header and saves it's slot where it will be saved
    while chunk != b"":
        if chunk[0]== 0x00 and chunk[1]== 0x00 and chunk[2]== 0x00 and chunk[3]== 0x00 and chunk[13] == 0xFF and chunk[14] == 0x00 and chunk[15] == 0x00:
            head_offsets.append(((f.tell())))
            print(hex(f.tell()))
            counter += 1
        chunk = f.read(16)

    #this copies the values and places it in the amt file 
    while chunk_head != b"":
        print(head_values) ####Do stuff here
    
    f.seek(head_offsets[0]) #Offset to after the last header
    
    
    
    

    
    f.close()
    head.close()
    tex1.close()
    tex2.close()
    
    #read in the tex256 file(f), separate it or set some pointers
    #read in the tex_head file(head), place it where it should be, change the values as necessary
    #read in the tex_1(tex1) and tex_2(tex2) files and place it where needed and change values of tex_head
    #make sure that the line containing heads are not full and if so, add one more and change values





#unwanted amt code (or needing revised)
def new_amt_edit(f):
    #Create a new texture file, and have each texture added onto the new templates
    #With every 5 textures, a new line is placed (as the 5th line would be placed on the new line)
    #Add shaders and textures (64x64 with 256 and 256x256 with 256)

    
    #Opening files

    tex_head = open("FILES/tex_head.bin", "r+b")
    tex_1 = open("FILES/tex_1.bin", "r+b")
    tex_2 = open("FILES/tex_2.bin", "r+b")
    
    shad_head = open("FILES/shad_head.bin", "r+b")
    shad_1 = open("FILES/shad_1.bin", "r+b")
    shad_2 = open("FILES/shad_2.bin", "r+b")
    
    main = open("FILES/main.bin", "r+b")
    line = open("FILES/extra_line.bin", "r+b")
    

    #Reading lines
    chunk = f.read(16)
    
    chunk_tex_head = tex_head.read(16)
    chunk_tex_1 = tex_1.read(16)
    chunk_tex_2 = tex_2.read(16)
    
    chunk_shad_head = shad_head.read(16)
    chunk_shad_1 = shad_1.read(16)
    chunk_shad_2 = shad_2.read(16)
    
    chunk_main = main.read(16)
    chunk_line = line.read(16)

    #arrays
    main_values = []
    line_values = []
    
    #Counters and placers

    #Actual code
    #be sure to actually use f.whatever() so that the empty file can be used 
    #If statement where you ask how many textures to be added with every 5 meaning to add a new line

    while chunk_main != b"":
        if chunk_main:
            main_values.append(f.read) #Somehow copy data, append it and write it

    print(main_values)





    
    tex_head.close()
    tex_1.close()
    tex_2.close()
    shad_head.close()
    shad_1.close()
    shad_2.close()
    main.close()
    line.close()
    f.close()
    
   
#incomplete aura editing code
def aura_edit(f):
    print("aura stuff")
    f.close()

#New AMT code
def amt_edit_new(f):
    print("amt stuff")

    #open the AMT, ask how many textures there are, determine if a line must be implemented, then add each texture
    
    
    
    f.close()
    

#AMB combining code
def amb_combine(f, m, t):
    offsets = []
    
    #Opens the AMB as a file that has files inserted into it (output), and the model as the file to be inserted (input)
    with open(f, "r+b") as output, open(m, "r+b") as input:
        #goes to the end of the AMB
        output.seek(64)
        #creates a variable that reads all the file
        data = input.read()
        #it then writes all the file (data), into output (the amb)
        output.write(data)

    #Opens the AMB as a file that has files inserted into it (output), and the texture as the file to be inserted (input)
    with open(f, "a+b") as output, open(t, "r+b") as input:
        data = input.read()
        output.write(data)

    #closes both files
    output.close()
    input.close()

    #opens the AMT
    amt = open(t, "r+b")
    #goes to the end of the file
    amt.seek(0,2)
    #sets the amt_length variable to whatever is told by the program
    amt_length = amt.tell()
    #closes the AMT file
    amt.close()

    #opens the AMB file
    f = open("amb.bin", "r+b")
    chunk = f.read(16)

    #Just searches for the line that begins with AMT, then saves it's location
    while chunk != b"":
        if chunk[0]== 0x23 and chunk[1] == 0x41 and chunk[2]== 0x4D and chunk[3] == 0x54:
            offsets.append(((f.tell() - 16)))
            

        chunk = f.read(16)

    #Goes to the AMB length of the AMO, then writes it down
    f.seek(36)
    f.write(struct.pack("<I", (offsets[0] - 64)))

    #Goes to the AMB location of the AMT, then writes it down
    f.seek(48)
    f.write(struct.pack("<I", offsets[0]))

    #Goes to the AMB length of AMT, then writes it down
    f.seek(52)
    f.write(struct.pack("<I", amt_length))
    
    
    #prints some stuff
    print("AMO and AMT have been added with the AMB adjusted")
    print("")
        
    
    

#Start of the program where you input the file and choose your option
print("Welcome to the Budokai 3 Modding tool!")
print("")
print("Please read the 'Tutorial.txt' file for more information and a mini walkthrough for this tool!")
print("")
#Infinite Loop
while True:
    x = input("Name of file (with extension): ")
    f = open(x, "r+b")
    print("")



    #just prints what you can do as options
    options = ["border", "b1 convert", "b4 edit", "b3 convert", "amt edit", "amb combine"]
    print(options)
    print("")
    print("")
    print("Using 'border' removes or adds borders to a model")
    print("")
    print("Using 'b1 convert' changes Budokai 1 files into Budokai 3 format with shading (with a set shader only)")
    print("")
    print("Using 'b4 edit' changes all the B4 01 lines in a character file to be shadable (with a set shader only)")
    print("")
    print("Use the 'amb.bin' file for importing IW or B1 files into Budokai 3")
    print("")
    
    #Asks what you want to do with the file
    choice = input("What would you like to do: ")
    choice = choice.lower()
    print("")
    #While you keep putting the wrong name from the options list, you keep trying
    while choice not in options:
        choice = input("That is not a valid choice, please pick from above: ")
        print("")
    #If is border, go to border and so on
    if choice == "border":
        borderless(f)
    if choice == "b4 edit":
        b4_edit(f)
    if choice == "b1 convert":
        b1_edit(f)
    if choice == "b3 convert":
        b3_edit(f)
    if choice == "amt edit":
        amt_edit_new(f)
    if choice == "amb combine":
        f.close()
        f = "amb.bin"
        m = input("Give me the AMO name to add in the AMB: ")
        t = input("Give me the AMT name to add in the AMB: ")
        amb_combine(f, m, t)

        

        

#Open Source Code Notes -
#
#For anyone who is new or unsure of Python, this is __N _ O _ T __ for first time (or beginner) users or Python,
#learn basics and principles first before coming near this mess
#
#I will be keeping copies of this and of each working stages of this program as we progress, just so we have states to revert to in case of failure
#
#We could perhaps have people working on different sections of the program in order to speed up progress of development
#
#Someone couldwork on framework and a UI version of this tool and import the functions and extras onto a UI as well
#


