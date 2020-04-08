# unofficial cards_against_humanity_bot
Cards Against Humanity is a party game for horrible people and now there's a bot for that.
If you haven't already you should consider buyng the real game from https://cardsagainsthumanity.com
## rules
You can check the official rules here: https://cardsagainsthumanity.com

## how to use the bot
### commands
the default prefix is '$' use it to call the bot.
- **$new** use this command to start a new game instance.
- **$join** adds the user who entered the command to the players list (but not in the game: see $start and $refresh).
- **$deck** select the main deck (use this command before $start).
- **$start** adds all the players waiting in a new game with the selected deck and expansions.
- **$play** when the black card is revealed use this card followed by the cards you want to play.
- **$skip** if a player is not responding use this command to skip to the voting phase.
- **$vote** if you are the card czar use this command to give an awesome point to the selected card.
- **$refresh** adds all the users in the player list to the current game.
- **$reset** reset the game to the initial state (but keeps the main deck)
- **$exit** use this command to close the game instance (please use it).

### deck format
If you want to add new decks or expansions there are a few simple rules to follow:
- new line for every card
- first all the black cards
- a line only with '@@' as a separator
- all the white cards following

## TODO
- [x] make a playable bot.
- [x] multi-server ready.
- [ ] expansion.
- [ ] read deck from file.
- [ ] only the admin should use certain commands.
- [ ] select the number of points needed to win the game.
- [ ] new decks
