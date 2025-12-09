import logging


def setup_logging():
    FORMAT = '%(asctime)s | %(levelname)s : %(message)s'
    logging.basicConfig(
        filename='/home/patrick/code_workspace/ai_ntracht/logs/tipper.log',
        format=FORMAT,
        level=logging.DEBUG
        )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info('Check Info')
    logger.error('Check Error')
    logger.debug('Check Debug')
    logger.warning('Check Warning')

if __name__ == '__main__':
    main()
    main()
