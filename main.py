import re
from pathlib import Path

from colorama import init
from rich.console import Console
from rich.panel import Panel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

init(autoreset=True)  # Inicializa o colorama
console = Console()  # Inicializa o console do rich


class Facebook:
    """Classe para automatizar o envio de mensagens em grupos do Facebook."""

    def __init__(self, session_dir: str = "facebook_session") -> None:
        """
        Inicializa o objeto Facebook.

        Args:
            session_dir (str): Diretório onde será salvo o perfil do Chrome.
        """
        self.session_dir = self._setup_session_dir(session_dir)
        self.browser = self._setup_browser()
        self.links = self._load_links()
        self.mensagem = self._load_mensagem()

    def _setup_session_dir(self, session_dir: str) -> Path:
        """
        Configura o diretório de sessão.

        Args:
            session_dir (str): Caminho do diretório de sessão.

        Returns:
            Path: Objeto Path representando o diretório de sessão.

        Raises:
            OSError: Se houver um erro ao criar o diretório.
        """
        path = Path(session_dir)
        path.mkdir(parents=True, exist_ok=True)
        console.print(
            Panel(
                f"[bold cyan]Diretório de sessão:[/] [green]{path}[/]",
                title="[yellow]Configuração[/]",
                expand=False,
            )
        )
        return path

    def _setup_browser(self) -> webdriver.Chrome:
        """
        Configura o browser Chrome.

        Returns:
            webdriver.Chrome: Instância configurada do Chrome WebDriver.

        Raises:
            WebDriverException: Se houver um erro ao configurar o WebDriver.
        """
        with console.status("[bold yellow]Configurando o navegador..."):
            chrome_options = Options()
            chrome_options.add_argument(f"user-data-dir={self.session_dir.absolute()}")
            service = Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service, options=chrome_options)
            console.print(
                Panel(
                    "[bold green]Navegador configurado com sucesso! 🚀",
                    title="[yellow]Chrome[/]",
                    expand=False,
                )
            )
        return browser

    def _load_links(self) -> list[str]:
        """
        Carrega os links dos grupos do Facebook.

        Returns:
            list[str]: Lista com os links dos grupos.

        Raises:
            FileNotFoundError: Se o arquivo 'grupos.txt' não for encontrado.
        """
        with console.status("[bold blue]Carregando links dos grupos..."):
            with open("grupos.txt", "r", encoding="utf-8") as file:
                links = [line.strip() for line in file if line.strip()]
            console.print(
                Panel(
                    f"[bold cyan]{len(links)} links carregados com sucesso! 📋",
                    title="[yellow]Links[/]",
                    expand=False,
                )
            )
        return links

    def _load_mensagem(self) -> str:
        """
        Carrega a mensagem que será enviada.

        Returns:
            str: A mensagem que será enviada.

        Raises:
            FileNotFoundError: Se o arquivo 'mensagem.txt' não for encontrado.
        """
        with console.status("[bold blue]Carregando mensagem..."):
            with open("mensagem.txt", "r", encoding="utf-8") as file:
                mensagem = file.read().strip()
            console.print(
                Panel(
                    "[bold cyan]Mensagem carregada com sucesso! 📝",
                    title="[yellow]Mensagem[/]",
                    expand=False,
                )
            )
        return mensagem

    def login(self) -> None:
        """
        Realiza o login no Facebook.

        Raises:
            TimeoutException: Se o login não for concluído dentro do tempo limite.
            WebDriverException: Se houver um erro durante o processo de login.
        """
        with console.status("[bold yellow]Realizando login no Facebook..."):
            self.browser.get("https://www.facebook.com")
            try:
                WebDriverWait(self.browser, 300).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'a[aria-label="Página inicial"]')
                    )
                )
                console.print(
                    Panel(
                        "[bold green]Login realizado com sucesso! 🎉",
                        title="[yellow]Login[/]",
                        expand=False,
                    )
                )
            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]Erro no login: {e}",
                        title="[yellow]Erro[/]",
                        expand=False,
                    )
                )
                raise

    def _send_post(self, group_link: str) -> None:
        """
        Envia a mensagem para um grupo.

        Args:
            group_link (str): Link do grupo para enviar a mensagem.

        Raises:
            TimeoutException: Se algum elemento não for encontrado dentro do tempo limite.
            WebDriverException: Se houver um erro durante o processo de postagem.
        """
        self.browser.get(group_link)

        try:
            self._click_text_box()
            self._type_message()
            self._click_post_button()
            self._wait_for_post_confirmation()
            console.print(
                f"[bold green]✅ Postagem enviada para:[/] [cyan]{group_link}"
            )
        except Exception as e:
            console.print(
                f"[bold red]❌ Erro ao postar no grupo {group_link}:[/] [yellow]{e}"
            )

    def _click_text_box(self) -> None:
        """
        Clica na caixa de texto.

        Raises:
            TimeoutException: Se a caixa de texto não for encontrada dentro do tempo limite.
        """
        WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Escreva algo...']"))
        ).click()

    def _type_message(self) -> None:
        """
        Digita a mensagem na caixa de texto.

        Raises:
            TimeoutException: Se a caixa de texto não for encontrada dentro do tempo limite.
        """
        text_box = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[aria-label="Crie uma publicação aberta…"]')
            )
        )
        text_box.send_keys(self.mensagem)

    def _click_post_button(self) -> None:
        """
        Clica no botão de postagem.

        Raises:
            TimeoutException: Se o botão de postagem não for encontrado dentro do tempo limite.
        """
        if re.search(r"https?://", self.mensagem):
            WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "div[aria-label='Remover prévia do link da sua publicação']",
                    )
                )
            )

        WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Publicar']"))
        ).click()

    def _wait_for_post_confirmation(self) -> None:
        """
        Espera a confirmação da postagem.

        Raises:
            TimeoutException: Se a confirmação não for recebida dentro do tempo limite.
        """
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div[aria-label='Criar publicação']")
            )
        )

    def send_posts(self) -> None:
        """
        Envia a mensagem para todos os grupos.

        Raises:
            Exception: Se houver um erro durante o processo de envio de postagens.
        """
        console.print(
            Panel(
                "[bold magenta]Iniciando envio de postagens 🚀",
                title="[yellow]Processo[/]",
                expand=False,
            )
        )
        for i, link in enumerate(self.links, 1):
            console.print(f"[cyan]Postagem {i}/{len(self.links)}[/]")
            self._send_post(link)
        console.print(
            Panel(
                "[bold green]Todas as postagens foram enviadas com sucesso! 🎉",
                title="[yellow]Conclusão[/]",
                expand=False,
            )
        )

    def close(self) -> None:
        """
        Fecha o browser.

        Raises:
            WebDriverException: Se houver um erro ao fechar o navegador.
        """
        with console.status("[bold yellow]Fechando o navegador..."):
            self.browser.quit()
            console.print(
                Panel(
                    "[bold green]Navegador fechado com sucesso! 👋",
                    title="[yellow]Encerramento[/]",
                    expand=False,
                )
            )


if __name__ == "__main__":
    console.print(
        Panel(
            "[bold magenta]🤖 Iniciando automação do Facebook 🤖[/]",
            title="[yellow]Início[/]",
            expand=False,
        )
    )
    fb = Facebook()
    try:
        fb.login()
        fb.send_posts()
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Erro durante a execução: {e}",
                title="[yellow]Erro Fatal[/]",
                expand=False,
            )
        )
    finally:
        fb.close()
    console.print(
        Panel(
            "[bold magenta]🎊 Automação do Facebook concluída 🎊[/]",
            title="[yellow]Fim[/]",
            expand=False,
        )
    )
