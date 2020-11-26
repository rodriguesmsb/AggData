#!/usr/bin/env python3

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTabBar,
                             QTableWidgetItem, QFileDialog, QStylePainter,
                             QStyle, QStyleOptionTab, QStyleFactory)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, QPoint
from pandas_profiling import ProfileReport

import qdarkstyle
import qdarkgraystyle
import pyqt5_material


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.West)


class Pydbsus_gui(QMainWindow):

    def __init__(self, *abas):
        super().__init__()

        # self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowTitle('pyBiss')
        self.tabs = TabWidget()
        self.tabs.setContentsMargins(100, 100, 100, 100)
        # self.tabs.setTabPosition(QTabWidget.West)

        for aba in abas:
            self.tabs.addTab(aba, QIcon(aba.windowIcon()), aba.windowTitle())

        self.setCentralWidget(self.tabs)

        self.show()


def escreve_tabela_download():
    download.visualizar_dados()
    download.tabela.clear()

    coluna_ordenada = {}

    if download.df.columns[0] == '_c0':
        for coluna in download.df.columns[1:]:
            coluna_ordenada[coluna] = []
    else:
        for coluna in download.df.columns:
            coluna_ordenada[coluna] = []

    colunas = list(coluna_ordenada.keys())
    colunas.sort()

    for i, column in enumerate(colunas):
        download.tabela.setItem(0, i, QTableWidgetItem(column))
        i += 1

    etl.tabela_adicionar.clear()
    for e, c in enumerate(colunas):
        etl.tabela_adicionar.setItem(e, 0, QTableWidgetItem(c))

    column_n = 0
    row = 1

    for column in colunas:
        for i in range(1, 11):
            download.tabela.setItem(
                row, column_n, QTableWidgetItem(
                    str(
                        download.df.select(
                            download.df[column]).take(i)[i - 1][0])))
            row += 1
        row = 1
        column_n += 1


def aplicar_itens_etl():
    etl.tabela_exportar.clear()
    colunas_selecionadas = []

    for coluna in etl.tabela_aplicar.selectedItems():
        colunas_selecionadas.append(coluna.text())

    remocao = []
    for coluna in download.df.columns:
        if coluna not in colunas_selecionadas:
            remocao.append(coluna)

    etl.new_df = download.df.drop(*remocao)

    for i, coluna in enumerate(etl.new_df.columns):
        etl.tabela_exportar.setItem(0, i, QTableWidgetItem(coluna))

    column_n = 0
    row = 1
    for coluna in etl.new_df.columns:
        for i in range(1, 11):
            etl.tabela_exportar.setItem(
                row, column_n, QTableWidgetItem(
                    str(etl.new_df.select(
                        etl.new_df[coluna]).take(i)[i - 1][0])))
            row += 1
        row = 1
        column_n += 1


def etl_exportar_csv():
    try:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(etl,
                                                  'Save File', '',
                                                  'Arquivo csv(*.csv)')
        if filename:
            etl.new_df.toPandas().to_csv(filename, index=False)
    except NameError:
        ...


def exportar_profile():
    try:
        etl.label_grafico.setText('Trabalhando na Analise')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(etl,
                                                  'Save File', '',
                                                  'html(*.txt)')
        if filename:
            try:
                tmp_new_df = etl.new_df.toPandas()
                profile = ProfileReport(tmp_new_df,
                                        title='Profile',
                                        explorative=True)
                profile.to_file(f'{filename}')
                etl.label_grafico.setText('Analise gerado com sucesso')
                tmp_df = download.df.toPandas()
                profile = ProfileReport(tmp_df,
                                        title='Profile',
                                        explorative=True)
                profile.to_file(f'{filename}')
                etl.label_grafico.setText('Analise gerado com sucesso')
            except AttributeError:
                ...
    except NameError:
        ...


def thread_visualizar_dados():
    download.thread_executar_visualizar = _Thread(escreve_tabela_download)
    download.thread_executar_visualizar.start()


def thread_exportar_dados():
    etl.thread_aplicar_itens_etl = _Thread(aplicar_itens_etl)
    etl.thread_aplicar_itens_etl.start()


def setStyle(text):
    if text == 'Fusion':
        app.setStyleSheet('')
        app.setStyle(QStyleFactory.create('Fusion'))
    elif text == 'Windows':
        app.setStyleSheet('')
        app.setStyle(QStyleFactory.create('Windows'))
    elif text == 'Dark':
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    elif text == 'DarkGray':
        app.setStyleSheet(qdarkgraystyle.load_stylesheet())


if __name__ == '__main__':
    import sys

    from tabs.download import Download, _Thread
    from tabs.etl import Etl
    from tabs.merge import Merge
    from tabs.config import Config

    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('Windows'))
    download = Download()
    download.visualizar_banco.clicked.connect(thread_visualizar_dados)

    etl = Etl()
    etl.botao_aplicar_extracao.clicked.connect(thread_exportar_dados)

    # etl.botao_aplicar_aplicar.clicked.connect(thread_exportar_dados)
    etl.botao_exportar.clicked.connect(etl_exportar_csv)
    # etl.botao_salvar_html.clicked.connect(exportar_profile)

    merge = Merge()
    config = Config()
    config.select_layout.currentTextChanged.connect(setStyle)

    main = Pydbsus_gui(download, etl, merge, config)
    sys.exit(app.exec_())
