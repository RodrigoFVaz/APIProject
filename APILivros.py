import tkinter
import json
import requests

url = "https://openlibrary.org/search.json"

class ProjetoProg():
    def __init__(self, telinha):

        self.tela = telinha

        self.PClique = 0

        self.CriarTelinha()

    def CriarTelinha(self):
        self.Fundo = tkinter.Frame(self.tela, bg="black", width="550", height="590")
        self.Fundo.grid()
        self.Fundo.grid_propagate(False)
        self.Fundo.grid_columnconfigure(0, weight=1)

        self.LivroT = tkinter.Label(self.Fundo, text="Livros:")
        self.LivroT.grid(row=0, column=0, pady=10, padx=100, sticky="w")

        self.AutorT = tkinter.Label(self.Fundo, text="Autor:")
        self.AutorT.grid(row=0, column=0, pady=10, padx=185, sticky="e")

        self.DadosT = tkinter.Entry(self.Fundo)
        self.DadosT.grid(row=1, column=0, pady=10, padx=100, sticky="w")

        self.DadosA = tkinter.Entry(self.Fundo)
        self.DadosA.grid(row=1, column=0, pady=10, padx=100, sticky="e")

        self.Botao_CL = tkinter.Button(self.Fundo, text="Pesquisar livro", command=self.CheckLivro)
        self.Botao_CL.grid(row=2, column=0, pady=20, padx=60, sticky="w")

        self.Botao_CA = tkinter.Button(self.Fundo, text="Pesquisar autor", command=self.CheckAutor)
        self.Botao_CA.grid(row=2, column=0, pady=20, padx=170, sticky="w")

        self.Botao_Hist = tkinter.Button(self.Fundo, text="Aceder Historico", command=self.Historico)
        self.Botao_Hist.grid(row=2, column=0, pady=20, padx=170, sticky="e")

        self.Botao_Fav = tkinter.Button(self.Fundo, text="Aceder Favoritos", command=self.Favoritos)
        self.Botao_Fav.grid(row=2, column=0, pady=20, padx=50, sticky="e")

        self.TextoA = tkinter.Text(self.Fundo, bg="white")
        self.TextoA.grid(row=3, column=0, pady=20, padx=20, sticky="")

        self.Fundo2 = tkinter.Frame(self.tela, bg="black", width="550", height="10")
        self.Fundo2.grid()
        self.Fundo2.grid_propagate(False)

    def Voltar(self):
        self.Fundo.destroy()

        self.CriarTelinha()

    def UserPesquisa(self):
        try:
            user_data = self.DadosT.get()
            autor_data = self.DadosA.get()
        except:
            user_data = ""
            autor_data = ""
        return user_data, autor_data

    def RequestReturn(self, user_data, autor_data):
        Parametros = {
        }
        if user_data:
            Parametros["title"] = user_data
        if autor_data:
            Parametros["author_name"] = autor_data
        if autor_data:
            Parametros["author"] = autor_data

        return requests.get(url, params=Parametros)
    
    def Collector(self):
        PUser, PAutor = self.UserPesquisa()
        checker = self.RequestReturn(PUser, PAutor)

        return PUser, PAutor, checker

    def Validar(self):
        PUser, PAutor, checker = self.Collector()

        CriarHist = {"Historico":[], "Apresentados":[], "Favoritos":[]}
        try:
            with open("Historico.json", "x", encoding="utf-8") as f:
                CriarHist["Historico"].append({
                    "nome" : None
                })
                CriarHist["Apresentados"].append({
                    "nome" : None
                })
                CriarHist["Favoritos"].append({
                    "nome" : None
                })
                json.dump(CriarHist,f, indent=4, ensure_ascii=False)

        except FileExistsError:
            with open("Historico.json", "r", encoding="utf-8") as f:
                try:
                    ValDoc = json.load(f)

                    if "Historico" not in ValDoc:
                        ValDoc["Historico"] = ({
                            "nome" : None
                        })

                    if "Apresentados" not in ValDoc:
                        ValDoc["Apresentados"] = ({
                            "nome" : None
                        })

                    if "Favoritos" not in ValDoc:
                        ValDoc["Favoritos"] = ({
                        "nome" : None
                        })

                    with open("Historico.json", "w", encoding="utf-8") as f:
                        json.dump(ValDoc, f, indent=4, ensure_ascii=False)
                except:
                    with open("Historico.json", "w", encoding="utf-8") as f:
                        CriarHist["Historico"].append({
                            "nome" : None
                        })
                        CriarHist["Apresentados"].append({
                            "nome" : None
                        })
                        CriarHist["Favoritos"].append({
                            "nome" : None
                        })
                        json.dump(CriarHist,f, indent=4, ensure_ascii=False)

        try:
            if checker.status_code == 200:
                self.TextoA.delete(1.0, tkinter.END)
                self.TextoA.insert(tkinter.END, "Pedido realizado com sucesso\n\n")
                return PUser, PAutor, checker
            else:
                self.TextoA.delete(1.0, tkinter.END)
                self.TextoA.insert(tkinter.END, f"Pedido não realizado devido a erro: {checker.status_code}\n\n")
        except Exception:
            self.TextoA.delete(1.0, tkinter.END)
            self.TextoA.insert(tkinter.END, "Não é possível aceder a API.\n\n")
            exit()
        
        return None, None, None
    
    def CheckLivro(self):
        PUser, PAutor, checker = self.Validar()
        try:
            ValChecker = checker.json()

            Controller = 0

            for i in ValChecker["docs"]:
                if PUser.lower() in i.get("title", "").lower():
                    Controller = 1
                    break

            if Controller != 1 and PUser == "":
                Controller = 2

            if Controller == 1:
                    self.GuardarLivros(checker)

            elif Controller == 2:
                self.TextoA.insert(tkinter.END, "Deve inserir um valor no campo de Livros, para pesquisar Livros.")

            else:
                self.TextoA.insert(tkinter.END, "Livro não encontrado.")
        except:
            self.TextoA.insert(tkinter.END, "Não foi possível aceder a API!")

    def CheckAutor(self):
        PUser, PAutor, checker = self.Validar()

        try:
            ValCheckerA = checker.json()

            ControllerA = 0

            for i in ValCheckerA["docs"]:
                ValAutor = ", ".join(i.get("author_name", ""))

                if PAutor.lower() in ValAutor.lower():
                    ControllerA = 1
                    break

            if ControllerA == 1:
                    self.GuardarAutor(checker, PAutor)

            elif ControllerA == 0 and PAutor == "":
                ControllerA = 2

            if ControllerA == 2:
                self.TextoA.insert(tkinter.END, "Deve pesquisar por um autor, ou por livro e depois por autor.")

            else:
                self.TextoA.insert(tkinter.END, "Autor não encontrado.")
        except:
            self.TextoA.insert(tkinter.END, "Não foi possível aceder a API!")
            
    def GuardarAutor(self, checker, PAutor):

        ValCheckerA = checker.json()

        AutorB = []
        AutorI = []

        AutF = ""

        for i in ValCheckerA["docs"]:
            Title = i.get("title", "")
        
            Aut = i.get("author_name", [])

            if type(Aut) == list:
                for i in Aut:
                    if PAutor.lower() in i.lower():
                        AutF = ", ".join(Aut)
                        break
            else:
                if PAutor.lower() in str(Aut).lower():
                    AutF = str(Aut)
            if AutF != "":
                AutorB.append(Title + " - " + AutF)

        with open("Historico.json", "r", encoding="utf-8") as f:
            try:
                Hist = json.load(f)

                if Hist["Historico"][0]["nome"] is None:
                    Hist["Historico"].pop(0)

                Hist["Apresentados"] = []

                for i in AutorB:
                    Hist["Historico"].append({
                        "nome": i
                    })

                    Hist["Apresentados"].append({
                        "nome": i
                    })

            except:
                self.TextoA.insert(tkinter.END, "Ficheiro a ser criado...\n\n")
        
        with open("Historico.json", "w", encoding="utf-8") as f:
            json.dump(Hist, f, indent=4, ensure_ascii=False)

        with open("Historico.json", "r", encoding="utf-8") as f:
            FILE = json.load(f)

            for i in FILE["Apresentados"]:
                Nomes = i.get("nome", None)

                if Nomes is not None:
                    AutorI.append(Nomes)

        listinha = "\n".join(AutorI)
        self.TextoA.insert(tkinter.END, listinha)
            
    def GuardarLivros(self, checker):

        ValChecker = checker.json()

        TitulosB = []
        TitulosI = []
        Hist = []

        for i in ValChecker["docs"]:
            TitulosB.append(i.get("title"))

        with open("Historico.json", "r", encoding="utf-8") as f:
            Hist = json.load(f)
            
            if Hist["Historico"][0]["nome"] is None:
                Hist["Historico"].pop(0)

            Hist["Apresentados"] = []

            for i in TitulosB:
                Hist["Historico"].append({
                    "nome": i
                })

                Hist["Apresentados"].append({
                    "nome": i
                })

        with open("Historico.json", "w", encoding="utf-8") as f:
            json.dump(Hist, f, indent=4, ensure_ascii=False)

        with open("Historico.json", "r", encoding="utf-8") as f:
            FILE = json.load(f)

            for i in FILE["Apresentados"]:
                Nomes = i.get("nome", None)

                if Nomes is not None:
                    TitulosI.append(Nomes)

        listinha = "\n".join(TitulosI)
        self.TextoA.insert(tkinter.END, listinha)

    def Historico(self):
        self.Validar()

        try:
            with open("Historico.json", "r", encoding="utf-8") as f:
                Hist = json.load(f)

                Histf = []

                for i in Hist["Historico"]:     
                    HistM = i.get("nome", None)

                    if HistM is not None:
                        Histf.append(HistM)
                HistF = "\n".join(Histf)

                self.TextoA.delete(1.0, tkinter.END)
                self.TextoA.insert(tkinter.END, HistF)

                if Hist["Historico"][0]["nome"] == None:
                    raise TypeError
        except TypeError:
            self.TextoA.delete(1.0, tkinter.END)
            self.TextoA.insert(tkinter.END, "Historico vazio! Por favor pesquise algo antes de visualizar o historico.")
    
    def Favoritos(self):
        self.Fundo.destroy()

        self.Fundo = tkinter.Frame(self.tela, bg="black", width="550", height="600")
        self.Fundo.grid()
        self.Fundo.grid_propagate(False)
        self.Fundo.grid_columnconfigure(0, weight=1)

        self.Index = tkinter.Label(self.Fundo, text="Index:")
        self.Index.grid(row=0, column=0, pady=10, padx=185, sticky="e")

        self.IndexD = tkinter.Entry(self.Fundo)
        self.IndexD.grid(row=1, column=0, pady=10, padx=100, sticky="e")

        self.Botao_Index = tkinter.Button(self.Fundo, text="Remover Favorito", command=self.RFav)
        self.Botao_Index.grid(row=2, column=0, pady=10, padx=60, sticky="w")

        self.Botao_VHist = tkinter.Button(self.Fundo, text="Adicionar Favorito via Historico anterior", command=self.HistFav)
        self.Botao_VHist.grid(row=2, column=0, pady=10, padx=60, sticky="e")

        self.TextoA = tkinter.Text(self.Fundo, bg="white")
        self.TextoA.grid(row=4, column=0, pady=10, padx=20, sticky="")

        Botao_Voltar = tkinter.Button(self.Fundo, text="Voltar...", command=self.Voltar)
        Botao_Voltar.grid(row=5, column=0, pady=20)

        self.Validar()
    
    def HistFav(self):
        if self.PClique == 0:
            IndexChecker = ""
            self.IndexD.delete(0, tkinter.END)
            self.PClique = 1
        else:
            IndexChecker = self.IndexD.get()

        IndexChecker = self.IndexD.get()

        if IndexChecker == "":
            self.TextoA.delete(1.0, tkinter.END)
            self.TextoA.insert(tkinter.END, "Escolha um dos livros preenchendo o campo index com o numero equivalente e clique novamente no botão!\n\n")

        with open("Historico.json", "r", encoding="utf-8") as f:
            HFav = json.load(f)
            if HFav["Favoritos"][0]["nome"] is None and HFav["Apresentados"][0]["nome"] is None:
                self.TextoA.delete(1.0, tkinter.END)
                self.TextoA.insert(tkinter.END, "Faça uma pesquisa primeiro!")
                self.PClique = 0

            HistFavVal = []

            for i, y in enumerate(HFav["Apresentados"]):
                
                GNomes = y.get("nome", None)

                if GNomes is not None:
                    iF = str(i)
                    HistFavVal.append(iF + " - " + GNomes)

            if HFav["Favoritos"][0]["nome"] is None and IndexChecker != "":
                HFav["Favoritos"].pop(0)

        for x, y in enumerate(HFav["Apresentados"]):
            if IndexChecker != "" and str(x) == IndexChecker:
                GNomeD = y.get("nome")
                
                DFav = {"nome": GNomeD}
                
                if DFav not in HFav["Favoritos"]:
                    HFav["Favoritos"].append(DFav)
                    self.TextoA.delete(1.0, tkinter.END)
                    self.TextoA.insert(tkinter.END, "Livro adicionado aos favoritos!\n\n")
                    self.PClique = 0
                else:
                    self.TextoA.delete(1.0, tkinter.END)
                    self.TextoA.insert(tkinter.END, "Livro já adicionado!\n\n")
                    self.PClique = 0
                
        with open("Historico.json", "w", encoding="utf-8") as f:
            json.dump(HFav, f, indent=4, ensure_ascii=False)
        listinha = "\n".join(HistFavVal)
        self.TextoA.insert(tkinter.END, listinha)

    def RFav(self):

        if self.PClique == 0:
            IndexChecker = ""
            self.IndexD.delete(0, tkinter.END)
            self.PClique = 1
        else:
            IndexChecker = self.IndexD.get()

        if IndexChecker == "":
            self.TextoA.delete(1.0, tkinter.END)
            self.TextoA.insert(tkinter.END, "Escolha um dos livros preenchendo o campo index e clique novamente no mesmo botão!\n\n")

        with open("Historico.json", "r", encoding="utf-8") as f:
            HFav = json.load(f)

            if HFav["Favoritos"][0]["nome"] is None:
                self.TextoA.delete(1.0, tkinter.END)
                self.TextoA.insert(tkinter.END, "Ainda não tem nenhum livro salvo!")
                self.PClique = 0

            for x, y in enumerate(HFav["Favoritos"]):
                if IndexChecker != "" and str(x) == IndexChecker:
                    HFav["Favoritos"].pop(x)
                    
                    if len(HFav["Favoritos"]) == 0:
                        HFav["Favoritos"].append({
                            "nome" : None
                        })
                    
                    self.TextoA.delete(1.0, tkinter.END)
                    self.TextoA.insert(tkinter.END, "Livro removido dos favoritos!\n\n")
                    self.PClique = 0
                    break
            else:
                if IndexChecker != "":
                    self.TextoA.delete(1.0, tkinter.END)
                    self.TextoA.insert(tkinter.END, "Escolha um valor válido da lista!\n\n")
                    self.PClique = 0

        with open("Historico.json", "w", encoding="utf-8") as f:
            json.dump(HFav, f, indent=4, ensure_ascii=False)

        RFavVal = []
        for i, y in enumerate(HFav["Favoritos"]):
                Nomes = y.get("nome", None)
                if Nomes is not None:
                    iF = str(i)
                    RFavVal.append(iF + " - " + Nomes)
                    
        if RFavVal != []:
                listinha = "\n".join(RFavVal)
                self.TextoA.insert(tkinter.END, listinha)

        elif IndexChecker != "":
                self.TextoA.insert(tkinter.END, "A sua lista de favoritos ficou vazia.")

TelaPrincipal = tkinter.Tk()
TelaPrincipal.geometry("550x600")
TelaPrincipal.title("Projeto")
ProjetoProg(TelaPrincipal)
TelaPrincipal.mainloop()