# import all necessary libaries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# refining dataframe
# read the files
hp = pd.read_csv('dataset/Characters.csv', delimiter = ";")

# reduce the dataframe to the necessary size
hp = hp[['Gender', 'House', 'Blood status', 'Hair colour', 'Eye colour', 'Loyalty']]

# replace some column labels so that it is easier to code e.g. when using hp.bloodstatus.values.tolist()
hp.columns = hp.columns.str.replace("Gender", "gender")
hp.columns = hp.columns.str.replace("Blood status", "bloodstatus")
hp.columns = hp.columns.str.replace("Hair colour", "haircolour")
hp.columns = hp.columns.str.replace("Eye colour", "eyecolour")
hp.columns = hp.columns.str.replace("Loyalty", "loyalty")


# unit ambiguous labels to one label
hp["bloodstatus"] = hp["bloodstatus"].replace(["Pure-blood or Half-blood", "Pure-blood or half-blood", "Half-blood or pure-blood"], "Pure-blood or half-blood")
hp["bloodstatus"] = hp["bloodstatus"].str.strip(']').str.strip('[')

# remove rows with certain labels, which in this case are outliers
outlier1 = ["Unknown", "Part-Human (Half-giant)", "Quarter-Veela", "Part-Goblin", "Squib", "Muggle"]
for i in outlier1:
    hp = hp.loc[hp['bloodstatus'] != i]

# unit ambiguous labels to one label
hp["haircolour"] = hp["haircolour"].replace(["Blond", "White-blond", "Silvery-blonde", "White blond", "Straw blond", "Reddish-blonde", "Dirty-blonde", "Sandy", "Straw-coloured"], "Blonde")
hp["haircolour"] = hp["haircolour"].replace(["Grey", "Silver", "Silver| formerly auburn", "Silver| formerly black", "White (balding)", "Iron grey", "White"], "Silver / White / Grey")
hp["haircolour"] = hp["haircolour"].replace(["Red ", "Ginger", "Red brown", "Brown/greying", "Auburn"], "Red")
hp["haircolour"] = hp["haircolour"].replace(["Bald", "Colourless and balding"], "Bald")
hp["haircolour"] = hp["haircolour"].replace(["Black", "Jet-black", "Colourless and balding"], "Dark")
hp["haircolour"] = hp["haircolour"].replace(["Mousy brown", "Reddish-brown", "Tawny", "Mousy", "Light brown flecked with grey"], "Brown")

# remove rows with certain labels, which in this case are outliers
outlier2 = ["Variable", "Green"]
for i in outlier2:
    hp = hp.loc[hp['haircolour'] != i]

# unit ambiguous labels to one label
hp["eyecolour"] = hp["eyecolour"].replace(["Bright green", "Gooseberry"], "Green")
hp["eyecolour"] = hp["eyecolour"].replace(["Bright brown", "Scarlet ", "Ruddy", "Hazel"], "Brown")
hp["eyecolour"] = hp["eyecolour"].replace(["Black"], "Dark")
hp["eyecolour"] = hp["eyecolour"].replace(["Bright Blue", "Grey/Blue[", "Astonishingly blue"], "Blue")
hp["eyecolour"] = hp["eyecolour"].replace(["Pale silvery", "Silvery", "Dark Grey"], "Grey")

# remove rows with certain labels, which in this case are outliers
outlier3 = ["One dark, one electric blue", "Pale, freckled", "Yellowish", "Yellow"]
for i in outlier3:
    hp = hp.loc[hp['eyecolour'] != i]

# unit ambiguous labels to one label
hp.loyalty = hp.loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Dumbledore" in x) else x) 
hp.loyalty = hp.loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Phoenix" in x) else x) 
hp.loyalty = hp.loyalty.apply(lambda x: "Lord Voldemort" if not pd.isnull(x) and ("Voldemort" in x) else x)
hp["loyalty"] = hp["loyalty"].replace(["Minister of Magic"], "Ministry of Magic")
hp["loyalty"] = hp["loyalty"].replace(["Hogwarts School of Witchcraft and Wizardry"], "Hogwarts School")

# remove rows with certain labels, which in this case are outliers
outlier4 = ["Gellert Grindelwald's Acolytes"]
for i in outlier4:
    hp = hp.loc[hp['loyalty'] != i]

# preparing lists to insert the data in order of 'gender', 'Blood status', 'Hair colour', 'Eye colour', 'loyalty' 
# create 2D house lists of traits in each hous [['gender'], ['Blood status'], ['Hair colour'], ['Eye colour'], ['loyalty']]
gryffindor = [] 
hufflepuff = [] 
ravenclaw = [] 
slytherin = []

# get the list of houses in order to sort them according to the gender, blood status, hair colour, eye colour, and loyalty
houselist = np.unique(hp.House.values.tolist())
houselist = houselist[1:5] # remove 'Durmstrang Institute' and 'nan'

gender_index = 0 # for future indexing of each house list
gender = np.unique(hp.gender.values.tolist())
gender = [x for x in gender if str(x) != 'nan'] # remove 'nan'

bloodstatus_index = 1
bloodstatus = np.unique(hp.bloodstatus.values.tolist())
bloodstatus = bloodstatus[0:4] # remove 'Pure-blood or half-blood' and 'nan'
bloodstatus = np.delete(bloodstatus, 2, 0) # remove 'Muggle-born or half-blood'

haircolour_index = 2
haircolour = np.unique(hp.haircolour.values.tolist())
haircolour = [x for x in haircolour if str(x) != 'nan'] # remove 'nan'

eyecolour_index = 3
eyecolour = np.unique(hp.eyecolour.values.tolist())
eyecolour = [x for x in eyecolour if str(x) != 'nan'] # remove 'nan'

loyalty_index = 4
loyalty = np.unique(hp.loyalty.values.tolist())
loyalty = [x for x in loyalty if str(x) != 'nan'] # remove 'nan'

def func(traitlist):
    # inserting data into 2D list 
    gryffindor_list = [] # number of people with certain traits in Gryffindor
    hufflepuff_list = [] # number of people with certain traits in Hufflepuff
    ravenclaw_list = []  # number of people with certain traits in Ravenclaw
    slytherin_list = []  # number of people with certain traits in Slytherin

    for house in houselist: 
        for trait in traitlist:
            
            # if traitlist == gender:
            #     column = "gender"
            # elif traitlist == bloodstatus:
            #     column = "bloodstatus"
            # elif traitlist == eyecolour:
            #     column = "eyecolour"
            # elif traitlist == haircolour:
            #     column = "haircolour"
            # elif traitlist == loyalty:
            #     column = "loyalty"
            # else:
            #     pass

            # reduce the dataframe from hp to df so that the column is house and row is blood

            column = str(traitlist)
            df = hp.loc[(hp['House'] == house) & (hp[column] == trait)]
            num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
                
            if house == 'Gryffindor':
                gryffindor_list.append(num_row_df)
            elif house == 'Hufflepuff':
                hufflepuff_list.append(num_row_df)
            elif house == 'Ravenclaw':
                ravenclaw_list.append(num_row_df)
            elif house == 'Slytherin':
                slytherin_list.append(num_row_df)

    gryffindor.append(gryffindor_list) # list gryffindor_list is appended to the list gryffindor
    hufflepuff.append(hufflepuff_list) # list hufflepuff_list is appended to the list hufflepuff
    ravenclaw.append(ravenclaw_list)   # list ravenclaw_list is appended to the list ravenclaw
    slytherin.append(slytherin_list)   # list slytherin_list is appended to the list slytherin

# col_list = hp.columns.values.tolist()

# for traitlist in col_list:
#     func(traitlist)

func(gender)
func(bloodstatus)
func(haircolour)
func(eyecolour)
func(loyalty)

def plot(n):
    '''plot is about gender, bloodstatus, haircolour, eyecolour, or loyalty depending on the house.
    the plot is about gender when n= 0, bloodstatus when n= 1, haircolour when n= 2, eyecolour when n= 3, loyalty when n = 4'''

    fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize=(10,10))
    try: 
        for row in [0,1]:
            for col in [0,1]:
                        if row == 0 and col == 0:   # upper left plot
                            x = gryffindor[n]       # e.g. if n = 0, it will be indicating to list of ['Female', 'Male'] in Gryffindor, 
                            title = 'Gryffindor'    # which is in index 0 in the list gryffindor
                        elif row == 0 and col == 1: # upper right plot
                            x = hufflepuff[n]
                            title = 'Hufflepuff'
                        elif row == 1 and col == 0: # botton left plot
                            x = ravenclaw[n]
                            title = 'Ravenclaw'
                        else:                       # bottom right plot
                            x = slytherin[n]
                            title = 'Slytherin'

                        axs[row, col].pie(x, shadow=True, startangle = 90) # create pie plots
                        axs[row, col].set_title(title) 

            if n == gender_index: 
                fig.legend(labels=gender,   # the labels for each line
                    loc="center",           # position of legend
                    borderaxespad=0.1,      # small spacing around legend box
                    title="gender",         # title for the legend
                    fontsize=12             # to make the legend fit the plot
                    )
            elif n == bloodstatus_index:
                fig.legend(labels=bloodstatus, # the labels for each line
                    loc="center",              # position of legend
                    borderaxespad=0.1,         # small spacing around legend box
                    title="Bloodstatus",       # title for the legend
                    fontsize=12                # to make the legend fit the plot
                    )
            elif n == haircolour_index:
                fig.legend(labels=haircolour,  # the labels for each line
                    loc="center",              # position of legend
                    borderaxespad=0.1,         # small spacing around legend box
                    title="Haircolour",        # title for the legend
                    fontsize=12                # to make the legend fit the plot
                    )
            elif n == eyecolour_index:
                fig.legend(labels=eyecolour,  # the labels for each line
                    loc="center",             # position of legend
                    borderaxespad=0.1,        # small spacing around legend box
                    title="Eyecolour",        # title for the legend
                    fontsize=12               # to make the legend fit the plot
                    )
            elif n == loyalty_index:
                fig.legend(labels=loyalty,   # the labels for each line
                    loc="center",            # position of legend
                    borderaxespad=0.1,       # small spacing around legend box
                    title="loyalty",         # title for the legend
                    fontsize=12              # to make the legend fit the plot
                    )
    except IndexError:
        print("n should be in range from 0 to 4.") # in case n is out of range from 0 to 4
       

# use explode, explode = (0.05, 0.05, 0.05, 0.05, 0.05)
# donut plot 
    # draw circle
    # centre_circle = plt.Circle((0, 0), 0.70, fc='black') # readjust color depending on background
    # fig = plt.gcf()
    # # Adding Circle in Pie chart
    # fig.gca().add_artist(centre_circle)

plot(0)
plot(1)
plot(2)
plot(3)
plot(4)

plt.show()

