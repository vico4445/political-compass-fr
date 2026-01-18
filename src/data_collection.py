"""
Module de collecte de données de l'Assemblée Nationale
"""
import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time


class DataCollector:
    """Collecteur de données des votes à l'Assemblée Nationale"""

    BASE_URL_NOSDEPUTES = "https://www.nosdeputes.fr"
    BASE_URL_AN = "https://data.assemblee-nationale.fr"

    def __init__(self, data_dir="../data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def test_nosdeputes_api(self):
        """Teste l'accès à l'API NosDéputés.fr"""
        try:
            response = requests.get(
                f"{self.BASE_URL_NOSDEPUTES}/synthese/data/json",
                timeout=10
            )

            if response.status_code == 200:
                print("✓ Connexion à NosDéputés.fr réussie")
                data = response.json()
                print(f"  Clés disponibles : {list(data.keys())}")
                return True
            else:
                print(f"✗ Erreur : {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Exception : {e}")
            return False

    def test_assemblee_api(self):
        """Teste l'API officielle de l'Assemblée Nationale"""
        try:
            legislature = 16  # Législature actuelle
            response = requests.get(
                f"{self.BASE_URL_AN}/api/opendata/scrutins/{legislature}",
                timeout=10
            )

            if response.status_code == 200:
                print("✓ Connexion à l'API officielle réussie")
                data = response.json()
                print(f"  Type de réponse : {type(data)}")
                if isinstance(data, list):
                    print(f"  Nombre d'éléments : {len(data)}")
                return True
            else:
                print(f"✗ Erreur : {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Exception : {e}")
            return False

    def get_scrutins_nosdeputes(self, limit=50):
        """
        Récupère les scrutins depuis NosDéputés.fr

        Args:
            limit: Nombre de scrutins à récupérer

        Returns:
            Liste des scrutins
        """
        try:
            print(f"\nRécupération de {limit} scrutins depuis NosDéputés.fr...")
            response = requests.get(
                f"{self.BASE_URL_NOSDEPUTES}/scrutins/data/json",
                timeout=20
            )

            if response.status_code == 200:
                data = response.json()
                scrutins = data.get('scrutins', [])
                print(f"✓ {len(scrutins)} scrutins disponibles")
                return scrutins[:limit]
            else:
                print(f"✗ Erreur : {response.status_code}")
                return []
        except Exception as e:
            print(f"✗ Exception : {e}")
            return []

    def get_scrutin_details(self, scrutin_num):
        """
        Récupère les détails d'un scrutin spécifique

        Args:
            scrutin_num: Numéro du scrutin

        Returns:
            Détails du scrutin avec votes par groupe
        """
        try:
            response = requests.get(
                f"{self.BASE_URL_NOSDEPUTES}/scrutin/{scrutin_num}/json",
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Erreur pour scrutin {scrutin_num}: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Exception pour scrutin {scrutin_num}: {e}")
            return None

    def collect_sample_with_details(self, sample_size=20):
        """
        Collecte un échantillon de scrutins avec leurs détails complets

        Args:
            sample_size: Nombre de scrutins à collecter

        Returns:
            Liste de scrutins avec détails
        """
        print(f"\n{'='*60}")
        print(f"COLLECTE DE {sample_size} SCRUTINS AVEC DÉTAILS")
        print(f"{'='*60}")

        # Récupérer la liste des scrutins
        scrutins = self.get_scrutins_nosdeputes(limit=sample_size)

        if not scrutins:
            print("✗ Aucun scrutin récupéré")
            return []

        # Récupérer les détails de chaque scrutin
        detailed_scrutins = []
        for i, scrutin in enumerate(scrutins, 1):
            scrutin_num = scrutin.get('numero')
            if scrutin_num:
                print(f"\n[{i}/{sample_size}] Récupération du scrutin n°{scrutin_num}...")
                details = self.get_scrutin_details(scrutin_num)
                if details:
                    detailed_scrutins.append(details)

                    # Afficher un aperçu
                    scrutin_info = details.get('scrutin', {})
                    titre = scrutin_info.get('titre', 'N/A')[:80]
                    print(f"  Titre: {titre}...")

                    # Pause pour ne pas surcharger l'API
                    time.sleep(0.5)

        print(f"\n✓ {len(detailed_scrutins)} scrutins collectés avec succès")
        return detailed_scrutins

    def analyze_scrutin_structure(self, scrutins):
        """
        Analyse la structure des scrutins collectés

        Args:
            scrutins: Liste de scrutins avec détails
        """
        if not scrutins:
            print("✗ Aucun scrutin à analyser")
            return

        print(f"\n{'='*60}")
        print("ANALYSE DE LA STRUCTURE DES DONNÉES")
        print(f"{'='*60}")

        # Analyser le premier scrutin en détail
        scrutin_sample = scrutins[0].get('scrutin', {})

        print("\n1. INFORMATIONS GÉNÉRALES")
        print(f"   - Numéro: {scrutin_sample.get('numero', 'N/A')}")
        print(f"   - Date: {scrutin_sample.get('date', 'N/A')}")
        print(f"   - Titre: {scrutin_sample.get('titre', 'N/A')[:100]}...")

        print("\n2. VOTES PAR GROUPE PARLEMENTAIRE")
        groupes = scrutin_sample.get('groupes', {})
        if groupes and 'groupe' in groupes:
            groupe_list = groupes['groupe']
            print(f"   Nombre de groupes: {len(groupe_list)}")

            for groupe in groupe_list[:5]:  # Afficher les 5 premiers
                nom = groupe.get('organe_libelle', 'N/A')
                pour = groupe.get('pour', {}).get('nombre', 0)
                contre = groupe.get('contre', {}).get('nombre', 0)
                abstention = groupe.get('abstention', {}).get('nombre', 0)

                print(f"\n   {nom}:")
                print(f"      Pour: {pour}, Contre: {contre}, Abstention: {abstention}")

        print("\n3. STATISTIQUES SUR L'ÉCHANTILLON")
        dates = []
        groupes_uniques = set()

        for scrutin_data in scrutins:
            scrutin = scrutin_data.get('scrutin', {})
            dates.append(scrutin.get('date', ''))

            groupes = scrutin.get('groupes', {})
            if groupes and 'groupe' in groupes:
                for groupe in groupes['groupe']:
                    groupes_uniques.add(groupe.get('organe_libelle', ''))

        print(f"   - Période couverte: {min(dates)} à {max(dates)}")
        print(f"   - Nombre de groupes parlementaires identifiés: {len(groupes_uniques)}")
        print(f"\n   Groupes parlementaires:")
        for groupe in sorted(groupes_uniques):
            print(f"      • {groupe}")

    def save_data(self, scrutins, filename="scrutins_detailed.json"):
        """
        Sauvegarde les données collectées

        Args:
            scrutins: Liste de scrutins
            filename: Nom du fichier de sortie
        """
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scrutins, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Données sauvegardées: {filepath}")
        print(f"  Taille du fichier: {filepath.stat().st_size / 1024:.2f} KB")

    def create_vote_matrix(self, scrutins):
        """
        Crée une matrice de votes (scrutins × groupes)

        Args:
            scrutins: Liste de scrutins avec détails

        Returns:
            DataFrame pandas avec la matrice de votes
        """
        print(f"\n{'='*60}")
        print("CRÉATION DE LA MATRICE DE VOTES")
        print(f"{'='*60}")

        # Extraire tous les groupes parlementaires
        all_groupes = set()
        for scrutin_data in scrutins:
            scrutin = scrutin_data.get('scrutin', {})
            groupes = scrutin.get('groupes', {})
            if groupes and 'groupe' in groupes:
                for groupe in groupes['groupe']:
                    all_groupes.add(groupe.get('organe_libelle', ''))

        # Créer la matrice
        vote_data = []

        for scrutin_data in scrutins:
            scrutin = scrutin_data.get('scrutin', {})
            scrutin_num = scrutin.get('numero', '')
            scrutin_titre = scrutin.get('titre', '')[:50]

            row = {
                'numero': scrutin_num,
                'titre': scrutin_titre,
                'date': scrutin.get('date', '')
            }

            # Pour chaque groupe, calculer un score de vote
            # +1 = pour, -1 = contre, 0 = abstention
            groupes = scrutin.get('groupes', {})
            if groupes and 'groupe' in groupes:
                for groupe in groupes['groupe']:
                    nom = groupe.get('organe_libelle', '')
                    pour = groupe.get('pour', {}).get('nombre', 0)
                    contre = groupe.get('contre', {}).get('nombre', 0)
                    abstention = groupe.get('abstention', {}).get('nombre', 0)

                    total = pour + contre + abstention
                    if total > 0:
                        # Score: % pour - % contre
                        score = (pour - contre) / total
                        row[nom] = score
                    else:
                        row[nom] = 0

            vote_data.append(row)

        df = pd.DataFrame(vote_data)

        print(f"\n✓ Matrice créée:")
        print(f"   - Dimensions: {df.shape[0]} scrutins × {df.shape[1]-3} groupes")
        print(f"   - Colonnes: {list(df.columns)}")

        return df


def main():
    """Fonction principale"""
    print(f"\n{'#'*60}")
    print("# COLLECTE DE DONNÉES - POLITICAL COMPASS FR")
    print(f"{'#'*60}\n")

    collector = DataCollector()

    # Test des APIs
    print("ÉTAPE 1: Test des APIs")
    print("-" * 60)
    collector.test_nosdeputes_api()
    print()
    collector.test_assemblee_api()

    # Collecte d'un échantillon
    scrutins = collector.collect_sample_with_details(sample_size=30)

    if scrutins:
        # Analyse
        collector.analyze_scrutin_structure(scrutins)

        # Sauvegarde
        collector.save_data(scrutins)

        # Création de la matrice de votes
        vote_matrix = collector.create_vote_matrix(scrutins)

        # Sauvegarde de la matrice
        matrix_path = collector.data_dir / "vote_matrix.csv"
        vote_matrix.to_csv(matrix_path, index=False)
        print(f"\n✓ Matrice de votes sauvegardée: {matrix_path}")

        print(f"\n{'='*60}")
        print("COLLECTE TERMINÉE AVEC SUCCÈS!")
        print(f"{'='*60}\n")
    else:
        print("\n✗ Échec de la collecte")


if __name__ == "__main__":
    main()
