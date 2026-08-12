<h1 align="center"> Gerenciador e Extrator de Fotos Antigas (CD to Local/Drive)</h1>

<table align="center">
<tr>
<!-- Lado Esquerdo: Frase, Links e Badges -->
<td align="center" valign="middle">
    <h3>"Deixe o robô trabalhar enquanto você toma um café."</h3>
    <h2>
        <a href="https://www.linkedin.com/in/wesley-henrique22" target="_blank" rel="noopener noreferrer">LinkedIn</a> |
        <a href="https://github.com/wesley-henrique1" target="_blank" rel="noopener noreferrer">GitHub</a> | 
        <a href="https://www.bing.com/search?q=aqui%20estou%20devendo%20link&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq=aqui%20estou%20devendo%20link&sc=12-23&sk=&cvid=989C403393164B4298A65FE780076F4B" target="_blank" rel="noopener noreferrer">Instagram</a>
    </h2>
    <p align="center">
        <img src="https://img.shields.io/badge/Python-3.13-blue?style=flat&logo=python" alt="Python">
        <img src="https://img.shields.io/badge/Status-Em_Produção-green?style=flat" alt="Status">
    </p>
</td>

<!-- Lado Direito: Imagem Principal -->
<td align="center" valign="middle" width="300">
    <img src="img/FleshPerfil.png" width="280" alt="Flash - Mascot">
</td>
</tr>
</table>
Uma automação em Python desenvolvida para resolver um problema real de resgate de memórias físicas armazenadas em mídias ópticas antigas (CD-ROM/DVD).

---

## 🎯 O Problema

Mídias ópticas antigas sofrem com degradação do tempo (disk rot/arranhões). Ao tentar transferir manualmente 6 CDs de fotos antigas pelo Gerenciador de Arquivos do Windows (File Explorer), a leitura pesada e lentidão causavam travamentos na interface do sistema operacional e interrupção do processo de cópia.

Além disso, grande parte das máquinas modernas não possui leitor físico de mídias, tornando o processo de leitura e migração urgente para evitar a perda definitiva das fotos.

---

## 💡 A Solução

Desenvolvimento de um script resiliente em **Python** (`GerenciadorFotos`) que:
- Mapeia diretórios e subpastas de mídias externas.
- Filtra formatos específicos de imagem (`.jpg`, `.jpeg`).
- Gerencia o fluxo de transferência para diretórios locais/nuvem.
- Trata erros de leitura em tempo de execução sem interromper o processo global de cópia (impede travamentos do SO).
- Registra logs/dicionários de falhas de leitura (`dicERROR`) para identificação de arquivos corrompidos.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **`pathlib` / `os` / `glob`**: Manipulação e navegação eficiente pelo sistema de arquivos.
- **`shutil`**: Operações de alto nível para cópia e movimentação de arquivos.
- **`time`**: Controle de delays e tolerância de leitura.

---

## 📁 Estrutura do Projeto

```text
├── gerenciador_fotos.py   # Classe principal GerenciadorFotos e lógica de extração
├── README.md              # Documentação do projeto
├── Acumulado              # Pasta destino das fotos
