![Python version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-blue)
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)

## Índice 📑

- [Sobre Anonymizer](#anonymizer)
- [Instalação e Execução 🛠️](#instalação-e-execução)
- [Ferramentas 🔧](#ferramentas-)
- [Como Funciona ⚙️](#como-funciona)
- [Impacto da ferramenta 🚀](#impacto-da-ferramenta-)
- [Licença](#licença)

# Anonymizer
### Ferramenta para Anonimização de Dados Sensíveis em PDFs

O projeto consiste em anonimizar dados sensíveis de documentos em PDF, sobreponto as informações com uma cor preta, mantendo o layout do documento original.

## Instalação e Execução 🛠️

Siga as etapas abaixo para instalar e rodar o Anonymizer em sua máquina:

1️⃣ Clonar o Repositório
Abra o terminal (ou prompt de comando) e execute:
```
git clone https://github.com/Gui-Pires/Anonymizer.git
cd Anonymizer
```

2️⃣ Instalar Dependências
Certifique-se de ter o Python 3.8+ instalado. Depois, instale as bibliotecas necessárias:
```
pip install -r requirements.txt
```

Se o arquivo requirements.txt ainda não existir, você pode criá-lo com:
```
pip freeze > requirements.txt
```

3️⃣ Executar o Programa
Após instalar as dependências, execute o seguinte comando:
```
python app.py
```

### Dicas Adicionais 💻

Caso o pip não seja reconhecido, tente `python -m pip install -r requirements.txt`.
Se estiver no Windows, pode ser necessário rodar `python main.py` em vez de `python3 main.py`.

Para evitar conflitos entre pacotes, considere usar um ambiente virtual:
```
python -m venv venv  # Cria o ambiente virtual
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate  # No Windows
pip install -r requirements.txt  # Instale as dependências dentro do ambiente virtual
```

## Ferramentas 🔧

- [HTML5](https://html.spec.whatwg.org/)
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Bootstrap v5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Python](https://docs.python.org/3/)
- [Flask v3.0.3](https://flask-docs-pt.readthedocs.io/pt/latest/)
- [PyMuPDF v1.25.3](https://pymupdf.readthedocs.io/en/latest/)

## Como Funciona ⚙️

Utilizando Python e Flask para servir uma página web com uma interface simples e flúida, com design moderno do Bootstrap, o usuário envia um arquivo PDF para aninomizar:

- Email
- CPF
- CNPJ
- RG
- CEP
- Links (de toda natureza)
- Endereços
- Imagens (Para remover QR Codes)

O arquivo original é salvo em uma pasta e uso o PyMuPDF para fazer as manipulações de texto e imagens (que diferente do texto, é sobreposto em branco). Depois de finalizado é salvo uma cópia com um prefixo do nome do arquivo na mesma pasta do original, em seguida é disponibilizado para o usuário um link para download do arquivo pronto.

Nota: Para conter o acúmulo dos arquivos na pasta do servidor é feita uma varredura dos arquivos que contém mais de 1 hora armazenados e deletados automáticamente. 
> A varredura para deletar arquivos antigos (mais de 1 hora) ocorre somente quando a ferramenta é usada novamente. Portanto, se você precisa recuperar um arquivo que tenha mais de 1 hora armazenado, ele pode ser recuperado até a próxima execução da ferramenta.

## Impacto da ferramenta 🚀

Os funcionários da empresa no qual trabalhei precisavam fazer algumas anonimizações semanalmente, onde era um processo trabalhoso identificar e sobrepor as informações sensíveis nos documentos, chegando a ocupar horas de trabalho em um único arquivo.

Com essa solução o tempo foi consideravelmente reduzido, passando de horas para 5 minutos no máximo, uma vez que a ferramenta era experimental e precisava de uma verificação dos dados anonimizado.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
