# -*- coding: utf-8 -*-
from tkinter import ttk
import connect_bd
import config
import signal
import sys
import traceback
import threading
from connect_bd import *
from oracleInstall import *
# путь к директории с библиотеками Oracle Instant Client
# oracle_client_dir = "instantclient_18_1/"
#
# # Инициализируем Oracle Client с указанным путем
# cx_Oracle.init_oracle_client(lib_dir=oracle_client_dir)


class PlaceholderEntry(tk.Entry):

    def __init__(self, master=None, placeholder="", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.put_placeholder()

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color


class SQLQueryForm(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Помогатор")
        self.db_indicator = tk.Label(self, text="Нет подключения", fg="red")
        self.db_indicator.pack(pady=5)

        # Создаем атрибут progress_bar и виджет Progressbar
        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X)
        # Фрейм для формы ввода и кнопок к базе данных
        input_frame_db = tk.Frame(self)
        input_frame_db.pack(pady=10)
        tk.Frame(self, height=2, bg="gray").pack(fill=tk.X, padx=10, pady=3)
        # Это окно слева целый столбец
        info_and_input_frame = tk.Frame(self)
        info_and_input_frame.pack(side=tk.LEFT, padx=15, pady=10)

        self.label_info = tk.Label(info_and_input_frame, text="Очистка билетов", fg="black",
                                   font=("Helvetica", 11, "bold"))
        self.label_info.pack(side=tk.TOP, padx=10, pady=0)

        # Окно для "билетов" в центральном столбце
        info_and_input_frame_top = tk.Frame(self)
        info_and_input_frame_top.pack(side=tk.LEFT, padx=15, pady=10)

        self.label_info = tk.Label(info_and_input_frame_top, text="Добавить карту в НБС", fg="black",
                                   font=("Helvetica", 11, "bold"))
        self.label_info.pack(side=tk.TOP, padx=10, pady=0)

        # Фрейм для формы ввода и кнопок для работы с очисткой билетов
        input_frame_clean_tic_procedure = tk.Frame(info_and_input_frame)
        input_frame_clean_tic_procedure.pack(side=tk.TOP, padx=15, pady=10)

        # Кнопки для подключения к разным базам данных
        self.dev2_button = tk.Button(input_frame_db, text="d2", command=self.connect_to_dev2)
        self.dev2_button.grid(row=0, column=0, padx=5)
        self.dev3_button = tk.Button(input_frame_db, text="d3", command=self.connect_to_dev3)
        self.dev3_button.grid(row=0, column=1, padx=5)
        self.mm_button = tk.Button(input_frame_db, text="m", command=self.connect_to_mm)
        self.mm_button.grid(row=0, column=2, padx=5)
        self.mm_button = tk.Button(input_frame_db, text="nt2", command=self.connect_to_ntstest2)
        self.mm_button.grid(row=0, column=3, padx=5)

        # Форма ввода для номера очистки
        self.entry_input_3 = PlaceholderEntry(input_frame_clean_tic_procedure, placeholder="Введите номер кристалла")
        self.entry_input_3.grid(row=1, column=0, padx=10)
        self.checkbox_var_del = tk.IntVar()
        self.checkbox = tk.Checkbutton(input_frame_clean_tic_procedure, text="все билеты/отложки",
                                       variable=self.checkbox_var_del)
        self.checkbox.grid(row=0, column=0)
        # По умолчанию установите значение переменной в 0 (False)
        self.checkbox_var_del.set(1)
        # Форма ввода для очистки сектора
        self.entry_input_4 = PlaceholderEntry(input_frame_clean_tic_procedure,
                                              placeholder="Введите номер сектора(необяз)")
        self.entry_input_4.grid(row=2, column=0, padx=15)
        # Кнопка "Выполнить очистку"
        self.execute_button_3 = tk.Button(input_frame_clean_tic_procedure, text="Очистить",
                                          command=self.execute_sql_query_3)
        self.execute_button_3.grid(row=3, column=0, pady=3)
        tk.Frame(info_and_input_frame, height=2, bg="black").pack(fill=tk.X, padx=10, pady=0)

        # Процедура сдвига даты
        self.label_info = tk.Label(info_and_input_frame, text="Сдвиг даты", fg="black",
                                   font=("Helvetica", 11, "bold"))
        self.label_info.pack(side=tk.TOP, padx=10, pady=5)
        # Фрейм для формы ввода и кнопок для работы со сдвигом даты
        input_frame_shift_date_procedure = tk.Frame(info_and_input_frame)
        input_frame_shift_date_procedure.pack(side=tk.TOP, padx=15, pady=10)
        self.entry_input_5 = PlaceholderEntry(input_frame_shift_date_procedure, placeholder="Введите номер билета")
        self.entry_input_5.grid(row=1, column=0, padx=10)
        # "Введите значение" над формой ввода для шестого запроса
        self.entry_input_6 = PlaceholderEntry(input_frame_shift_date_procedure, placeholder="Сдвиг +/- xx дней")
        self.entry_input_6.grid(row=2, column=0, padx=10)
        # Кнопка "Выполнить сдвиг"
        self.execute_button_4 = tk.Button(input_frame_shift_date_procedure, text="Изменить даты",
                                          command=self.execute_sql_query_4)
        self.execute_button_4.grid(row=3, column=0, pady=3)
        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(input_frame_shift_date_procedure, text="Билет актив/неактив",
                                       variable=self.checkbox_var)
        self.checkbox.grid(row=0, column=0)
        # По умолчанию установите значение переменной в 0 (False)
        self.checkbox_var.set(1)
        tk.Frame(info_and_input_frame, height=2, bg="black").pack(fill=tk.X, padx=10, pady=3)

        # Процедура сдвига заморозки
        self.label_info = tk.Label(info_and_input_frame, text="Сдвиг заморозки", fg="black",
                                   font=("Helvetica", 11, "bold"))
        self.label_info.pack(side=tk.TOP, padx=10, pady=0)
        # Фрейм для формы ввода и кнопок для работы со сдвигом даты
        input_frame_shift_date_suspension_procedure = tk.Frame(info_and_input_frame)
        input_frame_shift_date_suspension_procedure.pack(side=tk.TOP, padx=15, pady=10)

        self.entry_input_7 = PlaceholderEntry(input_frame_shift_date_suspension_procedure, placeholder="Введите номер заморозки")
        self.entry_input_7.grid(row=0, column=0, padx=10)
        # "Введите значение" над формой ввода для шестого запроса
        self.entry_input_8 = PlaceholderEntry(input_frame_shift_date_suspension_procedure, placeholder="Сдвиг +/- xx дней")
        self.entry_input_8.grid(row=1, column=0, padx=10)
        # Кнопка "Выполнить сдвиг"
        self.execute_button_5 = tk.Button(input_frame_shift_date_suspension_procedure, text="Изменить даты заморозки",
                                          command=self.execute_sql_query_5)
        self.execute_button_5.grid(row=2, column=0, pady=5)
        # Фрейм для формы ввода и кнопок для добавления карт
        input_frame_add_card_procedure = tk.Frame(info_and_input_frame_top)
        input_frame_add_card_procedure.pack(side=tk.TOP, padx=15, pady=10)

        # Фрейм для формы ввода и кнопок для работы c добавлением карты
        self.entry_input_9 = PlaceholderEntry(input_frame_add_card_procedure, placeholder="Введите номер кристалла")
        self.entry_input_9.grid(row=0, column=1, padx=10)
        # Кнопка "Добавить карту"
        self.execute_button_6 = tk.Button(input_frame_add_card_procedure, text="Добавить карту",
                                          command=self.execute_sql_query_6)
        self.execute_button_6.grid(row=1, column=1, pady=5)
        self.execute_button_8 = tk.Button(input_frame_add_card_procedure, text="Проверить карту",
                                          command=self.execute_sql_query_1)
        self.execute_button_8.grid(row=2, column=1, pady=5)
        tk.Frame(info_and_input_frame_top, height=2, bg="black").pack(fill=tk.X, padx=10, pady=3)
        # Добавить пользователя в НБС
        self.label_info = tk.Label(info_and_input_frame_top, text="Добавить пользователя в НБС", fg="black",
                                   font=("Helvetica", 11, "bold"))
        self.label_info.pack(side=tk.TOP, padx=10, pady=0)
        # Фрейм для формы ввода и кнопок для добавления пользоватей
        input_frame_add_passenger_procedure = tk.Frame(info_and_input_frame_top)
        input_frame_add_passenger_procedure.pack(side=tk.TOP, padx=15, pady=10)

        # Фрейм для формы ввода и кнопок для работы c добавлением карты
        self.entry_input_10 = PlaceholderEntry(input_frame_add_passenger_procedure, placeholder="Введите ID пользователя")
        self.entry_input_10.grid(row=0, column=1, padx=10)
        # Кнопка "Добавить карту"
        self.execute_button_7 = tk.Button(input_frame_add_passenger_procedure, text="Добавить пользователя",
                                          command=self.execute_sql_query_7)
        self.execute_button_7.grid(row=1, column=1, pady=5)
        self.execute_button_9 = tk.Button(input_frame_add_passenger_procedure, text="Проверить пользователя",
                                          command=self.execute_sql_query_2)
        self.execute_button_9.grid(row=2, column=1, pady=5)
        #tk.Frame(info_and_input_frame_top, height=2, bg="black").pack(fill=tk.X, padx=10, pady=3)

        # Фрейм для окна вывода
        result_frame = tk.Frame(self, bd=2, relief=tk.RIDGE)
        result_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Окно для вывода результатов
        self.result_text = tk.Text(result_frame, height=30, width=50)
        self.result_text.pack()

        # Инициализируем объект для работы с базой данных
        self.db = None
        # self.start_app()

   
    def connect_to_dev2(self):
        if self.db:
            self.db.close()
        # Создаем подключение к dev2 базе в отдельном потоке
        # Вызываем функцию для скачивания с передачей ссылки на текстовое окно вывода
        if not check_oci_dll_in_env():
            logger.info("Oracle Instant Client не найден. Установка...")
            # download_thread = threading.Thread(target=download_zip_file_with_progress,
            #                                    args=(zip_url, save_path, self.result_text))
            # download_thread.start()
            #install_instant_client(self.result_text)  # Передайте объект self.result_text в функцию

            print("Oracle Instant Client не найден. Установка...")
           # install_instant_client()

        connection_thread = threading.Thread(target=self.connect_to_dev2_thread)
        connection_thread.start()

    def connect_to_dev2_thread(self):
        try:
            self.db = connect_bd.OracleDB(username=config.dev2_username, password=config.dev2_password,
                                          host=config.dev2_host, port=config.dev2_port,
                                          service_name=config.dev2_service_name)
            self.db.connect()
            self.db_indicator.config(text="Подключено к dev2", fg="green")

        except Exception as e:
            self.db_indicator.config(text="Не удалось подключиться к dev2", fg="red")

    def connect_to_dev3(self):
        if self.db:
            self.db.close()
        if not check_oci_dll_in_env():
            logger.info("Oracle Instant Client не найден. Установка...")
            #install_instant_client(self.result_text)  # Передайте объект self.result_text в функцию

        # Создаем подключение к dev3 базе в отдельном потоке
        connection_thread = threading.Thread(target=self.connect_to_dev3_thread)
        connection_thread.start()

    def connect_to_dev3_thread(self):
        try:
            self.db = connect_bd.OracleDB(username=config.dev3_username, password=config.dev3_password,
                                          host=config.dev3_host, port=config.dev3_port,
                                          service_name=config.dev3_service_name)
            self.db.connect()
            self.db_indicator.config(text="Подключено к dev3", fg="green")
        except Exception as e:
            self.db_indicator.config(text="Не удалось подключиться к dev3", fg="red")

    def connect_to_mm(self):
        if self.db:
            self.db.close()
        if not check_oci_dll_in_env():
            logger.info("Oracle Instant Client не найден. Установка...")
            #install_instant_client(self.result_text)  # Передайте объект self.result_text в функцию

        # Создаем подключение к mm базе в отдельном потоке
        connection_thread = threading.Thread(target=self.connect_to_mm_thread)
        connection_thread.start()

    def connect_to_mm_thread(self):
        try:
            self.db = connect_bd.OracleDB(username=config.mm_username, password=config.mm_password,
                                          host=config.mm_host, port=config.mm_port,
                                          service_name=config.mm_service_name)
            self.db.connect()
            self.db_indicator.config(text="Подключено к mm", fg="green")
        except Exception as e:
            self.db_indicator.config(text="Не удалось подключиться к mm", fg="red")

    def connect_to_ntstest2(self):
        if self.db:
            self.db.close()
        if not check_oci_dll_in_env():
            logger.info("Oracle Instant Client не найден. Установка...")
            #install_instant_client(self.result_text)  # Передайте объект self.result_text в функцию

        # Создаем подключение к mm базе в отдельном потоке
        connection_thread = threading.Thread(target=self.connect_to_ntstest2_thread)
        connection_thread.start()

    def connect_to_ntstest2_thread(self):
        try:
            self.db = connect_bd.OracleDB(username=config.ntstest2_username, password=config.ntstest2_password,
                                          host=config.ntstest2_host, port=config.ntstest2_port,
                                          service_name=config.ntstest2_service_name)
            self.db.connect()
            self.db_indicator.config(text="Подключено к ntstest2", fg="green")
        except Exception as e:
            self.db_indicator.config(text="Не удалось подключиться к ntstest2", fg="red")

    def execute_sql_query_1(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return
        try:
            self.execute_sql_query(self.entry_input_9, self.db.execute_sql_select_card_query)
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения запроса: {error}\n")

    def execute_sql_query_2(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return
        try:
            self.execute_sql_query(self.entry_input_10, self.db.execute_sql_select_pass_query)
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения запроса: {error}\n")

    def execute_sql_query_3(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return

        # Получение данных из полей ввода и состояния чекбокса
        crd_serial_no = self.entry_input_3.get()
        sector = self.entry_input_4.get()
        remove_all_tickets = self.checkbox_var_del.get()
        if remove_all_tickets == 1:
            tic = 'все билеты'
        else:
            tic = 'все отложенные'

        try:
            # Если поле "сектор" пустое, передаем значение None (NULL)
            if sector == "Введите номер сектора(необяз)":
                sector = None
                sectors = ''
            else:
                sectors = f'и из сектора {sector}'
            # Вызов процедуры с передачей данных из полей и чекбокса
            self.db.execute_sql_clear_card_query(crd_serial_no, sector, remove_all_tickets)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Удалены {tic} с карты {crd_serial_no} {sectors}.\n")
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения процедуры: {error}\n")
        except Exception as error:
            # Выводим общую ошибку на экран для отладки
            print("Общая ошибка:", error)
            traceback.print_exc()
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Общая ошибка: {error}\n")

    def execute_sql_query_4(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return

        # Получение данных из полей ввода и состояния чекбокса
        ticket_guid = self.entry_input_5.get()
        days_left = self.entry_input_6.get()
        change_recharge_date = self.checkbox_var.get()

        try:
            # Вызов процедуры с передачей данных из полей и чекбокса
            self.db.execute_set_ticket_days_left(ticket_guid, days_left, change_recharge_date)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Для билета {ticket_guid} даты изменены на {days_left} дня/дней.\n")
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения процедуры: {error}\n")

    def execute_sql_query_5(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return

        # Получение данных из полей ввода и состояния чекбокса
        suspension_id = self.entry_input_7.get()
        add_days = self.entry_input_8.get()

        try:
            # Вызов процедуры с передачей данных из полей и чекбокса
            self.db.execute_set_suspension_days_left(suspension_id, add_days)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Заморозка номер {suspension_id} изменена на {add_days} дня/дней.\n")
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения процедуры: {error}\n")

    def execute_sql_query_6(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return

        # Получение данных из полей ввода и состояния чекбокса
        card_num = self.entry_input_9.get()
        try:
            # Вызов процедуры с передачей данных из полей и чекбокса
            self.db.execute_add_card(card_num)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Карта номер {card_num} добавлена в НБС.\n")
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения процедуры: {error}\n")

    def execute_sql_query_7(self):
        if not self.db:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Подключитесь к базе данных сначала.\n")
            return

        # Получение данных из полей ввода и состояния чекбокса
        passenger_id = self.entry_input_10.get()

        try:
            # Вызов процедуры с передачей данных из полей и чекбокса
            self.db.execute_add_passenger_id(passenger_id)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Пользователь ID {passenger_id} добавлен в НБС.\n")
        except cx_Oracle.Error as error:
            # Выводим ошибку в окно вывода
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка выполнения процедуры: {error}\n")

    def execute_sql_query(self, entry_input, query_method):
        if not self.db or not self.db.ping():
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "База данных недоступна. Проверьте подключение.\n")
            return

        # Получение данных из соответствующего поля ввода формы
        input_value = entry_input.get()
        # Вызываем метод для выполнения запроса и передаем значение из поля ввода
        result = query_method(input_value)

        # Вывод результатов на форме
        self.result_text.delete("1.0", tk.END)

        if isinstance(result, str):
            # Выводим сообщение об ошибке
            self.result_text.insert(tk.END, result + "\n")
        else:
            if not result:
                self.result_text.insert(tk.END, "Ничего не найдено в базе данных.\n")
                # self.result_text.config(state=tk.DISABLED)  # Запрещаем редактирование текста
            else:
                for row in result:
                    self.result_text.insert(tk.END, str(row) + "\n")


def sigterm_handler(signal, frame):
    if app.db:
        app.db.close()  # Закрываем соединение с базой данных при получении SIGTERM
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)  # Установка обработчика для SIGTERM
    app = SQLQueryForm()  # Создание экземпляра вашего класса
    app.mainloop()
