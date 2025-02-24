from PyQt5 import uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="bd_teste"
)

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO new_table (cliente_table,email_table,endereco_table) VALUES (%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    # Limpa os campos
    formulario.lineEdit.setText("")
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

    for i in range(0, len(dados_lidos)):
        for j in range(0, 4):
            listarcliente.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def excluir_cliente():
    linha = listarcliente.tableWidget.currentRow()  # Obtém a linha selecionada no QTableWidget
    listarcliente.tableWidget.removeRow(linha)  # Remove a linha selecionada da interface gráfica

    cursor = banco.cursor()
    cursor.execute("SELECT idnew_table FROM new_table")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM new_table WHERE idnew_table = %s", (valor_id,))
    banco.commit()

def Editar_cliente():
    linha = listarcliente.tableWidget.currentRow()  # Obtém a linha selecionada
    if linha != -1:  # Verifica se uma linha foi realmente selecionada
        # Pega os dados da linha selecionada
        dados_cliente = []
        for col in range(4):  # Assumindo que temos 3 colunas de dados (cliente, email, endereco)
            dados_cliente.append(listarcliente.tableWidget.item(linha, col).text())
        
        # Preenche os campos de edição com os dados
        Editarcliente.lineEdit.setText(dados_cliente[1])  # Cliente
        Editarcliente.lineEdit_2.setText(dados_cliente[2])  # Email
        Editarcliente.lineEdit_3.setText(dados_cliente[3])  # Endereço

        Editarcliente.show()  # Exibe a janela de edição

def salvar_edicoes():
    cliente = Editarcliente.lineEdit.text()
    email = Editarcliente.lineEdit_2.text()
    endereco = Editarcliente.lineEdit_3.text()

    linha = listarcliente.tableWidget.currentRow()
    id_cliente = listarcliente.tableWidget.item(linha, 0).text()  # Supondo que o ID está na primeira coluna

    cursor = banco.cursor()
    cursor.execute("""
        UPDATE new_table
        SET cliente_table = %s, email_table = %s, endereco_table = %s
        WHERE idnew_table = %s
    """, (cliente, email, endereco, id_cliente))

    banco.commit()
    listar_cliente()  # Atualiza a lista de clientes
    Editarcliente.close()  # Fecha a janela de edição


# Conexões de Botões
app = QtWidgets.QApplication([])
formulario = uic.loadUi('cadastro.ui')
listarcliente = uic.loadUi('listar_clientes.ui')
Editarcliente = uic.loadUi('Editar.ui')

formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(listar_cliente)
listarcliente.pushButton.clicked.connect(excluir_cliente)
listarcliente.pushButton_2.clicked.connect(Editar_cliente)  # Isso já chama a função correta Editar_cliente
Editarcliente.pushButton.clicked.connect(salvar_edicoes)  # Conectar o botão de salvar da janela de edição

formulario.show()
app.exec()
