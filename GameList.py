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

games_data = [
    {"title": "Grand Theft Auto 5", "price": 19.99, "review": 4.5, "genre": "Action", "esrb_rating": "Mature"},
    {"title": "Elden Ring", "price": 39.99, "review": 4.8, "genre": "Action", "esrb_rating": "Mature"},
    {"title": "Spider Man Miles Morales", "price": 24.99, "review": 4.7, "genre": "Action", "esrb_rating": "Teen"},
    {"title": "Star Wars Jedi Survivor", "price": 34.99, "review": 4.4, "genre": "Action", "esrb_rating": "Teen"},
    {"title": "LEGO Star Wars", "price": 29.99, "review": 4.6, "genre": "Action", "esrb_rating": "Everyone"},
    {"title": "Helldivers 2", "price": 39.99, "review": 4.6, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Call of Duty Modern Warfare 3", "price": 69.99, "review": 2.7, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Aliens Fireteam Elite", "price": 14.99, "review": 3.5, "genre": "Shooter", "esrb_rating": "Mature"},
    {"title": "Everspace 2", "price": 44.99, "review": 3.0, "genre": "Shooter", "esrb_rating": "Teen"},
    {"title": "Armored Core 6 Fires of Rubicon", "price": 39.99, "review": 4.9, "genre": "Shooter", "esrb_rating": "Teen"},
    {"title": "Final Fantasy 7 Rebirth", "price": 69.99, "review": 3.8, "genre": "RPG", "esrb_rating": "Teen"},
    {"title": "Scarlet Nexus", "price": 6.99, "review": 4.3, "genre": "RPG", "esrb_rating": "Teen"},
    {"title": "The Witcher 3", "price": 34.99, "review": 4.8, "genre": "RPG", "esrb_rating": "Mature"},
    {"title": "Minecraft Legends", "price": 29.99, "review": 4.7, "genre": "RPG", "esrb_rating": "Everyone"},
    {"title": "Diablo 4", "price": 59.99, "review": 2.4, "genre": "RPG", "esrb_rating": "Mature"},
    {"title": "Dead Space", "price": 29.99, "review": 4.5, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "Resident Evil 4", "price": 49.99, "review": 4.8, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "Five Nights at Freddy's Security Breach", "price": 39.99, "review": 3.9, "genre": "Horror", "esrb_rating": "Teen"},
    {"title": "White Day A Labyrinth Named School", "price": 9.99, "review": 3.1, "genre": "Horror", "esrb_rating": "Teen"},
    {"title": "The Callisto Protocol", "price": 14.99, "review": 3.5, "genre": "Horror", "esrb_rating": "Mature"},
    {"title": "MLB The Show 24", "price": 69.99, "review": 4.9, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "NBA 2K24", "price": 19.99, "review": 3.8, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "EA Sports FC24", "price": 34.99, "review": 3.5, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "Riders Republic", "price": 14.99, "review": 3.1, "genre": "Sports", "esrb_rating": "Teen"},
    {"title": "F1 Manager 2022", "price": 18.99, "review": 4.6, "genre": "Sports", "esrb_rating": "Everyone"},
    {"title": "Tekken 8", "price": 69.99, "review": 3.5, "genre": "Fightning", "esrb_rating": "Teen"},
    {"title": "Street Fighter 6", "price": 45.99, "review": 4.3, "genre": "Fightning", "esrb_rating": "Teen"},
    {"title": "Nickelodeon All Star Brawl 2", "price": 29.99, "review": 4.1, "genre": "Fightning", "esrb_rating": "Everyone"},
    {"title": "Mortal Kombat", "price": 59.99, "review": 4.4, "genre": "Fightning", "esrb_rating": "Mature"},
    {"title": "Dragon Ball FighterZ", "price": 19.99, "review": 4.5, "genre": "Fightning", "esrb_rating": "Teen"}
]

games = [Game(**game_data) for game_data in games_data]

def get_games():
    return games