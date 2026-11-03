import os
import random
import time
import pandas as pd
from colorama import Fore, init

# Initialize Colorama for colored terminal output
init(autoreset=True)

def dots(message="Fetching recommendations"):
    """Displays an animated loading sequence."""
    print(Fore.YELLOW + message, end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("\n")

def create_sample_dataset():
    """Generates a sample IMDb dataset if 'imdb_top_1000.csv' is missing."""
    data = {
        'Series_Title': [
            'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 
            'Pulp Fiction', 'Forrest Gump', 'Inception', 'Fight Club', 
            'Interstellar', 'Parasite', 'Gladiator', 'Whiplash', 'The Prestige'
        ],
        'Genre': [
            'Drama', 'Crime', 'Action', 'Crime', 'Drama', 
            'Action', 'Drama', 'Adventure', 'Drama', 'Action', 'Drama', 'Drama'
        ],
        'IMDB_Rating': [9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.8, 8.6, 8.5, 8.5, 8.5, 8.5],
        'Overview': [
            'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.',
            'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests.',
            'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
            'The presidencies of Kennedy and Johnson, the Vietnam War, and other history unfold from the perspective of an Alabama man with an IQ of 75.',
            'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.',
            'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more.',
            'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
            'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
            'A former Roman general sets out to exact vengeance against the corrupt emperor who murdered his family.',
            'A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor.',
            'After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything.'
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv("imdb_top_1000.csv", index=False)

def analyze_sentiment(text):
    """Basic keyword-based sentiment analyzer for movie overviews."""
    positive_words = {'redemption', 'solace', 'decency', 'survive', 'survival', 'love', 'triumph', 'greatness', 'success', 'family'}
    negative_words = {'chaos', 'menace', 'violence', 'murder', 'corrupt', 'tragic', 'destitute', 'greed', 'discrimination', 'battle', 'cut-throat'}
    
    words = text.lower().split()
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    
    if pos_count > neg_count:
        return Fore.GREEN + "Positive / Uplifting"
    elif neg_count > pos_count:
        return Fore.RED + "Dark / Intense"
    else:
        return Fore.CYAN + "Neutral / Balanced"

def load_data():
    """Loads the CSV file safely, creating a sample if missing."""
    file_name = "imdb_top_1000.csv"
    if not os.path.exists(file_name):
        print(Fore.YELLOW + f"[{file_name} not found. Generating a sample dataset...]")
        create_sample_dataset()
    
    try:
        return pd.read_csv(file_name)
    except Exception as e:
        print(Fore.RED + f"Error loading database: {e}")
        raise SystemExit

def display_movie(row):
    """Nicely formats and prints structured movie details."""
    sentiment = analyze_sentiment(row['Overview'])
    print(Fore.CYAN + "=" * 60)
    print(f"🎬 Title   : {Fore.WHITE + str(row['Series_Title'])}")
    print(f"🎭 Genre   : {Fore.YELLOW + str(row['Genre'])}")
    print(f"⭐ IMDb    : {Fore.GREEN + str(row['IMDB_Rating'])}")
    print(f"🧠 Mood    : {sentiment}")
    print(f"📖 Overview: {Fore.LIGHTBLACK_EX + str(row['Overview'])}")
    print(Fore.CYAN + "=" * 60)

def main():
    df = load_data()

    print(Fore.MAGENTA + "\n=== 🍿 AI MOVIE RECOMMENDATION SYSTEM ===")
    print("1. Filter by Genre")
    print("2. Filter by Minimum IMDb Rating")
    print("3. Random Recommendation (Surprise Me!)")
    
    choice = input(Fore.YELLOW + "\nSelect an option (1-3): ").strip()

    filtered_df = df.copy()

    if choice == '1':
        print(f"\nAvailable Genres: {', '.join(df['Genre'].unique())}")
        g_input = input(Fore.YELLOW + "Enter genre name: ").strip().title()
        filtered_df = df[df['Genre'].str.contains(g_input, case=False, na=False)]
        
    elif choice == '2':
        try:
            r_input = float(input(Fore.YELLOW + "Enter minimum IMDb rating (e.g., 8.5): "))
            filtered_df = df[df['IMDB_Rating'] >= r_input]
        except ValueError:
            print(Fore.RED + "Invalid number format. Showing random pick instead.")
            filtered_df = df
            
    elif choice == '3':
        filtered_df = df
    else:
        print(Fore.RED + "Invalid choice. Defaulting to Random Pick.")
        filtered_df = df

    if filtered_df.empty:
        print(Fore.RED + "\nNo movies found matching your criteria! Try a different filter.")
        return

    dots("Analyzing preferences and searching database")

    # Pick up to 3 recommendations
    sample_size = min(3, len(filtered_df))
    recommendations = filtered_df.sample(n=sample_size)

    print(Fore.GREEN + f"✨ Found {sample_size} Recommendation(s) For You:\n")
    for _, row in recommendations.iterrows():
        display_movie(row)
        time.sleep(0.3)

if __name__ == "__main__":
    main()