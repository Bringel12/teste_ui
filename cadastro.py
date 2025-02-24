from PyQt5 import uic,QtWidgets
import mysql.connector


banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "bd_teste"
)



def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()




    cursor = banco.cursor()
    comando_SQL = "INSERT INTO new_table (cliente_table,email_table,endereco_table) VALUES (%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    # formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def listar_cliente():
    listarcliente.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM  new_table"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    listarcliente.tableWidget.setRowCount(len(dados_lidos))
    listarcliente.tableWidget.setColumnCount(4)


    for i  in range(0, len(dados_lidos)):
        for j in range(0, 4):
            listarcliente.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    
app=QtWidgets.QApplication([])
formulario=uic.loadUi('cadastro.ui')
listarcliente=uic.loadUi('listar_clientes.ui')
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(listar_cliente)
# listarcliente.pushButon.clecked.connect(excluir_cliente)
formulario.show()
app.exec()