from tkinter import *
from tkinter import messagebox
from tkinter import ttk   
import sqlite3
from rapidfuzz import process, fuzz  
from  datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform

janela = Tk()

# ---------- CLASSE PRINCIPAL DA APLICAÇÃO ----------
class aplicacao:
    def __init__(self):
        self.janela = janela
        
        self.bd_manager = banco_de_dados()
        self.pet_manager = GerenciadorPets(self.bd_manager)
        self.cliente_manager = GerenciadorClientes(self.bd_manager)
        self.relatorio_manager = GeradorRelatorios()
        
        # Configurar interface
        self.tela()
        self.frames()
        self.botoes_superior()
        self.tela_inicial()
        
        # Inicializar banco de dados
        self.inicializar_banco_dados()
        self.atualizar_tabela_clientes()  
        self.janela.mainloop()

    def inicializar_banco_dados(self):
        self.bd_manager.criar_tabela_racas()
        self.bd_manager.popular_dados_racas()
        self.bd_manager.criar_tabela_genericas()
        self.bd_manager.popular_dados_genericos()
        self.bd_manager.criar_tabela_clientes()

    # ---------- TELA PRINCIPAL ----------
    def tela(self):
        self.janela.title("pet shop")
        self.janela.geometry("1024x768")
        self.janela.resizable(True, True)
        self.janela.configure(background="#E9EDF0")  

    def frames(self):
        self.header = Frame(self.janela, height=100, bg="#2C3E50")  
        self.header.pack(side="top", fill="x")
        for i in range(5):
            self.header.grid_columnconfigure(i, weight=1)

    def botoes_superior(self):
        btn_cfg = {
            "bd": 0,
            "relief": "flat",
            "bg": "#2C3E50",
            "fg": "#ECF0F1",
            "activebackground": "#34495E",
            "activeforeground": "#FFFFFF",
            "font": ("Segoe UI", 14, "bold"),
            "cursor": "hand2",
            "height": 2,
            "width": 25,
            "padx": 10,
            "pady": 10,
        }
        
        # Criando os botões
        self.btn_cadastrar = Button(self.header, text="🐾 Cadastrar Pet", command=self.abrir_janela_cadastro, **btn_cfg)
        self.btn_consultar = Button(self.header, text="🔍 Consultar Cadastro", command=self.consultar_cadastro_pet, **btn_cfg)
        self.btn_visita = Button(self.header, text="📅 Registrar Visita", command=self.registrar_visita, **btn_cfg)
        self.btn_excluir_pet = Button(self.header, text="➕ Cadastrar Raça", command=self.abrir_janela_cadastro_raca, **btn_cfg)

        # Organização dos botões
        self.btn_cadastrar.grid(row=0, column=0, sticky="nsew")
        self.btn_consultar.grid(row=0, column=1, sticky="nsew")
        self.btn_visita.grid(row=0, column=2, sticky="nsew")
        self.btn_excluir_pet.grid(row=0, column=4, sticky="nsew")

    def tela_inicial(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#0B0C0C", foreground="#000000", relief="flat")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#FFFFFF", foreground="#333333")
        
        colunas = ("Nome do Dono", "Telefone", "Última Visita")
        self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.janela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

    # ---------- JANELA DE CADASTRO ----------
    def abrir_janela_cadastro(self):
        self.top = Toplevel(self.janela)
        self.top.title("Cadastrar Novo Pet")
        self.top.configure(bg="#E0E0E0")
        self.top.resizable(False, False)

        largura, altura = 450, 600
        self.janela.update_idletasks()
        largura_principal = self.janela.winfo_width()
        altura_principal = self.janela.winfo_height()
        x_principal = self.janela.winfo_x()
        y_principal = self.janela.winfo_y()
        pos_x = x_principal + (largura_principal // 2) - (largura // 2)
        pos_y = y_principal + (altura_principal // 2) - (altura // 2)
        self.top.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        frame_principal = Frame(self.top, bg="#E0E0E0", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        Label(frame_principal, text="Registro de Pet", font=("Helvetica", 20, "bold"), bg="#E0E0E0", fg="#333333").pack(pady=(0, 20))

        label_cfg = {"bg": "#E0E0E0", "font": ("Helvetica", 10, "bold"), "fg": "#555555"}
        entry_cfg = {"bd": 1, "relief": "flat", "font": ("Helvetica", 10), "bg": "#FFFFFF", "fg": "#333333"}
    
        # Variáveis
        nome_pet_var = StringVar()
        raca_var = StringVar()
        idade_var = StringVar()
        peso_var = StringVar()
        tamanho_var = StringVar()
        nome_dono_var = StringVar()
        telefone_var = StringVar()

        # Campos
        Label(frame_principal, text="Nome do Pet:", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=nome_pet_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Raça:", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=raca_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Idade:", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=idade_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Peso (kg):", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=peso_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Tamanho (cm):", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=tamanho_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Nome do Dono:", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=nome_dono_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Label(frame_principal, text="Telefone:", **label_cfg).pack(anchor="w", pady=(5, 0))
        Entry(frame_principal, textvariable=telefone_var, **entry_cfg).pack(fill="x", pady=(0, 10))

        Button(
            frame_principal,
            text="Salvar e Comparar Raça",
            command=lambda: self.comparar_raca(
                nome_pet_var.get(), raca_var.get(), peso_var.get(),
                tamanho_var.get(), idade_var.get(), nome_dono_var.get(), telefone_var.get()
            ),
            bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
            bd=0, relief="flat", activebackground="#45A049",
            activeforeground="white", cursor="hand2"
        ).pack(pady=(20, 0), ipadx=10, ipady=5)

    # ---------- COMPARAÇÃO DE RAÇA ----------
    def comparar_raca(self, nome_pet, raca_digitada, peso, tamanho, idade, nome_dono, telefone):
        try:
            peso = float(peso)
            tamanho = float(tamanho)
        except ValueError:
            messagebox.showinfo("Erro", "Peso e tamanho devem ser números.", parent=self.janela)
            return

        raca_sugerida = self.pet_manager.sugerir_raca(raca_digitada)

        if raca_sugerida:
            if raca_sugerida.lower() != raca_digitada.lower():
                resposta = messagebox.askyesno(
                    "Sugestão de Raça",
                    f"Você digitou '{raca_digitada}'.\n"
                    f"A raça mais próxima encontrada foi '{raca_sugerida}'.\n\n"
                    "Deseja usar essa sugestão?"
                )
                if not resposta:
                    self.abrir_janela_generica(nome_pet, idade, peso, tamanho, nome_dono, telefone)
                    return

            resultado = self.pet_manager.obter_dados_raca(raca_sugerida)
            if resultado:
                self.relatorio_pet(nome_pet, raca_sugerida, peso, tamanho, idade, resultado, telefone, nome_dono)
                return

        self.abrir_janela_generica(nome_pet, idade, peso, tamanho, nome_dono, telefone)

    # ---------- RELATÓRIO DO PET ----------
    def relatorio_pet(self, nome_pet, raca, peso, tamanho, idade, resultado_raca, telefone, nome_dono):
        top = Toplevel(self.janela)
        top.title(f"Relatório do Pet: {nome_pet}")
        top.geometry("500x600")
        top.configure(bg="#dedbd3")

        divergencias = []

        if resultado_raca:
            tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max = resultado_raca
            
            Label(top, text=f"Nome: {nome_pet}", bg="#dedbd3").pack(pady=2)
            Label(top, text=f"Raça: {raca}", bg="#dedbd3").pack(pady=2)
            Label(top, text=f"Idade: {idade}", bg="#dedbd3").pack(pady=2)
            Label(top, text=f"Peso: {peso} kg", bg="#dedbd3").pack(pady=2)
            Label(top, text=f"Tamanho: {tamanho} cm", bg="#dedbd3").pack(pady=2)
            Label(top, text="--- Rotina de Cuidados da Raça ---", bg="#dedbd3", font=("Segoe UI", 10, "bold")).pack(pady=5)
            Label(top, text=f"Tipo de Pelo: {tipo_pelo}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Porte: {porte}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Escovação: {escovacao}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Tosa: {tosa}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Cuidados: {cuidados}", bg="#dedbd3").pack(pady=1)

            if not (peso_min <= peso <= peso_max):
                divergencias.append(f"Peso fora do padrão ({peso_min}-{peso_max} kg)")
            if not (tamanho_min <= tamanho <= tamanho_max):
                divergencias.append(f"Tamanho fora do padrão ({tamanho_min}-{tamanho_max} cm)")

            Label(top, text="--- Divergências ---", bg="#dedbd3", font=("Segoe UI", 10, "bold")).pack(pady=5)
            if divergencias:
                for d in divergencias:
                    Label(top, text=d, bg="#dedbd3", fg="red").pack(pady=1)
            else:
                Label(top, text="O pet está dentro dos padrões da raça.", bg="#dedbd3", fg="green").pack(pady=1)

            Button(top, text=" Relatório em PDF", bg="#4CAF50", fg="white",
                   command=lambda: [self.gerar_pdf_raca(nome_pet, raca, peso, tamanho, idade, resultado_raca, divergencias, telefone, nome_dono), top.destroy()]
            ).pack(pady=20)
        else:
            Label(top, text="Dados da raça não encontrados.", bg="#dedbd3", fg="red").pack(pady=20)

        Button(top, text="Fechar", bg="#f44336", fg="white", 
               command=lambda: [self.perguntar_cadastro_cliente(nome_dono, nome_pet, telefone), top.destroy()]
        ).pack(pady=10)

   
    def gerar_pdf_raca(self, nome_pet, raca, peso, tamanho, idade, resultado_raca, divergencias, telefone, nome_dono):
        nome_arquivo = self.relatorio_manager.gerar_pdf_raca(nome_pet, raca, peso, tamanho, idade, resultado_raca, divergencias, telefone, nome_dono)
        if nome_arquivo:
            messagebox.showinfo("Sucesso", f"Relatório salvo como {nome_arquivo}", parent=self.janela)
        else:
            messagebox.showinfo("Erro", "Dados da raça não encontrados.", parent=self.janela)
        self.perguntar_cadastro_cliente(nome_dono, nome_pet, telefone)

    def perguntar_cadastro_cliente(self, nome_dono, nome_pet, telefone):
        cadastrar_cliente = messagebox.askyesno("Cadastro", "Deseja cadastrar o cliente?", parent=self.janela)
        if cadastrar_cliente:
            self.cadastrar_cliente(nome_dono, nome_pet, telefone)

    def cadastrar_cliente(self, nome_dono, nome_pet, telefone):
        self.cliente_manager.cadastrar_cliente(nome_dono, nome_pet, telefone)
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!", parent=self.janela)
        self.top.destroy()
        self.atualizar_tabela_clientes()

    def atualizar_tabela_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        resultados = self.cliente_manager.buscar_clientes()
        for row in resultados:
            self.tree.insert("", "end", values=row)

    # ---------- AVALIAÇÃO GENÉRICA ----------
    def abrir_janela_generica(self, nome_pet, idade, peso, tamanho, nome_dono, telefone):
        janela_generica = Toplevel(self.janela)
        janela_generica.title("Avaliação Genérica do Pet")
        janela_generica.geometry("500x400")
        janela_generica.configure(bg="#dedbd3")

        tipo_pelo_var = StringVar()
        porte_var = self.pet_manager.definir_porte(peso, tamanho)

        Label(janela_generica, text=f"Nome: {nome_pet}", bg="#dedbd3").pack(pady=5)
        Label(janela_generica, text=f"Idade: {idade}", bg="#dedbd3").pack(pady=5)
        Label(janela_generica, text=f"Porte sugerido: {porte_var}", bg="#dedbd3").pack(pady=5)
        Label(janela_generica, text="Tipo de Pelo:", bg="#dedbd3").pack(pady=5)
        Entry(janela_generica, textvariable=tipo_pelo_var, width=30).pack(pady=5)
    
        Button(janela_generica, text="Gerar Relatório Genérico", bg="#4CAF50", fg="white",
               command=lambda: [self.relatorio_generico(nome_pet, idade, peso, tamanho, tipo_pelo_var.get(), porte_var, nome_dono, telefone), janela_generica.destroy()]
        ).pack(pady=20)

    def relatorio_generico(self, nome_pet, idade, peso, tamanho, tipo_pelo, porte, nome_dono, telefone):
        top = Toplevel(self.janela)
        top.title(f"Relatório Genérico do Pet: {nome_pet}")
        top.geometry("500x400")
        top.configure(bg="#dedbd3")

        faixa_etaria = self.pet_manager.sugerir_faixa_etaria(idade)
        resultado = self.pet_manager.obter_dados_genericos(tipo_pelo, porte, faixa_etaria)

        if resultado:
            escovacao, tosa, cuidados = resultado
            Label(top, text=f"Nome: {nome_pet}", bg="#dedbd3").pack(pady=5)
            Label(top, text=f"Idade: {idade} ({faixa_etaria})", bg="#dedbd3").pack(pady=5)
            Label(top, text=f"Peso: {peso} kg", bg="#dedbd3").pack(pady=5)
            Label(top, text=f"Tamanho: {tamanho} cm", bg="#dedbd3").pack(pady=5)
            Label(top, text="--- Rotina de Cuidados Genéricos ---", bg="#dedbd3", font=("Segoe UI", 10, "bold")).pack(pady=5)
            Label(top, text=f"Tipo de Pelo: {tipo_pelo}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Porte: {porte}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Faixa Etária: {faixa_etaria}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Escovação: {escovacao}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Tosa: {tosa}", bg="#dedbd3").pack(pady=1)
            Label(top, text=f"Cuidados: {cuidados}", bg="#dedbd3").pack(pady=1)
        else:
            messagebox.showinfo("Erro", "Nenhum dado genérico encontrado para os critérios fornecidos.", parent=self.janela)

        Button(top, text="Gerar Relatório em PDF", bg="#4CAF50", fg="white",
               command=lambda: [self.gerar_pdf_generico(nome_pet, idade, peso, tamanho, tipo_pelo, porte, faixa_etaria, nome_dono, telefone), top.destroy()]
        ).pack(pady=20)
        Button(top, text="Fechar", bg="#f44336", fg="white", 
               command=lambda: [self.perguntar_cadastro_cliente(nome_dono, nome_pet, telefone), top.destroy()]
        ).pack(pady=10)

    def gerar_pdf_generico(self, nome_pet, idade, peso, tamanho, tipo_pelo, porte, faixa_etaria, nome_dono, telefone):
        resultado = self.pet_manager.obter_dados_genericos(tipo_pelo, porte, faixa_etaria)
        
        if resultado:
            nome_arquivo = self.relatorio_manager.gerar_pdf_generico(nome_pet, idade, peso, tamanho, tipo_pelo, porte, faixa_etaria, nome_dono, telefone, resultado)
            if nome_arquivo:
                messagebox.showinfo("Sucesso", f"Relatório salvo como {nome_arquivo}", parent=self.janela)
        else:
            messagebox.showinfo("Erro", "Nenhum dado genérico encontrado para os critérios fornecidos.", parent=self.janela)

        cadastrar_cliente = messagebox.askyesno("Sucesso", "Deseja cadastrar o cliente?", parent=self.janela)
        if cadastrar_cliente:
            self.cadastrar_cliente(nome_dono, nome_pet, telefone)

    def consultar_cadastro_pet(self):
        janela_consulta = Toplevel(self.janela)
        janela_consulta.title("Consultar cadastro do Pet")
        janela_consulta.geometry("700x600")
        janela_consulta.configure(bg="#dedbd3")

        nome_cliente_var = StringVar()
        Label(janela_consulta, text="Pesquisar (Dono ou Pet):", bg="#dedbd3").pack(pady=10)
        Entry(janela_consulta, textvariable=nome_cliente_var).pack(pady=5)

        colunas = ("Nome do Dono", "Nome do Pet", "Telefone", "Ultima Visita")
        tree = ttk.Treeview(janela_consulta, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.current_tree = tree

        Button(janela_consulta, text="Consultar", bg="#4CAF50", fg="white",
               command=lambda: self.buscar_cliente(nome_cliente_var.get(), tree)).pack(pady=20)
        Button(janela_consulta, text="Editar Cadastro", bg="#f44336", fg="white",
               command=lambda: self.editar_cadastro(tree)).pack(pady=10)
        Button(janela_consulta, text="Excluir Cadastro", bg="#f44336", fg="white",
               command=lambda: self.excluir_cliente("", "")).pack(pady=10)

    def editar_cadastro(self, tree=None):
        if tree is None:
            if not hasattr(self, 'current_tree') or self.current_tree is None:
                messagebox.showwarning("Aviso", "Nenhuma lista de clientes aberta.")
                return
            tree = self.current_tree
            
        selecionado = tree.selection()  
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return

        item = tree.item(selecionado)
        nome_dono_atual, nome_pet_atual, telefone_atual, ultima_visita = item['values']

        janela_edicao = Toplevel(self.janela)
        janela_edicao.title("Editar Cadastro")
        janela_edicao.geometry("400x400")
        janela_edicao.configure(bg="#dedbd3")

        nome_dono_var = StringVar(value=nome_dono_atual)
        nome_pet_var = StringVar(value=nome_pet_atual)
        telefone_var = StringVar(value=telefone_atual)

        Label(janela_edicao, text="Nome do Dono:", bg="#dedbd3").pack(pady=5)
        Entry(janela_edicao, textvariable=nome_dono_var, width=30).pack(pady=5)
        Label(janela_edicao, text="Nome do Pet:", bg="#dedbd3").pack(pady=5)
        Entry(janela_edicao, textvariable=nome_pet_var, width=30).pack(pady=5)
        Label(janela_edicao, text="Telefone:", bg="#dedbd3").pack(pady=5)
        Entry(janela_edicao, textvariable=telefone_var, width=30).pack(pady=5)

        def salvar_alteracoes():
            self.cliente_manager.atualizar_cliente(nome_dono_atual, nome_pet_atual, nome_dono_var.get(), nome_pet_var.get(), telefone_var.get())
            messagebox.showinfo("Sucesso", "Cadastro atualizado com sucesso!", parent=janela_edicao)
            janela_edicao.destroy()
            self.buscar_cliente("", tree)

        Button(janela_edicao, text="Salvar Alterações", bg="#4CAF50", fg="white", command=salvar_alteracoes).pack(pady=20)

    def buscar_cliente(self, termo, tree):
        for item in tree.get_children():
            tree.delete(item)

        if termo.strip() == "":
            messagebox.showwarning("Aviso", "Digite um nome para pesquisar.")
            return

        try:
            resultados = self.cliente_manager.buscar_clientes(termo)
            if resultados:
                for row in resultados:
                    tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Aviso", "Nenhum cliente encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def excluir_cliente(self, nome_dono, nome_pet):
        tree = self.current_tree
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        
        item = tree.item(selecionado)
        nome_dono, nome_pet, telefone, ultima_visita = item['values']
        confirmar = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o cadastro de {nome_pet} do dono {nome_dono}?")
        if confirmar:
            self.cliente_manager.excluir_cliente(nome_dono, nome_pet)
            messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso!", parent=self.janela)
            self.buscar_cliente("", tree)
            self.atualizar_tabela_clientes()

    # ---------- REGISTRO DE VISITAS ----------
    def registrar_visita(self):
        janela_pesquisa = Toplevel(self.janela)
        janela_pesquisa.title("Registrar Visita")
        janela_pesquisa.geometry("600x500")
        janela_pesquisa.configure(bg="#dedbd3")

        nome_cliente_var = StringVar()
        Label(janela_pesquisa, text="Pesquisar Cliente:", bg="#dedbd3").pack(pady=10)
        Entry(janela_pesquisa, textvariable=nome_cliente_var).pack(pady=5)

        colunas = ("Nome do Dono", "Nome do Pet", "Telefone", "Última Visita")
        tree = ttk.Treeview(janela_pesquisa, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        tree.pack(fill="both", expand=True, pady=10)

        def buscar():
            for i in tree.get_children():
                tree.delete(i)
            resultados = self.cliente_manager.buscar_clientes(nome_cliente_var.get())
            for r in resultados:
                tree.insert("", "end", values=r[:4])

        def abrir_edicao():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente.", parent=janela_pesquisa)
                return

            item = tree.item(selecionado)["values"]
            cliente = self.cliente_manager.obter_dados_completos_cliente(item[0], item[2])
            nome_dono_atual, nome_pet_atual, telefone_atual, ultima_visita, peso_atual, tamanho_atual, raca_atual, idade_atual = cliente

            janela_visita = Toplevel(janela_pesquisa)
            janela_visita.title("Registrar Nova Visita")
            janela_visita.geometry("400x600")
            janela_visita.configure(bg="#dedbd3")

            peso_var = StringVar(value=peso_atual or "")
            tamanho_var = StringVar(value=tamanho_atual or "")

            Label(janela_visita, text="Nome do Dono:", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=StringVar(value=nome_dono_atual), state="readonly", width=30).pack(pady=5)
            Label(janela_visita, text="Nome do Pet:", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=StringVar(value=nome_pet_atual), state="readonly", width=30).pack(pady=5)
            Label(janela_visita, text="Raça:", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=StringVar(value=raca_atual or ""), state="readonly", width=30).pack(pady=5)
            Label(janela_visita, text="Idade:", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=StringVar(value=idade_atual or ""), state="readonly", width=30).pack(pady=5)
            Label(janela_visita, text="Telefone:", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=StringVar(value=telefone_atual), state="readonly", width=30).pack(pady=5)
            Label(janela_visita, text=f"Última visita: {ultima_visita}", bg="#dedbd3", fg="blue").pack(pady=10)
            Label(janela_visita, text="Novo Peso (kg):", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=peso_var, width=30).pack(pady=5)
            Label(janela_visita, text="Novo Tamanho (cm):", bg="#dedbd3").pack(pady=5)
            Entry(janela_visita, textvariable=tamanho_var, width=30).pack(pady=5)

            def registrar_nova_visita():
                try:
                    novo_peso = peso_var.get() if peso_var.get() else peso_atual
                    novo_tamanho = tamanho_var.get() if tamanho_var.get() else tamanho_atual
                    self.cliente_manager.registrar_visita(nome_dono_atual, nome_pet_atual, novo_peso, novo_tamanho)
                    messagebox.showinfo("Sucesso", "Visita registrada com sucesso!", parent=janela_visita)
                    janela_visita.destroy()
                    buscar()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao registrar visita: {e}", parent=janela_visita)

            Button(janela_visita, text="Registrar Visita", bg="#4CAF50", fg="white", command=registrar_nova_visita).pack(pady=20)

        Button(janela_pesquisa, text="Buscar", bg="#4CAF50", fg="white", command=buscar).pack(pady=5)
        Button(janela_pesquisa, text="Abrir Edição/Visita", bg="#f44336", fg="white", command=abrir_edicao).pack(pady=5)


    def abrir_janela_cadastro_raca(self):
        """Abre a janela de cadastro de nova raça"""
        self.pet_manager.tela_cadastro_raca()


class banco_de_dados:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def conectar_bd(self):
        self.conn = sqlite3.connect("petshop.db")
        self.cursor = self.conn.cursor()

    def desconectar_bd(self):
        if self.conn:
            self.conn.close()
            
    def criar_tabela_racas(self):
        self.conectar_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS racas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raca TEXT,
                tipo_pelo TEXT,
                porte TEXT,   
                idade TEXT,
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

    def popular_dados_racas(self):
        self.conectar_bd()
        racas_dados = [
            ("Labrador Retriever", "Curto", "Grande", "10-12 anos", "1x/semana", "Rara", 
             "Banhos frequentes, cuidado com frio", 25, 36, 55, 62),
            ("Bulldog Francês", "Curto", "Pequeno", "10-12 anos", "1x/semana", "Rara", 
             "Atenção com pele e exercícios", 8, 14, 30, 33),
        ]
        self.cursor.executemany("""
            INSERT OR IGNORE INTO racas 
            (raca, tipo_pelo, porte, idade, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, racas_dados)
        self.conn.commit()
        self.desconectar_bd()

    def criar_tabela_genericas(self):
        self.conectar_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genericas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_pelo TEXT,
                porte TEXT,
                faixa_etaria TEXT,
                escovacao TEXT,
                tosa TEXT,
                cuidados TEXT,
                peso_min REAL,
                peso_max REAL,
                altura_min REAL,
                altura_max REAL
            )
        """)
        self.conn.commit()
        self.desconectar_bd()

    def popular_dados_genericos(self):
        self.conectar_bd()
        dados = [
            ("Curto", "Pequeno", "Filhote", "1x/semana", "Rara", "Banhos mensais, cuidado com frio", 1, 10, 20, 30),
            ("Curto", "Médio", "Adulto", "1x/semana", "Rara", "Banhos mensais, cuidado com frio", 10, 25, 30, 60),
            ("Curto", "Grande", "Sênior", "1x/semana", "Rara", "Banhos mensais, cuidado com frio", 25, 45, 55, 80),
            ("Longo", "Pequeno", "Filhote", "2x/semana", "Mensal", "Escovação diária, banhos quinzenais", 1, 10, 20, 30),
            ("Longo", "Médio", "Adulto", "2x/semana", "Mensal", "Escovação diária, banhos quinzenais", 10, 25, 30, 60),
            ("Longo", "Grande", "Sênior", "2x/semana", "Mensal", "Escovação diária, banhos quinzenais", 25, 45, 55, 80),
            ("Cacheado", "Pequeno", "Filhote", "3x/semana", "Mensal", "Escovação diária, banhos quinzenais, hidratação semanal", 1, 10, 20, 30),
            ("Cacheado", "Médio", "Adulto", "3x/semana", "Mensal", "Escovação diária, banhos quinzenais, hidratação semanal", 10, 25, 30, 60),
            ("Cacheado", "Grande", "Sênior", "3x/semana", "Mensal", "Escovação diária, banhos quinzenais, hidratação semanal", 25, 45, 55, 80),
        ]
        self.cursor.executemany("""
            INSERT OR IGNORE INTO genericas
            (tipo_pelo, porte, faixa_etaria, escovacao, tosa, cuidados, peso_min, peso_max, altura_min, altura_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        self.conn.commit()
        self.desconectar_bd()

    def criar_tabela_clientes(self):
        self.conectar_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_dono TEXT NOT NULL,
                nome_pet TEXT NOT NULL,
                telefone TEXT,
                ultima_visita TEXT,
                peso REAL,
                tamanho REAL,
                raca TEXT,
                idade TEXT
            )
        """)
        self.conn.commit()
        self.desconectar_bd()


class GerenciadorPets:
    def __init__(self, bd_manager):
        self.bd_manager = bd_manager
        
    def sugerir_raca(self, raca_digitada):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("SELECT raca FROM racas")
        racas_cadastradas = [r[0] for r in self.bd_manager.cursor.fetchall()]
        self.bd_manager.desconectar_bd()
        melhor_match = process.extractOne(raca_digitada, racas_cadastradas, scorer=fuzz.WRatio, score_cutoff=60)
        if melhor_match:
            return melhor_match[0]
        return raca_digitada

    def definir_porte(self, peso, tamanho):
        if peso < 10 and tamanho < 30:
            return "Pequeno"
        elif peso < 25 and tamanho < 60:
            return "Médio"
        else:
            return "Grande"

    def sugerir_faixa_etaria(self, idade):
        try:
            idade = int(idade)
        except ValueError:
            return "Idade inválida"

        if idade < 1:
            return "Filhote"
        elif 1 <= idade <= 7:
            return "Adulto"
        else:
            return "Sênior"

    def obter_dados_raca(self, raca):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            SELECT tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max
            FROM racas WHERE raca = ?
        """, (raca,))
        resultado = self.bd_manager.cursor.fetchone()
        self.bd_manager.desconectar_bd()
        return resultado

    def obter_dados_genericos(self, tipo_pelo, porte, faixa_etaria):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            SELECT escovacao, tosa, cuidados FROM genericas
            WHERE tipo_pelo = ? AND porte = ? AND faixa_etaria = ?
        """, (tipo_pelo, porte, faixa_etaria))
        resultado = self.bd_manager.cursor.fetchone()
        self.bd_manager.desconectar_bd()
        return resultado
    
    def cadastrar_raca(self, raca, tipo_pelo, porte, idade, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            INSERT INTO racas (raca, tipo_pelo, porte, idade, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (raca, tipo_pelo, porte, idade, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max))
        self.bd_manager.conn.commit()
        self.bd_manager.desconectar_bd()

    def tela_cadastro_raca(self):
        top = Toplevel()
        top.title("Cadastro de Raça")
        top.geometry("400x800")
        top.configure(bg="#dedbd3")

        variaveis = {
            "raca": StringVar(),
            "tipo_pelo": StringVar(),
            "porte": StringVar(),
            "idade": StringVar(),
            "escovacao": StringVar(),
            "tosa": StringVar(),
            "cuidados": StringVar(),
            "peso_min": StringVar(),
            "peso_max": StringVar(),
            "tamanho_min": StringVar(),
            "tamanho_max": StringVar()
        }

        for idx, (label_text, var) in enumerate(variaveis.items()):
            Label(top, text=label_text.replace("_", " ").title() + ":", bg="#dedbd3").pack(pady=5)
            Entry(top, textvariable=var, width=30).pack(pady=5)

        def salvar_raca():
            try:
           
                if not variaveis["raca"].get().strip():
                    messagebox.showerror("Erro", "O nome da raça é obrigatório.", parent=top)
                    return
                
                if not variaveis["tipo_pelo"].get().strip():
                    messagebox.showerror("Erro", "O tipo de pelo é obrigatório.", parent=top)
                    return
                    
                if not variaveis["porte"].get().strip():
                    messagebox.showerror("Erro", "O porte é obrigatório.", parent=top)
                    return
                
                try:
                    peso_min = float(variaveis["peso_min"].get()) if variaveis["peso_min"].get().strip() else 0
                    peso_max = float(variaveis["peso_max"].get()) if variaveis["peso_max"].get().strip() else 0
                    tamanho_min = float(variaveis["tamanho_min"].get()) if variaveis["tamanho_min"].get().strip() else 0
                    tamanho_max = float(variaveis["tamanho_max"].get()) if variaveis["tamanho_max"].get().strip() else 0
                except ValueError:
                    messagebox.showerror("Erro", "Peso e tamanho devem ser números válidos.", parent=top)
                    return
                
                if peso_min > peso_max and peso_max > 0:
                    messagebox.showerror("Erro", "Peso mínimo não pode ser maior que peso máximo.", parent=top)
                    return
                    
                if tamanho_min > tamanho_max and tamanho_max > 0:
                    messagebox.showerror("Erro", "Tamanho mínimo não pode ser maior que tamanho máximo.", parent=top)
                    return
                
                self.cadastrar_raca(
                    variaveis["raca"].get().strip(), 
                    variaveis["tipo_pelo"].get().strip(), 
                    variaveis["porte"].get().strip(), 
                    variaveis["idade"].get().strip(),
                    variaveis["escovacao"].get().strip(), 
                    variaveis["tosa"].get().strip(), 
                    variaveis["cuidados"].get().strip(),
                    peso_min, peso_max, tamanho_min, tamanho_max
                )
                messagebox.showinfo("Sucesso", "Raça cadastrada com sucesso!", parent=top)
                top.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=top)

        Button(top, text="Salvar Raça", bg="#4CAF50", fg="white", command=salvar_raca).pack(pady=20)


class GerenciadorClientes:
    def __init__(self, bd_manager):
        self.bd_manager = bd_manager

    def cadastrar_cliente(self, nome_dono, nome_pet, telefone, peso=None, tamanho=None, raca=None, idade=None):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            INSERT INTO clientes (nome_dono, nome_pet, telefone, ultima_visita, peso, tamanho, raca, idade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome_dono, nome_pet, telefone, datetime.now().strftime("%d/%m/%Y"), peso, tamanho, raca, idade))
        self.bd_manager.conn.commit()
        self.bd_manager.desconectar_bd()

    def buscar_clientes(self, termo=""):
        self.bd_manager.conectar_bd()
        if termo.strip() == "":
            self.bd_manager.cursor.execute("SELECT nome_dono, telefone, ultima_visita FROM clientes")
        else:
            self.bd_manager.cursor.execute("""
                SELECT nome_dono, nome_pet, telefone, ultima_visita
                FROM clientes
                WHERE nome_dono LIKE ? OR nome_pet LIKE ?
            """, (f"%{termo}%", f"%{termo}%"))
        resultados = self.bd_manager.cursor.fetchall()
        self.bd_manager.desconectar_bd()
        return resultados

    def atualizar_cliente(self, nome_dono_antigo, nome_pet_antigo, novo_nome_dono, novo_nome_pet, novo_telefone):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            UPDATE clientes
            SET nome_dono = ?, nome_pet = ?, telefone = ?
            WHERE nome_dono = ? AND nome_pet = ?
        """, (novo_nome_dono, novo_nome_pet, novo_telefone, nome_dono_antigo, nome_pet_antigo))
        self.bd_manager.conn.commit()
        self.bd_manager.desconectar_bd()

    def excluir_cliente(self, nome_dono, nome_pet):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            DELETE FROM clientes
            WHERE nome_dono = ? AND nome_pet = ?
        """, (nome_dono, nome_pet))
        self.bd_manager.conn.commit()
        self.bd_manager.desconectar_bd()

    def registrar_visita(self, nome_dono, nome_pet, novo_peso=None, novo_tamanho=None):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            UPDATE clientes 
            SET ultima_visita = ?, peso = COALESCE(?, peso), tamanho = COALESCE(?, tamanho)
            WHERE nome_dono = ? AND nome_pet = ?
        """, (data_atual, novo_peso, novo_tamanho, nome_dono, nome_pet))
        self.bd_manager.conn.commit()
        self.bd_manager.desconectar_bd()

    def obter_dados_completos_cliente(self, nome_dono, telefone):
        self.bd_manager.conectar_bd()
        self.bd_manager.cursor.execute("""
            SELECT nome_dono, nome_pet, telefone, ultima_visita, peso, tamanho, raca, idade
            FROM clientes
            WHERE nome_dono = ? AND telefone = ?
        """, (nome_dono, telefone))
        resultado = self.bd_manager.cursor.fetchone()
        self.bd_manager.desconectar_bd()
        return resultado

class GeradorRelatorios:
    def __init__(self):
        pass

    def gerar_pdf_raca(self, nome_pet, raca, peso, tamanho, idade, resultado_raca, divergencias, telefone, nome_dono):
        if resultado_raca:
            tipo_pelo, porte, escovacao, tosa, cuidados, peso_min, peso_max, tamanho_min, tamanho_max = resultado_raca
            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"Relatorio_{nome_pet}_{data_atual}.pdf"
            c = canvas.Canvas(nome_arquivo, pagesize=A4)
            largura, altura = A4

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 50, f"Relatório do Pet: {nome_pet}")

            c.setFont("Helvetica", 12)
            y = altura - 80
            linhas = [
                f"Nome: {nome_pet}",
                f"Raça: {raca}",
                f"Idade: {idade}",
                f"Peso: {peso} kg",
                f"Tamanho: {tamanho} cm",
                "--- Rotina de Cuidados da Raça ---",
                f"Tipo de Pelo: {tipo_pelo}",
                f"Porte: {porte}",
                f"Escovação: {escovacao}",
                f"Tosa: {tosa}",
                f"Cuidados: {cuidados}",
                "--- Divergências ---"
            ] + (divergencias if divergencias else ["O pet está dentro dos padrões da raça."])

            for linha in linhas:
                c.drawString(50, y, linha)
                y -= 20
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = altura - 50

            c.save()
            self._abrir_pdf(nome_arquivo)
            return nome_arquivo
        return None

    def gerar_pdf_generico(self, nome_pet, idade, peso, tamanho, tipo_pelo, porte, faixa_etaria, nome_dono, telefone, resultado):
        if resultado:
            escovacao, tosa, cuidados = resultado
            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"Relatorio_Generico_{nome_pet}_{data_atual}.pdf"
            c = canvas.Canvas(nome_arquivo, pagesize=A4)
            largura, altura = A4

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 50, f"Relatório Genérico do Pet: {nome_pet}")

            c.setFont("Helvetica", 12)
            y = altura - 80
            linhas = [
                f"Nome: {nome_pet}",
                f"Idade: {idade} ({faixa_etaria})",
                f"Peso: {peso} kg",
                f"Tamanho: {tamanho} cm",
                f"Tipo de Pelo: {tipo_pelo}",
                f"Porte: {porte}",
                f"Faixa Etária: {faixa_etaria}",
                "--- Rotina de Cuidados Genéricos ---",
                f"Escovação: {escovacao}",
                f"Tosa: {tosa}",
                f"Cuidados: {cuidados}"
            ]

            for linha in linhas:
                c.drawString(50, y, linha)
                y -= 20
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = altura - 50

            c.save()
            self._abrir_pdf(nome_arquivo)
            return nome_arquivo
        return None

    def _abrir_pdf(self, nome_arquivo):
        if platform.system() == "Windows":
            os.startfile(nome_arquivo)
        elif platform.system() == "Darwin":  
            os.system(f"open {nome_arquivo}")
        else:  # Linux e outros
            os.system(f"xdg-open {nome_arquivo}")

aplicacao()
