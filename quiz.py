import pandas as pd
import random
import distance
import matplotlib.pyplot as plt
import numpy as np

def preprocessing():

    # read all CSV files
    hp1 = pd.read_csv('dataset/Harry Potter 1.csv', delimiter = ";")
    hp2 = pd.read_csv('dataset/Harry Potter 2.csv', delimiter = ";")
    hp3 = pd.read_csv('dataset/Harry Potter 3.csv', delimiter = ";")

    # unify column names
    hp3.columns = ["Character", "Sentence"]

    # unify characters
    # all character names are capitalize and have no spaces at the beggining and end
    hp1["Character"] = hp1["Character"].str.lower().str.strip().str.title()
    hp2["Character"] = hp2["Character"].str.lower().str.strip().str.title()
    hp3["Character"] = hp3["Character"].str.lower().str.strip().str.title()

    hp1["Character"].replace("Hermoine", "Hermione", inplace=True)
    
    return [hp1, hp2, hp3]

def random_quote(data):
    """"Returns random quote of one of the Harry Potter film scripts and the character that said that"""
    
    # choose a random data set
    dataset = random.choice(data)
    
    # save in which film the quote occurs
    film = 1 if dataset.equals(data[0]) else (2 if dataset.equals(data[1]) else 3)
        
    # choose a random line
    line = random.randrange(0, len(dataset))
    
    # save quote and character
    quote = dataset["Sentence"][line]
    character = dataset["Character"][line]
    
    start = True
    end = True 
    # extend quote if possible
    for i in range(1, 4):        
        # extend quote if character says something beforehand
        if(dataset["Character"][line-i] == character and start == True):                
            quote = dataset["Sentence"][line-i] + " " + quote
        else: 
            start = False
    
        # extend quote if character says something afterwards
        if(dataset["Character"][line+i] == character and end == True):
            quote += " " + dataset["Sentence"][line+i]

        else: 
            end = False
           
    return quote, character, film

def create_quotes(data, n=10):
    """Creates n random quotes"""
    quotes = []

    # create n random quotes
    for i in range(n): 
        # create random quote 
        q = random_quote(data)
        
        # ensure sufficient length of the quote -> not less than 5 words
        while(q[0].count(" ") < 5):
            # create random quote 
            q = random_quote(data)
 
        quotes.append(q)
    
    return quotes

def answer_evaluation(answer, character):
    # makes checking easier
    answer = answer.lower().strip()
    
    if(len(answer) < 3):
        return False
    
    # check for correct answer
    if(answer == character):
        return True
    
    # answer in name
    if((len(answer) > 3) and (answer in character)):
        return True
    
    # spelling mistakes
    if(distance.levenshtein(character, answer) < 4):
        return True
    
    # synonymous names
    if((answer and character) in ["draco", "malfoy"]):
        return True
    elif((answer and character) in ["mrs. weasley", "molly", "molly weasley"]):
        return True
    elif((answer and character) in ["mrs. dursley", "aunt petunia", "petunia", "petunia dursley"]):
        return True
    elif((answer and character) in ["aunt marge", "marge", "marjorie dursley", "marjorie eileen dursely"]):
        return True
    elif((answer and character) in ["lord voldemort", "voldemort", "voldemord", "tom riddle", "riddle", "tom"]):
        return True
    elif((answer and character) in ["arthur", "arthur weasley", "mr. weasley"]):
        return True
    
    return False

def quote_quiz(data, n=10):
    """Performs the Harry Potter Quote Quiz"""
    
    # save the movie names
    film_names = ("Harry Potter and the Philosopher’s Stone", "Harry Potter and the Chamber of Secrets", "Harry Potter and the Prisoner of Azkaban")
    
    score = 0
    bonus = 0
    
    # create amount of quote questions
    quotes = create_quotes(data, n)
        
    # asks the quote questions and count points
    for q in quotes: 
        answer = input(f"Who said the following? \n'{q[0]}'")
        print(f"Your answer: {answer}")
        
        if(answer_evaluation(answer, q[1])): 
            print("Your answer was correct!\n")
            score += 1            
        else:
            print(f"Your answer was wrong! Actually, {q[1].title()} said that\n")
        
        film = int(input("Bonus: From which movie is the quote? Pick 1 for Harry Potter and the Philosopher’s Stone, 2 for Harry Potter and the Chamber of Secrets, 3 for Harry Potter and the Prisoner of Azkaban."))
        print(f"Your answer: {film}")
        
        
        if(film == q[2] and film<4):
            print("Your answer was correct!\n")
            bonus += 1
        else:
            print(f"Your answer was wrong! Actually, the quote is from the movie {q[2]}: {film_names[q[2]-1]}.\n")
    
    print(f"Final score: {score} \nBonus points: {bonus}")
    
    return score, bonus

def plot(data):
    """Plots the line distribution of each movie and the amount of lines of Harry, Hermione, and Ron compared"""
    hp1 = data[0]
    hp2 = data[1]
    hp3 = data[2]
    
    # get the amount of lines of each character
    count_hp1 = hp1["Character"].value_counts()
    count_hp2 = hp2["Character"].value_counts()
    count_hp3 = hp3["Character"].value_counts()
    
    # preprocessing counts
    # sum up line counts of all characters except the top 5
    split_hp1 = np.split(count_hp1, [5])
    split_hp2 = np.split(count_hp2, [5])
    split_hp3 = np.split(count_hp3, [5])
    count_hp1 = pd.concat([split_hp1[0], pd.Series([split_hp1[1].sum()], index=["others"])])
    count_hp2 = pd.concat([split_hp2[0], pd.Series([split_hp2[1].sum()], index=["others"])])
    count_hp3 = pd.concat([split_hp3[0], pd.Series([split_hp3[1].sum()], index=["others"])])
    
    # create plot 
    fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize=(30,20))
    fig.tight_layout()
    
    # add plot titles
    ax[0,0].set_title('Harry Potter and the Philosopher’s Stone', fontsize=28, horizontalalignment="center", fontweight="bold")
    ax[0,1].set_title('Harry Potter and the Chamber of Secrets', fontsize=28, horizontalalignment="center", fontweight="bold")
    ax[1,0].set_title('Harry Potter and the Prisoner of Azkaban', fontsize=28, horizontalalignment="center", fontweight="bold")
    ax[1,1].set_title('All movies - Line Distribution of Harry, Ron, and Hermione', fontsize=28, horizontalalignment="center", fontweight="bold")
    
    
    def func(pct, allvalues):
        """Returns the layout for the percentages/numbers inside the pie charts"""
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d} lines)".format(pct, absolute)
    
    # create pie chart of the line distribution of each movie and add its legend
    wedges1, texts1, autotexts1 = ax[0,0].pie(count_hp1, autopct = lambda pct: func(pct, count_hp1))
    ax[0,0].legend(wedges1, count_hp1.index, title="Characters", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20, title_fontsize=25)
    wedges2, texts2, autotexts2 = ax[0,1].pie(count_hp2, autopct = lambda pct: func(pct, count_hp2))
    ax[0,1].legend(wedges2, count_hp2.index, title="Characters", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20, title_fontsize=25)
    wedges3, texts3, autotexts3 = ax[1,0].pie(count_hp3, autopct = lambda pct: func(pct, count_hp3))
    ax[1,0].legend(wedges3, count_hp3.index, title="Characters", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20, title_fontsize=25)
    
    # create stacked bar plot of the total amount of lines of Harry, Ron, and Hermione for each movie
    # create the according legend
    ax[1,1].bar(["Movie 1", "Movie 2", "Movie 3"], [count_hp1.loc["Harry"], count_hp2.loc["Harry"], count_hp3.loc["Harry"]], width=0.5)
    ax[1,1].bar(["Movie 1", "Movie 2", "Movie 3"], [count_hp1.loc["Ron"], count_hp2.loc["Ron"], count_hp3.loc["Ron"]], bottom=[count_hp1.loc["Harry"], count_hp2.loc["Harry"], count_hp3.loc["Harry"]], width=0.5)
    ax[1,1].bar(["Movie 1", "Movie 2", "Movie 3"], [count_hp1.loc["Hermione"], count_hp2.loc["Hermione"], count_hp3.loc["Hermione"]], bottom=[count_hp1.loc["Harry"]+count_hp1.loc["Ron"], count_hp2.loc["Harry"]+count_hp2.loc["Ron"], count_hp3.loc["Harry"]+count_hp3.loc["Ron"]], width=0.5)
    ax[1,1].legend(["Harry", "Ron", "Hermione"], title="Character", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20, title_fontsize=25)
    
    # change size and font of percentages in pie charts
    plt.setp(autotexts1, size=15, weight="bold")
    plt.setp(autotexts2, size=15, weight="bold")
    plt.setp(autotexts3, size=15, weight="bold")
    
    # hide yaxis of stacked bar plot
    # higher font size of x-ticks
    ax[1,1].get_yaxis().set_visible(False)
    ax[1,1].tick_params(labelsize=25)
     
    plt.show()