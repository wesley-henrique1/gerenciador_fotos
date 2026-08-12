import glob
import os
import time
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import multiprocessing
class GerenciadorFotos:
    def __init__(self):
        self.largura = 70

        self.caminho_pendrive = Path("D:/")
        self.PastaDestino = Path(r"C:\1_PROJETO\FotosCD\Acumulado")
        self.PastaDestino = Path(self.PastaDestino)
        self.PastaDestino.mkdir(parents=True, exist_ok=True)

        self.listaFotos = []
        self.ListaSub = []
        self.dicERROR = {}
        self.booleano = False
        self.extensoes = {".jpg", ".jpeg"}
        self.Executar()
        pass

    def __copiar_com_timeout(self, origem, destino, timeout=15):
        # Cria um processo separado para realizar a cópia
        processo = multiprocessing.Process(target=shutil.copy2, args=(origem, destino))
        processo.start()
        
        # Aguarda o processo terminar até o limite estipulado
        processo.join(timeout=timeout)
        
        # Se após o tempo o processo ainda estiver rodando, mata o processo
        if processo.is_alive():
            processo.terminate()
            processo.join()
            print(f"Erro: Cópia expirou após {timeout} segundos.")
            return False
            
        return True
    def __limpar_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

        pass
    def __validarerror(self):
        if self.dicERROR:
            print(f"\n>> {len(self.dicERROR)} arquivo(s) com erro de processamento:")
            print("-" * self.largura)
            for foto, erro in self.dicERROR.items():
                print(f">> {foto} -> {erro}")
            pass
    def __LimparList(self):
        self.listaFotos.clear()
        self.ListaSub.clear()

        pass
    def __Rastrear(self):
        try:
            self.__LimparList()
            
            subpastas = [p for p in self.caminho_pendrive.rglob("*") if p.is_dir()]
            self.ListaSub.extend(subpastas)

            for sub in subpastas:
                lista_de_arquivos = [
                    f for f in sub.iterdir()
                    if f.is_file() and f.suffix.lower() in self.extensoes
                ]
                self.listaFotos.extend(lista_de_arquivos)
            
            self.booleano = True
            return sorted(self.listaFotos), sorted(self.ListaSub)             
        except Exception as e:
            self.booleano = False
            print(f"Erros: {e}")

        pass
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
        input(">> [enter] para finalizar.")

        contador = 0
        for idx, foto in enumerate(listaFotos, start= inicio):
            contador +=1
            arquivo = Path(foto)
            nomeFoto = arquivo.name
            subpasta = arquivo.parent.name

            novoCaminho = self.PastaDestino / f"IMG{idx:04d}.jpg"
            mensagem = f"{subpasta}: {nomeFoto} -> {novoCaminho.name} | {contador}/{totalfoto}"
            try:
                self.__copiar_com_timeout(arquivo, novoCaminho, timeout=15)

                print(f"\r>> {mensagem.ljust(self.largura)}", end="", flush=True)
                time.sleep(0.4)
                listatrue.append(novoCaminho)

            except TimeoutError:
                chave_erro = f"{subpasta}/{nomeFoto}"
                self.dicERROR[chave_erro] = "Leitura travada (CD riscado ou setor danificado)"

            except Exception as e:
                chave_erro = f"{subpasta}/{nomeFoto}"
                self.dicERROR[chave_erro] = str(e)        
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
    GerenciadorFotos()
