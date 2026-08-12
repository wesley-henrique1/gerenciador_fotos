import os
import time
from pathlib import Path
import shutil
import multiprocessing

def _auxiliar_copia(origem, destino):
    shutil.copy2(origem, destino)

class GerenciadorFotos:
    def __init__(self):
        self.largura = 72

        self.caminho_pendrive = Path("D:/")
        self.PastaDestino = Path(r"C:\1_PROJETO\FotosCD\Acumulado")
        self.PastaDestino.mkdir(parents=True, exist_ok=True)

        self.listaFotos = []
        self.ListaSub = []
        self.dicERROR = {}
        self.booleano = False
        self.extensoes = {".jpg", ".jpeg"}
        self.Executar()

    def __copiar_com_timeout(self, origem, destino, timeout=15):
        """Copia arquivo criando um processo independente que pode ser encerrado se travar."""
        processo = multiprocessing.Process(target=_auxiliar_copia, args=(origem, destino))
        processo.start()
        processo.join(timeout=timeout)

        if processo.is_alive():
            processo.terminate()
            processo.join()
            raise TimeoutError("Leitura travada na mídia")

    def __limpar_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def __validarerror(self):
        if self.dicERROR:
            print(f"\n>> {len(self.dicERROR)} arquivo(s) com erro de processamento:")
            print("-" * self.largura)
            for foto, erro in self.dicERROR.items():
                print(f">> {foto} -> {erro}")

    def __LimparList(self):
        self.listaFotos.clear()
        self.ListaSub.clear()

    def __Rastrear(self):
        try:
            self.__LimparList()
            print("s")
            
            subpastas = [p for p in self.caminho_pendrive.rglob("*") if p.is_dir()]
            self.ListaSub.extend(subpastas)

            for sub in subpastas:
                lista_de_arquivos = [
                    f for f in sub.iterdir()
                    if f.is_file() and f.suffix.lower() in self.extensoes
                ]
                self.listaFotos.extend(lista_de_arquivos)
            print("s")
            self.booleano = True
            return sorted(self.listaFotos), sorted(self.ListaSub)             
        except Exception as e:
            self.booleano = False
            print(f"Erros: {e}")

    def __Processar(self, listaFotos):
        listatrue = []
        print()
        fotos_existentes = [
            f for f in self.PastaDestino.iterdir()
            if f.is_file() and f.suffix.lower() in self.extensoes
        ]        
        inicio = len(fotos_existentes) + 1
        totalfoto = len(listaFotos)
        print(f">> Fotos já na pasta de destino: {len(fotos_existentes)}")
        print(f">> Próxima foto será nomeada como: IMG{inicio:04d}.jpg\n")
        print("-" * self.largura)
        input(">> [enter] para continuar.")
        print()

        contador = 0
        for idx, foto in enumerate(listaFotos, start=inicio):
            contador += 1
            arquivo = Path(foto)
            nomeFoto = arquivo.name
            subpasta = arquivo.parent.name

            if subpasta.lower() == 'chip 30':
                continue
            novoCaminho = self.PastaDestino / f"IMG{idx:04d}.jpg"
            mensagem = f"{subpasta}: {nomeFoto} -> {novoCaminho.name} | {contador}/{totalfoto}"
            try:
                print(f"\r>> {mensagem.ljust(self.largura)}", end="", flush=True)
                time.sleep(0.05)
                self.__copiar_com_timeout(arquivo, novoCaminho, timeout=15)

                listatrue.append(novoCaminho)

            except TimeoutError:
                chave_erro = f"{subpasta}/{nomeFoto}"
                self.dicERROR[chave_erro] = "Leitura travada (CD riscado ou setor danificado)"
                if novoCaminho.exists():
                    try:
                        novoCaminho.unlink()
                    except Exception:
                        pass

            except Exception as e:
                chave_erro = f"{subpasta}/{nomeFoto}"
                self.dicERROR[chave_erro] = str(e)  
        print()      
        return listatrue

    def Executar(self):
        while True:
            self.__limpar_terminal()
            print(" Sistema de transferencia ".center(self.largura, "-"))
            print("Procurando, aguarde...")

            fotoList, subList = self.__Rastrear()
            totalList = len(fotoList)

            if not self.booleano or totalList == 0:
                print("\n>> Sem dados a processar ou nenhuma foto encontrada no drive.")
                input(">> [enter] para finalizar.")
                break

            self.__limpar_terminal()
            print(" Sistema de transferencia ".center(self.largura, "-"))
            print(f">> Foram encontradas {len(subList)} pastas e {totalList} fotos")
            print(">> Iniciando processo...\n")

            valor = self.__Processar(fotoList)
            total = len(valor)

            # Exibe o resultado da cópia
            print("\n" + "-" * self.largura)
            if total == totalList:
                print(">> Processamento finalizado com sucesso!")
            else:
                print(">> Processamento finalizado Parcialmente!")
                self.__validarerror()

            input("\n>> [enter] para finalizar.")
            break

if __name__ == "__main__":
    multiprocessing.freeze_support()
    GerenciadorFotos()