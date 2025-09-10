from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from rapidfuzz import process, fuzz  # Para correção de raça

janela = Tk()

class Aplicativo:
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames()
        self.botoes_superior()
        self.tela_inicial()
        self.criar_tabela_pets()
        self.criar_tabela_racas()
        self.popular_racas()
        self.listar_pets()
        self.janela.mainloop()

    # ------------------- TELA -------------------
    def tela(self):
        self.janela.title("Pet Shop")
        self.janela.geometry("1150x600")
        self.janela.resizable(True, True)
        self.janela.configure(background="#f5f5f5")

    def frames(self):
        self.header = Frame(self.janela, height=80, bg="#4CAF50")
        self.header.pack(side="top", fill="x")
        for i in range(5):
            self.header.grid_columnconfigure(i, weight=1)

    def botoes_superior(self):
        btn_cfg = {
            "bd": 0,
            "relief": "flat",
            "bg": "#4CAF50",
            "fg": "#ffffff",
            "activebackground": "#45a049",
            "activeforeground": "#ffffff",
            "font": ("Segoe UI", 12, "bold"),
            "cursor": "hand2",
            "height": 2
        }

        self.btn_cadastrar = Button(self.header, text="Cadastrar Pet", command=self.abrir_janela_cadastro, **btn_cfg)
        self.btn_consultar = Button(self.header, text="Consultar Pets", command=self.consultar_pet_detalhes, **btn_cfg)
        self.btn_visita    = Button(self.header, text="Registrar Visita", command=self.registrar_visita, **btn_cfg)
        self.btn_excluir_visita = Button(self.header, text="Excluir Visita", command=self.excluir_visita, **btn_cfg)
        self.btn_excluir_pet = Button(self.header, text="Excluir Pet", command=self.excluir_pet, **btn_cfg)

        self.btn_cadastrar.grid(row=0, column=0, sticky="nsew")
        self.btn_consultar.grid(row=0, column=1, sticky="nsew")
        self.btn_visita.grid(row=0, column=2, sticky="nsew")
        self.btn_excluir_visita.grid(row=0, column=3, sticky="nsew")
        self.btn_excluir_pet.grid(row=0, column=4, sticky="nsew")

    def tela_inicial(self):
        colunas = ("ID", "Nome do Pet", "Raça", "Idade", "Peso", "Tamanho", "Dono", "Telefone", "Última Visita")
        self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10, padx=10)

    # ------------------- BANCO DE DADOS -------------------
    def conectar_bd(self):
        self.conn = sqlite3.connect("petshop.db")
        self.cursor = self.conn.cursor()

    def desconectar_bd(self):
        self.conn.close()

    def criar_tabela_pets(self):
        self.conectar_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                raca TEXT,
                idade TEXT,
                peso REAL,
                tamanho REAL,
                dono TEXT,
                telefone TEXT,
                ultima_visita TEXT DEFAULT 'Sem visitas'
            )
        """)
        self.conn.commit()
        self.desconectar_bd()

    def criar_tabela_racas(self):
        self.conectar_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS racas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raca TEXT,
                tipo_pelo TEXT,
                porte TEXT,
                escovacao TEXT,
                tosa TEXT,
                cuidados TEXT,
                peso_min REAL,
                peso_max REAL,
                tamanho_min REAL,
                tamanho_max REAL
            )
        """)
        self.conn.commit()
        self.desconectar_bd()

    def popular_racas(self):
        self.conectar_bd()
        self.cursor.execute("SELECT COUNT(*) FROM racas")
        if self.cursor.fetchone()[0] == 0:
            racas_dados = [
                ("Labrador Retriever", "Curto", "Grande", "1x/semana", "Rara", "Banhos frequentes, cuidado com frio", 25, 36, 55, 62),
                ("Bulldog Francês", "Curto", "Pequeno", "1x/semana", "Rara", "Atenção com pele e exercícios", 8, 14, 30, 33),
            ]
            self.cursor.executemany("""
                INSERT INTO racas
                (raca, tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, racas_dados)
            self.conn.commit()
        self.desconectar_bd()

    # ------------------- CADASTRO DE PET -------------------
    def abrir_janela_cadastro(self):
        self.top = Toplevel(self.janela)
        self.top.title("Cadastro de Pet")
        largura, altura = 400, 520
        self.janela.update_idletasks()
        largura_principal = self.janela.winfo_width()
        altura_principal = self.janela.winfo_height()
        x_principal = self.janela.winfo_x()
        y_principal = self.janela.winfo_y()
        pos_x = x_principal + (largura_principal // 2) - (largura // 2)
        pos_y = y_principal + (altura_principal // 2) - (altura // 2)
        self.top.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.top.configure(bg="#dedbd3")
        self.top.resizable(False, False)

        Label(self.top, text="Nome do Pet:", bg="#dedbd3").pack(pady=5)
        self.entry_nome = Entry(self.top, width=35)
        self.entry_nome.pack(pady=5)

        Label(self.top, text="Raça:", bg="#dedbd3").pack(pady=5)
        self.entry_raca = Entry(self.top, width=35)
        self.entry_raca.pack(pady=5)

        Label(self.top, text="Idade:", bg="#dedbd3").pack(pady=5)
        self.entry_idade = Entry(self.top, width=35)
        self.entry_idade.pack(pady=5)

        Label(self.top, text="Peso (kg):", bg="#dedbd3").pack(pady=5)
        self.entry_peso = Entry(self.top, width=35)
        self.entry_peso.pack(pady=5)

        Label(self.top, text="Tamanho (cm):", bg="#dedbd3").pack(pady=5)
        self.entry_tamanho = Entry(self.top, width=35)
        self.entry_tamanho.pack(pady=5)

        Label(self.top, text="Nome do Dono:", bg="#dedbd3").pack(pady=5)
        self.entry_dono = Entry(self.top, width=35)
        self.entry_dono.pack(pady=5)

        Label(self.top, text="Telefone:", bg="#dedbd3").pack(pady=5)
        self.entry_telefone = Entry(self.top, width=35)
        self.entry_telefone.pack(pady=5)

        Button(self.top, text="Salvar e Comparar Raça", bg="#4CAF50", fg="white",
               command=self.salvar_e_comparar).pack(pady=20)

    # ------------------- SUGESTÃO DE RAÇA -------------------
    def sugerir_raca(self, raca_digitada):
        self.conectar_bd()
        self.cursor.execute("SELECT raca FROM racas")
        racas_cadastradas = [r[0] for r in self.cursor.fetchall()]
        self.desconectar_bd()
        melhor_match = process.extractOne(raca_digitada, racas_cadastradas, scorer=fuzz.WRatio, score_cutoff=60)
        if melhor_match:
            return melhor_match[0]
        return raca_digitada

    def salvar_e_comparar(self):
        try:
            peso = float(self.entry_peso.get())
            tamanho = float(self.entry_tamanho.get())
        except ValueError:
            messagebox.showwarning("Erro", "Peso e tamanho devem ser números.")
            return

        nome = self.entry_nome.get()
        raca_digitada = self.entry_raca.get()
        idade = self.entry_idade.get()
        dono = self.entry_dono.get()
        telefone = self.entry_telefone.get()

        if nome == "" or dono == "":
            messagebox.showwarning("Erro", "Preencha pelo menos o nome do pet e do dono.")
            return

        raca_correta = self.sugerir_raca(raca_digitada)
        if raca_correta.lower() != raca_digitada.lower():
            confirmar = messagebox.askyesno(
                "Confirmação de Raça",
                f"A raça digitada foi '{raca_digitada}'. Deseja corrigir para '{raca_correta}'?"
            )
            if confirmar:
                raca_digitada = raca_correta

        self.conectar_bd()
        self.cursor.execute("""
            INSERT INTO pets (nome, raca, idade, peso, tamanho, dono, telefone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, raca_digitada, idade, peso, tamanho, dono, telefone))
        self.conn.commit()
        self.desconectar_bd()
        self.listar_pets()
        self.top.destroy()

        self.comparar_raca(nome, raca_digitada, peso, tamanho, idade)

    # ------------------- LISTAR PETS -------------------
    def listar_pets(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.conectar_bd()
        self.cursor.execute("SELECT * FROM pets")
        for pet in self.cursor.fetchall():
            self.tree.insert("", END, values=pet)
        self.desconectar_bd()

    # ------------------- CONSULTA DETALHADA -------------------
    def consultar_pet_detalhes(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Erro", "Selecione um pet para consultar.")
            return

        pet_id = self.tree.item(selecionado[0], "values")[0]

        self.conectar_bd()
        self.cursor.execute("SELECT nome, raca, idade, peso, tamanho, dono, telefone FROM pets WHERE id=?", (pet_id,))
        pet = self.cursor.fetchone()
        self.cursor.execute("SELECT tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max FROM racas WHERE raca=?", (pet[1],))
        raca = self.cursor.fetchone()
        self.desconectar_bd()

        top = Toplevel(self.janela)
        top.title(f"Detalhes do Pet: {pet[0]}")
        top.geometry("500x400")
        top.configure(bg="#dedbd3")

        Label(top, text=f"Nome: {pet[0]}", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Raça: {pet[1]}", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Idade: {pet[2]}", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Peso: {pet[3]} kg", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Tamanho: {pet[4]} cm", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Dono: {pet[5]}", bg="#dedbd3").pack(pady=2)
        Label(top, text=f"Telefone: {pet[6]}", bg="#dedbd3").pack(pady=2)

        if raca:
            tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max = raca
            Label(top, text="--- Cuidados Recomendados ---", bg="#dedbd3", font=("Segoe UI", 10, "bold")).pack(pady=5)
            Label(top, text=f"Tipo de Pelo: {tipo_pelo}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Porte: {porte}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Escovação: {escovacao}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Tosa: {tosa}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Cuidados: {cuidados}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Peso ideal: {peso_min}-{peso_max} kg", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Tamanho ideal: {tamanho_min}-{tamanho_max} cm", bg="#dedbd3").pack(pady=1)
        else:
            Label(top, text="Raça não encontrada no banco.", bg="#dedbd3").pack(pady=5)

    # ------------------- REGISTRAR VISITA -------------------
    def registrar_visita(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Erro", "Selecione um pet para registrar visita.")
            return
        pet_id = self.tree.item(selecionado[0], "values")[0]
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.conectar_bd()
        self.cursor.execute("UPDATE pets SET ultima_visita=? WHERE id=?", (data, pet_id))
        self.conn.commit()
        self.desconectar_bd()
        self.listar_pets()

    # ------------------- EXCLUIR VISITA -------------------
    def excluir_visita(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Erro", "Selecione um pet para excluir visita.")
            return
        pet_id = self.tree.item(selecionado[0], "values")[0]
        self.conectar_bd()
        self.cursor.execute("UPDATE pets SET ultima_visita='Sem visitas' WHERE id=?", (pet_id,))
        self.conn.commit()
        self.desconectar_bd()
        self.listar_pets()

    # ------------------- EXCLUIR PET -------------------
    def excluir_pet(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Erro", "Selecione um pet para excluir.")
            return
        pet_id = self.tree.item(selecionado[0], "values")[0]
        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este pet?")
        if confirmar:
            self.conectar_bd()
            self.cursor.execute("DELETE FROM pets WHERE id=?", (pet_id,))
            self.conn.commit()
            self.desconectar_bd()
            self.listar_pets()

# ------------------- RODAR APLICATIVO -------------------
Aplicativo()