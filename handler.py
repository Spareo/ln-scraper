import json
try:
    import main
except:
    import ln_scraper.main as main


def run(event, context):
    main.run()
    return


if __name__ == "__main__":
    run('','')