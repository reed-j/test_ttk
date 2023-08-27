import cx_Oracle
import socket
from oracleInstall import *


def check_instant_client():
    # Путь к файлу oci.dll или другому файлу из Oracle Instant Client
    instant_client_file = "dist/instantclient_18_1/"  
    #для винды
    #instant_client_file = r"C:\instantclient"  

    if not os.path.exists(instant_client_file):
        return False
    return True


def check_oci_dll_in_env():
    env_path = os.environ.get("PATH")
    paths = env_path.split(os.pathsep)

    for path in paths:
        oci_dll_path = os.path.join(path, "oci.dll")
        if os.path.exists(oci_dll_path):
            logger.info('Клиент найден в переменной окружения')
            return True

    logger.info('Клиент не найден в переменной окружения')
    return False


class OracleDB:
    def __init__(self, username, password, host, port, service_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name
        self.connection = None

    def connect(self):
        # Проверка наличия Oracle Instant Client
        # if not check_instant_client():
        #     logger.info("Oracle Instant Client не найден. Установка...")
        #     # download_zip_file_with_progress(zip_url, save_path)
        #     print("Oracle Instant Client не найден. Установка...")
        #     install_instant_client()
        dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
        logger.info(f"Попытка подключения к базе данных: адрес={self.host}, порт={self.port}, сервис={self.service_name}")
        try:
            self.connection = cx_Oracle.connect(self.username, self.password, dsn, encoding="UTF-8", nencoding="UTF-8", threaded=True)
            logger.info("Подключение к базе данных выполнено успешно.")
        except socket.timeout:
            logger.error("Таймаут подключения к базе данных")
            raise Exception("Таймаут подключения к базе данных")
        except cx_Oracle.DatabaseError as e:
            error_msg = "Ошибка подключения к базе данных: " + str(e)
            logger.error(error_msg)
            raise Exception(error_msg)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def ping(self):
        if self.connection:
            try:
                self.connection.ping()
                return True
            except cx_Oracle.InterfaceError:
                return False
        else:
            return False

    def execute_sql_select_card_query(self, input_value):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        try:
            # Формирование SQL запроса на основе введенных данных
            sql_query = f"select crd card where crd_serial_no = {input_value}"

            # Выполнение запроса
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            logger.info(f"Выполнили поиск по карте {input_value}")
            return result

        except cx_Oracle.Error as error:
            print("Ошибка выполнения запроса:", error)
            return f"Ошибка выполнения запроса: {error}"

    def execute_sql_clear_card_query(self, crd_serial_no, sector, remove_all_tickets):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        # Формирование и выполнение хранимой процедуры
        try:
            cursor = self.connection.cursor()
            cursor.callproc("FORCARD",
                            [crd_serial_no, sector, remove_all_tickets])
            self.connection.commit()
            cursor.close()

            return ("Процедура успешно выполнена.\n")

        except cx_Oracle.Error as error:
            # Перевыбрасываем ошибку, чтобы она была поймана в методе execute_sql_query_3
            print("мы тут")
            raise error

    def execute_set_ticket_days_left(self, ticket_guid, days_left, change_recharge_date):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        # Формирование и выполнение хранимой процедуры
        try:
            cursor = self.connection.cursor()
            cursor.callproc("DAYSLEFT",
                            [ticket_guid, days_left, change_recharge_date])
            self.connection.commit()
            cursor.close()

            return ("Процедура успешно выполнена.\n")

        except cx_Oracle.Error as error:
            # Перевыбрасываем ошибку, чтобы она была поймана в методе execute_sql_query_3
            raise error

    def execute_add_passenger_id(self, passenger_id):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        # Формирование и выполнение хранимой процедуры
        try:
            cursor = self.connection.cursor()
            o_rs = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc('EDIT."ADD"',
                            [o_rs, passenger_id])
            self.connection.commit()
            cursor.close()

            return ("Процедура успешно выполнена.\n")

        except cx_Oracle.Error as error:
            # Перевыбрасываем ошибку, чтобы она была поймана в методе execute_sql_query_3
            raise error

    def execute_add_card(self, card_num):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        # Формирование и выполнение хранимой процедуры
        try:

            cursor = self.connection.cursor()
            o_rs = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc('ADD_LINK', [o_rs, card_num])
            self.connection.commit()
            cursor.close()

            return ("Процедура успешно выполнена.\n")

        except cx_Oracle.Error as error:
            # Перевыбрасываем ошибку, чтобы она была поймана в методе execute_sql_query_3
            raise error

    def execute_set_suspension_days_left(self, suspension_id, add_days):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        # Формирование и выполнение хранимой процедуры
        try:
            cursor = self.connection.cursor()
            cursor.callproc("DATEDAYS",
                            [suspension_id, add_days])
            self.connection.commit()
            cursor.close()

            return ("Процедура успешно выполнена.\n")

        except cx_Oracle.Error as error:
            # Перевыбрасываем ошибку, чтобы она была поймана в методе execute_sql_query_3
            raise error

    def execute_sql_select_pass_query(self, input_value):
        if not self.connection:
            raise Exception("Нет подключения к базе данных")

        try:
            # Формирование SQL запроса на основе введенных данных
            sql_query = f"select id where id = {input_value}"

            # Выполнение запроса
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()

            return result

        except cx_Oracle.Error as error:
            print("Ошибка выполнения запроса:", error)
            return f"Ошибка выполнения запроса: {error}"
