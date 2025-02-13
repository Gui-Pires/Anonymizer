# Anonymizer

Um projeto feito para uma solução interna da empresa no qual trabalhei, que consiste em anonimizar dados sensíveis de documentos que viríam a ser públicos.

# Ferramentas 🔧

- HTML5
- CSS3
- Bootstrap v5.3
- Python v3
- Flask v3.0.3
- PyMuPDF v1.25.3

# Como Funciona? ⚙️

Utilizando Python e Flask para servir uma página web com uma interface simples e flúida, com design moderno do Bootstrap, o usuário envia um arquivo PDF para aninomizar:

- Email
- CPF
- CNPJ
- RG
- CEP
- Links (de toda natureza)
- Endereços
- Imagens (Para remover QR Codes)

O arquivo original é salvo em uma pasta e uso o PyMuPDF para fazer as manipulações de texto e imagens. Depois de finalizado é salvo uma cópia com um prefixo do nome do arquivo na mesma pasta do original, em seguida é disponibilizado para o usuário um link para download do arquivo pronto.

Nota: Para conter o acúmulo dos arquivos na pasta do servidor é feita uma varredura dos arquivos que contém mais de 1 hora armazenados e deletados automáticamente. 
> A varredura no entando só é realizada no próximo uso da ferramenta, o que pode ser considerado para recuperar arquivos com mais de 1 hora armazenados.

# Impacto da ferramenta 🚀

Os funcionários da empresa não precisavam fazer as anonimizações diariamente, apenas algumas vezes por semana. No entanto, era um processo trabalhoso identificar e sobrepor as informações sensíveis nos documentos, chegando a ocupar horas de trabalho em um único arquivo.
Com essa solução o tempo foi consideravelmente reduzido, passando de horas para alguns minutos, sendo necessário apenas a verificação dos dados anonimizado, uma vez que a ferramenta era experimental, algo em torno de 10 minutos no máximo.
