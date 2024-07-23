import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog, BOTH, CENTER
from datetime import datetime
import json
import matplotlib.pyplot as plt

class Tipo:
    def __init__(self, nome):
        self.nome = nome

class Lote:
    def __init__(self, numero):
        self.numero = numero

class Validade:
    def __init__(self, data):
        self.data = datetime.strptime(data, "%d/%m/%Y")

class Produto:
    def __init__(self, nome, quantidade, preco, tipo, lote, validade, codigo_barras):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.tipo = tipo
        self.lote = lote
        self.validade = validade
        self.codigo_barras = codigo_barras

estoque = []

def cadastrar_item():
    def salvar():
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get().replace(',', '.')  # Substitui vírgula por ponto
        tipo = entry_tipo.get()
        lote = entry_lote.get()
        validade = entry_validade.get()
        codigo_barras = entry_codigo_barras.get()
        
        if not quantidade.isdigit():
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
            return
        
        try:
            quantidade = int(quantidade)
            preco = float(preco) * 100  # Converter para centavos
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.")
            return
        
        tipo = Tipo(tipo)
        lote = Lote(lote)
        validade = Validade(validade)
        produto = Produto(nome, quantidade, preco, tipo, lote, validade, codigo_barras)
        estoque.append(produto)
        listar_estoque()
        window_cadastro.destroy()

    window_cadastro = ttk.Toplevel()
    window_cadastro.title("Cadastrar Item")

    frame = ttk.Frame(window_cadastro, padding=20)
    frame.pack()

    ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky=W)
    entry_nome = ttk.Entry(frame)
    entry_nome.grid(row=0, column=1)

    ttk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky=W)
    entry_quantidade = ttk.Entry(frame)
    entry_quantidade.grid(row=1, column=1)

    ttk.Label(frame, text="Preço:").grid(row=2, column=0, sticky=W)
    entry_preco = ttk.Entry(frame)
    entry_preco.grid(row=2, column=1)

    ttk.Label(frame, text="Tipo:").grid(row=3, column=0, sticky=W)
    entry_tipo = ttk.Entry(frame)
    entry_tipo.grid(row=3, column=1)

    ttk.Label(frame, text="Lote:").grid(row=4, column=0, sticky=W)
    entry_lote = ttk.Entry(frame)
    entry_lote.grid(row=4, column=1)

    ttk.Label(frame, text="Validade (dd/mm/yyyy):").grid(row=5, column=0, sticky=W)
    entry_validade = ttk.Entry(frame)
    entry_validade.grid(row=5, column=1)

    ttk.Label(frame, text="Código de Barras:").grid(row=6, column=0, sticky=W)
    entry_codigo_barras = ttk.Entry(frame)
    entry_codigo_barras.grid(row=6, column=1)

    btn_salvar = ttk.Button(frame, text="Salvar", command=salvar, style='info.TButton')
    btn_salvar.grid(row=7, columnspan=2, pady=10)

def listar_estoque():
    for item in tabela_estoque.get_children():
        tabela_estoque.delete(item)
    for produto in estoque:
        tabela_estoque.insert("", "end", values=(produto.nome, produto.quantidade, produto.preco / 100, produto.tipo.nome, produto.lote.numero, produto.validade.data.strftime("%d/%m/%Y"), produto.codigo_barras))

# Função para verificar validade dos itens e exibir alerta
def verificar_validade():
    hoje = datetime.now()
    for produto in estoque:
        if produto.validade.data < hoje:
            messagebox.showwarning("Aviso de Validade", f"O produto {produto.nome} está vencido!")

# Função para consultar item pelo código de barras
def consultar_item_codigo_barras():
    def consultar():
        codigo_barras = entry_codigo.get()
        for produto in estoque:
            if produto.codigo_barras == codigo_barras:
                messagebox.showinfo("Consulta de Item", f"Nome: {produto.nome}\nQuantidade: {produto.quantidade}\nPreço: {produto.preco / 100:.2f}\nTipo: {produto.tipo.nome}\nLote: {produto.lote.numero}\nValidade: {produto.validade.data.strftime('%d/%m/%Y')}")
                return
        messagebox.showwarning("Consulta de Item", "Item não encontrado.")
        window_consulta.destroy()

    window_consulta = ttk.Toplevel()
    window_consulta.title("Consultar Item pelo Código de Barras")

    frame = ttk.Frame(window_consulta, padding=20)
    frame.pack()

    ttk.Label(frame, text="Código de Barras:").grid(row=0, column=0, sticky=W)
    entry_codigo = ttk.Entry(frame)
    entry_codigo.grid(row=0, column=1)

    btn_consultar = ttk.Button(frame, text="Consultar", command=consultar, style='info.TButton')
    btn_consultar.grid(row=1, columnspan=2, pady=10)

# Função para gerar gráfico informativo
def gerar_grafico():
    categorias = ["Saídas", "Perdas", "Entradas"]
    valores = [sum(produto.quantidade for produto in estoque), 0, sum(produto.quantidade for produto in estoque)]  # Placeholder para perdas
    plt.bar(categorias, valores)
    plt.xlabel('Categorias')
    plt.ylabel('Quantidade')
    plt.title('Gráfico Informativo')
    plt.show()

# Função para salvar o estoque em JSON
def salvar_estoque_json():
    dados_para_salvar = []
    for produto in estoque:
        dados_produto = {
            'nome': produto.nome,
            'quantidade': produto.quantidade,
            'preco': produto.preco,
            'tipo': produto.tipo.nome,
            'lote': produto.lote.numero,
            'validade': produto.validade.data.strftime("%d/%m/%Y"),
            'codigo_barras': produto.codigo_barras
        }
        dados_para_salvar.append(dados_produto)
    
    with open('estoque.json', 'w') as arquivo_json:
        json.dump(dados_para_salvar, arquivo_json, indent=4)

    messagebox.showinfo("Salvar Estoque", "Estoque salvo em 'estoque.json'.")

# Função para carregar o estoque de um arquivo JSON
def carregar_estoque_json():
    global estoque
    estoque = []  # Limpa a lista de estoque antes de carregar
    try:
        with open('estoque.json', 'r') as arquivo_json:
            conteudo = arquivo_json.read()
            dados = json.loads(conteudo)
            for item in dados:
                tipo = Tipo(item['tipo'])
                lote = Lote(item['lote'])
                validade = Validade(item['validade'])
                produto = Produto(item['nome'], item['quantidade'], item['preco'], tipo, lote, validade, item['codigo_barras'])
                estoque.append(produto)
        messagebox.showinfo("Carregar Estoque", "Estoque carregado de 'estoque.json'.")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Arquivo 'estoque.json' não encontrado. Iniciando com estoque vazio.")
    except json.JSONDecodeError as e:
        messagebox.showerror("Erro", f"Erro ao carregar o JSON: {e}")

# Função para subtrair item com código de barras
def subtrair_item_codigo_barras():
    def remover():
        codigo_barras = entry_codigo.get()
        quantidade = entry_quantidade.get()

        # Se a quantidade não for especificada, assumir 1 unidade
        if not quantidade.isdigit():
            quantidade = 1
        else:
            quantidade = int(quantidade)

        # Buscar o produto pelo código de barras
        for produto in estoque:
            if produto.codigo_barras == codigo_barras:
                # Verificar se a quantidade a ser removida é válida
                if quantidade > 0 and produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                    listar_estoque()
                    window_subtrair.destroy()
                    return
                else:
                    messagebox.showerror("Erro", "Quantidade inválida ou insuficiente no estoque.")
                    return
        
        # Se não encontrar o produto pelo código de barras
        messagebox.showerror("Erro", "Código de barras não encontrado.")

# Criar a janela para remover itens
    window_subtrair = ttk.Toplevel()
    window_subtrair.title("Subtrair Itens com Código de Barras")

    frame = ttk.Frame(window_subtrair, padding=20)
    frame.pack()

    ttk.Label(frame, text="Código de Barras:").grid(row=0, column=0, sticky=W)
    entry_codigo = ttk.Entry(frame)
    entry_codigo.grid(row=0, column=1)

    ttk.Label(frame, text="Quantidade (opcional):").grid(row=1, column=0, sticky=W)
    entry_quantidade = ttk.Entry(frame)
    entry_quantidade.grid(row=1, column=1)
    btn_remover = ttk.Button(frame, text="Remover", command=remover, style='info.TButton')
    btn_remover.grid(row=2, columnspan=2, pady=10)

# Função para sair do programa
def sair_programa():
    salvar_estoque_json()
    root.quit()

# Função para criar a interface gráfica
def criar_interface():
    global root, tabela_estoque

    # Inicializar a janela principal
    root = ttk.Window(themename="superhero")
    root.title("Sistema de Gestão de Estoque")

    # Criar o frame para os botões
    frame = ttk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Criar os botões e posicionar
    btn_cadastrar = ttk.Button(frame, text="Cadastrar Item", command=cadastrar_item, style='info.TButton')
    btn_cadastrar.grid(row=0, column=0, padx=10, pady=5)

    btn_remover = ttk.Button(frame, text="Remover Item", command=remover_item, style='info.TButton')
    btn_remover.grid(row=0, column=1, padx=10, pady=5)

    btn_adicionar = ttk.Button(frame, text="Adicionar Itens com Código de Barras", command=adicionar_item_codigo_barras, style='info.TButton')
    btn_adicionar.grid(row=0, column=2, padx=10, pady=5)

    btn_subtrair = ttk.Button(frame, text="Subtrair Itens com Código de Barras", command=subtrair_item_codigo_barras, style='info.TButton')
    btn_subtrair.grid(row=1, column=2, padx=10, pady=5)

    btn_consultar = ttk.Button(frame, text="Consultar Item pelo Código de Barras", command=consultar_item_codigo_barras, style='info.TButton')
    btn_consultar.grid(row=1, column=0, padx=10, pady=5)

    btn_verificar = ttk.Button(frame, text="Verificar Validade dos Itens", command=verificar_validade, style='info.TButton')
    btn_verificar.grid(row=1, column=1, padx=10, pady=5)

    btn_grafico = ttk.Button(frame, text="Gerar Gráfico Informativo", command=gerar_grafico, style='info.TButton')
    btn_grafico.grid(row=2, column=2, padx=10, pady=5)

    btn_salvar = ttk.Button(frame, text="Salvar Estoque", command=salvar_estoque_json, style='info.TButton')
    btn_salvar.grid(row=2, column=0, padx=10, pady=5)

    btn_carregar = ttk.Button(frame, text="Carregar Estoque", command=carregar_estoque_json, style='info.TButton')
    btn_carregar.grid(row=2, column=1, padx=10, pady=5)

    # Adicionando o botão "Salvar e Sair" na parte inferior direita
    btn_sair = ttk.Button(root, text="Salvar e Sair", command=sair_programa, style='info.TButton')
    btn_sair.pack(side="bottom", padx=20, pady=10, anchor='se')

    # Frame para a tabela
    frame_tabela = ttk.Frame(root)
    frame_tabela.pack(pady=10, padx=20, fill=BOTH, expand=True)  # Ajustando o padding para posicionar mais para cima

    # Configuração da tabela
    tabela_estoque = ttk.Treeview(frame_tabela, columns=["Nome", "Quantidade", "Preço", "Tipo", "Lote", "Validade", "Código de Barras"], show="headings", style="Custom.Treeview")
    
    # Configurar colunas para ajustar automaticamente ao conteúdo
    for col in tabela_estoque["columns"]:
        tabela_estoque.column(col, width=120, anchor=CENTER)  # Ajuste a largura conforme necessário

    for col in tabela_estoque["columns"]:
        tabela_estoque.heading(col, text=col)

    tabela_estoque.pack(fill=BOTH, expand=True)

    # Adicionar linhas divisórias singelas
    style = ttk.Style()
    style.configure("Custom.Treeview", rowheight=25, font=("Helvetica", 10), borderwidth=1, relief="solid", background="white")
    style.configure("Custom.Treeview.Heading", font=("Helvetica", 10, "bold"))
    style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])

    carregar_estoque_json()
    listar_estoque()
    verificar_validade()

    root.mainloop()

# Função para remover item
def remover_item():
    nome = simpledialog.askstring("Remover Item", "Digite o nome do item a ser removido:")
    for produto in estoque:
        if produto.nome == nome:
            estoque.remove(produto)
            messagebox.showinfo("Sucesso", "Item removido do estoque com sucesso.")
            salvar_estoque_json()  # Salvar após remover um item
            return
    messagebox.showerror("Erro", "Item não encontrado no estoque.")
    listar_estoque()

# Função para adicionar itens pelo código de barras
def adicionar_item_codigo_barras():
    def adicionar():
        codigo_barras = entry_codigo.get()
        quantidade = entry_quantidade.get()
        
        # Verificar se a quantidade é um número inteiro
        if not quantidade.isdigit():
            # Se não for um número inteiro, adicionar uma unidade por padrão
            quantidade = 1  # Adiciona uma unidade por padrão
        else:
            quantidade = int(quantidade)

        for produto in estoque:
            if produto.codigo_barras == codigo_barras:
                produto.quantidade += quantidade
                listar_estoque()
                window_adicionar.destroy()
                return
        messagebox.showwarning("Adicionar Itens", "Item não encontrado.")
        window_adicionar.destroy()

    window_adicionar = ttk.Toplevel()
    window_adicionar.title("Adicionar Itens com Código de Barras")

    frame = ttk.Frame(window_adicionar, padding=20)
    frame.pack()

    ttk.Label(frame, text="Código de Barras:").grid(row=0, column=0, sticky=W)
    entry_codigo = ttk.Entry(frame)
    entry_codigo.grid(row=0, column=1)

    ttk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky=W)
    entry_quantidade = ttk.Entry(frame)
    entry_quantidade.grid(row=1, column=1)

    btn_adicionar = ttk.Button(frame, text="Adicionar", command=adicionar, style='info.TButton')
    btn_adicionar.grid(row=2, columnspan=2, pady=10)

# Criar a interface
criar_interface()
