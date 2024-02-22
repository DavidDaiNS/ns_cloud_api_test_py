from includes import *

BUFFER_SIZE = 10240

is_connect = False
is_stop = False

sys_mutex = threading.Lock()

class cloudAPIParam(object):
    def __init__(self, logger = None):
        if logger is not None:
            self.logger = logger
        else: 
            self.logger = setup_custom_logger("PCLocalAPI")

        # NETWORK_SETTING
        self.url = ""

        # Authentication
        self.email = ""
        self.password = ""
        self.token = ""
        
        # Param
        self.param_realdata_id = 0
        
        # NZPlus Response
        self.device_status = None
        self.device_info = None
        self.device_response = None
        
        # NZPlus alarm
        self.activate_alarm = None        

        # NZPlus Schedule
        self.schedule_list = []


    def loadUserConfig(self, userConfig: UserConfig):
        self.url = userConfig.url
        self.email = userConfig.email
        self.password = userConfig.password
        self.token = userConfig.token
        self.param_realdata_id = userConfig.param_realdata_id


# 函式：廣播訊息
def fetch_real_data_thread(apiParam: cloudAPIParam):
    global is_stop

    url = apiParam.url
    headers = {
        "Authorization": apiParam.token
    }
    
    params = {
        "deviceId": apiParam.param_realdata_id  # 新增的參數
    }

    while not is_stop:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                ns_data = response.json()
                with sys_mutex:
                    # Process the real_data as needed
                    apiParam.device_status = ns_data.get("NS_data")
                    apiParam.logger.info(f"Real data fetched successfully: {ns_data}")
            else:
                apiParam.logger.error(f"Failed to fetch real data, status code: {response.status_code}")
        except Exception as e:
            apiParam.logger.error(f"Error fetching real data: {e}")
        time.sleep(15)  # Fetch every 15 seconds


def print_cipher(cipher_bytes):
    formatted_bytes = ["{:02x}".format(byte) for byte in cipher_bytes]
    formatted_str = ' '.join(formatted_bytes)
    return formatted_str


def ensure_excel_file_exists(filepath):
    # 檢查文件是否存在
    if not os.path.exists(filepath):
        # 如果文件不存在，創建一個空的 DataFrame 並將其保存為 Excel 文件
        df_empty = pd.DataFrame()
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df_empty.to_excel(writer)


def write_power_data_to_excel(apiParam: cloudAPIParam):
    global is_stop

    write_dir = "./data"
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)
    
    while not is_stop:
        if apiParam.device_status:
            # 將 JSON 數據轉換為字典
            ns_data = apiParam.device_status
            
            # 從字典中提取所需的電源數據
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            power_data = {
                'DateTime': current_datetime,
                'Battery_SOC': ns_data['NS_Battery']['NS_SOC'],
                'Battery_Power': ns_data['NS_BatteryPower'],
                'Grid_P': ns_data['NS_GridPower'],
                'Load_P': ns_data['NS_LoadPower'],
                'Solar_P': ns_data['NS_SolarPower']
            }
            
            # 將數據轉換為 pandas DataFrame
            df = pd.DataFrame([power_data])
    
            # Gen name
            time_str_h = datetime.now().strftime("%Y%m%d_%H")
            excel_filename = f'self_cloud_api_{time_str_h}.xlsx'
            excel_filepath = os.path.join(write_dir, excel_filename)
            
            # 決定是否需要寫入標題
            if not os.path.exists(excel_filepath):
                header = True
                startrow = 0
            else:
                header = False
                startrow = None
            
            # 確保目標 Excel 文件存在
            ensure_excel_file_exists(excel_filepath)
            
            # 將 DataFrame 寫入 Excel 文件
            with pd.ExcelWriter(excel_filepath, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                if 'Sheet1' in writer.book.sheetnames and startrow is None:
                    startrow = writer.sheets['Sheet1'].max_row
                df.to_excel(writer, sheet_name='Sheet1', index=False, header=header, startrow=startrow)
            
            # 清除 device_status 以等待新的數據
            with sys_mutex:
                apiParam.device_status = None
        
        # 等待一段時間再次檢查，以避免過度佔用 CPU
        time.sleep(1)