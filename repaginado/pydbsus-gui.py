#!/usr/bin/env python3


from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QProgressBar, QComboBox, QSlider, QSpinBox,
                             QGridLayout, QComboBox, QSizePolicy, QLineEdit,
                             QProgressBar, QGroupBox, QLabel, QTableWidget,
                             QPushButton, QTableWidgetItem, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (QObject, QThread, QSize, QRect, Qt, pyqtSignal,
                          pyqtSlot, QFile)
import qdarkstyle




class _Loop(QThread):
    sinal = pyqtSignal(int)

    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    def run(self):
        n = 0
        [botao.setEnabled(False) for botao in download.lista_botoes]
        while self.thread.isRunning():
            n += 1
            if n == 100:
                n = 0
            sleep(0.3)
            self.sinal.emit(n)
        self.sinal.emit(100)
        [botao.setEnabled(True) for botao in download.lista_botoes]


class _Thread(QThread):

    def __init__(self, fn, *arg, **kw):
        super().__init__()
        self.fn = fn
        self.arg = arg
        self.kw = kw

#   def __del__(self):
#       self.wait()

    @pyqtSlot()
    def run(self):
        self.fn(*self.arg, **self.kw)


class Download(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Iniciar')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)
        self.spark = ''
        self.estados = {
            'Acre': ['Rio Branco', 'AC', 'Norte'],
            'Alagoas': ['Maceió', 'AL', 'Nordeste'],
            'Amapá': ['Macapá', 'AP', 'Norte'],
            'Amazonas': ['Manaus', 'AM', 'Norte'],
            'Bahia': ['Salvador', 'BA', 'Nordeste'],
            'Ceará': ['Fortaleza', 'CE', 'Nordeste'],
            'Distrito Federal': ['Brasília', 'DF',
                                 'Centro-Oeste'],
            'Espírito Santo': ['Vitória', 'ES', 'Sudeste'],
            'Goiás': ['Goiânia', 'GO', 'Centro-Oeste'],
            'Maranhão': ['São Luís', 'MA', 'Nordeste'],
            'Mato Grosso': ['Cuiabá', 'MT', 'Centro-Oeste'],
            'Mato Grosso do Sul': ['Campo Grande', 'MS',
                                   'Centro-Oeste'],
            'Minas Gerais': ['Belo Horizonte', 'MG', 'Sudeste'],
            'Pará': ['Belém', 'PA', 'Norte'],
            'Paraíba': ['João Pessoa', 'PB', 'Nordeste'],
            'Paraná': ['Curitiba', 'PR', 'Sul'],
            'Pernambuco': ['Recife', 'PE', 'Nordeste'],
            'Piauí': ['Teresina', 'PI', 'Nordeste'],
            'Rio de Janeiro': ['Rio de Janeiro', 'RJ',
                               'Sudeste'],
            'Rio Grande do Norte': ['Natal', 'RN', 'Nordeste'],
            'Rio Grande do Sul': ['Porto Alegre', 'RS', 'Sul'],
            'Rondônia': ['Porto Velho', 'RO', 'Norte'],
            'Roraima': ['Boa Vista', 'RR', 'Norte'],
            'Santa Catarina': ['Florianópolis', 'SC', 'Sul'],
            'São Paulo': ['São Paulo', 'SP', 'Sudeste'],
            'Sergipe': ['Aracaju', 'SE', 'Nordeste'],
            'Tocantins': ['Palmas', 'TO', 'Norte']
        }

        self.group_system = QGroupBox('Sistemas')
        self.grid_sys = QGridLayout()
        self.grid_sys.setSpacing(50)

        self.sistema = QComboBox()
        self.bases = QComboBox()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.locais = QComboBox()
        self.estados_regioes = QComboBox()

        self.ano_inicial_label = QLabel('ANO INICIAL:')
        self.ano_final_label = QLabel('ANO FINAL:')
        self.ano_inicial = QSpinBox()
        self.ano_inicial.setRange(2010, 2019)
        self.ano_final = QSpinBox()
        self.ano_final.setRange(2010, 2019)
        self.spin_cores_label = QLabel('SETAR CORES:')
        self.spin_cores = QSpinBox()
        self.spin_memoria_label = QLabel('SETAR MEMORIA:')
        self.spin_memoria = QSpinBox()
        self.carregar_banco = QPushButton('CARREGAR BANCO')
        self.visualizar_banco = QPushButton('VISUALIZAR BANCO')

        self.lista_botoes = [
            self.sistema, self.bases, self.locais, self.estados_regioes,
            self.ano_inicial, self.ano_final, self.spin_cores,
            self.spin_memoria, self.carregar_banco, self.visualizar_banco
        ]

        self.grid_sys.addWidget(self.sistema, 0, 0)
        self.grid_sys.addWidget(self.bases, 1, 0)
        self.grid_sys.addWidget(self.progress_bar, 2, 0, 2, 2)
        self.grid_sys.addWidget(self.locais, 0, 1)
        self.grid_sys.addWidget(self.estados_regioes, 1, 1)

        self.group_system.setLayout(self.grid_sys)

        self.group_funct = QGroupBox('Opções')
        self.grid_funct = QGridLayout()

        self.grid_funct.addWidget(self.ano_inicial_label, 0, 0)
        self.grid_funct.addWidget(self.ano_final_label, 1, 0)
        self.grid_funct.addWidget(self.ano_inicial, 0, 1, Qt.AlignLeft)
        self.grid_funct.addWidget(self.ano_final, 1, 1, Qt.AlignLeft)

        self.grid_funct.addWidget(self.spin_cores_label, 0, 2)
        self.grid_funct.addWidget(self.spin_cores, 0, 3, Qt.AlignLeft)
        self.grid_funct.addWidget(self.spin_memoria_label, 1, 2)
        self.grid_funct.addWidget(self.spin_memoria, 1, 3, Qt.AlignLeft)

        self.group_funct.setLayout(self.grid_funct)

        self.group_botoes = QGroupBox()
        self.grid_buttons = QGridLayout()

        self.grid_buttons.addWidget(self.carregar_banco, 0, 0)
        self.grid_buttons.addWidget(self.visualizar_banco, 0, 1)

        self.group_botoes.setLayout(self.grid_buttons)

        self.tabela = QTableWidget(10, 150)
        self.tabela.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.group_table = QGroupBox('Tabela')
        self.grid_table = QGridLayout()
        self.grid_table.addWidget(self.tabela)
        self.group_table.setLayout(self.grid_table)

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(10)

        self.main_layout.addWidget(self.group_system, 0, 0)
        self.main_layout.addWidget(self.group_funct, 0, 1)
        self.main_layout.addWidget(self.group_botoes, 1, 1)
        self.main_layout.addWidget(self.group_table, 2, 0, 1, 0)

        self.setLayout(self.main_layout)

        self.show()


class Transform(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Transform')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.show()


class Profile(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Profile')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.show()


class Exportar(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Exportar')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.show()


class Ajuda(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Ajuda')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.show()


class Configuracoes(QWidget):

    def __init__(self):
        super().__init__()
        # Em desenvolvimento
        self.setWindowTitle('Configurações')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.grupo_configuracoes = QGroupBox()
        self.grid_configuracoes = QGridLayout()

        self.layout_principal = QGridLayout()

        self.show()


class Pydbsus_gui(QMainWindow):

    def __init__(self, *abas):
        super().__init__()

        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.tabs = QTabWidget()

        for aba in abas:
            self.tabs.addTab(aba, aba.windowTitle())

        self.setCentralWidget(self.tabs)

        self.show()


class Etl(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('E.T.L')
        screen = QApplication.primaryScreen()
        screen = screen.size()
        self.setGeometry(0, 0, screen.width() - 100, screen.height() - 100)

        self.main_layout = QGridLayout()

        self.tabela_adicionar = QTableWidget(150, 1)
        self.tabela_aplicar = QTableWidget(150, 1)
        self.tabela_aplicar = QTableWidget(150, 1)
        self.botao_adicionar = QPushButton('Adicionar')
        self.botao_remover = QPushButton('Remover')
        self.botao_aplicar = QPushButton('Aplicar')

        self.grupo_tabelas = QGroupBox()
        self.grid_tabelas = QGridLayout()

        self.grupo_botoes = QGroupBox()
        self.grid_botoes = QGridLayout()

        self.grupo_tabelas.setLayout(self.grid_tabelas)

        self.grupo_extracao = QGroupBox('Extração')
        self.grid_extracao = QGridLayout()

        self.grid_extracao.addWidget(self.tabela_adicionar, 0, 0)
        self.grid_extracao.addWidget(self.tabela_aplicar, 0, 1)

        self.grid_extracao.addWidget(self.botao_adicionar, 1, 1, Qt.AlignRight)
        self.grid_extracao.addWidget(self.botao_remover, 2, 1, Qt.AlignRight)
        self.grid_extracao.addWidget(self.botao_aplicar, 3, 1, Qt.AlignRight)

        self.grupo_transformar = QGroupBox('Transformação')
        self.grid_transformar = QGridLayout()

        self.tabela_transformar = QTableWidget(50, 150)
        self.botao_condicao_2 = QComboBox()
        self.botao_condicao_2.addItems(['Condição 1', 'Condição 2'])
        self.botao_condicao_3 = QComboBox()
        self.botao_condicao_3.addItems(['Condição 1', 'Condição 2'])
        self.botao_condicao_4 = QComboBox()
        self.botao_condicao_4.addItems(['Condição 1', 'Condição 2'])
        self.botao_aleatorio_3 = QPushButton('Filtrar')
        self.linha_editar = QLineEdit()

        self.grupo_botoes_transformar = QGroupBox()
        self.grid_botoes_transformar = QGridLayout()
        self.grid_botoes_transformar.addWidget(self.botao_condicao_2,
                                               0, 0)
        self.grid_botoes_transformar.addWidget(self.botao_condicao_3,
                                               1, 0)
        self.grid_botoes_transformar.addWidget(self.botao_condicao_4,
                                               2, 0)
        self.grid_botoes_transformar.addWidget(self.botao_aleatorio_3,
                                               3, 0)
        self.grupo_botoes_transformar.setLayout(self.grid_botoes_transformar)

        self.grid_transformar.addWidget(self.tabela_transformar, 0, 1)
        self.grid_transformar.addWidget(self.grupo_botoes_transformar, 0, 0,
                                        Qt.AlignTop)
        self.grid_transformar.addWidget(self.linha_editar, 1, 1,
                                        Qt.AlignBottom)

        self.grupo_exportar = QGroupBox('Exportação')
        self.grid_exportar = QGridLayout()

        self.tabela_exportar = QTableWidget(10, 90)
        self.botao_exportar = QPushButton('Exportar .csv')

        self.grid_exportar.addWidget(self.tabela_exportar, 0, 0, 1, 0,
                                     Qt.AlignTop)
        self.grid_exportar.addWidget(self.botao_exportar, 1, 1)

        self.botao_salvar_html = QPushButton('Salvar Imagem')

        self.grupo_profile = QGroupBox('Profile')
        self.grid_profile = QGridLayout()

        self.grid_profile.addWidget(self.botao_salvar_html, 0, 0)

        self.grupo_extracao.setLayout(self.grid_extracao)
        self.grupo_transformar.setLayout(self.grid_transformar)
        self.grupo_exportar.setLayout(self.grid_exportar)
        self.grupo_profile.setLayout(self.grid_profile)

        self.main_layout.addWidget(self.grupo_extracao, 0, 0)
        self.main_layout.addWidget(self.grupo_transformar, 0, 1)
        self.main_layout.addWidget(self.grupo_exportar, 1, 0)
        self.main_layout.addWidget(self.grupo_profile, 1, 1)

        self.setLayout(self.main_layout)

        self.show()


def sistema_bases(text):
    download.bases.clear()
    download.bases.setEnabled(True)

    if text == 'SIH':
        download.bases.addItem('Autorizações Hospitalares')
    elif text == 'SIM':
        download.bases.addItems(['Óbito', 'Óbito Fetal'])
    elif text == 'SINAN':
        download.bases.addItems([
            'Animais Peçonhentos', 'Botulismo', 'Chagas', 'Cólera',
            'Coqueluche', 'Difteria', 'Esquistossomose', 'Febre Maculosa',
            'Febre Tifóide', 'Hanseníase', 'Leptospirose', 'Meningite',
            'Raiva', 'Tétano', 'Tuberculose'
        ])
    elif text == 'SINASC':
        download.bases.addItem('Nascidos Vivos')
    else:
        download.bases.setEnabled(False)


def estado_regiao(text):
    download.estados_regioes.clear()
    download.estados_regioes.setEnabled(True)
    if text == 'ESTADO':
        for estado in download.estados.keys():
            download.estados_regioes.addItem(estado)
    elif text == 'REGIÃO':
        download.estados_regioes.addItems([
            'Norte', 'Nordeste', 'Sul', 'Sudeste', 'Centro-Oeste'
        ])
    else:
        download.estados_regioes.setEnabled(False)


def memoria():
    if platform.system().lower() == 'linux':
        with open('/proc/meminfo', 'r') as mem:
            ret = {}
            tmp = 0
            for i in mem:
                sline = i.split()
                if str(sline[0]) == 'MemTotal:':
                    ret['total'] = int(sline[1])
                elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                    tmp += int(sline[1])
            ret['free'] = tmp
            ret['used'] = int(ret['total']) - int(ret['free'])
        return round(int(ret['total'] / 1024) / 1000)

    elif platform.system().lower() == 'windows':
        return 4


def pega_datas():
    if download.ano_inicial.value() == download.ano_final.value():
        return download.ano_inicial.value()

    elif download.ano_inicial.value() < download.ano_final.value():
        return [data for data in range(download.ano_inicial.value(),
                                       download.ano_final.value())]
    elif download.ano_inicial.value() > download.ano_final.value():
        return [data for data in range(download.ano_final.value(),
                                       download.ano_inicial.value())]


def confere_regiao():
    if download.locais.currentText() == 'REGIÃO':
        return ([value[1] for value in list(download.estados.values())
                 if value[2] == download.estados_regioes.currentText()])

    elif download.locais.currentText() == 'ESTADO':
        return download.estados.get(
            download.estados_regioes.currentText())[1]

    elif download.locais.currentText() == 'TODOS':
        ufs = []
        for value in download.estados.values():
            ufs.append(value[1])

        return ufs


@pyqtSlot(int)
def update_progressbar(val):
    download.progress_bar.setValue(val)


def baixar_banco():
    condicao = [
        download.sistema.currentText() != 'SELECIONAR SISTEMA',
        download.locais.currentText() != 'SELECIONAR LOCAL'
    ]

    if all(condicao):
        sistema = download.sistema.currentText()
        base = download.bases.currentText()
        estados = confere_regiao()
        datas = pega_datas()

        argumentos = [sistema, base, estados, datas, download.estados]

        download.csv = _Thread(PyDatasus().get_csv_db_complete, *argumentos)
        download.loop = _Loop(download.csv)
        # download.loop.moveToThread(download.main_thread)
        download.loop.sinal.connect(update_progressbar)
        # download.csv.moveToThread(download.main_thread)
        download.csv.start()
        download.loop.start()


def ligar_spark():

    try:
        download.spark.stop()
    except AttributeError:
        ...

    cores = download.spin_cores.value()
    memoria = download.spin_memoria.value()

    conf = spark_conf('AggData', cores, memoria, 20)
    download.spark = start_spark(conf)
    return download.spark


def seleciona_banco():
    dicionario_doencas = {
        'Óbito': 'DO', 'Óbito Fetal': 'DOFE',
        'Animais Peçonhentos': 'ANIM', 'Botulismo': 'BOTU',
        'Chagas': 'CHAG', 'Cólera': 'COLE',
        'Coqueluche': 'COQU', 'Difteria': 'DIFT',
        'Esquistossomose': 'ESQU', 'Febre Maculosa': 'FMAC',
        'Febre Tifóide': 'FTIF', 'Hanseníase': 'HANS',
        'Leptospirose': 'LEPT', 'Meningite': 'MENI',
        'Raiva': 'RAIV', 'Tétano': 'TETA',
        'Tuberculose': 'TUBE', 'Nascidos Vivos': 'DN'
    }
    if download.bases.currentText() in dicionario_doencas:
        return dicionario_doencas.get(download.bases.currentText())


def visualizar_banco():
    global df
    spark = ligar_spark()

    sistema = download.sistema.currentText()
    datas = pega_datas()

    locais = confere_regiao()

    base = seleciona_banco()

    banco = []
    if sistema != 'SINAN':
        if isinstance(datas, list) and isinstance(locais, list):
            banco = [base + local + str(data) + '.csv'
                     for local in locais
                     for data in datas]

        elif isinstance(datas, int) and isinstance(locais, list):
            banco = [base + str(local) + str(datas) + '.csv'
                     for local in locais]

        elif isinstance(datas, list) and isinstance(locais, str):
            banco = [base + str(locais) + str(data) + '.csv'
                     for data in datas]

        elif isinstance(datas, int) and isinstance(locais, str):
            banco = [base + str(locais) + str(datas) + '.csv']
    elif sistema == 'SINAN':
        if isinstance(datas, list) and isinstance(locais, list):
            banco = [base + local + str(data)[2:4] + '.csv'
                     for local in locais
                     for data in datas]

        elif isinstance(datas, int) and isinstance(locais, list):
            banco = [base + str(local) + str(datas)[2:4] + '.csv'
                     for local in locais]

        elif isinstance(datas, list) and isinstance(locais, str):
            banco = [base + str(locais) + str(data)[2:4] + '.csv'
                     for data in datas]

        elif isinstance(datas, int) and isinstance(locais, str):
            banco = [base + str(locais) + str(datas)[2:4] + '.csv']

    bases = re.compile('|'.join(banco), re.IGNORECASE)
    caminho_sistema = path.expanduser(f'~/Documentos/files_db/{sistema}/')

    arquivos = []
    for arquivo_csv in listdir(caminho_sistema):
        if re.search(bases, arquivo_csv):
            arquivos.append(caminho_sistema + arquivo_csv)

    df = spark.read.csv(arquivos, header=True)

    return df


def insere_na_tabela():
    df = visualizar_banco()
    download.tabela.clear()
    etl.tabela_adicionar.clear()

    rows = {}
    if df.columns[0] == '_c0':
        for key in df.columns[1:]:
            rows[key] = []
    else:
        for key in df.columns:
            rows[key] = []

    for i, key in enumerate(list(rows.keys())):
        download.tabela.setItem(0, i, QTableWidgetItem(key))
        etl.tabela_adicionar.setItem(i, 0, QTableWidgetItem(key))
    column_n = 0
    row = 1

    for column in rows.keys():
        for i in range(1, 11):
            download.tabela.setItem(
                row, column_n, QTableWidgetItem(
                    str(df.select(df[column]).take(i)[i - 1][0])))
            row += 1
        row = 1
        column_n += 1


def funciona_tabela():
    if (download.sistema.currentText() != 'SELECIONAR SISTEMA' and
            download.locais.currentText() != 'SELECIONAR LOCAL'):

        download.funcao_tabela = _Thread(insere_na_tabela)
        download.funcao_tabela.start()

        download.loop = _Loop(download.funcao_tabela)
        download.loop.sinal.connect(update_progressbar)
        download.loop.start()


def adicionar_item():
    selecionado = etl.tabela_adicionar.currentRow()
    local_aplicar = etl.tabela_aplicar.currentRow()
    try:
        coluna = etl.tabela_adicionar.item(selecionado, 0).text()
    except AttributeError:
        ...
    try:
        etl.tabela_aplicar.setItem(local_aplicar, 0, QTableWidgetItem(coluna))
    except UnboundLocalError:
        ...


def remover_item():
    selecionado = etl.tabela_aplicar.currentRow()
    etl.tabela_aplicar.removeRow(selecionado)


def aplicar_itens():
    global new_df
    etl.tabela_exportar.clear()
    colunas_selecionadas = []

    try:
        for coluna in etl.tabela_aplicar.selectedItems():
            colunas_selecionadas.append(coluna.text())

        new_df = ''

        remocao = []
        try:
            for coluna in df.columns:
                if coluna not in colunas_selecionadas:
                    remocao.append(coluna)
        except NameError:
            ...

        try:
            new_df = df.drop(*remocao)
        except NameError:
            ...

        try:
            for i, coluna in enumerate(new_df.columns):
                etl.tabela_exportar.setItem(0, i, QTableWidgetItem(coluna))
            numero_column = new_df.select(new_df.columns[0]).count()
        except AttributeError:
            ...

        column_n = 0
        row = 1
        try:
            for columns in new_df.columns:
                for i in range(1, 11):
                    etl.tabela_exportar.setItem(
                        row, column_n, QTableWidgetItem(
                            str(new_df.select(new_df[columns]).take(i)[i - 1][0])))
                    row += 1
                row = 1
                column_n += 1
        except AttributeError:
            ...
    except IndexError:
        ...


def thread_aplicar_itens():
    etl.thread = _Thread(aplicar_itens)
    etl.thread.start()


def exportar_df_csv():
    try:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(etl,
                                                  'Save File', '',
                                                  'csv(*.txt)')
        if filename:
            new_df.toPandas().to_csv(filename)
    except NameError:
        ...


if __name__ == '__main__':
    from sys import argv, exit
    from functools import reduce
    from os import path, listdir
    from multiprocessing import cpu_count
    from time import sleep
    from threading import Thread
    import platform
    import re

    from pydatasus import PyDatasus
    from f_spark import spark_conf, start_spark

    app = QApplication(argv)

    download = Download()

    # download.main_thread = QThread()
    # download.main_thread.start()

    download.sistema.addItems([
        'SELECIONAR SISTEMA', 'SIH', 'SIM', 'SINAN', 'SINASC'
    ])
    download.sistema.currentTextChanged.connect(sistema_bases)
    download.bases.setEnabled(False)

    download.locais.addItems([
        'SELECIONAR LOCAL', 'TODOS', 'ESTADO', 'REGIÃO'
    ])
    download.locais.currentTextChanged.connect(estado_regiao)

    download.spin_cores.setMinimum(2)
    download.spin_cores.setValue(4)
    download.spin_cores.setMaximum(cpu_count() - 2)

    download.spin_memoria.setMinimum(2)
    download.spin_memoria.setValue(4)
    download.spin_memoria.setMaximum(memoria() - 4)

    download.carregar_banco.clicked.connect(baixar_banco)
    download.visualizar_banco.clicked.connect(funciona_tabela)

    etl = Etl()
    etl.botao_adicionar.clicked.connect(adicionar_item)
    etl.botao_remover.clicked.connect(remover_item)
    etl.botao_aplicar.clicked.connect(thread_aplicar_itens)
    etl.botao_exportar.clicked.connect(exportar_df_csv)

    ajuda = Ajuda()

    pydb = Pydbsus_gui(download, etl, ajuda)
    exit(app.exec_())
