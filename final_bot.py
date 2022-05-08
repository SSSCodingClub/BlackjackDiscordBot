SECRET = "" # <- Put your Discord bot authentication token here!
GUILD_ID = 000000000000000000 # <- Replace this with your server/guild ID

import discord
from blackjack import Blackjack, BlackjackResult

bot = discord.Bot()

class BlackjackEmbed(discord.Embed):

    def __init__(self, user):
        super().__init__(title="Blackjack")
        # Display the user profile picture and name on the top of the embed
        self.set_author(name=user.name, icon_url=user.display_avatar)

    def update_hands(self, player_hand, dealer_hand, hide_dealer_cards = True):
        # Clear previous contents if they exist
        self.clear_fields()
        # Show all of our cards
        self.add_field(name="Your Hand", value=f"{player_hand}\nValue: {player_hand.get_optimal_value()}")
        if hide_dealer_cards:
            # Show only the first dealer card
            self.add_field(name="Dealer Hand", value=f"{dealer_hand.cards[0]} ???")
        else:
            # Show all dealer cards
            self.add_field(name="Dealer Hand", value=f"{dealer_hand}\nValue: {dealer_hand.get_optimal_value()}")

    def show_result(self, result): 
        if result == BlackjackResult.BLACKJACK:
            self.color = discord.Color.green()
            self.title = "Blackjack!"
            self.description = "You win (1.5x bet)."
        elif result == BlackjackResult.DEALER_WIN:
            self.color = discord.Color.red()
            self.title = "Dealer wins!"
            self.description = "You lost (1x bet)."
        elif result == BlackjackResult.PLAYER_WIN:
            self.color = discord.Color.green()
            self.title = "You win!"
            self.description = "You win (1x bet)."
        elif result == BlackjackResult.TIE:
            self.color = discord.Color.yellow()
            self.title = "Tie!"
            self.description = "Your bet was returned."

    def show_timeout(self):
        self.color = discord.Color.red()
        self.title = "Game timed out"
        self.description = "Game was not played in time. You lost (1x bet)."
        self.clear_fields()

class BlackjackView(discord.ui.View):

    def __init__(self, user):
        super().__init__()

        # This is my implementation of the Blackjack game (all game logic is in here)
        self.game = Blackjack()
        self.user = user

        # This is the dark gray box/card looking thing which shows the game state
        self.embed = BlackjackEmbed(self.user)

        # If the game is over (if the player gets a natural) then we can display the result now
        if self.game.is_over():
            self.on_game_over()
        else: # Otherwise just show the initial hands
            self.embed.update_hands(self.game.player.hand, self.game.dealer.hand)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("You're not allowed to play this game!", ephemeral=True)
            return False
        return True

    # Adds a button to the view
    # Registers the function it is wrapping as the callback function
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def on_hit(self, button, interaction):
        self.game.hit()
        if self.game.is_over():
            self.on_game_over()
        else:
            self.embed.update_hands(self.game.player.hand, self.game.dealer.hand)

        # Edit the existing message with new game state
        await interaction.response.edit_message(view=self, embed=self.embed)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def on_stand(self, button, interaction):
        self.game.stand()
        self.on_game_over()

        # Edit the existing message with new game state
        await interaction.response.edit_message(view=self, embed=self.embed)

    def on_game_over(self):
        self.game.play_dealer()
        # Game is now over, we can reveal the dealer cards
        self.embed.update_hands(self.game.player.hand, self.game.dealer.hand, hide_dealer_cards=False)
        # Update the embed with game result (player win, dealer win, etc.)
        self.embed.show_result(self.game.get_outcome())
        self.clear_items() # Remove buttons
        self.stop() # View does not need to listen for interactions anymore

@bot.event
async def on_ready(): # Called when the bot is active
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="blackjack", guild_ids=[GUILD_ID])
async def start_game(ctx): # Called when a user does /blackjack
    view = BlackjackView(ctx.user)
    await ctx.respond(embed=view.embed, view=view) # Respond with a message

bot.run(SECRET)

# LESSON PLAN 
# 1. Explain context
# 2. Create a basic embed inside of the command function
# 3. Create the game inside of the command function, display its state in the embed
# 4. Bring out the embed functionality into its own class which inherits discord.Embed
# 5. Add buttons using discord.ui.View inside of the command function (buttons won't do anything)
# 6. Bring it out to its own class and add button callbacks
# 7. Prevent users from clicking on other people's games
# 8. Add a timeout feature (it already does this, but it should say something when it times out)