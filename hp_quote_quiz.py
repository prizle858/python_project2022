import pandas as pd
import random

# read all the files 
hp1 = pd.read_csv('Harry Potter 1.csv', delimiter = ";")
hp2 = pd.read_csv('Harry Potter 2.csv', delimiter = ";")
hp3 = pd.read_csv('Harry Potter 3.csv', delimiter = ";")

# change column names to lower case ones
hp3.columns = ["Character", "Sentence"]

# reformatting such that just first letter is capitalize
hp2["Character"] = hp2["Character"].str.lower().str.capitalize()
hp3["Character"] = hp3["Character"].str.lower().str.capitalize()

def random_quote_hp():
    """"Returns random quote of one of the Harry Potter film scripts and the character that said that"""
    
    # choose a random data set
    dataset = random.choice([hp1, hp2, hp3])
    
    # save in which film the quote occurs
    film = 1 if dataset.equals(hp1) else (2 if dataset.equals(hp2) else 3)
    
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
    
        # extend quote if character says somthing afterwards
        if(dataset["Character"][line+i] == character and end == True):
            quote += " " + dataset["Sentence"][line+i]

        else: 
            end = False
           
    return quote, character, film


def create_quotes(n=10):
    """Creates n random quotes"""
    quotes = []

    # create n random quotes
    for i in range(n): 
        # create random quote 
        q = random_quote_hp()
        
        # ensure sufficient length of the quote -> not less than 5 words
        while(q[0].count(" ") < 5):
            # create random quote 
            q = random_quote_hp()
 
        quotes.append(q)
    
    return quotes

def quote_quiz(n=10):
    """Performs the Harry Potter Quote Quiz"""
    
    print(f"""Welcome to the Harry Potter Quote Quiz!

    In the following you will be ask {n} questions. Your task is to guess which character said it. Each correct answer earns you one 
    point. Furthermore, you can get bonus points, if you also know from which movie the quote is. All quotes are from the first 3 movies.  

    Let the test begin!
    """)
    
    score = 0
    bonus = 0
    
    # create amount of quote questions
    quotes = create_quotes(n)
        
    # asks the quote questions and count points
    for q in quotes: 
        answer = input(f"Who said the follwing? \n'{q[0]}'")
    
        if(answer == q[1]): 
            print("Your answer was correct!\n")
            score += 1
        else:
            print(f"Your answer was wrong! Actually, {q[1]} said that\n")
    
        film = int(input("Bonus: From which movie is the quote?"))
    
        if(film == q[2]):
            print("Your answer was correct!\n")
            bonus += 1
        else:
            print(f"Your answer was wrong! Actually, the quote is from {q[2]} movie\n")
    
    print(f"Your final score is: {score} and you have reached {bonus} bonus points.")
    
    return score, bonus

quote_quiz(3)