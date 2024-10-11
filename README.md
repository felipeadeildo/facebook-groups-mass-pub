# 🤖 Automação de Postagens em Grupos do Facebook

## 📜 Descrição

Este projeto consiste em um script Python que semi-automatiza o processo de postagem de mensagens em múltiplos grupos do Facebook. Ele utiliza Selenium WebDriver para interagir com o navegador e realiza as postagens de forma automática após o login manual, economizando tempo e esforço nas postagens repetitivas.

## ✨ Funcionalidades

- Abertura automática do navegador na página de login do Facebook
- Login manual realizado pelo usuário para garantir segurança
- Carregamento de links de grupos a partir de um arquivo
- Carregamento de mensagem a partir de um arquivo
- Postagem automática da mensagem em cada grupo após o login
- Interface de linha de comando colorida e informativa

## 🛠 Pré-requisitos

- Python 3.7+
- Google Chrome instalado
- Conexão com a internet

## 📦 Instalação

1. Clone este repositório:

   ```
   git clone https://github.com/felipeadeildo/facebook-groups-mass-pub.git
   cd facebook-groups-mass-pub
   ```

2. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

   Ou instale manualmente:

   ```
   pip install selenium webdriver_manager colorama rich
   ```

## ⚙ Configuração

1. Crie um arquivo `grupos.txt` na mesma pasta do script e adicione os links dos grupos do Facebook, um por linha.

2. Crie um arquivo `mensagem.txt` na mesma pasta do script e adicione a mensagem que deseja postar.

## 🚀 Uso

1. Execute o script:

   ```
   python main.py
   ```

2. Quando o navegador Chrome abrir na página do Facebook, faça login manualmente na sua conta.

   - Este passo é intencional para garantir a segurança da sua conta.
   - O script não tem acesso às suas credenciais de login.

3. Após concluir o login manualmente, o script detectará que você está logado e começará a postar automaticamente nos grupos listados.

## 🔐 Segurança

- O script requer que você faça login manualmente no Facebook. Isso é uma medida de segurança intencional para proteger suas credenciais.
- Suas informações de login não são armazenadas ou acessadas pelo script em nenhum momento.
- O script utiliza um perfil de Chrome personalizado para salvar sua sessão após o login manual. Isso evita a necessidade de fazer login toda vez que o script for executado, mas ainda mantém suas credenciais seguras.

## ⚠️ Avisos

- Use este script de forma responsável e de acordo com os Termos de Serviço do Facebook.
- Evite fazer muitas postagens em um curto período para não ser marcado como spam.
- O uso excessivo de automação pode resultar em restrições na sua conta do Facebook.

## 🐛 Resolução de Problemas

- Se encontrar problemas com o ChromeDriver, tente atualizar o Chrome para a versão mais recente.
- Certifique-se de que os arquivos `grupos.txt` e `mensagem.txt` estão no mesmo diretório do script e contêm informações válidas.
- Se o script não detectar que você está logado, tente limpar os cookies do navegador e fazer login novamente.

## 🤝 Contribuições

Contribuições, issues e pedidos de features são bem-vindos! Sinta-se à vontade para checar a página de [issues](https://github.com/felipeadeildo/facebook-groups-mass-pub/issues).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com ❤️ por [felipeadeildo](https://felipeadeildo.com)
