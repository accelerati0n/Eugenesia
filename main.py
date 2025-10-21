"""
main.py
Punto de entrada principal del juego Eugenesia
Ejecuta este archivo para iniciar el juego
"""

from game import Game


def main():
    """
    Función principal del programa.
    Crea una instancia del juego y lo ejecuta.
    """
    print("""
    ╔════════════════════════════════════════╗
    ║         EUGENESIA GAME v1.0            ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    
    Controles:
    - WASD o Flechas: Mover personaje
    - ESC: Salir
    
    """)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
