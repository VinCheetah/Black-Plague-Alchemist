import pygame
import sys

pygame.init()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Graph Drawer")

points = []
selected_point = None

class OptionsVolet:
    def __init__(self, pos):
        self.pos = pos
        self.largeur, self.hauteur = 150, 100
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.largeur, self.hauteur)

    def afficher(self):
        pygame.draw.rect(fenetre, BLANC, self.rect)
        pygame.draw.rect(fenetre, NOIR, self.rect, 2)

        font = pygame.font.Font(None, 24)
        textes = ["Supprimer", "Déplacer", "Ajouter voisin"]
        for i, texte in enumerate(textes):
            texte_surface = font.render(texte, True, NOIR)
            texte_rect = texte_surface.get_rect(center=(self.pos[0] + self.largeur / 2, self.pos[1] + i * 30 + 30))
            texte_rect.move_ip(0, i * 30)
            fenetre.blit(texte_surface, texte_rect)

def dessiner_sommet(coord, couleur):
    pygame.draw.circle(fenetre, couleur, coord, 10)

def dessiner_lignes():
    if len(points) > 1:
        pygame.draw.lines(fenetre, ROUGE, False, points, 2)

def selectionner_sommet(pos_souris):
    for i, point in enumerate(points):
        distance = pygame.math.Vector2(point[0] - pos_souris[0], point[1] - pos_souris[1]).length()
        if distance < 10:
            return i
    return None

running = True
options_volet = None
options_active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_souris = pygame.mouse.get_pos()
            selected_point = selectionner_sommet(pos_souris)
            if selected_point is None:
                points.append(pos_souris)
            else:
                # Affiche le volet d'options près du sommet sélectionné
                options_volet = OptionsVolet(pos_souris)
                options_active = True
        elif event.type == pygame.MOUSEMOTION and selected_point is not None:
            points[selected_point] = pygame.mouse.get_pos()
            if options_volet is not None:
                # Déplace le volet d'options avec le sommet sélectionné
                options_volet.pos = points[selected_point]
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_point = None
            if options_active:
                options_active = False
                # Traite l'événement seulement si le bouton de la souris a été relâché dans le volet d'options
                if options_volet.rect.collidepoint(event.pos):
                    # Vérifie quelle option a été cliquée
                    if options_volet.rect.collidepoint(event.pos[0], options_volet.pos[1] + 30):
                        # Supprimer le sommet
                        points.pop(selected_point)
                    elif options_volet.rect.collidepoint(event.pos[0], options_volet.pos[1] + 60):
                        # Déplacer le sommet
                        # Vous pouvez implémenter le déplacement ici
                        pass
                    elif options_volet.rect.collidepoint(event.pos[0], options_volet.pos[1] + 90):
                        # Ajouter un voisin
                        voisin_pos = (points[selected_point][0] + 50, points[selected_point][1])
                        points.append(voisin_pos)
                options_volet = None

    fenetre.fill(BLANC)

    for i, point in enumerate(points):
        couleur = VERT if i == selected_point else NOIR
        dessiner_sommet(point, couleur)

    dessiner_lignes()

    if options_volet is not None:
        options_volet.afficher()

    pygame.display.flip()

pygame.quit()
sys.exit()
