[BACKLOG]

[v] Update database by new models

Structure of the application must consist of the next blocks:
1. Main bot
    1. Goes by promo link
        1. Add name and username
        > [!Importnamt]
        > username adds from your telegram account and must be added before start AAnswers bot.
        2. Pay bill
        3. Connect oneself bot
        > [!NOTE]
        > There is possible add several bots
        4. Connect new Wildberries maeket
        > [!NOTE]
        > Threre is must be possibility add several markets
    2. Goes directly
        1. Add name and username
        2. Add promo word or goes without it
        3. Connect onself bot
        4. Connect WB market
        5. Pay the bill
    3. Commands
        1. Addm -- Add manager
        2. Delm -- Delete manager
        3. Addb -- Add bot
        4. Delb -- Delete bot
        5. Pay -- Increase a balance of application
        > [!Importnant]
        > If balance would be zero it impossible use ai generation. Other functions are free.

        [ ] Create a notification when balance under 150 Rub. 
    4. Marketer
        1. Buttons
            1. Create promocodes
            2. Edit promocodes
            3. Show promocodes

            [ ] Make request for marketer for get erned sum
        2. Info
            1. Balance

            [ ] Make field with total sum and sum for pay 
2. Subbots
    1. Notification with feedbacks info
        1. Buttons
            1. Answer
            2. Generate again
            3. Answer oneself
    2. Settings
        1. Commands

            [ ] agen -- Set autogenerattion. Autogeneration settiongs must be for individual user.
            - Generate and answer
            - Not generate
            - Generate and check

            [ ] analysis -- Get analysis for product by nmID (Articul).
            Flow: Command analysis -> Enter article number -> Quantity of days to analyze -> Result