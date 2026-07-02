"""Definição dos personagens jogáveis.

Cada personagem é uma instância de Personagem (dataclass), guardada no
dicionário PERSONAGENS por chave (ex: "shelly"). Isso mantém o acesso
O(1) por chave que o resto do jogo já usa, e ao mesmo tempo dá autocomplete
e checagem de atributos — errar o nome de um campo agora é AttributeError
na hora, não um KeyError silencioso escondido num dicionário aninhado.

A chave (ex: "shelly") existe SÓ como chave do dicionário — não é repetida
dentro do objeto Personagem. Isso evita duas fontes da mesma informação
divergirem silenciosamente (ex: copiar/colar um personagem novo e esquecer
de atualizar um campo "chave" interno).

Os stats (vida_maxima, velocidade, dano_base) hoje são iguais para todos
os personagens — são valores padrão pensados para quando o balanceamento
por personagem for implementado. Até lá, o gameplay pode continuar
assumindo que todo personagem tem o mesmo desempenho.
"""

from dataclasses import dataclass
import config_gameplay as config


@dataclass
class Personagem:
    nome: str              # nome exibido na tela de seleção, ex: "Shelly"
    asset_pasta: str        # pasta em assets/ onde ficam os sprites deste personagem
    standing_file: str       # arquivo do sprite parado (ex: "shelly.png")

    # Stats de gameplay — hoje iguais para todos, prontos para diferenciação futura
    vida_maxima: int = config.VIDA_MAXIMA
    velocidade: int = config.VELOCIDADE_BASE
    dano_base: int = config.PROJETIL_DANO_BASE


PERSONAGENS = {
    "shelly": Personagem(
        nome="Shelly",
        asset_pasta="shelly",
        standing_file="shelly.png",
    ),
    "piper": Personagem(
        nome="Piper",
        asset_pasta="piper",
        standing_file="piper.png",
    ),
    "colt": Personagem(
        nome="Colt",
        asset_pasta="colt",
        standing_file="colt.png",
    ),
    "iyoda": Personagem(
        nome="Iyoda",
        asset_pasta="iyoda",
        standing_file="iyoda.png",
    ),
}