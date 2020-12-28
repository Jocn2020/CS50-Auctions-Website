# CS50-Auctions-Website
Auction website using Django and SQLite as database.
The Framework used for this project is Django, and for the frontend, I used html/css and some bootstraps features

This is a website for auctions from the Project2 of CS50
Using Django, I develop this website with featues:

1. Username, password and registration for account
2. Page of active listing, each listing is a post of auction created by some users.
3. Listing page which shows more detail information about that item, including:
    - name
    - description and image
    - current bidders and highest bid
    - comments from each user
    - feature to bid only for authenticated user and close bid for the auctioneer
    - add post to watchlist
4. Create listing page and save it in models.form composed by name, description, initial price, tags, and image (all required except image)
5. Search feature to search listings using regex
6. Watchlist page with all post that has been added to watchlist
7. Tag features, by clicking the link, it will redirect to a list of all pages with given tag
8. Profile, that shows all users listings and comments

