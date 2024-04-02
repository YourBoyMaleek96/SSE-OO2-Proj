# Game Class and Game List

class Game:
    def __init__(self, title, price, review, genre, esrb_rating):
        self.title = title
        self.price = price
        self.review = review
        self.genre = genre
        self.esrb_rating = esrb_rating

    def display_info(self):
        return f"{self.title} - ${self.price} - Rating: {self.review} - Genre: {self.genre} - ESRB: {self.esrb_rating}"

class GameGraph:
    def __init__(self, games):
        self.graph = {}
        self.build_graph(games)

    def build_graph(self, games):
        for game in games:
            if game.genre not in self.graph:
                self.graph[game.genre] = []
            for other_game in games:
                if game != other_game and game.genre == other_game.genre:
                    self.graph[game.genre].append(other_game.title)
    
    def get_recommendations(self, genre):
        similar_games = self.graph.get(genre, [])
        return similar_games
    

games_data = [
    {"title": "Grand Theft Auto 5", "price": 19.99, "review": 4.5, "genre": "Action", "esrb_rating": "Mature"},
    {"title": "Elden Ring", "price": 39.99, "review": 4.89, "genre": "Action", "esrb_rating": "Mature"},
    {"title": "Spider Man Miles Morales", "price": 24.99, "review": 4.78, "genre": "Action", "esrb_rating": "Teen"},
    {"title": "Star Wars Jedi Survivor", "price": 34.99, "review": 4.41, "genre": "Action", "esrb_rating": "Teen"},
    {"title": "LEGO Star Wars", "price": 29.99, "review": 4.62, "genre": "Action", "esrb_rating": "Everyone"},
    {"title": "Helldivers 2", "price": 33.99, "review": 4.69, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Call of Duty Modern Warfare 3", "price": 61.99, "review": 2.73, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Aliens Fireteam Elite", "price": 14.99, "review": 3.68, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Everspace 2", "price": 44.99, "review": 3.01, "genre": "Shooter", "esrb_rating": "Teen"},
    {"title": "Armored Core 6 Fires of Rubicon", "price": 35.99, "review": 4.95, "genre": "Shooter", "esrb_rating": "Teen"},
    {"title": "Final Fantasy 7 Rebirth", "price": 69.99, "review": 3.89, "genre": "RPG", "esrb_rating": "Teen"},
    {"title": "Scarlet Nexus", "price": 6.99, "review": 4.31, "genre": "RPG", "esrb_rating": "Teen"},
    {"title": "The Witcher 3", "price": 32.99, "review": 4.84, "genre": "RPG", "esrb_rating": "Mature"},
    {"title": "Minecraft Legends", "price": 25.99, "review": 4.74, "genre": "RPG", "esrb_rating": "Everyone"},
    {"title": "Diablo 4", "price": 59.99, "review": 3.47, "genre": "RPG", "esrb_rating": "Mature"},
    {"title": "Dead Space", "price": 20.99, "review": 4.57, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "Resident Evil 4", "price": 49.99, "review": 4.81, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "Five Nights at Freddy's Security Breach", "price": 31.99, "review": 3.98, "genre": "Horror", "esrb_rating": "Teen"},
    {"title": "White Day A Labyrinth Named School", "price": 9.99, "review": 3.17, "genre": "Horror", "esrb_rating": "Teen"},
    {"title": "The Callisto Protocol", "price": 12.99, "review": 3.62, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "MLB The Show 24", "price": 65.99, "review": 4.91, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "NBA 2K24", "price": 18.99, "review": 3.81, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "EA Sports FC24", "price": 38.99, "review": 3.55, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "Riders Republic", "price": 11.99, "review": 3.28, "genre": "Sports", "esrb_rating": "Teen"},
    {"title": "F1 Manager 2022", "price": 16.99, "review": 4.60, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "Tekken 8", "price": 67.99, "review": 3.51, "genre": "Fightning", "esrb_rating": "Teen"},
    {"title": "Street Fighter 6", "price": 45.99, "review": 4.30, "genre": "Fightning", "esrb_rating": "Teen"},
    {"title": "Nickelodeon All Star Brawl 2", "price": 28.99, "review": 4.10, "genre": "Fightning", "esrb_rating": "Everyone"},
    {"title": "Mortal Kombat", "price": 54.99, "review": 4.46, "genre": "Fightning", "esrb_rating": "Mature"},
    {"title": "Dragon Ball FighterZ", "price": 17.99, "review": 4.54, "genre": "Fightning", "esrb_rating": "Teen"}
]

games = [Game(**game_data) for game_data in games_data]

game_graph = GameGraph(games)

def get_recommendations_for_genre(genre):
    return game_graph.get_recommendations(genre)
def get_games():
    return games