"""
Création de la matrice de votes à partir des données collectées
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path


class VoteMatrixBuilder:
    """Constructeur de matrice de votes"""

    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_scrutins(self, filename="scrutins_fake_data.json"):
        """Charge les scrutins depuis un fichier JSON"""
        filepath = self.raw_dir / filename
        print(f"\nChargement des données depuis: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            scrutins = json.load(f)

        print(f"✓ {len(scrutins)} scrutins chargés")
        return scrutins

    def create_vote_matrix(self, scrutins):
        """
        Crée une matrice de votes (scrutins × groupes)

        Pour chaque scrutin et chaque groupe:
        - Score = (pour - contre) / total
        - Range de -1 (100% contre) à +1 (100% pour)
        - 0 = abstention ou neutre

        Args:
            scrutins: Liste de scrutins avec détails

        Returns:
            DataFrame pandas avec la matrice de votes
        """
        print(f"\n{'='*60}")
        print("CRÉATION DE LA MATRICE DE VOTES")
        print(f"{'='*60}")

        # Extraire tous les groupes parlementaires uniques
        all_groupes = set()
        for scrutin_data in scrutins:
            scrutin = scrutin_data.get('scrutin', {})
            groupes = scrutin.get('groupes', {})
            if groupes and 'groupe' in groupes:
                for groupe in groupes['groupe']:
                    all_groupes.add(groupe.get('organe_libelle', ''))

        all_groupes = sorted(list(all_groupes))
        print(f"\nGroupes parlementaires identifiés: {len(all_groupes)}")
        for groupe in all_groupes:
            print(f"  • {groupe}")

        # Créer la matrice
        vote_data = []

        for scrutin_data in scrutins:
            scrutin = scrutin_data.get('scrutin', {})
            scrutin_num = scrutin.get('numero', '')
            scrutin_titre = scrutin.get('titre', '')
            scrutin_date = scrutin.get('date', '')
            scrutin_theme = scrutin.get('thematique', '')

            row = {
                'numero': scrutin_num,
                'titre': scrutin_titre,
                'date': scrutin_date,
                'thematique': scrutin_theme
            }

            # Pour chaque groupe, calculer un score de vote
            groupes = scrutin.get('groupes', {})
            if groupes and 'groupe' in groupes:
                groupe_dict = {}
                for groupe in groupes['groupe']:
                    nom = groupe.get('organe_libelle', '')
                    groupe_dict[nom] = groupe

                # Remplir les scores pour tous les groupes
                for groupe_nom in all_groupes:
                    if groupe_nom in groupe_dict:
                        groupe = groupe_dict[groupe_nom]
                        pour = groupe.get('pour', {}).get('nombre', 0)
                        contre = groupe.get('contre', {}).get('nombre', 0)
                        abstention = groupe.get('abstention', {}).get('nombre', 0)

                        total = pour + contre + abstention
                        if total > 0:
                            # Score: (pour - contre) / total
                            # Range: -1 (100% contre) à +1 (100% pour)
                            score = (pour - contre) / total
                            row[groupe_nom] = score
                        else:
                            row[groupe_nom] = 0
                    else:
                        # Groupe absent = 0 (neutre/absent)
                        row[groupe_nom] = 0

            vote_data.append(row)

        df = pd.DataFrame(vote_data)

        # Trier par date
        df = df.sort_values('date').reset_index(drop=True)

        print(f"\n✓ Matrice créée:")
        print(f"   - Dimensions: {df.shape[0]} scrutins × {df.shape[1]-4} groupes")
        print(f"   - Colonnes métadonnées: numero, titre, date, thematique")
        print(f"   - Colonnes de votes: {df.shape[1]-4}")
        print(f"\n   Aperçu de la matrice:")
        print(df.head())

        return df

    def analyze_matrix(self, df):
        """Analyse statistique de la matrice"""
        print(f"\n{'='*60}")
        print("ANALYSE DE LA MATRICE")
        print(f"{'='*60}")

        # Colonnes de votes (exclure les métadonnées)
        vote_cols = [col for col in df.columns if col not in ['numero', 'titre', 'date', 'thematique']]

        # Statistiques par groupe
        print("\nStatistiques par groupe (score moyen):")
        for col in vote_cols:
            mean_score = df[col].mean()
            std_score = df[col].std()
            print(f"  {col:50s}: {mean_score:+.3f} (σ={std_score:.3f})")

        # Matrice de corrélation entre groupes
        print("\n\nMatrice de corrélation entre groupes:")
        corr_matrix = df[vote_cols].corr()
        print(corr_matrix.round(2))

        # Paires les plus corrélées
        print("\n\nPaires de groupes les plus corrélées:")
        corr_pairs = []
        for i in range(len(vote_cols)):
            for j in range(i+1, len(vote_cols)):
                corr = corr_matrix.iloc[i, j]
                corr_pairs.append((vote_cols[i], vote_cols[j], corr))

        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        for g1, g2, corr in corr_pairs[:10]:
            print(f"  {g1[:25]:25s} ↔ {g2[:25]:25s}: {corr:+.3f}")

        # Statistiques par thématique
        print("\n\nRépartition par thématique:")
        theme_counts = df['thematique'].value_counts()
        for theme, count in theme_counts.items():
            print(f"  {theme:25s}: {count:3d} scrutins")

        return corr_matrix

    def save_matrix(self, df, filename="vote_matrix.csv"):
        """Sauvegarde la matrice"""
        filepath = self.processed_dir / filename
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"\n✓ Matrice sauvegardée: {filepath}")
        return filepath

    def save_matrix_for_projection(self, df, filename="vote_matrix_numeric.csv"):
        """
        Sauvegarde uniquement les colonnes numériques pour la projection

        Args:
            df: DataFrame avec matrice complète
            filename: Nom du fichier de sortie
        """
        # Extraire uniquement les colonnes de votes (numériques)
        vote_cols = [col for col in df.columns if col not in ['numero', 'titre', 'date', 'thematique']]

        df_numeric = df[vote_cols]

        filepath = self.processed_dir / filename
        df_numeric.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✓ Matrice numérique sauvegardée: {filepath}")
        print(f"  Dimensions: {df_numeric.shape}")

        return filepath


def main():
    """Fonction principale"""
    print(f"\n{'#'*60}")
    print("# CRÉATION DE LA MATRICE DE VOTES")
    print("# POLITICAL COMPASS FR")
    print(f"{'#'*60}\n")

    builder = VoteMatrixBuilder()

    # Charger les scrutins
    scrutins = builder.load_scrutins()

    # Créer la matrice
    vote_matrix = builder.create_vote_matrix(scrutins)

    # Analyser
    corr_matrix = builder.analyze_matrix(vote_matrix)

    # Sauvegarder
    builder.save_matrix(vote_matrix)
    builder.save_matrix_for_projection(vote_matrix)

    # Sauvegarder aussi la matrice de corrélation
    corr_path = builder.processed_dir / "correlation_matrix.csv"
    corr_matrix.to_csv(corr_path, encoding='utf-8')
    print(f"✓ Matrice de corrélation sauvegardée: {corr_path}")

    print(f"\n{'='*60}")
    print("CRÉATION DE LA MATRICE TERMINÉE!")
    print(f"{'='*60}\n")
    print("Prochaine étape: projections (LDA, PCA, t-SNE, UMAP)")


if __name__ == "__main__":
    main()
