from HttpLogin import WiFlyLogger, TpeLogger, ITaiwanLogger, FamiLogger, TpeChtLogger


def main():
    # logger = ITaiwanLogger()
    logger = TpeLogger()
    # logger = WiFlyLogger()
    # logger = FamiLogger()
    # logger = TpeChtLogger()
    print logger.login()
    # if not logger.has_internet_ability():
    #     print logger.login()
    # else:
    #     print 'alreay connected'



if __name__ == '__main__':
    main()
