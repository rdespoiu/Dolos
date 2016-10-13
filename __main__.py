from app import *

if __name__ == '__main__':
    Tweeter(INTERVAL, dbModels, db, api, DEPTH)
    DataScraper(SCRAPE_INTERVAL, dbModels, db, api)
    app.run(debug=True, use_reloader=False)
