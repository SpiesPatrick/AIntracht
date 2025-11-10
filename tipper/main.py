from components import tipp_generator, tipp_sender


def main():

    '''
    Check if tipps already safed in DB. If not:
      -> generate prompt and send it to bot
      -> receive tipps and safe them into DB
    '''
    tipp_generator.generate()

    '''
    Check if tipps already safed AND tipped in DB (bool "getippt"). If not:
      -> get tipps from current matchday
      -> navigate through Kicktipp and tipp the shit out of hell
    '''
    tipp_sender.send()

if __name__ == '__main__':
    main()
