"""
Générateur de données factices pour le développement
Crée des scrutins réalistes basés sur la structure de l'Assemblée Nationale
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class FakeDataGenerator:
    """Générateur de données de votes factices mais réalistes"""

    # Groupes parlementaires de la 16ème législature (réels)
    GROUPES = {
        "Renaissance (RE)": {"size": 169, "orientation": "centre"},
        "Rassemblement National (RN)": {"size": 88, "orientation": "droite-nationale"},
        "La France insoumise - NUPES (LFI)": {"size": 75, "orientation": "gauche"},
        "Les Républicains (LR)": {"size": 62, "orientation": "droite"},
        "Socialistes et apparentés (SOC)": {"size": 31, "orientation": "gauche"},
        "Horizons et apparentés (HOR)": {"size": 30, "orientation": "centre-droit"},
        "Écologiste - NUPES (ECO)": {"size": 28, "orientation": "gauche-écolo"},
        "Libertés, Indépendants, Outre-mer et Territoires (LIOT)": {"size": 22, "orientation": "centre"},
        "Gauche démocrate et républicaine - NUPES (GDR)": {"size": 22, "orientation": "gauche"},
        "Non-inscrits (NI)": {"size": 10, "orientation": "mixte"}
    }

    # Thématiques de lois avec leurs positions types
    THEMATIQUES = {
        "sécurité_répressive": {
            "titres": [
                "Projet de loi renforçant les mesures de lutte contre la délinquance",
                "Proposition de loi visant à durcir les peines pour les infractions violentes",
                "Projet de loi relatif à la sécurité intérieure et à la police de proximité",
                "Proposition de loi pour le renforcement des sanctions pénales",
            ],
            "votes": {  # Pour/Contre/Abstention selon orientation
                "gauche": (0.1, 0.7, 0.2),
                "gauche-écolo": (0.05, 0.8, 0.15),
                "centre": (0.6, 0.2, 0.2),
                "centre-droit": (0.8, 0.1, 0.1),
                "droite": (0.85, 0.05, 0.1),
                "droite-nationale": (0.9, 0.05, 0.05),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "social_progressiste": {
            "titres": [
                "Projet de loi visant à améliorer les conditions de travail",
                "Proposition de loi pour le renforcement du dialogue social",
                "Projet de loi relatif au pouvoir d'achat des ménages",
                "Proposition de loi pour l'augmentation du SMIC",
                "Projet de loi pour la réduction du temps de travail",
            ],
            "votes": {
                "gauche": (0.9, 0.05, 0.05),
                "gauche-écolo": (0.85, 0.05, 0.1),
                "centre": (0.4, 0.4, 0.2),
                "centre-droit": (0.3, 0.5, 0.2),
                "droite": (0.15, 0.7, 0.15),
                "droite-nationale": (0.2, 0.6, 0.2),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "écologie": {
            "titres": [
                "Projet de loi climat et résilience",
                "Proposition de loi visant à interdire les pesticides dangereux",
                "Projet de loi relatif à la transition énergétique",
                "Proposition de loi pour la protection de la biodiversité",
                "Projet de loi sur l'économie circulaire",
            ],
            "votes": {
                "gauche": (0.8, 0.1, 0.1),
                "gauche-écolo": (0.95, 0.02, 0.03),
                "centre": (0.6, 0.2, 0.2),
                "centre-droit": (0.5, 0.3, 0.2),
                "droite": (0.3, 0.5, 0.2),
                "droite-nationale": (0.15, 0.7, 0.15),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "économie_libérale": {
            "titres": [
                "Projet de loi pour la liberté économique",
                "Proposition de loi facilitant la création d'entreprises",
                "Projet de loi relatif à la simplification administrative",
                "Proposition de loi pour la compétitivité des entreprises",
                "Projet de loi sur la réforme fiscale",
            ],
            "votes": {
                "gauche": (0.1, 0.8, 0.1),
                "gauche-écolo": (0.05, 0.85, 0.1),
                "centre": (0.8, 0.1, 0.1),
                "centre-droit": (0.85, 0.05, 0.1),
                "droite": (0.9, 0.05, 0.05),
                "droite-nationale": (0.4, 0.4, 0.2),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "immigration": {
            "titres": [
                "Projet de loi pour contrôler l'immigration",
                "Proposition de loi relative au droit d'asile",
                "Projet de loi sur l'intégration des étrangers",
                "Proposition de loi pour la maîtrise des flux migratoires",
            ],
            "votes": {
                "gauche": (0.15, 0.7, 0.15),
                "gauche-écolo": (0.2, 0.65, 0.15),
                "centre": (0.6, 0.25, 0.15),
                "centre-droit": (0.75, 0.15, 0.1),
                "droite": (0.85, 0.1, 0.05),
                "droite-nationale": (0.95, 0.03, 0.02),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "institutions": {
            "titres": [
                "Projet de loi constitutionnelle pour la réforme des institutions",
                "Proposition de loi relative au fonctionnement de l'Assemblée",
                "Projet de loi organique sur le Conseil économique",
                "Proposition de loi pour la transparence de la vie publique",
            ],
            "votes": {
                "gauche": (0.5, 0.3, 0.2),
                "gauche-écolo": (0.5, 0.3, 0.2),
                "centre": (0.7, 0.2, 0.1),
                "centre-droit": (0.7, 0.2, 0.1),
                "droite": (0.6, 0.3, 0.1),
                "droite-nationale": (0.4, 0.4, 0.2),
                "mixte": (0.5, 0.3, 0.2)
            }
        },
        "santé": {
            "titres": [
                "Projet de loi de financement de la sécurité sociale",
                "Proposition de loi pour l'amélioration de l'hôpital public",
                "Projet de loi relatif à la bioéthique",
                "Proposition de loi sur la santé mentale",
                "Projet de loi pour le remboursement des soins",
            ],
            "votes": {
                "gauche": (0.7, 0.2, 0.1),
                "gauche-écolo": (0.75, 0.15, 0.1),
                "centre": (0.65, 0.25, 0.1),
                "centre-droit": (0.6, 0.3, 0.1),
                "droite": (0.5, 0.4, 0.1),
                "droite-nationale": (0.55, 0.35, 0.1),
                "mixte": (0.6, 0.25, 0.15)
            }
        },
        "éducation": {
            "titres": [
                "Projet de loi pour l'école de la confiance",
                "Proposition de loi visant à revaloriser les enseignants",
                "Projet de loi relatif à l'enseignement supérieur",
                "Proposition de loi pour l'égalité des chances à l'école",
            ],
            "votes": {
                "gauche": (0.65, 0.25, 0.1),
                "gauche-écolo": (0.7, 0.2, 0.1),
                "centre": (0.7, 0.2, 0.1),
                "centre-droit": (0.65, 0.25, 0.1),
                "droite": (0.6, 0.3, 0.1),
                "droite-nationale": (0.5, 0.4, 0.1),
                "mixte": (0.6, 0.25, 0.15)
            }
        }
    }

    def __init__(self, data_dir="../data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        random.seed(42)  # Pour la reproductibilité

    def generate_votes(self, orientation, vote_probs):
        """
        Génère des votes pour un groupe selon son orientation

        Args:
            orientation: Orientation politique du groupe
            vote_probs: Probabilités (pour, contre, abstention)

        Returns:
            Dict avec nombre de pour/contre/abstention
        """
        prob_pour, prob_contre, prob_abstention = vote_probs.get(orientation, (0.33, 0.33, 0.34))

        # Normaliser pour s'assurer que ça somme à 1
        total = prob_pour + prob_contre + prob_abstention
        prob_pour /= total
        prob_contre /= total
        prob_abstention /= total

        return {
            "pour": prob_pour,
            "contre": prob_contre,
            "abstention": prob_abstention
        }

    def generate_scrutin(self, numero, date, thematique_key=None):
        """
        Génère un scrutin factice

        Args:
            numero: Numéro du scrutin
            date: Date du scrutin
            thematique_key: Clé de la thématique (si None, aléatoire)

        Returns:
            Dict représentant un scrutin complet
        """
        # Choisir une thématique
        if thematique_key is None:
            thematique_key = random.choice(list(self.THEMATIQUES.keys()))

        thematique = self.THEMATIQUES[thematique_key]
        titre = random.choice(thematique["titres"])

        # Générer les votes par groupe
        groupes_data = []
        for groupe_nom, groupe_info in self.GROUPES.items():
            orientation = groupe_info["orientation"]
            size = groupe_info["size"]

            vote_probs = self.generate_votes(orientation, thematique["votes"])

            # Calculer les nombres avec un peu d'aléa
            pour = int(size * vote_probs["pour"] * random.uniform(0.85, 1.15))
            contre = int(size * vote_probs["contre"] * random.uniform(0.85, 1.15))
            abstention = int(size * vote_probs["abstention"] * random.uniform(0.85, 1.15))

            # Ajuster pour que le total ne dépasse pas la taille du groupe
            total = pour + contre + abstention
            if total > size:
                ratio = size / total
                pour = int(pour * ratio)
                contre = int(contre * ratio)
                abstention = size - pour - contre

            groupes_data.append({
                "organe_libelle": groupe_nom,
                "pour": {"nombre": max(0, pour)},
                "contre": {"nombre": max(0, contre)},
                "abstention": {"nombre": max(0, abstention)}
            })

        scrutin = {
            "scrutin": {
                "numero": str(numero),
                "date": date.strftime("%Y-%m-%d"),
                "titre": titre,
                "sort": "adopté" if random.random() > 0.3 else "rejeté",
                "thematique": thematique_key,
                "groupes": {
                    "groupe": groupes_data
                }
            }
        }

        return scrutin

    def generate_dataset(self, num_scrutins=100):
        """
        Génère un dataset complet de scrutins

        Args:
            num_scrutins: Nombre de scrutins à générer

        Returns:
            Liste de scrutins
        """
        print(f"\n{'='*60}")
        print(f"GÉNÉRATION DE {num_scrutins} SCRUTINS FACTICES")
        print(f"{'='*60}")

        scrutins = []
        start_date = datetime(2024, 1, 1)

        # Répartir les scrutins par thématique
        thematiques = list(self.THEMATIQUES.keys())
        for i in range(num_scrutins):
            # Date aléatoire dans l'année
            days_offset = random.randint(0, 365)
            date = start_date + timedelta(days=days_offset)

            # Choisir une thématique (avec distribution réaliste)
            thematique = random.choice(thematiques)

            scrutin = self.generate_scrutin(i + 1, date, thematique)
            scrutins.append(scrutin)

            if (i + 1) % 20 == 0:
                print(f"  {i + 1}/{num_scrutins} scrutins générés...")

        print(f"\n✓ {len(scrutins)} scrutins générés avec succès")

        # Statistiques
        print(f"\n{'='*60}")
        print("STATISTIQUES SUR LES DONNÉES GÉNÉRÉES")
        print(f"{'='*60}")

        thematique_counts = {}
        for scrutin in scrutins:
            theme = scrutin["scrutin"]["thematique"]
            thematique_counts[theme] = thematique_counts.get(theme, 0) + 1

        print("\nRépartition par thématique:")
        for theme, count in sorted(thematique_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {theme:25s}: {count:3d} scrutins ({count/len(scrutins)*100:.1f}%)")

        print(f"\nGroupes parlementaires: {len(self.GROUPES)}")
        for groupe, info in self.GROUPES.items():
            print(f"  {groupe:50s}: {info['size']:3d} députés ({info['orientation']})")

        return scrutins

    def save_data(self, scrutins, filename="scrutins_fake_data.json"):
        """Sauvegarde les données générées"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scrutins, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Données sauvegardées: {filepath}")
        print(f"  Taille du fichier: {filepath.stat().st_size / 1024:.2f} KB")
        return filepath


def main():
    """Fonction principale"""
    print(f"\n{'#'*60}")
    print("# GÉNÉRATEUR DE DONNÉES FACTICES")
    print("# POLITICAL COMPASS FR")
    print(f"{'#'*60}\n")

    generator = FakeDataGenerator()

    # Générer le dataset
    scrutins = generator.generate_dataset(num_scrutins=100)

    # Sauvegarder
    generator.save_data(scrutins)

    print(f"\n{'='*60}")
    print("GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print(f"{'='*60}\n")
    print("Les données peuvent maintenant être utilisées pour:")
    print("  1. Créer la matrice de votes")
    print("  2. Tester les projections (LDA, PCA, t-SNE, UMAP)")
    print("  3. Développer les visualisations")


if __name__ == "__main__":
    main()
