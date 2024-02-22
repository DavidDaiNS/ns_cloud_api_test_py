from includes import *

if __name__ == '__main__':
    logger = logging.getLogger()
    logger = setup_custom_logger("MAIN")

    userConfig = UserConfig(logger)
    userConfig.getLocalAPIInfo()

    apiParam = cloudAPIParam(logger)
    apiParam.loadUserConfig(userConfig)


    # 建立並啟動執行緒
    request_thread = threading.Thread(target=fetch_real_data_thread, args=[apiParam])
    data_processing_thread = threading.Thread(target=write_power_data_to_excel, args=[apiParam])
    
    # start Thread
    request_thread.start()
    data_processing_thread.start()

    while not is_stop:
        logger.info("Menu:")

        # logger.info("Option 1. Request Schedule")
        # self.logger.info("Option 2. ")
        # self.logger.info("Option 3. Not implemented yet")
        # self.logger.info("Option 4. Not implemented yet ")
        logger.info("Option 0. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '0':
            logger.info("Exiting, please wait sub-thread to finish...")
            is_stop = True
            # 停止廣播執行緒和接收執行緒
            request_thread.join()
            data_processing_thread.join()
        else:
            logger.error("Invalid choice. Please enter a valid option.")
