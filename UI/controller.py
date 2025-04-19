import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None
        self._fermataArrivo = None

    def handleCreaGrafo(self,e):
        self._model.buildGraph()
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        self._view.lst_result.controls.clear()


        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f'Il grafo ha {nNodes} nodi'))
        self._view.lst_result.controls.append(ft.Text(f'Il grafo ha {nEdges} archi'))
        self._view._btnCalcola.disabled = False
        self._view.update_page()
        pass

    def handleCreaGrafoPesato(self, e):
        self._model.buildGraphPesato()
        # ...(54.56)

    def handleCercaRaggiungibili(self,e):
        # visited = self._model.getBFSNodes(self._fermataPartenza)
        visited = self._model.getDFSNodes(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(
            ft.Text(f"Dalla stazione {self._fermataPartenza} posso raggiungere {len(visited)} stazioni.")
        )
        for v in visited:
            self._view.lst_result.controls.append(ft.Text(v))
        self._view.update_page()
        pass

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza)) # unico modo ( se faccio .value restituisce stringa e non oggetto)
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
